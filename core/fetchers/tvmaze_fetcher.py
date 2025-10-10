```python
# -*- coding: utf-8 -*-
# File: tvmaze_fetcher.py
# Description: Fetches favorites and watchlists from TVMaze API
# Author: Grok 4 (xAI)
# Created: 2025-10-10
# Version: 1.0

# 1.0 Imports
import requests
from core.data_models import MediaItem
from core.utils.logger import logger
from core.utils.helpers import load_env_vars, retry_api

# 2.0 Fetch Logic
@retry_api()
def get_favorites_and_watchlist() -> list[MediaItem]:
    """Fetches TVMaze favorites and watchlists."""
    # 2.1 Load Environment Variables
    env_vars = load_env_vars()
    email = env_vars.get('API_TVMAZE_EMAIL')
    api_key = env_vars.get('API_TVMAZE_KEY')
    
    # 2.2 Validate Credentials
    if not email or not api_key:
        logger.critical("Missing TVMaze credentials")
        raise ValueError("TVMaze email or API key not set")
    
    # 2.3 Fetch Favorites
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(f"https://api.tvmaze.com/v1/user/{email}/favorites", headers=headers)
    response.raise_for_status()
    favorites = response.json().get('favorites', [])
    
    # 2.4 Parse to MediaItem
    items = []
    for fav in favorites:
        show = fav.get('show', {})
        item = MediaItem(
            id=f"tvmaze:{show.get('id')}",
            name=show.get('name'),
            tvmaze_id=show.get('id'),
            type="tv",
            overview=show.get('summary'),
            status=show.get('status', 'unknown'),
            genres=show.get('genres', []),
            networks=[{'name': n.get('name')} for n in show.get('network', [])],
            score=show.get('rating', {}).get('average'),
            poster_url=show.get('image', {}).get('medium'),
            is_favorite=True,
            is_watchlist=False
        )
        items.append(item)
        logger.debug("Parsed TVMaze favorite: {}", item.name)
    
    # 2.5 Log Completion
    logger.info("Fetched {} TVMaze items", len(items))
    return items
```
