import logging
from enum import Enum


class LogLevels(Enum):
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    INFO = logging.INFO
    DEBUG = logging.DEBUG


LOG_LEVEL = LogLevels.INFO
LOGGER = logging.getLogger("BullETS")
HANDLER = logging.StreamHandler()
FORMATTER = logging.Formatter("BullETS - %(levelname)s: %(message)s")

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
    LOGGER.error(message)


def warning(message: str):
    LOGGER.warning(message)


def info(message: str):
    LOGGER.info(message)


def debug(message: str):
    LOGGER.debug(message)
