"""
Pydantic models for Email Box Analyzer API.

Defines request and response schemas for all API endpoints.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, EmailStr, Field


# Authentication Models
class UserCreate(BaseModel):
    """User registration model."""

    email: EmailStr
    password: str = Field(..., min_length=8)
    name: str = Field(..., min_length=1, max_length=100)


class UserLogin(BaseModel):
    """User login model."""

    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """User response model."""

    id: str
    email: str
    name: str
    created_at: datetime
    preferences: Dict[str, Any] = {}


class TokenResponse(BaseModel):
    """Authentication token response."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


# Email Provider Models
class EmailProviderResponse(BaseModel):
    """Email provider response model."""

    id: str
    name: str
    imap_host: str
    imap_port: int
    smtp_host: str
    smtp_port: int
    use_ssl: bool
    use_tls: bool
    oauth2_supported: bool


# Connection Models
class ConnectionRequest(BaseModel):
    """Email connection request model."""
    email: EmailStr
    password: Optional[str] = None  # Only needed for non-OAuth2 providers
    use_oauth2: bool = True  # Default to OAuth2 for better security


class ConnectionResponse(BaseModel):
    """Email connection response model."""

    connected: bool
    message: str
    folders: Optional[List[Dict[str, Any]]] = None
    stats: Optional[Dict[str, Any]] = None


# Email Models
class EmailAddress(BaseModel):
    """Email address model."""

    name: str
    email: str


class Attachment(BaseModel):
    """Email attachment model."""

    id: str
    filename: str
    content_type: str
    size: int
    url: Optional[str] = None


class EmailResponse(BaseModel):
    """Email response model."""

    id: str
    subject: str
    sender: EmailAddress
    recipients: List[EmailAddress]
    cc: List[EmailAddress] = []
    bcc: List[EmailAddress] = []
    date: datetime
    body: str
    html_body: Optional[str] = None
    attachments: List[Attachment] = []
    flags: List[str] = []
    size: int
    thread_id: Optional[str] = None
    message_id: str


class EmailFolder(BaseModel):
    """Email folder model."""

    name: str
    path: str
    message_count: int
    unread_count: int
    flags: List[str] = []


class EmailStats(BaseModel):
    """Email statistics model."""

    total_messages: int
    unread_messages: int
    recent_messages: int
    total_size_mb: float
    average_size_kb: float


# Analysis Models
class AnalysisRequest(BaseModel):
    """Email analysis request model."""

    folder: str = "INBOX"
    limit: int = Field(1000, ge=1, le=50000)
    include_attachments: bool = True
    include_sentiment: bool = True
    date_range: Optional[Dict[str, datetime]] = None


class AnalysisStatus(BaseModel):
    """Analysis status model."""

    analysis_id: str
    status: str  # "pending", "running", "completed", "failed"
    progress: int = Field(0, ge=0, le=100)
    current_step: str
    error: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class SenderStats(BaseModel):
    """Sender statistics model."""

    email: str
    name: str
    count: int
    percentage: float
    total_size: int
    average_size: float


class TimeActivityStats(BaseModel):
    """Time activity statistics model."""

    hourly: Dict[int, int]
    daily: Dict[str, int]
    weekly: Dict[str, int]
    monthly: Dict[str, int]


class AttachmentStats(BaseModel):
    """Attachment statistics model."""

    total_attachments: int
    total_size: int
    by_type: Dict[str, int]
    by_size: Dict[str, int]
    top_types: List[Dict[str, Any]]


class SentimentStats(BaseModel):
    """Sentiment analysis statistics model."""

    positive: int
    negative: int
    neutral: int
    average_sentiment: float
    by_sender: Dict[str, float]
    by_time: Dict[str, float]


class ThreadStats(BaseModel):
    """Thread analysis statistics model."""

    total_threads: int
    average_thread_length: float
    longest_thread: int
    thread_distribution: Dict[int, int]
    active_threads: List[Dict[str, Any]]


