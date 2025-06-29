# Changelog

All notable changes to TorTrack will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2025-06-29

### Sprint 2: Prowlarr Integration & Smart Downloads

#### Added
- **Prowlarr Integration**: Full integration with Prowlarr API for torrent search
- **Real Search Results**: Live torrent search with 275+ indexers via Prowlarr
- **Smart Download Paths**: Automatic categorization (TV shows → C:/shows, Movies → C:/movies)
- **qBittorrent Integration**: Complete download functionality with API integration
- **Sequential Downloads**: Enabled first/last piece priority for faster streaming
- **Search Optimization**: Limited to top 50 results sorted by quality and seeders
- **Quality Detection**: Automatic quality extraction (4K, 1080p, BluRay, etc.)
- **Seeder Health Indicators**: Color-coded seeder counts (green/yellow/red)
- **Category Parsing**: Intelligent category detection from Prowlarr data
- **Error Handling**: Comprehensive error handling for API failures
- **Download Feedback**: Success/error messages for download attempts

#### Enhanced
- **Search Performance**: Faster results with intelligent sorting and limiting
- **UI Improvements**: Better torrent card display with quality badges
- **Download UX**: Clear feedback on download status and save location
- **Logging**: Detailed logging for debugging and monitoring

#### Technical Improvements
- **API Integration**: Robust Prowlarr and qBittorrent API handling
- **Data Normalization**: Consistent torrent data structure
- **Session Management**: Proper qBittorrent authentication handling
- **Configuration**: Environment-based API key management
- **Docker Setup**: Updated volumes for proper file organization

#### Security
- **Authentication**: Secure API key handling with environment variables
- **qBittorrent Config**: Disabled authentication for local development
- **Error Sanitization**: Safe error messages without sensitive data

#### Fixed
- **Category Parsing**: Fixed bug in category ID handling from Prowlarr
- **Search Results**: Resolved "no results found" issue with proper API integration
- **Download Paths**: Corrected file saving to specified directories

---

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

### Coming in Sprint 3
- TMDb API integration for metadata enrichment
- Movie/show posters and descriptions
- Title cleaning from torrent names
- Enhanced UI with rich media display 