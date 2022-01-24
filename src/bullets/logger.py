import logging
import sys
from enum import Enum


class LogLevels(Enum):
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    INFO = logging.INFO
    DEBUG = logging.DEBUG


class CustomFormatter(logging.Formatter):
    default_fmt = "BullETS - %(levelname)s: %(message)s"
    error_fmt = "\u001b[31m%(levelname)s: %(message)s\u001b[0m"
    warning_fmt = "\u001b[33m%(levelname)s: %(message)s\u001b[0m"
    info_fmt = "\u001b[36m%(message)s\u001b[0m"
    debug_fmt = "\u001b[35m%(message)s\u001b[0m"

    def format(self, record):
        if record.levelno == LogLevels.ERROR.value:
            self._style._fmt = CustomFormatter.error_fmt
        elif record.levelno == LogLevels.WARNING.value:
            self._style._fmt = CustomFormatter.warning_fmt
        elif record.levelno == LogLevels.INFO.value:
            self._style._fmt = CustomFormatter.info_fmt
        elif record.levelno == LogLevels.DEBUG.value:
            self._style._fmt = CustomFormatter.debug_fmt
        else:
            self._style._fmt = CustomFormatter.default_fmt

        return super().format(record)


LOG_LEVEL = LogLevels.INFO
LOGGER = logging.getLogger("BullETS")
HANDLER = logging.StreamHandler(sys.stdout)
FORMATTER = CustomFormatter()

HANDLER.setLevel(LOG_LEVEL.value)
HANDLER.setFormatter(FORMATTER)

LOGGER.setLevel(LogLevels.DEBUG.value)
LOGGER.addHandler(HANDLER)


def set_log_level(level: str):
    """
    Change the logging level that will be displayed
    Args:
        level: Can be either "ERROR", "WARNING", "INFO" or "DEBUG"
    """
    global LOG_LEVEL

    if level == LogLevels.ERROR.name:
        LOG_LEVEL = LogLevels.ERROR
    elif level == LOG_LEVEL.WARNING.name:
        LOG_LEVEL = LogLevels.WARNING
    elif level == LogLevels.INFO.name:
        LOG_LEVEL = LogLevels.INFO
    elif level == LogLevels.DEBUG.name:
        LOG_LEVEL = LogLevels.DEBUG
    else:
        warning("Invalid log level specified.")
        return

    HANDLER.setLevel(LOG_LEVEL.value)


def error(message: str):
    """
    Log an error message
    Args:
        message: The message that will be logged
    """
    LOGGER.error(message)


def warning(message: str):
    """
    Log a warning message
    Args:
        message: The message that will be logged
    """
    LOGGER.warning(message)


def info(message: str):
    """
    Log an info message
    Args:
        message: The message that will be logged
    """
    LOGGER.info(message)


def debug(message: str):
    """
    Log a debug message
    Args:
        message: The message that will be logged
    """
    LOGGER.debug(message)
