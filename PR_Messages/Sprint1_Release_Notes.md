# TorTrack v0.1.0 - Sprint 1 Release

**Release Date**: June 29, 2025  
**Codename**: "Foundation"

## 🎉 Introducing TorTrack

TorTrack is a self-hosted web application for searching and downloading torrents with a beautiful Jellyfin-inspired interface. This initial release establishes the foundation for a modern, user-friendly torrent management system.

## ✨ Highlights

### 🎨 Jellyfin-Inspired Design
- Beautiful dark theme with purple accents
- Responsive media grid that adapts from mobile to desktop
- Smooth animations and transitions
- Modern, clean interface that feels familiar to Jellyfin users

### 🏗️ Solid Foundation
- Flask-based RESTful API backend
- Docker containerization for easy deployment
- Integrated qBittorrent for torrent management
- Production-ready with Gunicorn

### 🔒 Security First
- Secure API key management with environment variables
- Comprehensive documentation for safe configuration
- Git-ignored sensitive files

## 📦 What's Included

### Core Features
- **Search Interface**: Clean search bar with loading states
- **Media Grid**: Responsive layout (2-6 columns)
- **Notifications**: Toast-style success messages
- **Keyboard Shortcuts**: Ctrl/Cmd + K for quick search
- **Error Handling**: User-friendly error messages

### API Endpoints
- `GET /` - Frontend application
- `GET /api/health` - Service health check
- `POST /api/search` - Search for torrents (ready for integration)
- `POST /api/download` - Trigger downloads (ready for integration)

### Docker Services
- **tortrack-app**: Main application container
- **tortrack-qbittorrent**: qBittorrent with web interface

## 🚀 Getting Started

1. Clone the repository
2. Copy environment template and add your API keys
3. Run `docker-compose up -d`
4. Visit http://localhost:5000

See [SETUP.md](../SETUP.md) for detailed instructions.

## 📋 Requirements

- Docker and Docker Compose
- API keys for TMDb (coming in Sprint 2)
- API key for Prowlarr (coming in Sprint 2)

## 🛠️ Technical Stack

- **Backend**: Python 3.11, Flask 3.0, Gunicorn
- **Frontend**: HTML5, CSS3, JavaScript, Tailwind CSS
- **Container**: Docker, Docker Compose
- **Torrent Client**: qBittorrent

## 📸 Preview

The UI features:
- Dark background (#101010)
- Purple accent color (#aa5cc3)
- Media card grid layout
- Hover animations
- Loading spinners
- Toast notifications

## 🔜 Coming Next (Sprint 2)

- Prowlarr integration for torrent search
- Real search results with torrent information
- Metadata enrichment
- Torrent health indicators

## 📝 Notes

This is an early release focused on establishing the foundation. Search and download functionality will be implemented in Sprint 2.

## 🙏 Acknowledgments

- Inspired by Jellyfin's beautiful UI
- Built with Flask and modern web technologies
- Containerized for easy self-hosting

---

**Full Changelog**: [CHANGELOG.md](CHANGELOG.md)  
**Documentation**: [README.md](../README.md)  
**License**: MIT 