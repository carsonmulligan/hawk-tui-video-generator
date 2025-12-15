"""Logging utilities for Hawk TUI."""

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

from hawk.config import VERBOSE, LOG_FILE

# Create logger
_logger: Optional[logging.Logger] = None
_log_messages: list[str] = []  # In-memory log for TUI display


def get_logger() -> logging.Logger:
    """Get or create the application logger."""
    global _logger
    
    if _logger is not None:
        return _logger
    
    _logger = logging.getLogger("hawk")
    _logger.setLevel(logging.DEBUG if VERBOSE else logging.INFO)
    
    # File handler - always log to file
    file_handler = logging.FileHandler(LOG_FILE, mode="a")
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_formatter)
    _logger.addHandler(file_handler)
    
    # Console handler - only if verbose
    if VERBOSE:
        console_handler = logging.StreamHandler(sys.stderr)
        console_handler.setLevel(logging.DEBUG)
        console_formatter = logging.Formatter("[%(levelname)s] %(message)s")
        console_handler.setFormatter(console_formatter)
        _logger.addHandler(console_handler)
    
    return _logger


def log(message: str, level: str = "info") -> None:
    """Log a message and store in memory for TUI display."""
    logger = get_logger()
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    # Log to file/console
    log_func = getattr(logger, level.lower(), logger.info)
    log_func(message)
    
    # Store in memory for TUI
    _log_messages.append(f"[{timestamp}] {message}")
    # Keep only last 100 messages
    if len(_log_messages) > 100:
        _log_messages.pop(0)


def debug(message: str) -> None:
    """Log debug message."""
    log(message, "debug")


def info(message: str) -> None:
    """Log info message."""
    log(message, "info")


def warning(message: str) -> None:
    """Log warning message."""
    log(message, "warning")


def error(message: str) -> None:
    """Log error message."""
    log(message, "error")


def get_recent_logs(count: int = 20) -> list[str]:
    """Get recent log messages for TUI display."""
    return _log_messages[-count:]


def clear_logs() -> None:
    """Clear in-memory logs."""
    _log_messages.clear()


# Module-level logger instance for convenience
logger = get_logger()

