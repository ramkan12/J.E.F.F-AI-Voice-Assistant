"""
Utility functions for J.E.F.F voice assistant.
"""

import os
import yaml
import logging
from typing import Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


def load_config(config_path: str = "config/config.yaml") -> Dict[str, Any]:
    """
    Load configuration from YAML file and/or environment variables.
    Environment variables override file values (for production deployment).

    Args:
        config_path: Path to configuration file

    Returns:
        Configuration dictionary
    """
    # Try to load from file first
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
            logger.info(f"Configuration loaded from {config_path}")
            config = config or {}
    except FileNotFoundError:
        logger.warning(f"Config file not found: {config_path}, using environment variables")
        config = {}
    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML config: {e}")
        config = {}

    # Override with environment variables if present (for production)
    if os.environ.get('WEATHER_API_KEY'):
        config['weather_api_key'] = os.environ.get('WEATHER_API_KEY')
        logger.info("Using WEATHER_API_KEY from environment")

    if os.environ.get('GROQ_API_KEY'):
        config['groq_api_key'] = os.environ.get('GROQ_API_KEY')
        config['use_ai_fallback'] = True
        logger.info("Using GROQ_API_KEY from environment")

    return config


def setup_logging(
    level: str = "INFO",
    log_file: Optional[str] = None,
    format_string: Optional[str] = None
) -> None:
    """
    Set up logging configuration.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path to write logs
        format_string: Custom format string for log messages
    """
    if format_string is None:
        format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    handlers = [logging.StreamHandler()]

    if log_file:
        # Create logs directory if it doesn't exist
        log_dir = Path(log_file).parent
        log_dir.mkdir(parents=True, exist_ok=True)
        handlers.append(logging.FileHandler(log_file))

    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format=format_string,
        handlers=handlers
    )

    logger.info(f"Logging initialized at {level} level")


def ensure_directory_exists(directory: str) -> None:
    """
    Ensure a directory exists, create it if it doesn't.

    Args:
        directory: Path to directory
    """
    Path(directory).mkdir(parents=True, exist_ok=True)
    logger.debug(f"Ensured directory exists: {directory}")


def get_project_root() -> Path:
    """
    Get the project root directory.

    Returns:
        Path object pointing to project root
    """
    # Get the directory containing this file, then go up to project root
    return Path(__file__).parent.parent.parent


def validate_api_key(api_key: Optional[str]) -> bool:
    """
    Validate that an API key exists and is not a placeholder.

    Args:
        api_key: API key to validate

    Returns:
        True if valid, False otherwise
    """
    if not api_key:
        return False

    placeholders = ['your_api_key_here', 'YOUR_API_KEY', 'xxx', '']
    return api_key not in placeholders and len(api_key) > 10
