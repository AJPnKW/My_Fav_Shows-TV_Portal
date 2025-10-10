```python
# -*- coding: utf-8 -*-
# File: helpers.py
# Description: Utility functions for MY_Fav_Shows+TV_Portal, including OAuth2 helpers and data sanitization
# Author: Grok 4 (xAI)
# Created: 2025-10-10
# Version: 1.0

# 1.0 Imports
import os
from dotenv import load_dotenv
from requests_oauthlib import OAuth2Session
from core.utils.logger import logger

# 2.0 Environment Setup
def load_env_vars() -> dict:
    """Loads environment variables from .env file."""
    # 2.1 Load .env File
    load_dotenv()
    
    # 2.2 Collect Relevant Variables
    env_vars = {
        'API_TMDB_KEY': os.getenv('API_TMDB_KEY'),
        'API_TMDB_TOKEN': os.getenv('API_TMDB_TOKEN'),
        'API_TVMAZE_EMAIL': os.getenv('API_TVMAZE_EMAIL'),
        'API_TVMAZE_KEY': os.getenv('API_TVMAZE_KEY'),
        'API_TRAKT.TV_USER': os.getenv('API_TRAKT.TV_USER'),
        'API_GOOGLE_OAUTH2.0_CLIENTID': os.getenv('API_GOOGLE_OAUTH2.0_CLIENTID'),
        'API_GOOGLE_OAUTH2.0_CLIENTSECRET': os.getenv('API_GOOGLE_OAUTH2.0_CLIENTSECRET')
    }
    
    # 2.3 Log Loaded Variables (Sanitized)
    logger.debug("Loaded environment variables: {}", logger.sanitize_vars(env_vars))
    return env_vars

# 3.0 OAuth2 Helper for Trakt
def get_trakt_oauth_session() -> OAuth2Session:
    """Creates an OAuth2 session for Trakt API."""
    # 3.1 Load Client Credentials
    env_vars = load_env_vars()
    client_id = env_vars.get('API_GOOGLE_OAUTH2.0_CLIENTID')
    client_secret = env_vars.get('API_GOOGLE_OAUTH2.0_CLIENTSECRET')
    
    # 3.2 Validate Credentials
    if not client_id or not client_secret:
        logger.critical("Missing Trakt OAuth credentials")
        raise ValueError("Trakt client ID or secret not set in .env")
    
    # 3.3 Initialize OAuth2 Session
    trakt = OAuth2Session(
        client_id=client_id,
        redirect_uri="urn:ietf:wg:oauth:2.0:oob",  # Manual flow for desktop
        scope=["public"]
    )
    
    # 3.4 Check for Cached Token
    token_path = "data/trakt_token.json"
    if os.path.exists(token_path):
        with open(token_path, 'r') as f:
            token = json.load(f)
        logger.info("Loaded cached Trakt token")
        trakt.token = token
    else:
        # 3.5 Generate Authorization URL (Manual Flow)
        auth_url, state = trakt.authorization_url("https://api.trakt.tv/oauth/authorize")
        logger.info("Visit {} to authorize and enter code", auth_url)
        # Note: Manual step; future module can automate via web UI
        raise NotImplementedError("Manual OAuth flow required; save token to data/trakt_token.json")
    
    # 3.6 Log Session Creation
    logger.debug("Trakt OAuth session initialized")
    return trakt

# 4.0 Retry Decorator for API Calls
def retry_api(max_attempts: int = 3, backoff_factor: int = 2):
    """Decorator to retry API calls on failure."""
    # 4.1 Define Decorator
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 4.2 Attempt API Call with Retries
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.warning("Attempt {} failed: {}", attempt + 1, str(e))
                    if attempt == max_attempts - 1:
                        logger.critical("Max retries reached for {}", func.__name__)
                        raise
                    time.sleep(backoff_factor ** attempt)
        return wrapper
    return decorator
```
