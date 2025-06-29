# TorTrack v0.2.0 - Sprint 2 Release

**Release Date**: June 29, 2025  
**Codename**: "Prowlarr Integration"

## 🎉 Major Update: Real Torrent Search & Smart Downloads

TorTrack now provides a complete torrent search and download experience with full Prowlarr integration and intelligent qBittorrent downloads.

## ✨ Highlights

### 🔍 Real Torrent Search
- **Prowlarr Integration**: Search across 275+ torrent indexers
- **Live Results**: Real-time search with instant results
- **Smart Sorting**: Top 50 results sorted by quality and seeders
- **Quality Detection**: Automatic detection of 4K, 1080p, BluRay, etc.

### ⚡ Smart Download System
- **Automatic Categorization**: TV shows → C:/shows, Movies → C:/movies
- **Sequential Downloads**: First/last piece priority for faster streaming
- **qBittorrent Integration**: Complete API integration with session management
- **Download Feedback**: Clear success/error messages with save paths

### 🎨 Enhanced UI
- **Quality Badges**: Visual indicators for video quality
- **Seeder Health**: Color-coded seeder counts (green/yellow/red)
- **Torrent Cards**: Rich information display with category and size
- **Better Feedback**: Improved error handling and user notifications

## 📦 What's New

### Core Features
- **Live Search**: Real-time torrent search via Prowlarr API
- **Smart Downloads**: Automatic file organization by content type
- **Quality Detection**: Intelligent quality extraction from torrent names
- **Performance**: Optimized search with intelligent result limiting
- **Error Handling**: Comprehensive error handling for all API calls

### API Endpoints
- `POST /api/search` - Prowlarr-powered torrent search ✅
- `POST /api/download` - qBittorrent download with categorization ✅

### Docker Services
- **tortrack-app**: Enhanced with Prowlarr + qBittorrent APIs
- **tortrack-qbittorrent**: Updated with sequential download settings

## 🚀 Getting Started

1. Ensure Prowlarr is running on http://localhost:9696
2. Configure your API keys in `.env` file
3. Run `docker-compose up -d --build`
4. Visit http://localhost:5000
5. Search for any movie or TV show
6. Click download to test automatic categorization

## 📋 Requirements

- Docker and Docker Compose
- Prowlarr running on localhost:9696
- API keys for Prowlarr and TMDb
- C:/shows and C:/movies directories (auto-created)

## 🛠️ Technical Stack

- **Backend**: Python 3.11, Flask 3.0, Prowlarr API, qBittorrent API
- **Frontend**: HTML5, CSS3, JavaScript, Tailwind CSS
- **Container**: Docker, Docker Compose
- **Integration**: Full API connectivity with session management

## 📸 New Features

The UI now displays:
- Quality badges (4K, 1080p, BluRay, etc.)
- Seeder health indicators
- Category and file size information
- Download buttons with proper feedback
- Smart categorization messages

## 🔜 Coming Next (Sprint 3)

- TMDb metadata integration
- Movie/show posters and descriptions
- Title cleaning from torrent names
- Enhanced UI with rich media display

## 📝 Migration Notes

This is a major update that adds real functionality:
- Search now returns actual torrent results
- Downloads are fully functional with qBittorrent
- Files are automatically organized by type
- Performance is significantly improved

## 🙏 Acknowledgments

- Prowlarr for the excellent torrent indexer aggregation
- qBittorrent for the robust download client
- The torrent community for maintaining quality indexers

---

**Full Changelog**: [CHANGELOG.md](CHANGELOG.md)  
**Documentation**: [README.md](../README.md)  
**License**: MIT 