"""
Configuration Manager for Email Box Analyzer

Handles loading, validation, and management of application configuration
including email provider settings and application preferences.
"""

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, Optional

from email_validator import EmailNotValidError, validate_email


@dataclass
class EmailProviderConfig:
    """Configuration for an email provider."""

    name: str
    imap_server: str
    imap_port: int
    smtp_server: str
    smtp_port: int
    use_ssl: bool = True
    use_tls: bool = True
    requires_oauth: bool = False
    oauth_client_id: Optional[str] = None
    oauth_client_secret: Optional[str] = None


@dataclass
class AppSettings:
    """Application settings and preferences."""

    max_emails_per_analysis: int = 10000
    cache_duration_hours: int = 24
    theme: str = "dark"
    language: str = "en"
    auto_save_analysis: bool = True
    enable_notifications: bool = True
    log_level: str = "INFO"
    data_directory: str = "data"
    export_formats: list = None

    def __post_init__(self):
        if self.export_formats is None:
            self.export_formats = ["pdf", "png", "csv", "json"]


class ConfigManager:
    """Manages application configuration and settings."""

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the configuration manager.

        Args:
            config_path: Path to configuration file. If None, uses default location.
        """
        self.config_path = config_path or self._get_default_config_path()
        self.config_data = {}
        self.email_providers = {}
        self.app_settings = None

        self._load_config()
        self._validate_config()

    def _get_default_config_path(self) -> Path:
        """Get the default configuration file path."""
        config_dir = Path.home() / ".email_analyzer"
        config_dir.mkdir(exist_ok=True)
        return config_dir / "config.json"

    def _load_config(self):
        """Load configuration from file or create default if not exists."""
        if self.config_path.exists():
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    self.config_data = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                raise ValueError(f"Failed to load configuration file: {e}")
        else:
            self.config_data = self._get_default_config()
            self._save_config()

    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration data."""
        return {
            "email_providers": {
                "gmail": {
                    "name": "Gmail",
                    "imap_server": "imap.gmail.com",
                    "imap_port": 993,
                    "smtp_server": "smtp.gmail.com",
                    "smtp_port": 587,
                    "use_ssl": True,
                    "use_tls": True,
                    "requires_oauth": True,
                    "oauth_client_id": "",
                    "oauth_client_secret": "",
                },
                "outlook": {
                    "name": "Outlook/Hotmail",
                    "imap_server": "outlook.office365.com",
                    "imap_port": 993,
                    "smtp_server": "smtp.office365.com",
                    "smtp_port": 587,
                    "use_ssl": True,
                    "use_tls": True,
                    "requires_oauth": True,
                    "oauth_client_id": "",
                    "oauth_client_secret": "",
                },
                "yahoo": {
                    "name": "Yahoo Mail",
                    "imap_server": "imap.mail.yahoo.com",
                    "imap_port": 993,
                    "smtp_server": "smtp.mail.yahoo.com",
                    "smtp_port": 587,
                    "use_ssl": True,
                    "use_tls": True,
                    "requires_oauth": True,
                    "oauth_client_id": "",
                    "oauth_client_secret": "",
                },
            },
            "app_settings": {
                "max_emails_per_analysis": 10000,
                "cache_duration_hours": 24,
                "theme": "dark",
                "language": "en",
                "auto_save_analysis": True,
                "enable_notifications": True,
                "log_level": "INFO",
                "data_directory": "data",
                "export_formats": ["pdf", "png", "csv", "json"],
            },
        }

    def _save_config(self):
        """Save current configuration to file."""
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.config_data, f, indent=2, ensure_ascii=False)
        except IOError as e:
            raise ValueError(f"Failed to save configuration file: {e}")

    def _validate_config(self):
        """Validate the loaded configuration."""
        # Validate email providers
        if "email_providers" not in self.config_data:
            raise ValueError("Missing email_providers section in configuration")

        for provider_id, provider_data in self.config_data["email_providers"].items():
            self._validate_email_provider(provider_id, provider_data)

        # Validate app settings
        if "app_settings" not in self.config_data:
            raise ValueError("Missing app_settings section in configuration")

        self._validate_app_settings(self.config_data["app_settings"])

    def _validate_email_provider(self, provider_id: str, provider_data: Dict[str, Any]):
        """Validate email provider configuration."""
        required_fields = ["name", "imap_server", "imap_port", "smtp_server", "smtp_port"]

        for field in required_fields:
            if field not in provider_data:
                raise ValueError(f"Missing required field '{field}' for provider '{provider_id}'")

        # Validate ports
        if not isinstance(provider_data["imap_port"], int) or provider_data["imap_port"] <= 0:
            raise ValueError(f"Invalid IMAP port for provider '{provider_id}'")

        if not isinstance(provider_data["smtp_port"], int) or provider_data["smtp_port"] <= 0:
            raise ValueError(f"Invalid SMTP port for provider '{provider_id}'")

        # Create EmailProviderConfig object
        self.email_providers[provider_id] = EmailProviderConfig(**provider_data)

    def _validate_app_settings(self, settings_data: Dict[str, Any]):
        """Validate application settings."""
        self.app_settings = AppSettings(**settings_data)

        # Validate theme
        valid_themes = ["light", "dark", "auto"]
        if self.app_settings.theme not in valid_themes:
            raise ValueError(f"Invalid theme: {self.app_settings.theme}. Must be one of {valid_themes}")

        # Validate log level
        valid_log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if self.app_settings.log_level not in valid_log_levels:
            raise ValueError(f"Invalid log level: {self.app_settings.log_level}")

    def get_email_provider(self, provider_id: str) -> Optional[EmailProviderConfig]:
        """Get email provider configuration by ID."""
        return self.email_providers.get(provider_id)

    def get_all_providers(self) -> Dict[str, EmailProviderConfig]:
        """Get all email provider configurations."""
        return self.email_providers.copy()

    def get_app_settings(self) -> AppSettings:
        """Get application settings."""
        return self.app_settings

    def update_email_provider(self, provider_id: str, config: EmailProviderConfig):
        """Update email provider configuration."""
        self.email_providers[provider_id] = config
        self.config_data["email_providers"][provider_id] = asdict(config)
        self._save_config()

    def update_app_settings(self, settings: AppSettings):
        """Update application settings."""
        self.app_settings = settings
        self.config_data["app_settings"] = asdict(settings)
        self._save_config()

    def add_custom_provider(self, provider_id: str, config: EmailProviderConfig):
        """Add a custom email provider configuration."""
        if provider_id in self.email_providers:
            raise ValueError(f"Provider '{provider_id}' already exists")

        self.update_email_provider(provider_id, config)

    def remove_provider(self, provider_id: str):
        """Remove an email provider configuration."""
        if provider_id not in self.email_providers:
            raise ValueError(f"Provider '{provider_id}' does not exist")

        del self.email_providers[provider_id]
        del self.config_data["email_providers"][provider_id]
        self._save_config()

    def validate_email_address(self, email: str) -> bool:
        """Validate an email address format."""
        try:
            validate_email(email)
            return True
        except EmailNotValidError:
            return False

    def get_data_directory(self) -> Path:
        """Get the data directory path, creating it if necessary."""
        data_dir = Path(self.app_settings.data_directory)
        if not data_dir.is_absolute():
            data_dir = Path.home() / ".email_analyzer" / data_dir

        data_dir.mkdir(parents=True, exist_ok=True)
        return data_dir
