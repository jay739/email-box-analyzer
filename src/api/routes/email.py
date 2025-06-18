"""
Email connection and management routes for Email Box Analyzer API.

Handles email account connections, folder listing, and email operations.
"""

import asyncio
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from api.models import (ConnectionRequest, ConnectionResponse, EmailFolder,
                        EmailResponse, EmailStats)
from api.routes.auth import get_current_user
# from core.email_manager import EmailManager

router = APIRouter()

# Global email manager instance (in production, use proper session management)
# email_manager: EmailManager = None


@router.post("/connect", response_model=ConnectionResponse)
async def connect_to_email(connection_data: ConnectionRequest, current_user: dict = Depends(get_current_user)):
    """Connect to an email account using OAuth2 or App Password based on provider."""
    global email_manager

    try:
        # Extract domain from email
        email_domain = connection_data.email.split('@')[1].lower()
        
        # Detect provider from email domain
        provider_mapping = {
            'gmail.com': 'gmail',
            'googlemail.com': 'gmail',
            'outlook.com': 'outlook',
            'hotmail.com': 'outlook',
            'live.com': 'outlook',
            'yahoo.com': 'yahoo',
            'ymail.com': 'yahoo'
        }
        
        detected_provider = provider_mapping.get(email_domain)
        
        if not detected_provider:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"Unsupported email provider: {email_domain}. Supported providers: Gmail, Outlook, Yahoo"
            )
        
        # For Gmail, redirect to OAuth2 flow
        if detected_provider == 'gmail':
            from api.routes.oauth import start_gmail_oauth_public
            return await start_gmail_oauth_public()
        
        # For other providers, use App Password approach
        provider_config = {
            "outlook": {
                "name": "Outlook",
                "imap_server": "outlook.office365.com",
                "imap_port": 993,
                "smtp_server": "smtp.office365.com",
                "smtp_port": 587,
                "use_ssl": True,
                "use_tls": True,
                "requires_oauth": False,
            },
            "yahoo": {
                "name": "Yahoo",
                "imap_server": "imap.mail.yahoo.com",
                "imap_port": 993,
                "smtp_server": "smtp.mail.yahoo.com",
                "smtp_port": 587,
                "use_ssl": True,
                "use_tls": True,
                "requires_oauth": False,
            },
        }

        if detected_provider not in provider_config:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"Provider {detected_provider} not yet supported for password-based authentication. Please use OAuth2."
            )

        config_data = provider_config[detected_provider]
        from core.config_manager import EmailProviderConfig
        config = EmailProviderConfig(**config_data)

        # Create email manager
        from core.email_manager import EmailManager
        email_manager = EmailManager(config)

        # Connect to email server
        try:
            success = await asyncio.to_thread(email_manager.connect, connection_data.email, connection_data.password)
            
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail=f"Authentication failed for {detected_provider}. Please check your email and password."
                )
        except Exception as e:
            if "authentication" in str(e).lower() or "login" in str(e).lower():
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail=f"Authentication failed for {detected_provider}: {str(e)}"
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
                    detail=f"Connection failed: {str(e)}"
                )

        # Get folders
        folders = await asyncio.to_thread(email_manager.list_folders)
        folder_data = [
            {
                "name": folder.name,
                "path": folder.path,
                "message_count": folder.message_count,
                "unread_count": folder.unread_count,
                "flags": folder.flags,
            }
            for folder in folders
        ]

        # Get stats for INBOX
        stats = await asyncio.to_thread(email_manager.get_email_statistics, "INBOX")

        return ConnectionResponse(
            connected=True, 
            message=f"Successfully connected to {detected_provider} account", 
            folders=folder_data, 
            stats=stats
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Connection failed: {str(e)}")


@router.post("/disconnect")
async def disconnect_from_email(current_user: dict = Depends(get_current_user)):
    """Disconnect from the email account."""
    # global email_manager

    if email_manager:
        try:
            await asyncio.to_thread(email_manager.disconnect)
            # email_manager = None
            return {"message": "Successfully disconnected from email account"}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Disconnect failed: {str(e)}"
            )
    else:
        return {"message": "No active email connection"}


@router.get("/folders", response_model=List[EmailFolder])
async def get_email_folders(current_user: dict = Depends(get_current_user)):
    """Get list of email folders."""
    # global email_manager

    if not email_manager:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No active email connection")

    try:
        # folders = email_manager.list_folders()
        folders = await asyncio.to_thread(email_manager.list_folders)
        return [
            EmailFolder(
                name=folder.name,
                path=folder.path,
                message_count=folder.message_count,
                unread_count=folder.unread_count,
                flags=folder.flags,
            )
            for folder in folders
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to get folders: {str(e)}"
        )


@router.get("/stats", response_model=EmailStats)
async def get_email_stats(folder: str = "INBOX", current_user: dict = Depends(get_current_user)):
    """Get email statistics for a specific folder."""
    # global email_manager

    if not email_manager:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No active email connection")

    try:
        # stats = email_manager.get_email_statistics(folder)
        stats = await asyncio.to_thread(email_manager.get_email_statistics, folder)
        return EmailStats(**stats)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to get stats: {str(e)}")


@router.get("/emails", response_model=List[EmailResponse])
async def get_emails(
    folder: str = "INBOX", limit: int = 50, offset: int = 0, current_user: dict = Depends(get_current_user)
):
    """Get emails from a specific folder."""
    # global email_manager

    if not email_manager:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No active email connection")

    try:
        # emails = email_manager.fetch_emails(...)
        emails = await asyncio.to_thread(email_manager.fetch_emails, folder, limit=limit, offset=offset)

        email_responses = []
        for email in emails:
            email_response = EmailResponse(
                id=email.id,
                subject=email.subject,
                sender=email.sender,
                recipients=email.recipients,
                cc=email.cc,
                bcc=email.bcc,
                date=email.date,
                body=email.body,
                html_body=email.html_body,
                attachments=email.attachments,
                flags=email.flags,
                size=email.size,
                thread_id=email.thread_id,
                message_id=email.message_id,
            )
            email_responses.append(email_response)

        return email_responses

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to get emails: {str(e)}")


@router.get("/emails/{email_id}", response_model=EmailResponse)
async def get_email(email_id: str, folder: str = "INBOX", current_user: dict = Depends(get_current_user)):
    """Get a specific email by ID."""
    # global email_manager

    if not email_manager:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No active email connection")

    try:
        # email = email_manager.fetch_email(email_id, folder)
        email = await asyncio.to_thread(email_manager.fetch_email, folder, email_id)

        return EmailResponse(
            id=email.id,
            subject=email.subject,
            sender=email.sender,
            recipients=email.recipients,
            cc=email.cc,
            bcc=email.bcc,
            date=email.date,
            body=email.body,
            html_body=email.html_body,
            attachments=email.attachments,
            flags=email.flags,
            size=email.size,
            thread_id=email.thread_id,
            message_id=email.message_id,
        )

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to get email: {str(e)}")


@router.get("/status")
async def get_connection_status(current_user: dict = Depends(get_current_user)):
    """Get the current email connection status."""
    # global email_manager

    if email_manager and email_manager.is_connected():
        return {
            "connected": True,
            "provider": "email_provider",  # You can store this in the manager
            "email": "user@example.com",  # You can store this in the manager
        }
    else:
        return {"connected": False, "provider": None, "email": None}
