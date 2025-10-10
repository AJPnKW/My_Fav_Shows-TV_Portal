```python
# -*- coding: utf-8 -*-
# File: show_mapper.py
# Description: Maps media items across TVMaze, TMDB, and Trakt APIs using fuzzy matching
# Author: Grok 4 (xAI)
# Created: 2025-10-10
# Version: 1.0

# 1.0 Imports
from rapidfuzz import fuzz
from core.data_models import MediaItem
from core.utils.logger import logger

# 2.0 Mapping Logic
def map_shows(items: list[MediaItem]) -> list[MediaItem]:
    """Consolidates media items from multiple sources."""
    # 2.1 Initialize Result
    consolidated = {}
    
    # 2.2 Group by Name (Fuzzy Matching)
    for item in items:
        name = item.name.lower()
        matched = False
        
        # 2.3 Check for Existing Match
        for key, existing in consolidated.items():
            if item.tmdb_id and item.tmdb_id == existing.tmdb_id:
                matched = True
                existing.id = f"{existing.id}|{item.id}"
                existing.tvmaze_id = existing.tvmaze_id or item.tvmaze_id
                existing.trakt_id = existing.trakt_id or item.trakt_id
                existing.is_favorite |= item.is_favorite
                existing.is_watchlist |= item.is_watchlist
                logger.debug("Merged by TMDB ID: {}", item.name)
                break
            elif fuzz.ratio(name, key.lower()) > 80:
                matched = True
                existing.id = f"{existing.id}|{item.id}"
                existing.tvmaze_id = existing.tvmaze_id or item.tvmaze_id
                existing.trakt_id = existing.trakt_id or item.trakt_id
                existing.is_favorite |= item.is_favorite
                existing.is_watchlist |= item.is_watchlist
                logger.debug("Merged by fuzzy match: {}", item.name)
                break
        
        # 2.4 Add New Item
        if not matched:
            consolidated[name] = item
            logger.debug("Added new item: {}", item.name)
    
    # 2.5 Log Completion
    logger.info("Consolidated {} items", len(consolidated))
    return list(consolidated.values())
```
