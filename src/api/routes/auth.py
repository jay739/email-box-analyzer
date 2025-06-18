"""
Authentication routes for Email Box Analyzer API.

Handles user registration, login, logout, and token management.
"""

import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from api.models import (TokenResponse, UserCreate, UserLogin, UserResponse)

router = APIRouter()
security = HTTPBearer()

# In-memory user storage (replace with database in production)
users_db: Dict[str, Dict[str, Any]] = {}

# Security configuration
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def hash_password(password: str) -> str:
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return hash_password(plain_password) == hashed_password


def create_access_token(data: dict, expires_delta: timedelta = None):
    """Create JWT access token."""
    import jwt

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current authenticated user."""
    import jwt

    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None or username not in users_db:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return users_db[username]
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/register", response_model=TokenResponse)
async def register(user_data: UserCreate):
    """Register a new user."""
    # Check if user already exists
    if user_data.email in users_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email already exists")

    # Create new user
    user_id = secrets.token_urlsafe(16)
    hashed_password = hash_password(user_data.password)

    user = {
        "id": user_id,
        "email": user_data.email,
        "name": user_data.name,
        "hashed_password": hashed_password,
        "created_at": datetime.utcnow(),
        "preferences": {
            "theme": "auto",
            "language": "en",
            "timezone": "UTC",
            "email_refresh_interval": 300,
            "default_analysis_limit": 1000,
            "auto_save_results": True,
        },
    }

    users_db[user_data.email] = user

    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user_data.email}, expires_delta=access_token_expires)

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=UserResponse(
            id=user["id"],
            email=user["email"],
            name=user["name"],
            created_at=user["created_at"],
            preferences=user["preferences"],
        ),
    )


@router.post("/login", response_model=TokenResponse)
async def login(user_data: UserLogin):
    """Login user and return access token."""
    user = users_db.get(user_data.email)
    if not user or not verify_password(user_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user_data.email}, expires_delta=access_token_expires)

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=UserResponse(
            id=user["id"],
            email=user["email"],
            name=user["name"],
            created_at=user["created_at"],
            preferences=user["preferences"],
        ),
    )


@router.post("/logout")
async def logout(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Logout user (invalidate token on client side)."""
    # In a real application, you might want to blacklist the token
    # For now, we'll just return a success message
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Get current user information."""
    return UserResponse(
        id=current_user["id"],
        email=current_user["email"],
        name=current_user["name"],
        created_at=current_user["created_at"],
        preferences=current_user["preferences"],
    )


@router.put("/me", response_model=UserResponse)
async def update_user_info(user_update: Dict[str, Any], current_user: Dict[str, Any] = Depends(get_current_user)):
    """Update current user information."""
    # Update allowed fields
    allowed_fields = ["name", "preferences"]
    for field in allowed_fields:
        if field in user_update:
            current_user[field] = user_update[field]

    # Update in database
    users_db[current_user["email"]] = current_user

    return UserResponse(
        id=current_user["id"],
        email=current_user["email"],
        name=current_user["name"],
        created_at=current_user["created_at"],
        preferences=current_user["preferences"],
    )


@router.post("/refresh")
async def refresh_token(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Refresh access token."""
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": current_user["email"]}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer", "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60}
