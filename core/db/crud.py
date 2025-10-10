```python
# -*- coding: utf-8 -*-
# File: crud.py
# Description: Database CRUD operations for MY_Fav_Shows+TV_Portal using SQLAlchemy
# Author: Grok 4 (xAI)
# Created: 2025-10-10
# Version: 1.0

# 1.0 Imports
from sqlalchemy.orm import Session
from core.db.models import MediaItemDB
from core.data_models import MediaItem
from core.utils.logger import logger

# 2.0 Database Session
def get_db_session():
    """Creates a SQLAlchemy session for database operations."""
    # 2.1 Import Database Engine
    from sqlalchemy import create_engine
    # 2.2 Create Engine
    engine = create_engine("sqlite:///data/media.db", echo=False)
    # 2.3 Create Session
    session = Session(bind=engine)
    logger.debug("Created database session")
    return session

# 3.0 Upsert Media Items
def upsert_media_items(session: Session, items: list[MediaItem]) -> None:
    """Upserts media items into the database."""
    # 3.1 Iterate Over Items
    for item in items:
        # 3.2 Create or Update Record
        db_item = session.query(MediaItemDB).filter_by(id=item.id).first()
        if db_item:
            # 3.3 Update Existing
            for key, value in item.dict().items():
                setattr(db_item, key, value)
            logger.debug("Updated MediaItemDB: {}", item.name)
        else:
            # 3.4 Create New
            db_item = MediaItemDB(**item.dict())
            session.add(db_item)
            logger.debug("Added MediaItemDB: {}", item.name)
    # 3.5 Commit Changes
    session.commit()
    logger.info("Upserted {} media items", len(items))
```
