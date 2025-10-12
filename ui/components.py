```python
# -*- coding: utf-8 -*-
# File: components.py
# Description: Reusable Streamlit components for MY_Fav_Shows-TV_Portal UI
# Author: Grok 4 (xAI)
# Created: 2025-10-10
# Version: 1.0

# 1.0 Imports
import streamlit as st
import polars as pl  # Replaced pandas with polars
from core.utils.logger import logger

# 2.0 Editable Table
def editable_watchlist_table(df: pl.DataFrame) -> pl.DataFrame:
    """Renders an editable table for watchlist/favorites."""
    # 2.1 Configure Table
    logger.info("Rendering watchlist table with {} items", df.height)
    
    # 2.2 Display Table
    edited_df = st.data_editor(
        df,
        column_config={
            "Poster": st.column_config.ImageColumn("Poster"),
            "Favorite": st.column_config.CheckboxColumn("Favorite"),
            "Watchlist": st.column_config.CheckboxColumn("Watchlist"),
            "Trakt Synced": st.column_config.TextColumn("Trakt Synced", disabled=True)
        },
        use_container_width=True
    )
    
    # 2.3 Log Changes
    logger.debug("Table edited: {} rows", edited_df.height)
    return edited_df
```


































