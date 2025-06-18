"""
Unit tests for configuration manager.
"""

import pytest
import json
from pathlib import Path
from unittest.mock import patch, mock_open

from src.core.config_manager import ConfigManager, EmailProviderConfig, AppSettings
from src.utils.exceptions import ConfigurationError


class TestEmailProviderConfig:
    """Test EmailProviderConfig dataclass."""
    
    def test_email_provider_config_creation(self):
        """Test creating EmailProviderConfig instance."""
        config = EmailProviderConfig(
            name="Test Provider",
            imap_server="test.imap.com",
            imap_port=993,
            smtp_server="test.smtp.com",
            smtp_port=587,
            use_ssl=True,
            use_tls=True,
            requires_oauth=False
        )
        
        assert config.name == "Test Provider"
        assert config.imap_server == "test.imap.com"
        assert config.imap_port == 993
        assert config.smtp_server == "test.smtp.com"
        assert config.smtp_port == 587
        assert config.use_ssl is True
        assert config.use_tls is True
        assert config.requires_oauth is False


class TestAppSettings:
    """Test AppSettings dataclass."""
    
    def test_app_settings_creation(self):
        """Test creating AppSettings instance."""
        settings = AppSettings(
            max_emails_per_analysis=1000,
            cache_duration_hours=24,
            theme="dark",
            language="en",
            auto_save_analysis=True,
            enable_notifications=True,
            log_level="INFO",
            data_directory="data",
            export_formats=["pdf", "png", "csv", "json"]
        )
        
        assert settings.max_emails_per_analysis == 1000
        assert settings.cache_duration_hours == 24
        assert settings.theme == "dark"
        assert settings.language == "en"
        assert settings.auto_save_analysis is True
        assert settings.enable_notifications is True
        assert settings.log_level == "INFO"
        assert settings.data_directory == "data"
        assert settings.export_formats == ["pdf", "png", "csv", "json"]
    
    def test_app_settings_default_export_formats(self):
        """Test AppSettings with default export formats."""
        settings = AppSettings()
        assert settings.export_formats == ["pdf", "png", "csv", "json"]


