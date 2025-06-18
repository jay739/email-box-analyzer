"""
Email providers routes for Email Box Analyzer API.

Handles email provider configuration and management.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from api.models import EmailProviderResponse
from api.routes.auth import get_current_user

router = APIRouter()


@router.get("/public", response_model=List[EmailProviderResponse])
async def get_public_email_providers():
    """Get all available email providers (public endpoint, no auth required)."""
    providers = [
        {
            "id": "gmail",
            "name": "Gmail",
            "imap_host": "imap.gmail.com",
            "imap_port": 993,
            "smtp_host": "smtp.gmail.com",
            "smtp_port": 587,
            "use_ssl": True,
            "use_tls": True,
            "oauth2_supported": True,
        },
        {
            "id": "outlook",
            "name": "Outlook/Hotmail",
            "imap_host": "outlook.office365.com",
            "imap_port": 993,
            "smtp_host": "smtp-mail.outlook.com",
            "smtp_port": 587,
            "use_ssl": True,
            "use_tls": True,
            "oauth2_supported": True,
        },
        {
            "id": "yahoo",
            "name": "Yahoo Mail",
            "imap_host": "imap.mail.yahoo.com",
            "imap_port": 993,
            "smtp_host": "smtp.mail.yahoo.com",
            "smtp_port": 587,
            "use_ssl": True,
            "use_tls": True,
            "oauth2_supported": True,
        },
        {
            "id": "icloud",
            "name": "iCloud Mail",
            "imap_host": "imap.mail.me.com",
            "imap_port": 993,
            "smtp_host": "smtp.mail.me.com",
            "smtp_port": 587,
            "use_ssl": True,
            "use_tls": True,
            "oauth2_supported": False,
        },
        {
            "id": "protonmail",
            "name": "ProtonMail",
            "imap_host": "127.0.0.1",
            "imap_port": 1143,
            "smtp_host": "127.0.0.1",
            "smtp_port": 1025,
            "use_ssl": False,
            "use_tls": False,
            "oauth2_supported": False,
        },
        {
            "id": "custom",
            "name": "Custom IMAP",
            "imap_host": "",
            "imap_port": 993,
            "smtp_host": "",
            "smtp_port": 587,
            "use_ssl": True,
            "use_tls": True,
            "oauth2_supported": False,
        },
    ]

    return [EmailProviderResponse(**provider) for provider in providers]


@router.get("/", response_model=List[EmailProviderResponse])
async def get_email_providers(current_user: dict = Depends(get_current_user)):
    """Get all available email providers."""
    providers = [
        {
            "id": "gmail",
            "name": "Gmail",
            "imap_host": "imap.gmail.com",
            "imap_port": 993,
            "smtp_host": "smtp.gmail.com",
            "smtp_port": 587,
            "use_ssl": True,
            "use_tls": True,
            "oauth2_supported": True,
        },
        {
            "id": "outlook",
            "name": "Outlook/Hotmail",
            "imap_host": "outlook.office365.com",
            "imap_port": 993,
            "smtp_host": "smtp-mail.outlook.com",
            "smtp_port": 587,
            "use_ssl": True,
            "use_tls": True,
            "oauth2_supported": True,
        },
        {
            "id": "yahoo",
            "name": "Yahoo Mail",
            "imap_host": "imap.mail.yahoo.com",
            "imap_port": 993,
            "smtp_host": "smtp.mail.yahoo.com",
            "smtp_port": 587,
            "use_ssl": True,
            "use_tls": True,
            "oauth2_supported": True,
        },
        {
            "id": "icloud",
            "name": "iCloud Mail",
            "imap_host": "imap.mail.me.com",
            "imap_port": 993,
            "smtp_host": "smtp.mail.me.com",
            "smtp_port": 587,
            "use_ssl": True,
            "use_tls": True,
            "oauth2_supported": False,
        },
        {
            "id": "protonmail",
            "name": "ProtonMail",
            "imap_host": "127.0.0.1",
            "imap_port": 1143,
            "smtp_host": "127.0.0.1",
            "smtp_port": 1025,
            "use_ssl": False,
            "use_tls": False,
            "oauth2_supported": False,
        },
        {
            "id": "custom",
            "name": "Custom IMAP",
            "imap_host": "",
            "imap_port": 993,
            "smtp_host": "",
            "smtp_port": 587,
            "use_ssl": True,
            "use_tls": True,
            "oauth2_supported": False,
        },
    ]

    return [EmailProviderResponse(**provider) for provider in providers]


@router.get("/{provider_id}", response_model=EmailProviderResponse)
async def get_email_provider(provider_id: str, current_user: dict = Depends(get_current_user)):
    """Get specific email provider configuration."""
    providers = {
        "gmail": {
            "id": "gmail",
            "name": "Gmail",
            "imap_host": "imap.gmail.com",
            "imap_port": 993,
            "smtp_host": "smtp.gmail.com",
            "smtp_port": 587,
            "use_ssl": True,
            "use_tls": True,
            "oauth2_supported": True,
        },
        "outlook": {
            "id": "outlook",
            "name": "Outlook/Hotmail",
            "imap_host": "outlook.office365.com",
            "imap_port": 993,
            "smtp_host": "smtp-mail.outlook.com",
            "smtp_port": 587,
            "use_ssl": True,
            "use_tls": True,
            "oauth2_supported": True,
        },
        "yahoo": {
            "id": "yahoo",
            "name": "Yahoo Mail",
            "imap_host": "imap.mail.yahoo.com",
            "imap_port": 993,
            "smtp_host": "smtp.mail.yahoo.com",
            "smtp_port": 587,
            "use_ssl": True,
            "use_tls": True,
            "oauth2_supported": True,
        },
        "icloud": {
            "id": "icloud",
            "name": "iCloud Mail",
            "imap_host": "imap.mail.me.com",
            "imap_port": 993,
            "smtp_host": "smtp.mail.me.com",
            "smtp_port": 587,
            "use_ssl": True,
            "use_tls": True,
            "oauth2_supported": False,
        },
        "protonmail": {
            "id": "protonmail",
            "name": "ProtonMail",
            "imap_host": "127.0.0.1",
            "imap_port": 1143,
            "smtp_host": "127.0.0.1",
            "smtp_port": 1025,
            "use_ssl": False,
            "use_tls": False,
            "oauth2_supported": False,
        },
        "custom": {
            "id": "custom",
            "name": "Custom IMAP",
            "imap_host": "",
            "imap_port": 993,
            "smtp_host": "",
            "smtp_port": 587,
            "use_ssl": True,
            "use_tls": True,
            "oauth2_supported": False,
        },
    }

    if provider_id not in providers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Provider '{provider_id}' not found")

    return EmailProviderResponse(**providers[provider_id])
