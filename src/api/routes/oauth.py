"""
OAuth2 routes for Gmail authentication.

Handles OAuth2 flow for Gmail API authentication.
"""

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import RedirectResponse
from typing import Dict, Any
import asyncio

from api.models import OAuthRequest, OAuthResponse, OAuthCallbackRequest
from api.routes.auth import get_current_user
from core.gmail_oauth_manager import GmailOAuthManager

router = APIRouter()

# Global OAuth manager instance
oauth_manager: GmailOAuthManager = None


@router.post("/gmail/auth", response_model=OAuthResponse)
async def start_gmail_oauth(current_user: dict = Depends(get_current_user)):
    """Start Gmail OAuth2 authentication flow."""
    global oauth_manager
    
    try:
        oauth_manager = GmailOAuthManager()
        auth_url = oauth_manager.authenticate()
        
        if auth_url == "authenticated":
            # Already authenticated
            user_info = oauth_manager.get_user_info()
            return OAuthResponse(
                success=True,
                message="Already authenticated",
                auth_url=None,
                user_info=user_info
            )
        else:
            # Need to authenticate
            return OAuthResponse(
                success=True,
                message="Please visit the authorization URL",
                auth_url=auth_url,
                user_info=None
            )
            
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OAuth2 credentials not found. Please set up Google Cloud Console credentials."
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"OAuth2 authentication failed: {str(e)}"
        )


@router.post("/gmail/callback", response_model=OAuthResponse)
async def complete_gmail_oauth(
    callback_data: OAuthCallbackRequest,
    current_user: dict = Depends(get_current_user)
):
    """Complete Gmail OAuth2 authentication with authorization code."""
    global oauth_manager
    
    if not oauth_manager:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No OAuth2 session found. Please start authentication first."
        )
        
    try:
        success = oauth_manager.complete_authentication(callback_data.authorization_code)
        
        if success:
            user_info = oauth_manager.get_user_info()
            return OAuthResponse(
                success=True,
                message="Successfully authenticated with Gmail",
                auth_url=None,
                user_info=user_info
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Failed to complete OAuth2 authentication"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"OAuth2 callback failed: {str(e)}"
        )


@router.get("/gmail/status")
async def get_gmail_oauth_status(current_user: dict = Depends(get_current_user)):
    """Get Gmail OAuth2 authentication status."""
    global oauth_manager
    
    if oauth_manager and oauth_manager.is_authenticated():
        user_info = oauth_manager.get_user_info()
        return {
            "authenticated": True,
            "user_info": user_info
        }
    else:
        return {
            "authenticated": False,
            "user_info": None
        }


@router.post("/gmail/disconnect")
async def disconnect_gmail_oauth(current_user: dict = Depends(get_current_user)):
    """Disconnect Gmail OAuth2 session."""
    global oauth_manager
    
    if oauth_manager:
        oauth_manager.disconnect()
        oauth_manager = None
        
    return {"message": "Successfully disconnected from Gmail OAuth2"}


@router.get("/gmail/labels")
async def get_gmail_labels(current_user: dict = Depends(get_current_user)):
    """Get Gmail labels (folders)."""
    global oauth_manager
    
    if not oauth_manager or not oauth_manager.is_authenticated():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated with Gmail OAuth2"
        )
        
    try:
        labels = await asyncio.to_thread(oauth_manager.list_labels)
        return {"labels": labels}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get Gmail labels: {str(e)}"
        )


@router.get("/gmail/messages")
async def get_gmail_messages(
    label_id: str = "INBOX",
    max_results: int = 50,
    current_user: dict = Depends(get_current_user)
):
    """Get Gmail messages from a specific label."""
    global oauth_manager
    
    if not oauth_manager or not oauth_manager.is_authenticated():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated with Gmail OAuth2"
        )
        
    try:
        messages = await asyncio.to_thread(
            oauth_manager.get_messages,
            label_id=label_id,
            max_results=max_results
        )
        return {"messages": messages}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get Gmail messages: {str(e)}"
        )


@router.get("/gmail/stats")
async def get_gmail_stats(
    label_id: str = "INBOX",
    current_user: dict = Depends(get_current_user)
):
    """Get Gmail statistics for a specific label."""
    global oauth_manager
    
    if not oauth_manager or not oauth_manager.is_authenticated():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated with Gmail OAuth2"
        )
        
    try:
        stats = await asyncio.to_thread(oauth_manager.get_statistics, label_id)
        return stats
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get Gmail statistics: {str(e)}"
        )


@router.post("/gmail/auth/public", response_model=OAuthResponse)
async def start_gmail_oauth_public():
    """Start Gmail OAuth2 authentication flow (public endpoint)."""
    global oauth_manager
    
    try:
        oauth_manager = GmailOAuthManager()
        auth_url = oauth_manager.authenticate()
        
        if auth_url == "authenticated":
            # Already authenticated
            user_info = oauth_manager.get_user_info()
            return OAuthResponse(
                success=True,
                message="Already authenticated",
                auth_url=None,
                user_info=user_info
            )
        else:
            # Need to authenticate
            return OAuthResponse(
                success=True,
                message="Please visit the authorization URL",
                auth_url=auth_url,
                user_info=None
            )
            
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OAuth2 credentials not found. Please set up Google Cloud Console credentials."
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"OAuth2 authentication failed: {str(e)}"
        ) 