class TestConfigManager:
    """Test ConfigManager class."""
    
    def test_config_manager_initialization(self, mock_config_manager):
        """Test ConfigManager initialization."""
        assert mock_config_manager is not None
        assert mock_config_manager.email_providers is not None
        assert mock_config_manager.app_settings is not None
    
    def test_get_email_provider(self, mock_config_manager):
        """Test getting email provider configuration."""
        provider = mock_config_manager.get_email_provider("gmail")
        assert provider is not None
        assert provider.name == "Gmail"
        assert provider.imap_server == "imap.gmail.com"
        assert provider.imap_port == 993
    
    def test_get_email_provider_nonexistent(self, mock_config_manager):
        """Test getting non-existent email provider."""
        provider = mock_config_manager.get_email_provider("nonexistent")
        assert provider is None
    
    def test_get_all_providers(self, mock_config_manager):
        """Test getting all email providers."""
        providers = mock_config_manager.get_all_providers()
        assert isinstance(providers, dict)
        assert "gmail" in providers
        assert isinstance(providers["gmail"], EmailProviderConfig)
    
    def test_get_app_settings(self, mock_config_manager):
        """Test getting application settings."""
        settings = mock_config_manager.get_app_settings()
        assert isinstance(settings, AppSettings)
        assert settings.max_emails_per_analysis == 1000
        assert settings.theme == "dark"
    
    def test_validate_email_address_valid(self, mock_config_manager):
        """Test email address validation with valid email."""
        assert mock_config_manager.validate_email_address("test@example.com") is True
        assert mock_config_manager.validate_email_address("user.name+tag@domain.co.uk") is True
    
    def test_validate_email_address_invalid(self, mock_config_manager):
        """Test email address validation with invalid email."""
        assert mock_config_manager.validate_email_address("invalid-email") is False
        assert mock_config_manager.validate_email_address("@example.com") is False
        assert mock_config_manager.validate_email_address("test@") is False
    
    def test_get_data_directory(self, mock_config_manager):
        """Test getting data directory."""
        data_dir = mock_config_manager.get_data_directory()
        assert isinstance(data_dir, Path)
        assert data_dir.exists()
    
    def test_update_email_provider(self, mock_config_manager, sample_email_provider):
        """Test updating email provider configuration."""
        mock_config_manager.update_email_provider("test", sample_email_provider)
        
        updated_provider = mock_config_manager.get_email_provider("test")
        assert updated_provider is not None
        assert updated_provider.name == "Test Provider"
        assert updated_provider.imap_server == "test.imap.com"
    
    def test_update_app_settings(self, mock_config_manager, sample_app_settings):
        """Test updating application settings."""
        mock_config_manager.update_app_settings(sample_app_settings)
        
        updated_settings = mock_config_manager.get_app_settings()
        assert updated_settings.max_emails_per_analysis == 1000
        assert updated_settings.theme == "dark"
    
    def test_add_custom_provider(self, mock_config_manager, sample_email_provider):
        """Test adding custom email provider."""
        mock_config_manager.add_custom_provider("custom", sample_email_provider)
        
        custom_provider = mock_config_manager.get_email_provider("custom")
        assert custom_provider is not None
        assert custom_provider.name == "Test Provider"
    
    def test_add_custom_provider_existing(self, mock_config_manager, sample_email_provider):
        """Test adding custom provider with existing name."""
        mock_config_manager.add_custom_provider("custom", sample_email_provider)
        
        with pytest.raises(ValueError, match="Provider 'custom' already exists"):
            mock_config_manager.add_custom_provider("custom", sample_email_provider)
    
    def test_remove_provider(self, mock_config_manager):
        """Test removing email provider."""
        # First add a provider
        provider = EmailProviderConfig(
            name="Test Provider",
            imap_server="test.imap.com",
            imap_port=993,
            smtp_server="test.smtp.com",
            smtp_port=587
        )
        mock_config_manager.add_custom_provider("test", provider)
        
        # Then remove it
        mock_config_manager.remove_provider("test")
        
        # Verify it's removed
        assert mock_config_manager.get_email_provider("test") is None
    
    def test_remove_provider_nonexistent(self, mock_config_manager):
        """Test removing non-existent provider."""
        with pytest.raises(ValueError, match="Provider 'nonexistent' does not exist"):
            mock_config_manager.remove_provider("nonexistent")
    
    def test_invalid_config_file(self, temp_dir):
        """Test handling invalid configuration file."""
        config_file = temp_dir / "invalid_config.json"
        
        # Create invalid JSON file
        with open(config_file, 'w') as f:
            f.write("invalid json content")
        
        with patch('src.core.config_manager.ConfigManager._get_default_config_path') as mock_path:
            mock_path.return_value = config_file
            
            with pytest.raises(ValueError, match="Failed to load configuration file"):
                ConfigManager()
    
    def test_missing_config_sections(self, temp_dir):
        """Test handling configuration with missing sections."""
        config_file = temp_dir / "incomplete_config.json"
        
        # Create config with missing sections
        incomplete_config = {
            "email_providers": {}
            # Missing app_settings section
        }
        
        with open(config_file, 'w') as f:
            json.dump(incomplete_config, f)
        
        with patch('src.core.config_manager.ConfigManager._get_default_config_path') as mock_path:
            mock_path.return_value = config_file
            
            with pytest.raises(ValueError, match="Missing app_settings section"):
                ConfigManager()
    
    def test_invalid_provider_config(self, temp_dir):
        """Test handling invalid provider configuration."""
        config_file = temp_dir / "invalid_provider_config.json"
        
        # Create config with invalid provider
        invalid_config = {
            "email_providers": {
                "gmail": {
                    "name": "Gmail"
                    # Missing required fields
                }
            },
            "app_settings": {
                "max_emails_per_analysis": 1000,
                "cache_duration_hours": 24,
                "theme": "dark",
                "language": "en",
                "auto_save_analysis": True,
                "enable_notifications": True,
                "log_level": "INFO",
                "data_directory": "data",
                "export_formats": ["pdf", "png", "csv", "json"]
            }
        }
        
        with open(config_file, 'w') as f:
            json.dump(invalid_config, f)
        
        with patch('src.core.config_manager.ConfigManager._get_default_config_path') as mock_path:
            mock_path.return_value = config_file
            
            with pytest.raises(ValueError, match="Missing required field"):
                ConfigManager()
    
    def test_invalid_app_settings(self, temp_dir):
        """Test handling invalid application settings."""
        config_file = temp_dir / "invalid_settings_config.json"
        
        # Create config with invalid settings
        invalid_config = {
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
                    "oauth_client_secret": ""
                }
            },
            "app_settings": {
                "max_emails_per_analysis": 1000,
                "cache_duration_hours": 24,
                "theme": "invalid_theme",  # Invalid theme
                "language": "en",
                "auto_save_analysis": True,
                "enable_notifications": True,
                "log_level": "INFO",
                "data_directory": "data",
                "export_formats": ["pdf", "png", "csv", "json"]
            }
        }
        
        with open(config_file, 'w') as f:
            json.dump(invalid_config, f)
        
        with patch('src.core.config_manager.ConfigManager._get_default_config_path') as mock_path:
            mock_path.return_value = config_file
            
            with pytest.raises(ValueError, match="Invalid theme"):
                ConfigManager() 