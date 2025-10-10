```python
# -*- coding: utf-8 -*-
# File: tvmaze_syncer.py
# Description: Syncs media item changes to TVMaze API
# Author: Grok 4 (xAI)
# Created: 2025-10-10
# Version: 1.0

# 1.0 Imports
import requests
from core.data_models import MediaItem
from core.utils.logger import logger
from core.utils.helpers import load_env_vars, retry_api

# 2.0 Sync Logic
@retry_api()
def sync_to_tvmaze(items: list[MediaItem]) -> bool:
    """Syncs changed items to TVMaze favorites."""
    # 2.1 Load Environment Variables
    env_vars = load_env_vars()
    email = env_vars.get('API_TVMAZE_EMAIL')
    api_key = env_vars.get('API_TVMAZE_KEY')
    
    # 2.2 Validate Credentials
    if not email or not api_key:
        logger.critical("Missing TVMaze credentials")
        return False
    
    # 2.3 Sync Items
    headers = {"Authorization": f"Bearer {api_key}"}
    for item in items:
        if not item.tvmaze_id:
            logger.warning("Skipping sync for {}: No TVMaze ID", item.name)
            continue
        try:
            # 2.4 Update Favorite Status
            if item.is_favorite:
                requests.post(
                    f"https://api.tvmaze.com/v1/user/{email}/favorites/{item.tvmaze_id}",
                    headers=headers
                ).raise_for_status()
                logger.info("Added {} to TVMaze favorites", item.name)
            else:
                requests.delete(
                    f"https://api.tvmaze.com/v1/user/{email}/favorites/{item.tvmaze_id}",
                    headers=headers
                ).raise_for_status()
                logger.info("Removed {} from TVMaze favorites", item.name)
        except Exception as e:
            logger.error("Failed to sync {}: {}", item.name, str(e))
            return False
    
    # 2.5 Log Completion
    logger.info("TVMaze sync complete")
    return True
```
