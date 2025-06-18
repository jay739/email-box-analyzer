"""
Pytest configuration and fixtures for Email Box Analyzer tests.
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch

from src.core.config_manager import ConfigManager, EmailProviderConfig, AppSettings


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)


@pytest.fixture
def sample_config():
    """Sample configuration data for testing."""
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
                "oauth_client_secret": ""
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


@pytest.fixture
def mock_config_manager(sample_config, temp_dir):
    """Mock configuration manager for testing."""
    config_file = temp_dir / "test_config.json"
    
    with patch('src.core.config_manager.ConfigManager._get_default_config_path') as mock_path:
        mock_path.return_value = config_file
        
        # Create a temporary config file
        import json
        with open(config_file, 'w') as f:
            json.dump(sample_config, f)
        
        config_manager = ConfigManager()
        return config_manager


@pytest.fixture
def sample_email_provider():
    """Sample email provider configuration."""
    return EmailProviderConfig(
        name="Test Provider",
        imap_server="test.imap.com",
        imap_port=993,
        smtp_server="test.smtp.com",
        smtp_port=587,
        use_ssl=True,
        use_tls=True,
        requires_oauth=False
    )


@pytest.fixture
def sample_app_settings():
    """Sample application settings."""
    return AppSettings(
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


@pytest.fixture
def mock_email_manager():
    """Mock email manager for testing."""
    mock_manager = Mock()
    mock_manager.is_connected.return_value = True
    mock_manager.list_folders.return_value = []
    mock_manager.fetch_emails.return_value = []
    mock_manager.get_email_statistics.return_value = {
        'total_messages': 0,
        'unread_messages': 0,
        'recent_messages': 0,
        'read_percentage': 0
    }
    return mock_manager


@pytest.fixture
def sample_emails():
    """Sample email messages for testing."""
    from src.core.email_manager import EmailMessage
    from datetime import datetime
    
    return [
        EmailMessage(
            uid="1",
            subject="Test Email 1",
            sender="test1@example.com",
            recipients=["recipient@example.com"],
            date=datetime.now(),
            body="This is a test email body",
            html_body="<p>This is a test email body</p>",
            attachments=[],
            flags=[],
            size=1024
        ),
        EmailMessage(
            uid="2",
            subject="Test Email 2",
            sender="test2@example.com",
            recipients=["recipient@example.com"],
            date=datetime.now(),
            body="This is another test email body",
            html_body="<p>This is another test email body</p>",
            attachments=["document.pdf"],
            flags=["SEEN"],
            size=2048
        )
    ]


@pytest.fixture
def mock_analyzer():
    """Mock email analyzer for testing."""
    mock_analyzer = Mock()
    mock_analyzer.analyze_emails.return_value = {
        'total_emails': 2,
        'date_range': '2024-01-01 to 2024-01-02',
        'total_size_mb': 0.003,
        'top_senders': [('test1@example.com', 1), ('test2@example.com', 1)],
        'activity_by_time': {'Morning (6-12)': 1, 'Afternoon (12-17)': 1},
        'activity_by_day': {'Monday': 1, 'Tuesday': 1},
        'activity_by_hour': {9: 1, 14: 1},
        'subject_analysis': {},
        'attachment_analysis': {},
        'email_size_distribution': {},
        'thread_analysis': {},
        'domain_analysis': {},
        'sentiment_analysis': {},
        'keyword_analysis': {},
        'response_time_analysis': {}
    }
    return mock_analyzer


@pytest.fixture
def mock_chart_manager():
    """Mock chart manager for testing."""
    mock_manager = Mock()
    mock_manager.create_charts.return_value = {
        'activity_by_time': {'type': 'time_activity', 'data': {}, 'file_path': '/tmp/test.png'},
        'daily_activity': {'type': 'daily_activity', 'data': {}, 'file_path': '/tmp/test2.png'}
    }
    return mock_manager 