```python
# -*- coding: utf-8 -*-
# File: tmdb_syncer.py
# Description: Syncs media item changes to TMDB API
# Author: Grok 4 (xAI)
# Created: 2025-10-10
# Version: 1.0

# 1.0 Imports
from tmdbv3api import TMDb, Account
from core.data_models import MediaItem
from core.utils.logger import logger
from core.utils.helpers import load_env_vars, retry_api

# 2.0 Sync Logic
@retry_api()
def sync_to_tmdb(items: list[MediaItem]) -> bool:
    """Syncs changed items to TMDB favorites/watchlist."""
    # 2.1 Load Environment Variables
    env_vars = load_env_vars()
    api_key = env_vars.get('API_TMDB_KEY')
    token = env_vars.get('API_TMDB_TOKEN')
    
    # 2.2 Validate Credentials
    if not api_key or not token:
        logger.critical("Missing TMDB credentials")
        return False
    
    # 2.3 Initialize TMDB Client
    tmdb = TMDb()
    tmdb.api_key = api_key
    account = Account()
    
    # 2.4 Sync Items
    for item in items:
        if not item.tmdb_id:
            logger.warning("Skipping sync for {}: No TMDB ID", item.name)
            continue
        try:
            # 2.5 Update Favorite Status
            account.mark_as_favorite(
                session_id=token,
                media_type=item.type,
                media_id=item.tmdb_id,
                favorite=item.is_favorite
            )
            logger.info("Updated {} favorite status on TMDB", item.name)
            
            # 2.6 Update Watchlist Status
            account.add_to_watchlist(
                session_id=token,
                media_type=item.type,
                media_id=item.tmdb_id,
                watchlist=item.is_watchlist
            )
            logger.info("Updated {} watchlist status on TMDB", item.name)
        except Exception as e:
            logger.error("Failed to sync {}: {}", item.name, str(e))
            return False
    
    # 2.7 Log Completion
    logger.info("TMDB sync complete")
    return True
```
