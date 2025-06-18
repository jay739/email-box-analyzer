"""
Gmail OAuth2 Manager for Email Box Analyzer

Handles Gmail API authentication and operations using OAuth2.
"""

import os
import json
import pickle
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import logging

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .config_manager import EmailProviderConfig


class GmailOAuthManager:
    """Manages Gmail API operations using OAuth2 authentication."""
    
    # Gmail API scopes
    SCOPES = [
        'https://www.googleapis.com/auth/gmail.readonly',
        'https://www.googleapis.com/auth/gmail.modify',
        'https://www.googleapis.com/auth/gmail.labels'
    ]
    
    def __init__(self, credentials_path: Optional[str] = None, token_path: Optional[str] = None):
        """
        Initialize the Gmail OAuth manager.
        
        Args:
            credentials_path: Path to OAuth2 credentials JSON file
            token_path: Path to store/load OAuth2 tokens
        """
        self.logger = logging.getLogger(__name__)
        self.credentials_path = credentials_path or self._get_default_credentials_path()
        self.token_path = token_path or self._get_default_token_path()
        self.service = None
        self.credentials = None
        self.user_info = None
        
    def _get_default_credentials_path(self) -> Path:
        """Get default path for OAuth2 credentials."""
        config_dir = Path.home() / ".email_analyzer" / "oauth"
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir / "credentials.json"
        
    def _get_default_token_path(self) -> Path:
        """Get default path for OAuth2 tokens."""
        config_dir = Path.home() / ".email_analyzer" / "oauth"
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir / "token.pickle"
        
    def authenticate(self) -> str:
        """
        Authenticate with Gmail API using OAuth2.
        
        Returns:
            Authorization URL for user to visit
        """
        try:
            # Load existing credentials
            if self.token_path.exists():
                with open(self.token_path, 'rb') as token:
                    self.credentials = pickle.load(token)
                    
            # If credentials don't exist or are invalid, get new ones
            if not self.credentials or not self.credentials.valid:
                if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                    self.credentials.refresh(Request())
                else:
                    if not self.credentials_path.exists():
                        raise FileNotFoundError(
                            f"OAuth2 credentials file not found at {self.credentials_path}. "
                            "Please download credentials.json from Google Cloud Console."
                        )
                        
                    flow = InstalledAppFlow.from_client_secrets_file(
                        str(self.credentials_path), self.SCOPES
                    )
                    
                    # Get authorization URL with proper redirect URI
                    auth_url, _ = flow.authorization_url(
                        access_type='offline',
                        include_granted_scopes='true'
                    )
                    
                    return auth_url
                    
            # Save credentials
            with open(self.token_path, 'wb') as token:
                pickle.dump(self.credentials, token)
                
            # Build service
            self.service = build('gmail', 'v1', credentials=self.credentials)
            
            # Get user info
            self.user_info = self.service.users().getProfile(userId='me').execute()
            
            self.logger.info(f"Successfully authenticated as {self.user_info['emailAddress']}")
            return "authenticated"
            
        except Exception as e:
            self.logger.error(f"Authentication failed: {e}")
            raise
            
    def complete_authentication(self, authorization_code: str) -> bool:
        """
        Complete OAuth2 authentication with authorization code.
        
        Args:
            authorization_code: Authorization code from Google OAuth2 flow
            
        Returns:
            True if authentication successful
        """
        try:
            flow = InstalledAppFlow.from_client_secrets_file(
                str(self.credentials_path), self.SCOPES
            )
            
            # Exchange authorization code for credentials with proper redirect URI
            flow.fetch_token(code=authorization_code)
            self.credentials = flow.credentials
            
            # Save credentials
            with open(self.token_path, 'wb') as token:
                pickle.dump(self.credentials, token)
                
            # Build service
            self.service = build('gmail', 'v1', credentials=self.credentials)
            
            # Get user info
            self.user_info = self.service.users().getProfile(userId='me').execute()
            
            self.logger.info(f"Successfully authenticated as {self.user_info['emailAddress']}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to complete authentication: {e}")
            return False
            
    def is_authenticated(self) -> bool:
        """Check if user is authenticated."""
        return self.service is not None and self.credentials is not None
        
    def get_user_info(self) -> Optional[Dict[str, Any]]:
        """Get authenticated user information."""
        if not self.is_authenticated():
            return None
        return self.user_info
        
    def list_labels(self) -> List[Dict[str, Any]]:
        """
        List Gmail labels (folders).
        
        Returns:
            List of label information
        """
        if not self.is_authenticated():
            raise Exception("Not authenticated")
            
        try:
            results = self.service.users().labels().list(userId='me').execute()
            labels = results.get('labels', [])
            
            # Convert to our format
            folders = []
            for label in labels:
                if label['type'] == 'user':  # Only user-created labels
                    folders.append({
                        'name': label['name'],
                        'path': label['id'],
                        'message_count': label.get('messagesTotal', 0),
                        'unread_count': label.get('messagesUnread', 0),
                        'flags': []
                    })
                    
            return folders
            
        except HttpError as error:
            self.logger.error(f"Failed to list labels: {error}")
            raise
            
    def get_messages(self, label_id: str = 'INBOX', max_results: int = 100, 
                    query: str = None) -> List[Dict[str, Any]]:
        """
        Get messages from a specific label.
        
        Args:
            label_id: Gmail label ID (use 'INBOX' for inbox)
            max_results: Maximum number of messages to retrieve
            query: Gmail search query
            
        Returns:
            List of message information
        """
        if not self.is_authenticated():
            raise Exception("Not authenticated")
            
        try:
            # Build query
            gmail_query = f"label:{label_id}"
            if query:
                gmail_query += f" {query}"
                
            # Get message IDs
            results = self.service.users().messages().list(
                userId='me',
                labelIds=[label_id],
                maxResults=max_results,
                q=query
            ).execute()
            
            messages = results.get('messages', [])
            
            # Get full message details
            full_messages = []
            for message in messages:
                msg = self.service.users().messages().get(
                    userId='me', 
                    id=message['id'],
                    format='full'
                ).execute()
                
                # Parse message
                parsed_msg = self._parse_gmail_message(msg)
                full_messages.append(parsed_msg)
                
            return full_messages
            
        except HttpError as error:
            self.logger.error(f"Failed to get messages: {error}")
            raise
            
    def _parse_gmail_message(self, gmail_msg: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse Gmail API message format to our format.
        
        Args:
            gmail_msg: Raw Gmail API message
            
        Returns:
            Parsed message in our format
        """
        headers = gmail_msg['payload']['headers']
        
        # Extract headers
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '')
        sender = next((h['value'] for h in headers if h['name'] == 'From'), '')
        date_str = next((h['value'] for h in headers if h['name'] == 'Date'), '')
        
        # Parse date
        try:
            from email.utils import parsedate_to_datetime
            date = parsedate_to_datetime(date_str)
        except:
            date = datetime.now()
            
        # Extract body
        body = self._extract_message_body(gmail_msg['payload'])
        
        return {
            'id': gmail_msg['id'],
            'subject': subject,
            'sender': sender,
            'recipients': [],
            'date': date,
            'body': body,
            'html_body': body,
            'attachments': [],
            'flags': gmail_msg.get('labelIds', []),
            'size': gmail_msg.get('sizeEstimate', 0),
            'thread_id': gmail_msg.get('threadId', ''),
            'message_id': gmail_msg.get('id', '')
        }
        
    def _extract_message_body(self, payload: Dict[str, Any]) -> str:
        """Extract text body from Gmail message payload."""
        if 'body' in payload and payload['body'].get('data'):
            import base64
            return base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
            
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    if 'data' in part['body']:
                        import base64
                        return base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                        
        return ''
        
    def get_statistics(self, label_id: str = 'INBOX') -> Dict[str, Any]:
        """
        Get email statistics for a label.
        
        Args:
            label_id: Gmail label ID
            
        Returns:
            Statistics dictionary
        """
        if not self.is_authenticated():
            raise Exception("Not authenticated")
            
        try:
            # Get label info
            label = self.service.users().labels().get(userId='me', id=label_id).execute()
            
            # Get recent messages for additional stats
            messages = self.get_messages(label_id, max_results=100)
            
            total_size = sum(msg.get('size', 0) for msg in messages)
            avg_size = total_size / len(messages) if messages else 0
            
            return {
                'total_messages': label.get('messagesTotal', 0),
                'unread_messages': label.get('messagesUnread', 0),
                'recent_messages': len(messages),
                'total_size_mb': total_size / (1024 * 1024),
                'average_size_kb': avg_size / 1024
            }
            
        except HttpError as error:
            self.logger.error(f"Failed to get statistics: {error}")
            raise
            
    def disconnect(self):
        """Disconnect and clear credentials."""
        self.service = None
        self.credentials = None
        self.user_info = None
        self.logger.info("Disconnected from Gmail API") 