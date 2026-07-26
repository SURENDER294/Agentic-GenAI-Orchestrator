import logging
import sys
from typing import Optional

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
VALID_LOG_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}

logger = logging.getLogger(__name__)



def setup_logging(level: str = "INFO") -> None:
    \"\"\"
    Sets up the global logging configuration for the orchestrator.
    \"\"\"
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

def validate_api_key(api_key: Optional[str], provider: str) -> bool:
    \"\"\"
    Validates the presence of an API key for a given provider.
    \"\"\"
    if not api_key:
        logging.error(f"Missing API key for provider: {provider}")
        return False
    return True
