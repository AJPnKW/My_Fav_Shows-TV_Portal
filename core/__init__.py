```python
# -*- coding: utf-8 -*-
# File: __init__.py
# Description: Initializes the core package for MY_Fav_Shows-TV_Portal
# Author: Grok 4 (xAI)
# Created: 2025-10-10
# Version: 1.0

from .data_models import MediaItem, Season, Episode, Schedule
from .db.models import Base, Media
from .db.crud import CRUDS
from .fetchers.tmdb_fetcher import fetch_tmdb_data
from .fetchers.tvmaze_fetcher import fetch_tvmaze_data
from .fetchers.trakt_fetcher import fetch_trakt_data
from .mappers.show_mapper import map_shows
from .modules.watchlist_module import WatchlistModule
from .syncers.tmdb_syncer import sync_to_tmdb
from .syncers.tvmaze_syncer import sync_to_tvmaze
from .syncers.trakt_syncer import sync_to_trakt
from .utils.helpers import get_tmdb_session, get_trakt_oauth_session, get_tvmaze_session, retry_api
from .utils.logger import logger

__all__ = [
    "MediaItem",
    "Season",
    "Episode",
    "Schedule",
    "Base",
    "Media",
    "CRUDS",
    "fetch_tmdb_data",
    "fetch_tvmaze_data",
    "fetch_trakt_data",
    "map_shows",
    "WatchlistModule",
    "sync_to_tmdb",
    "sync_to_tvmaze",
    "sync_to_trakt",
    "get_tmdb_session",
    "get_trakt_oauth_session",
    "get_tvmaze_session",
    "retry_api",
    "logger",
]
```


































































