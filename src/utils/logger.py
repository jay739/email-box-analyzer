"""
Logger utility for Email Box Analyzer

Provides consistent logging configuration across the application.
"""

import logging
import sys
from pathlib import Path
from typing import Optional

from loguru import logger


def setup_logger(log_level: str = "INFO", log_file: Optional[str] = None) -> logger:
    """
    Setup application logger.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file. If None, uses default location.

    Returns:
        Configured logger instance
    """
    # Remove default handler
    logger.remove()

    # Create log directory
    if log_file is None:
        log_dir = Path.home() / ".email_analyzer" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "email_analyzer.log"

    # Add console handler
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=log_level,
        colorize=True,
    )

    # Add file handler
    logger.add(
        str(log_file),
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level=log_level,
        rotation="10 MB",
        retention="30 days",
        compression="zip",
    )

    # Intercept standard logging
    class InterceptHandler(logging.Handler):
        def emit(self, record):
            try:
                level = logger.level(record.levelname).name
            except ValueError:
                level = record.levelno

            frame, depth = logging.currentframe(), 2
            while frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back
                depth += 1

            logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())

    # Replace standard logging handlers
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

    return logger


def get_logger(name: str) -> logger:
    """
    Get a logger instance for a specific module.

    Args:
        name: Logger name (usually __name__)

    Returns:
        Logger instance
    """
    return logger.bind(name=name)


# Default logger setup
default_logger = setup_logger()
