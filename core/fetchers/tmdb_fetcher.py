```python
# -*- coding: utf-8 -*-
# File: tmdb_fetcher.py
# Description: Fetches favorites and watchlists from TMDB API
# Author: Grok 4 (xAI)
# Created: 2025-10-10
# Version: 1.0

# 1.0 Imports
from tmdbv3api import TMDb, Account
from core.data_models import MediaItem
from core.utils.logger import logger
from core.utils.helpers import load_env_vars, retry_api

# 2.0 Fetch Logic
@retry_api()
def get_favorites_and_watchlist() -> list[MediaItem]:
    """Fetches TMDB favorites and watchlists."""
    # 2.1 Load Environment Variables
    env_vars = load_env_vars()
    api_key = env_vars.get('API_TMDB_KEY')
    token = env_vars.get('API_TMDB_TOKEN')
    
    # 2.2 Validate Credentials
    if not api_key or not token:
        logger.critical("Missing TMDB credentials")
        raise ValueError("TMDB API key or token not set")
    
    # 2.3 Initialize TMDB Client
    tmdb = TMDb()
    tmdb.api_key = api_key
    account = Account()
    
    # 2.4 Fetch Favorites and Watchlist
    favorites = account.get_favorites(session_id=token)
    watchlist = account.get_watchlist(session_id=token)
    
    # 2.5 Parse to MediaItem
    items = []
    for media in favorites + watchlist:
        item = MediaItem(
            id=f"tmdb:{media.get('id')}",
            name=media.get('title') or media.get('name'),
            tmdb_id=media.get('id'),
            type=media.get('media_type'),
            overview=media.get('overview'),
            status="unknown",
            genres=[g['name'] for g in media.get('genres', [])],
            score=media.get('vote_average'),
            poster_url=f"https://image.tmdb.org/t/p/w500{media.get('poster_path')}",
            is_favorite=media in favorites,
            is_watchlist=media in watchlist
        )
        items.append(item)
        logger.debug("Parsed TMDB item: {}", item.name)
    
    # 2.6 Log Completion
    logger.info("Fetched {} TMDB items", len(items))
    return items
```
