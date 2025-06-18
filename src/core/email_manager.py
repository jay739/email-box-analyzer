"""
Email Manager for Email Box Analyzer

Handles IMAP connections,
email fetching, and processing from various email providers.
Supports Gmail, Outlook, Yahoo, and other IMAP-compatible providers.
"""

import email
import imaplib
import logging
import re
import ssl
from dataclasses import dataclass
from datetime import datetime, timedelta
from email.header import decode_header
from typing import Any, Dict, List, Optional, Tuple

from .config_manager import EmailProviderConfig


@dataclass
class EmailMessage:
    """Represents a processed email message."""

    uid: str
    subject: str
    sender: str
    recipients: List[str]
    date: datetime
    body: str
    html_body: str
    attachments: List[str]
    flags: List[str]
    size: int
    thread_id: Optional[str] = None
    reply_to: Optional[str] = None
    cc: List[str] = None
    bcc: List[str] = None

    def __post_init__(self):
        if self.cc is None:
            self.cc = []
        if self.bcc is None:
            self.bcc = []


@dataclass
class EmailFolder:
    """Represents an email folder/mailbox."""

    name: str
    path: str
    message_count: int
    unread_count: int
    flags: List[str]


class EmailConnectionError(Exception):
    """Raised when there's an error connecting to the email server."""



class EmailAuthenticationError(Exception):
    """Raised when authentication fails."""



