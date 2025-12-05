```python
# -*- coding: utf-8 -*-
# File: app.py
# Description: Streamlit entrypoint for MY_Fav_Shows-TV_Portal, managing multi-page UI
# Author: Grok 4 (xAI)
# Created: 2025-10-10
# Version: 1.0

# 1.0 Imports
import streamlit as st
import polars as pl  # Replaced pandas with polars
from core.modules.watchlist_module import get_personal_watchlist, edit_and_sync
from ui.components import editable_watchlist_table
from core.utils.logger import logger

# 2.0 App Setup
st.set_page_config(
    page_title="MY_Fav_Shows+TV_Portal",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.theme({
    'primary': '#FF6B6B',
    'background': '#1E1E1E',
    'text': '#FFFFFF'
})

# 3.0 Sidebar Navigation
st.sidebar.title("🚀 Portal Menu")
page = st.sidebar.selectbox(
    "Go to",
    ["Home", "Watchlist", "Sync", "Help"],
    help="Navigate easily!"
)

# 4.0 Page Rendering
if page == "Watchlist":
    # 4.1 Watchlist Page
    st.header("📺 My Watchlist & Favorites")
    st.info("Edit below to update favorites/watchlist. Sync pushes to APIs.")
    
    # 4.2 Refresh Button
    if st.button("🔄 Refresh Data", help="Pull latest from APIs"):
        with st.spinner("Fetching from TVMaze, TMDB, Trakt..."):
            watchlist = get_personal_watchlist()
            st.session_state.watchlist = watchlist
            logger.info("Watchlist refreshed")
    
    # 4.3 Display Table
    if 'watchlist' in st.session_state:
        df = pl.DataFrame([{
            'Poster': i.poster_url,
            'Name': i.name,
            'Type': i.type,
            'Score': i.score,
            'Networks': ', '.join(n['name'] for n in i.networks or []),
            'Favorite': i.is_favorite,
            'Watchlist': i.is_watchlist,
            'Trakt Synced': '✅' if i.trakt_id else '❌'
        } for i in st.session_state.watchlist])
        
        edited_df = editable_watchlist_table(df)
        
        # 4.4 Sync Changes
        if st.button("💾 Save & Sync", help="Save to DB and push to APIs"):
            changes = {}
            for idx, row in edited_df.iter_rows(named=True):
                orig = st.session_state.watchlist[idx]
                if row['Favorite'] != orig.is_favorite or row['Watchlist'] != orig.is_watchlist:
                    changes[orig.id] = {
                        'is_favorite': row['Favorite'],
                        'is_watchlist': row['Watchlist']
                    }
            if changes:
                with st.spinner("Syncing to APIs..."):
                    success = edit_and_sync(st.session_state.watchlist, changes)
                    if success:
                        st.success("Synced to TVMaze, TMDB, Trakt! 🎉")
                    else:
                        st.error("Sync failed—check logs/errors.log")

elif page == "Help":
    # 4.5 Help Page
    st.markdown("""
    ### Quick Start
    1. Add API keys to `.env`.
    2. For Trakt: Run OAuth flow (check logs for URL).
    3. Run `streamlit run app.py`.
    4. Refresh to pull data.
    5. Edit table, then Sync.
    
    ### Layout
    - **Sidebar**: Simple navigation.
    - **Table**: Searchable, shows posters, sync status.
    - **Errors**: Check `logs/errors.log`.
    """)
else:
    # 4.6 Home Page
    st.title("Welcome to MY_Fav_Shows+TV_Portal")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Shows", len(st.session_state.get('watchlist', [])))
    with col2:
        st.metric("Sources Synced", "3/3" if 'watchlist' in st.session_state else "0/3")
    with col3:
        st.metric("Last Sync", "Never" if 'watchlist' not in st.session_state else "Just now")
```




















































































































































































































