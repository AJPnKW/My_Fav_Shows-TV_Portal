```python
# -*- coding: utf-8 -*-
# File: data_models.py
# Description: Defines Pydantic schemas for MY_Fav_Shows-TV_Portal to validate and structure media data
# Author: Grok 4 (xAI)
# Created: 2025-10-10
# Version: 1.0

# 1.0 Imports
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from core.utils.logger import logger

# 2.0 Media Item Schema
class MediaItem(BaseModel):
    """Represents a unified show or movie from multiple API sources."""
    # 2.1 Core Fields
    id: str = Field(..., description="Composite ID (e.g., 'tmdb:123|tvmaze:456|trakt:789')")
    name: str = Field(..., description="Title of the show or movie")
    tmdb_id: Optional[int] = Field(None, description="TMDB ID, if available")
    tvmaze_id: Optional[int] = Field(None, description="TVMaze ID, if available")
    trakt_id: Optional[int] = Field(None, description="Trakt ID, if available")
    type: str = Field(..., description="Media type: 'tv' or 'movie'")
    overview: Optional[str] = Field(None, description="Brief description")
    status: str = Field(default="unknown", description="Production status (e.g., 'ended')")
    
    # 2.2 Metadata Fields
    genres: List[str] = Field(default_factory=list, description="List of genres")
    networks: Optional[List[dict]] = Field(None, description="Networks, e.g., [{'name': 'HBO', 'country': 'US'}]")
    score: Optional[float] = Field(None, description="Average score across sources")
    poster_url: Optional[str] = Field(None, description="URL to poster image")
    banner_url: Optional[str] = Field(None, description="URL to banner image")
    
    # 2.3 User-Specific Fields
    is_favorite: bool = Field(default=False, description="User marked as favorite")
    is_watchlist: bool = Field(default=False, description="User marked for watchlist")
    watch_progress: Optional[str] = Field(None, description="Watch progress, e.g., 'S1E5'")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")

    # 2.4 Validation
    class Config:
        """Pydantic configuration for MediaItem."""
        validate_assignment = True
        extra = "forbid"

    def __init__(self, **data):
        """Initialize MediaItem and log creation."""
        super().__init__(**data)
        logger.debug("Created MediaItem: {}", self.name)

# 3.0 Season Schema
class Season(BaseModel):
    """Represents a season of a TV show."""
    # 3.1 Core Fields
    number: int = Field(..., description="Season number")
    name: Optional[str] = Field(None, description="Season name, if available")
    poster_url: Optional[str] = Field(None, description="URL to season poster")
    episodes: List["Episode"] = Field(default_factory=list, description="List of episodes")

    # 3.2 Validation
    class Config:
        validate_assignment = True
        extra = "forbid"

    def __init__(self, **data):
        """Initialize Season and log creation."""
        super().__init__(**data)
        logger.debug("Created Season: number {}", self.number)

# 4.0 Episode Schema
class Episode(BaseModel):
    """Represents an episode of a TV show."""
    # 4.1 Core Fields
    number: int = Field(..., description="Episode number")
    name: str = Field(..., description="Episode title")
    air_date: Optional[datetime] = Field(None, description="Air date of episode")
    image_url: Optional[str] = Field(None, description="URL to episode image")

    # 4.2 Validation
    class Config:
        validate_assignment = True
        extra = "forbid"

    def __init__(self, **data):
        """Initialize Episode and log creation."""
        super().__init__(**data)
        logger.debug("Created Episode: {} (number {})", self.name, self.number)

# 5.0 Schedule Schema
class Schedule(BaseModel):
    """Represents a broadcast schedule for episodes."""
    # 5.1 Core Fields
    date: datetime = Field(..., description="Schedule date")
    episodes: List[Episode] = Field(default_factory=list, description="Episodes airing on date")

    # 5.2 Validation
    class Config:
        validate_assignment = True
        extra = "forbid"

    def __init__(self, **data):
        """Initialize Schedule and log creation."""
        super().__init__(**data)
        logger.debug("Created Schedule for date: {}", self.date)

# 6.0 Resolve Forward Reference
Season.update_forward_refs()
```