class EmailManager:
    """Manages email connections and operations."""

    def __init__(self, config: EmailProviderConfig):
        """
        Initialize the email manager.

        Args:
            config: Email provider configuration
        """
        self.config = config
        self.connection = None
        self.logger = logging.getLogger(__name__)
        self._connected = False

    def connect(self, username: str, password: str) -> bool:
        """
        Connect to the email server.

        Args:
            username: Email username/address
            password: Email password or app password

        Returns:
            True if connection successful, False otherwise

        Raises:
            EmailConnectionError: If connection fails
            EmailAuthenticationError: If authentication fails
        """
        try:
            # Create SSL context
            ssl_context = ssl.create_default_context()

            # Connect to IMAP server
            if self.config.use_ssl:
                self.connection = imaplib.IMAP4_SSL(
                    self.config.imap_server, self.config.imap_port, ssl_context=ssl_context
                )
            else:
                self.connection = imaplib.IMAP4(self.config.imap_server, self.config.imap_port)

            # Start TLS if required
            if self.config.use_tls and not self.config.use_ssl:
                self.connection.starttls(ssl_context=ssl_context)

            # Authenticate
            self.connection.login(username, password)

            self._connected = True
            self.logger.info(f"Successfully connected to {self.config.name}")
            return True

        except imaplib.IMAP4.error as e:
            self.logger.error(f"Authentication failed: {e}")
            raise EmailAuthenticationError(f"Authentication failed: {e}")
        except Exception as e:
            self.logger.error(f"Connection failed: {e}")
            raise EmailConnectionError(f"Connection failed: {e}")

    def disconnect(self):
        """Disconnect from the email server."""
        if self.connection and self._connected:
            try:
                self.connection.logout()
                self.logger.info("Disconnected from email server")
            except Exception as e:
                self.logger.warning(f"Error during disconnect: {e}")
            finally:
                self.connection = None
                self._connected = False

    def is_connected(self) -> bool:
        """Check if connected to email server."""
        return self._connected and self.connection is not None

    def list_folders(self) -> List[EmailFolder]:
        """
        List all available email folders.

        Returns:
            List of email folders
        """
        if not self.is_connected():
            raise EmailConnectionError("Not connected to email server")

        try:
            status, folders = self.connection.list()
            if status != "OK":
                raise EmailConnectionError(f"Failed to list folders: {status}")

            email_folders = []
            for folder in folders:
                # Parse folder information
                folder_info = folder.decode("utf-8")
                flags, delimiter, name = imaplib.ParseFlags(folder_info)

                # Get folder path
                folder_path = name.strip('"')

                # Get folder statistics
                status, messages = self.connection.select(folder_path, readonly=True)
                if status == "OK":
                    message_count = int(messages[0])

                    # Get unread count
                    status, unread = self.connection.search(None, "UNSEEN")
                    unread_count = len(unread[0].split()) if status == "OK" and unread[0] else 0

                    email_folders.append(
                        EmailFolder(
                            name=name.strip('"'),
                            path=folder_path,
                            message_count=message_count,
                            unread_count=unread_count,
                            flags=list(flags),
                        )
                    )

            return email_folders

        except Exception as e:
            self.logger.error(f"Error listing folders: {e}")
            raise EmailConnectionError(f"Failed to list folders: {e}")

    def fetch_emails(
        self, folder: str = "INBOX", limit: int = 100, offset: int = 0, criteria: str = "ALL"
    ) -> List[EmailMessage]:
        """
        Fetch emails from a folder.

        Args:
            folder: Folder name to fetch from
            limit: Maximum number of emails to fetch
            offset: Number of emails to skip
            criteria: IMAP search criteria (e.g., 'ALL', 'UNSEEN', 'FROM "sender"')

        Returns:
            List of email messages
        """
        if not self.is_connected():
            raise EmailConnectionError("Not connected to email server")

        try:
            # Select folder
            status, messages = self.connection.select(folder, readonly=True)
            if status != "OK":
                raise EmailConnectionError(f"Failed to select folder {folder}: {status}")

            # Search for emails based on criteria
            status, message_numbers = self.connection.search(None, criteria)
            if status != "OK":
                raise EmailConnectionError(f"Failed to search emails: {status}")

            # Get message UIDs
            uids = message_numbers[0].split()

            # Apply offset and limit
            start_idx = max(0, len(uids) - offset - limit)
            end_idx = len(uids) - offset
            target_uids = uids[start_idx:end_idx]

            emails = []
            for uid in target_uids:
                try:
                    email_msg = self._fetch_single_email(uid)
                    if email_msg:
                        emails.append(email_msg)
                except Exception as e:
                    self.logger.warning(f"Failed to fetch email {uid}: {e}")
                    continue

            return emails

        except Exception as e:
            self.logger.error(f"Error fetching emails: {e}")
            raise EmailConnectionError(f"Failed to fetch emails: {e}")

    def _fetch_single_email(self, uid: bytes) -> Optional[EmailMessage]:
        """Fetch a single email by UID."""
        try:
            # Fetch email data
            status, data = self.connection.uid("FETCH", uid, "(RFC822 FLAGS)")
            if status != "OK":
                return None

            # Parse email message
            raw_email = data[0][1]
            email_message = email.message_from_bytes(raw_email)

            # Extract headers
            subject = self._decode_header(email_message.get("Subject", ""))
            sender = self._decode_header(email_message.get("From", ""))
            date_str = email_message.get("Date", "")
            recipients = self._parse_addresses(email_message.get("To", ""))
            cc = self._parse_addresses(email_message.get("Cc", ""))
            bcc = self._parse_addresses(email_message.get("Bcc", ""))
            reply_to = self._decode_header(email_message.get("Reply-To", ""))

            # Parse date
            try:
                date = email.utils.parsedate_to_datetime(date_str)
            except Exception:
                date = datetime.now()

            # Extract body
            body, html_body = self._extract_body(email_message)

            # Extract attachments
            attachments = self._extract_attachments(email_message)

            # Get flags
            flags = []
            if len(data[0]) > 2:
                flag_data = data[0][2]
                if flag_data:
                    flags = [flag.decode("utf-8").strip("()").split() for flag in flag_data]
                    flags = [item for sublist in flags for item in sublist]

            # Get message size
            size = len(raw_email)

            return EmailMessage(
                uid=uid.decode("utf-8"),
                subject=subject,
                sender=sender,
                recipients=recipients,
                date=date,
                body=body,
                html_body=html_body,
                attachments=attachments,
                flags=flags,
                size=size,
                reply_to=reply_to,
                cc=cc,
                bcc=bcc,
            )

        except Exception as e:
            self.logger.warning(f"Error parsing email {uid}: {e}")
            return None

    def _decode_header(self, header: str) -> str:
        """Decode email header."""
        try:
            decoded_parts = decode_header(header)
            decoded_string = ""
            for part, encoding in decoded_parts:
                if isinstance(part, bytes):
                    if encoding:
                        decoded_string += part.decode(encoding)
                    else:
                        decoded_string += part.decode("utf-8", errors="ignore")
                else:
                    decoded_string += part
            return decoded_string
        except Exception:
            return header

    def _parse_addresses(self, addresses: str) -> List[str]:
        """Parse email addresses from a string."""
        if not addresses:
            return []

        # Simple regex to extract email addresses
        email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        return re.findall(email_pattern, addresses)

    def _extract_body(self, email_message) -> Tuple[str, str]:
        """Extract text and HTML body from email message."""
        body = ""
        html_body = ""

        if email_message.is_multipart():
            for part in email_message.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition", ""))

                # Skip attachments
                if "attachment" in content_disposition:
                    continue

                if content_type == "text/plain":
                    try:
                        body = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                    except Exception:
                        body = part.get_payload(decode=True).decode("latin-1", errors="ignore")
                elif content_type == "text/html":
                    try:
                        html_body = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                    except Exception:
                        html_body = part.get_payload(decode=True).decode("latin-1", errors="ignore")
        else:
            content_type = email_message.get_content_type()
            if content_type == "text/plain":
                try:
                    body = email_message.get_payload(decode=True).decode("utf-8", errors="ignore")
                except Exception:
                    body = email_message.get_payload(decode=True).decode("latin-1", errors="ignore")
            elif content_type == "text/html":
                try:
                    html_body = email_message.get_payload(decode=True).decode("utf-8", errors="ignore")
                except Exception:
                    html_body = email_message.get_payload(decode=True).decode("latin-1", errors="ignore")

        return body, html_body

    def _extract_attachments(self, email_message) -> List[str]:
        """Extract attachment filenames from email message."""
        attachments = []

        if email_message.is_multipart():
            for part in email_message.walk():
                content_disposition = str(part.get("Content-Disposition", ""))

                if "attachment" in content_disposition:
                    filename = part.get_filename()
                    if filename:
                        attachments.append(self._decode_header(filename))

        return attachments

    def get_email_statistics(self, folder: str = "INBOX") -> Dict[str, Any]:
        """
        Get basic statistics for a folder.

        Args:
            folder: Folder name to analyze

        Returns:
            Dictionary with email statistics
        """
        if not self.is_connected():
            raise EmailConnectionError("Not connected to email server")

        try:
            # Select folder
            status, messages = self.connection.select(folder, readonly=True)
            if status != "OK":
                raise EmailConnectionError(f"Failed to select folder {folder}: {status}")

            total_messages = int(messages[0])

            # Get unread count
            status, unread = self.connection.search(None, "UNSEEN")
            unread_count = len(unread[0].split()) if status == "OK" and unread[0] else 0

            # Get recent messages (last 30 days)
            thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime("%d-%b-%Y")
            status, recent = self.connection.search(None, f"SINCE {thirty_days_ago}")
            recent_count = len(recent[0].split()) if status == "OK" and recent[0] else 0

            return {
                "total_messages": total_messages,
                "unread_messages": unread_count,
                "recent_messages": recent_count,
                "read_percentage": (
                    ((total_messages - unread_count) / total_messages * 100) if total_messages > 0 else 0
                ),
            }

        except Exception as e:
            self.logger.error(f"Error getting statistics: {e}")
            raise EmailConnectionError(f"Failed to get statistics: {e}")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()
