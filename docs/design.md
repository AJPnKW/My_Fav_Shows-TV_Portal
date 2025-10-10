# MY_Fav_Shows+TV_Portal Design Document

<!-- File: design.md -->
<!-- Description: Comprehensive design for MY_Fav_Shows+TV_Portal -->
<!-- Author: Grok 4 (xAI) -->
<!-- Created: 2025-10-10 -->
<!-- Version: 1.1 -->

## 1.0 Version History
- **Version 1.1**: Added full file implementations, corrected `docs` folder (2025-10-10).
- **Version 1.0**: Initial draft (2025-10-10).

## 2.0 Project Overview
A modular Python app to manage media favorites/watchlists across TVMaze, TMDB, Trakt with a Streamlit GUI.

## 3.0 Requirements
### 3.1 Functional
- Fetch show/movie data (no cast/reviews) from APIs.
- Consolidate via fuzzy mapping.
- Edit and sync watchlist/favorites.
- Neurodivergent-friendly UI.
- Comprehensive logging.

### 3.2 Non-Functional
- Performance: Fetch/sync < 10s for 100 items.
- Usability: High-contrast, simple nav.
- Security: Keys in `.env`.

## 4.0 Architecture
- **Hexagonal**: Core logic decoupled from UI/DB.
- **Structure**:

  my-fav-shows-portal/  ├── app.py  ├── launch_app.py  ├── run_app.bat  ├── requirements.txt  ├── .env.example  ├── .gitignore  ├── cache/  ├── config/  │   └── app_config.yaml  ├── core/  │   ├── init.py  │   ├── data_models.py  │   ├── fetchers/  │   ├── mappers/  │   ├── db/  │   ├── syncers/  │   ├── utils/  │   ├── modules/  ├── data/  ├── docs/  ├── inputs/  ├── logs/  ├── outputs/  ├── reports/  ├── temp/  ├── tests/  ├── ui/

## 5.0 Data Models
- `MediaItem`: Composite ID, name, type, etc.
- `Season`, `Episode`, `Schedule`.

## 6.0 Technology Stack
- Python 3.10+, Streamlit, SQLAlchemy, Pydantic, Loguru, etc.

## 7.0 Version Control
- Git: Track all files except `.env`, `logs/`, `data/`, `cache/`, `temp/`.
- Semantic commits: `feat:`, `fix:`.

## 8.0 Commenting Standards
- Headers: File, Description, Author, Created, Version.
- Numbered sections: `# 1.0 Imports`, `# 2.1 Fetch Logic`.

## 9.0 Logging
- Loguru: `logs/app_YYYY-MM-DD.log`, `logs/errors.log`.
- Levels: INFO, DEBUG, WARNING, CRITICAL.

## 10.0 UI/UX
- Dark theme, editable tables, sidebar nav.
- Accessibility: ARIA, tooltips.

## 11.0 Deployment
- Local: `streamlit run app.py`.
- Streamlit Cloud: Secrets for `.env`.

## 12.0 Future Considerations
- Modules: Settings, analytics, recommendations.
- Enhancements: Real-time sync, cloud DB.
