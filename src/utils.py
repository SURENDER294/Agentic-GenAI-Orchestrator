import logging
import sys
from typing import Optional

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
VALID_LOG_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}

logger = logging.getLogger(__name__)


def setup_logging(level: str = "INFO") -> logging.Logger:
    normalized_level = level.strip().upper()

    if normalized_level not in VALID_LOG_LEVELS:
        raise ValueError(f"Invalid log level: {level}")

    root_logger = logging.getLogger()

    if not root_logger.handlers:
        logging.basicConfig(
            level=getattr(logging, normalized_level),
            format=LOG_FORMAT,
            handlers=[logging.StreamHandler(sys.stdout)],
        )
    else:
        root_logger.setLevel(getattr(logging, normalized_level))

    return logger


def validate_api_key(api_key: Optional[str], provider: str) -> bool:
    if api_key is None or not api_key.strip():
        logger.error("Missing API key for provider: %s", provider)
        return False
    return True
