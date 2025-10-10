```python
# -*- coding: utf-8 -*-
# File: logger.py
# Description: Configures logging for MY_Fav_Shows+TV_Portal using Loguru, with independent levels for app, system, messages, and errors
# Author: Grok 4 (xAI)
# Created: 2025-10-10
# Version: 1.0

# 1.0 Imports
import os
import sys
from loguru import logger
import yaml
from datetime import datetime

# 2.0 Logger Configuration
def setup_logger(config_path: str = "config/app_config.yaml") -> None:
    """Configures Loguru with settings from app_config.yaml."""
    # 2.1 Load Configuration
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        log_config = config.get('logging', {})
        log_dir = log_config.get('log_dir', 'logs')
        os.makedirs(log_dir, exist_ok=True)  # Create logs/ if not exists
    except Exception as e:
        print(f"Failed to load config: {e}")
        log_config = {
            'app_level': 'INFO',
            'system_level': 'DEBUG',
            'message_level': 'WARNING',
            'error_level': 'CRITICAL',
            'log_dir': 'logs'
        }

    # 2.2 Remove Default Logger
    logger.remove()  # Clear default console handler

    # 2.3 Add App Log Handler
    logger.add(
        os.path.join(log_config['log_dir'], "app_{time:YYYY-MM-DD}.log"),
        level=log_config.get('app_level', 'INFO'),
        rotation="1 day",
        format="{time} | {level} | {name}:{function}:{line} | {message}",
        backtrace=True,
        diagnose=True
    )

    # 2.4 Add Error Log Handler
    logger.add(
        os.path.join(log_config['log_dir'], "errors.log"),
        level=log_config.get('error_level', 'CRITICAL'),
        rotation="1 week",
        format="{time} | {level} | {name}:{function}:{line} | {extra[trace]} | {message}",
        backtrace=True,
        diagnose=True
    )

    # 2.5 Add Console Handler for Messages
    logger.add(
        sys.stderr,
        level=log_config.get('message_level', 'WARNING'),
        format="{time} | {level} | {message}"
    )

    # 2.6 Log Setup Completion
    logger.info("Logger initialized with config from {}", config_path)

# 3.0 Sanitize Sensitive Data
def sanitize_vars(data: dict) -> dict:
    """Sanitizes sensitive data (e.g., API keys) before logging."""
    # 3.1 Copy Input
    sanitized = data.copy()
    
    # 3.2 Mask Sensitive Keys
    sensitive_keys = [
        'API_TMDB_KEY', 'API_TMDB_TOKEN', 'API_TVMAZE_EMAIL', 'API_TVMAZE_KEY',
        'API_TRAKT.TV_USER', 'API_GOOGLE_OAUTH2.0_CLIENTID', 'API_GOOGLE_OAUTH2.0_CLIENTSECRET'
    ]
    for key in sensitive_keys:
        if key in sanitized:
            sanitized[key] = '***'  # Mask sensitive value
    return sanitized

# 4.0 Initialize Logger on Module Import
if __name__ != "__main__":
    # 4.1 Setup Logger for Module Usage
    setup_logger()
    logger.debug("Logger module loaded")
```
