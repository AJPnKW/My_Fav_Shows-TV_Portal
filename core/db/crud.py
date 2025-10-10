```python
# -*- coding: utf-8 -*-
# File: crud.py
# Description: JSON-based CRUD operations for MY_Fav_Shows-TV_Portal (initial storage, migrate to DB later)
# Author: Grok 4 (xAI)
# Created: 2025-10-10
# Version: 1.0

# 1.0 Imports
import json
from pathlib import Path
from core.data_models import MediaItem
from core.utils.logger import logger

# 2.0 JSON File Path
DATA_FILE = Path("data/media.json")

# 3.0 Load Data
def load_media_items() -> list[MediaItem]:
    """Loads media items from JSON file."""
    # 3.1 Check File Existence
    if not DATA_FILE.exists():
        logger.info("JSON file not found, creating empty file")
        DATA_FILE.parent.mkdir(exist, parents=True)
        with DATA_FILE.open("w") as f:
            json.dump([], f)
        return []
    
    # 3.2 Load JSON
    with DATA_FILE.open("r") as f:
        data = json.load(f)
    
    # 3.3 Parse to MediaItem
    items = [MediaItem(**d) for d in data]
    logger.debug("Loaded {} media items from JSON", len(items))
    return items

# 4.0 Save Data
def save_media_items(items: list[MediaItem]) -> None:
    """Saves media items to JSON file."""
    # 4.1 Convert to Dict
    data = [i.dict() for i in items]
    
    # 4.2 Write JSON
    with DATA_FILE.open("w") as f:
        json.dump(data, f, indent=4)
    
    # 4.3 Log Completion
    logger.info("Saved {} media items to JSON", len(items))

# 5.0 Upsert Media Items
def upsert_media_items(items: list[MediaItem]) -> None:
    """Upserts media items into JSON (replace or add)."""
    # 5.1 Load Existing Data
    existing = {i.id: i for i in load_media_items()}
    
    # 5.2 Upsert Items
    for item in items:
        existing[item.id] = item
        logger.debug("Upserted item: {}", item.name)
    
    # 5.3 Save Updated Data
    save_media_items(list(existing.values()))
    logger.info("Upserted {} media items to JSON", len(items))
```














































