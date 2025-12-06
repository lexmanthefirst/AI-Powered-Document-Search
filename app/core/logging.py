import logging
import os
import sys
from contextvars import ContextVar
from typing import Optional

# Configuration
DEFAULT_LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
SERVICE_NAME = "RAG Chatbot"

# Context variable to store correlation ID across async calls
correlation_id_context: ContextVar[Optional[str]] = ContextVar("correlation_id", default=None)


def _resolve_log_level(level: str) -> int:
    """Convert log level string to logging constant."""
    level_name = level.upper()
    return getattr(logging, level_name, logging.INFO)


class CorrelationIDFilter(logging.Filter):
    """Filter to inject correlation ID into log records."""
    
    def filter(self, record: logging.LogRecord) -> bool:
        """Add correlation_id to the log record."""
        record.correlation_id = correlation_id_context.get() or "N/A"
        return True


def setup_logging(level: str = DEFAULT_LOG_LEVEL) -> logging.Logger:
    """
    Configure structured logging with correlation ID support.
    
    Args:
        level: Logging level (default from environment or INFO)
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(SERVICE_NAME)
    logger.setLevel(_resolve_log_level(level))
    logger.propagate = False
    
    # Prevent duplicate handlers when running under reloaders
    if logger.handlers:
        return logger
    
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(_resolve_log_level(level))
    
    # JSON-formatted logs for production
    formatter = logging.Formatter(
        (
            '{"timestamp": "%(asctime)s", "level": "%(levelname)s", '
            '"correlation_id": "%(correlation_id)s", "service": "' + SERVICE_NAME + '", '
            '"message": "%(message)s", "module": "%(module)s", "function": "%(funcName)s"}'
        )
    )
    handler.setFormatter(formatter)
    handler.addFilter(CorrelationIDFilter())
    
    logger.addHandler(handler)
    
    return logger


def set_correlation_id(correlation_id: Optional[str]) -> None:
    """
    Set the correlation ID for the current context.
    
    Args:
        correlation_id: The correlation ID to set (None to clear)
    """
    if correlation_id is None:
        clear_correlation_id()
        return
    correlation_id_context.set(correlation_id)


def get_correlation_id() -> Optional[str]:
    """
    Get the correlation ID from the current context.
    
    Returns:
        The current correlation ID or None
    """
    return correlation_id_context.get()


def clear_correlation_id() -> None:
    """Reset the correlation ID for the current context."""
    correlation_id_context.set(None)


# Global logger instance
logger = setup_logging()


__all__ = [
    "logger",
    "set_correlation_id",
    "get_correlation_id",
    "clear_correlation_id",
]
