#!/usr/bin/env python3
"""
Email Box Analyzer - FastAPI Backend Server

A comprehensive email analysis API that connects to various email providers
and generates insightful visualizations from email data.
"""

import sys
import os
from pathlib import Path
from contextlib import asynccontextmanager
from typing import Dict, Any
import uvicorn
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
import jwt
from datetime import datetime, timedelta
from core.config_manager import ConfigManager
from core.email_manager import EmailManager, EmailConnectionError, EmailAuthenticationError
from analyzers.email_analyzer import EmailAnalyzer
from visualizers.chart_manager import ChartManager
from utils.logger import setup_logger
from utils.exceptions import EmailAnalyzerException
from api.routes import auth, email, analysis, providers, export, charts, oauth

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent))

# Global variables for application state
config_manager: ConfigManager = None
logger = None
email_manager: EmailManager = None
analyzer: EmailAnalyzer = None
chart_manager: ChartManager = None

# Security
security = HTTPBearer()
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# In-memory storage (replace with database in production)
users_db: Dict[str, Dict[str, Any]] = {}
analysis_results: Dict[str, Dict[str, Any]] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    global config_manager, logger, analyzer, chart_manager

    # Startup
    logger = setup_logger()
    logger.info("Email Box Analyzer API starting up...")

    try:
        config_manager = ConfigManager()
        analyzer = EmailAnalyzer()
        chart_manager = ChartManager()
        logger.info("API components initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize API components: {e}")
        raise

    yield

    # Shutdown
    logger.info("Email Box Analyzer API shutting down...")


# Create FastAPI application
app = FastAPI(
    title="Email Box Analyzer API",
    description="A comprehensive email analysis API with advanced visualizations",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js dev server
        "http://127.0.0.1:3000",  # Next.js dev server (alternative)
        "http://localhost:8000",  # API server
        "https://your-domain.com",  # Production domain
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(TrustedHostMiddleware, allowed_hosts=["localhost", "127.0.0.1", "your-domain.com"])


# Dependency functions
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current authenticated user."""
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


def create_access_token(data: dict, expires_delta: timedelta = None):
    """Create JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(providers.router, prefix="/api/providers", tags=["providers"])
app.include_router(email.router, prefix="/api/email", tags=["email"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["analysis"])
app.include_router(charts.router, prefix="/api/charts", tags=["charts"])
app.include_router(export.router, prefix="/api/export", tags=["export"])
app.include_router(oauth.router, prefix="/api/oauth", tags=["oauth"])


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {"message": "Email Box Analyzer API", "version": "1.0.0", "docs": "/docs", "status": "running"}


# Health check endpoint
@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat(), "version": "1.0.0"}


# Error handlers
@app.exception_handler(EmailAnalyzerException)
async def email_analyzer_exception_handler(request, exc):
    """Handle EmailAnalyzerException."""
    logger.error(f"EmailAnalyzerException: {exc}")
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": str(exc)})


@app.exception_handler(EmailConnectionError)
async def email_connection_exception_handler(request, exc):
    """Handle EmailConnectionError."""
    logger.error(f"EmailConnectionError: {exc}")
    return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content={"error": str(exc)})


@app.exception_handler(EmailAuthenticationError)
async def email_authentication_exception_handler(request, exc):
    """Handle EmailAuthenticationError."""
    logger.error(f"EmailAuthenticationError: {exc}")
    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"error": str(exc)})


def main():
    """Main entry point for the API server."""
    import argparse

    parser = argparse.ArgumentParser(description="Email Box Analyzer API Server")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind the server to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind the server to")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload for development")
    parser.add_argument("--workers", type=int, default=1, help="Number of worker processes")

    args = parser.parse_args()

    logger = setup_logger()
    logger.info(f"Starting Email Box Analyzer API server on {args.host}:{args.port}")

    uvicorn.run("main:app", host=args.host, port=args.port, reload=args.reload, workers=args.workers, log_level="info")


if __name__ == "__main__":
    main()
