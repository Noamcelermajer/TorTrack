# Changelog

All notable changes to TorTrack will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2025-06-29

### Sprint 1: Project Foundation & Jellyfin-Inspired UI

#### Added
- Initial project structure with Flask backend and vanilla JS frontend
- Docker containerization with docker-compose
- qBittorrent integration (container included)
- Jellyfin-inspired UI with dark theme and purple accents (#aa5cc3)
- Responsive media grid layout (2-6 columns)
- Search functionality with loading states
- Toast notifications for user feedback
- Keyboard shortcuts (Ctrl/Cmd + K for search)
- Health check API endpoint
- Secure environment variable management
- Comprehensive documentation (README, SETUP, API_KEYS)
- Sprint-based development plan
- PR documentation folder

#### Security
- API keys stored in `.env` files (excluded from Git)
- CORS properly configured
- Comprehensive `.gitignore` file

#### Technical Details
- **Backend**: Flask 3.0.0, Flask-CORS 4.0.0, Gunicorn 21.2.0
- **Frontend**: HTML5, CSS3, Vanilla JavaScript, Tailwind CSS (CDN)
- **Containerization**: Docker, Docker Compose v3.8
- **Python**: 3.11-slim base image

#### UI Components
- Header with app branding
- Search bar with icon
- Results grid with media cards
- Loading spinner (dual-color animation)
- Error alerts with icons
- Empty state illustration
- Success toast notifications

#### API Endpoints
- `GET /` - Serves the frontend application
- `GET /api/health` - Returns health status
- `POST /api/search` - Search endpoint (scaffolded)
- `POST /api/download` - Download trigger (scaffolded)

#### Docker Services
- `tortrack-app`: Main application (Flask + Gunicorn)
- `tortrack-qbittorrent`: qBittorrent with Web UI

#### Fixed
- Flask static file serving in Docker environment
- Path resolution for frontend assets
- Windows PowerShell command compatibility

---

### Coming in Sprint 2
- Prowlarr API integration
- Real torrent search results
- Torrent data parsing and normalization
- Enhanced result display with torrent details 