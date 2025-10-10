```python
# -*- coding: utf-8 -*-
# File: watchlist_module.py
# Description: Core module for managing watchlist and favorites across APIs
# Author: Grok 4 (xAI)
# Created: 2025-10-10
# Version: 1.0

# 1.0 Imports
from core.fetchers import tvmaze_fetcher, tmdb_fetcher, trakt_fetcher
from core.mappers import map_shows
from core.db.crud import get_db_session, upsert_media_items
from core.syncers import tvmaze_syncer, tmdb_syncer, trakt_syncer
from core.utils.logger import logger

# 2.0 Fetch Watchlist
def get_personal_watchlist() -> list[MediaItem]:
    """Fetches and consolidates watchlist/favorites from all sources."""
    # 2.1 Fetch Data
    logger.info("Starting watchlist fetch")
    tvmaze_data = tvmaze_fetcher.get_favorites_and_watchlist()
    tmdb_data = tmdb_fetcher.get_favorites_and_watchlist()
    trakt_data = trakt_fetcher.get_favorites_and_watchlist()
    
    # 2.2 Log Fetch Results
    logger.debug("Fetched {} TVMaze, {} TMDB, {} Trakt items", 
                 len(tvmaze_data), len(tmdb_data), len(trakt_data))
    
    # 2.3 Consolidate Data
    combined = map_shows(tvmaze_data + tmdb_data + trakt_data)
    
    # 2.4 Save to Database
    with get_db_session() as session:
        upsert_media_items(session, combined)
    
    # 2.5 Log Completion
    logger.info("Consolidated {} unique items", len(combined))
    return combined

# 3.0 Edit and Sync
def edit_and_sync(watchlist: list[MediaItem], changes: dict) -> bool:
    """Applies edits and syncs to APIs."""
    # 3.1 Apply Changes
    logger.info("Applying changes and syncing")
    for item_id, updates in changes.items():
        item = next(i for i in watchlist if i.id == item_id)
        for k, v in updates.items():
            setattr(item, k, v)
        with get_db_session() as session:
            upsert_media_items(session, [item])
    
    # 3.2 Prepare Sync Data
    tvmaze_deltas = [i for i in watchlist if i.tvmaze_id]
    tmdb_deltas = [i for i in watchlist if i.tmdb_id]
    trakt_deltas = [i for i in watchlist if i.trakt_id]
    
    # 3.3 Sync to APIs
    success = all([
        tvmaze_syncer.sync_to_tvmaze(tvmaze_deltas),
        tmdb_syncer.sync_to_tmdb(tmdb_deltas),
        trakt_syncer.sync_to_trakt(trakt_deltas)
    ])
    
    # 3.4 Log Completion
    logger.info("Sync {}", "complete" if success else "failed")
    return success
```