class DomainStats(BaseModel):
    """Domain analysis statistics model."""

    top_domains: List[Dict[str, Any]]
    domain_distribution: Dict[str, int]
    internal_vs_external: Dict[str, int]


class KeywordStats(BaseModel):
    """Keyword analysis statistics model."""

    top_keywords: List[Dict[str, Any]]
    keyword_trends: Dict[str, Dict[str, int]]
    subject_keywords: List[Dict[str, Any]]
    body_keywords: List[Dict[str, Any]]


class ResponseTimeStats(BaseModel):
    """Response time statistics model."""

    average_response_time: float
    response_time_distribution: Dict[str, int]
    fastest_responders: List[Dict[str, Any]]
    slowest_responders: List[Dict[str, Any]]


class SizeDistribution(BaseModel):
    """Email size distribution model."""

    small: int  # < 1KB
    medium: int  # 1KB - 100KB
    large: int  # 100KB - 1MB
    very_large: int  # > 1MB
    average_size: float
    median_size: float


class LanguageStats(BaseModel):
    """Language analysis statistics model."""

    detected_languages: Dict[str, int]
    primary_language: str
    language_confidence: float


class EmailAnalysis(BaseModel):
    """Complete email analysis results model."""

    analysis_id: str
    total_emails: int
    date_range: Dict[str, datetime]
    total_size_mb: float
    top_senders: List[SenderStats]
    activity_by_time: TimeActivityStats
    attachment_stats: AttachmentStats
    sentiment_analysis: SentimentStats
    thread_analysis: ThreadStats
    domain_analysis: DomainStats
    keyword_analysis: KeywordStats
    response_time_analysis: ResponseTimeStats
    email_size_distribution: SizeDistribution
    language_analysis: LanguageStats
    created_at: datetime
    processing_time_seconds: float


class AnalysisResponse(BaseModel):
    """Analysis response model."""

    success: bool
    analysis: Optional[EmailAnalysis] = None
    error: Optional[str] = None


# Chart Models
class ChartData(BaseModel):
    """Chart data model."""

    type: str  # "line", "bar", "pie", "scatter", "area", "heatmap"
    title: str
    data: List[Dict[str, Any]]
    options: Optional[Dict[str, Any]] = None


class ChartResponse(BaseModel):
    """Chart response model."""

    charts: Dict[str, ChartData]
    chart_urls: Dict[str, str]


# Export Models
class ExportRequest(BaseModel):
    """Export request model."""

    analysis_id: str
    format: str = Field(..., pattern="^(json|csv|excel|pdf)$")
    include_charts: bool = True
    include_raw_data: bool = False
    date_range: Optional[Dict[str, datetime]] = None


class ExportResponse(BaseModel):
    """Export response model."""

    success: bool
    file_url: Optional[str] = None
    file_name: Optional[str] = None
    file_size: Optional[int] = None
    error: Optional[str] = None


# Error Models
class ErrorResponse(BaseModel):
    """Error response model."""

    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# Health Check Models
class HealthResponse(BaseModel):
    """Health check response model."""

    status: str
    timestamp: datetime
    version: str
    uptime_seconds: float
    memory_usage_mb: float
    cpu_usage_percent: float


# OAuth2 Models
class OAuthRequest(BaseModel):
    """OAuth2 authentication request model."""
    provider: str = Field(..., pattern="^(gmail|outlook|yahoo)$")


class OAuthCallbackRequest(BaseModel):
    """OAuth2 callback request model."""
    authorization_code: str = Field(..., description="Authorization code from OAuth2 provider")


class OAuthUserInfo(BaseModel):
    """OAuth2 user information model."""
    email: str
    name: Optional[str] = None
    picture: Optional[str] = None


class OAuthResponse(BaseModel):
    """OAuth2 authentication response model."""
    success: bool
    message: str
    auth_url: Optional[str] = None
    user_info: Optional[OAuthUserInfo] = None
