```python
# -*- coding: utf-8 -*-
# File: models.py
# Description: Defines SQLAlchemy ORM tables for MY_Fav_Shows+TV_Portal database
# Author: Grok 4 (xAI)
# Created: 2025-10-10
# Version: 1.0

# 1.0 Imports
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from core.utils.logger import logger

# 2.0 Base Setup
Base = declarative_base()

# 3.0 Media Item Table
class MediaItemDB(Base):
    """SQLAlchemy table for MediaItem schema."""
    # 3.1 Table Definition
    __tablename__ = "media_items"
    
    id = Column(String, primary_key=True)  # Composite ID (e.g., "tmdb:123|tvmaze:456|trakt:789")
    name = Column(String, nullable=False)
    tmdb_id = Column(Integer, nullable=True)
    tvmaze_id = Column(Integer, nullable=True)
    trakt_id = Column(Integer, nullable=True)
    type = Column(String, nullable=False)  # "tv" or "movie"
    overview = Column(String, nullable=True)
    status = Column(String, default="unknown")
    genres = Column(JSON, default=[])  # List of genres
    networks = Column(JSON, nullable=True)  # List of network dicts
    score = Column(Float, nullable=True)
    poster_url = Column(String, nullable=True)
    banner_url = Column(String, nullable=True)
    is_favorite = Column(Boolean, default=False)
    is_watchlist = Column(Boolean, default=False)
    watch_progress = Column(String, nullable=True)
    updated_at = Column(DateTime, nullable=False)

    # 3.2 Initialization
    def __init__(self, **kwargs):
        """Initialize MediaItemDB and log creation."""
        super().__init__(**kwargs)
        # 3.3 Log Creation
        logger.debug("Created MediaItemDB: {}", self.name)
```
