"""
Custom exceptions for Email Box Analyzer

Defines application-specific exceptions for better error handling.
"""


class EmailAnalyzerException(Exception):
    """Base exception for Email Box Analyzer application."""
    pass



class ConfigurationError(EmailAnalyzerException):
    """Raised when there's an error with application configuration."""
    pass



class EmailConnectionError(EmailAnalyzerException):
    """Raised when there's an error connecting to email servers."""
    pass



class EmailAuthenticationError(EmailAnalyzerException):
    """Raised when email authentication fails."""
    pass



class AnalysisError(EmailAnalyzerException):
    """Raised when there's an error during email analysis."""
    pass



class VisualizationError(EmailAnalyzerException):
    """Raised when there's an error creating visualizations."""
    pass



class ExportError(EmailAnalyzerException):
    """Raised when there's an error exporting results."""
    pass



class DataValidationError(EmailAnalyzerException):
    """Raised when data validation fails."""
    pass



class ProviderNotSupportedError(EmailAnalyzerException):
    """Raised when an email provider is not supported."""
    pass



class RateLimitError(EmailAnalyzerException):
    """Raised when email server rate limits are exceeded."""
    pass



class NetworkError(EmailAnalyzerException):
    """Raised when there are network connectivity issues."""
    pass

