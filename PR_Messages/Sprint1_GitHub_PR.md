## Sprint 1: Project Foundation & Jellyfin-Inspired UI 🎬

### Summary
Completes Sprint 1 of TorTrack - a self-hosted torrent downloader with a beautiful Jellyfin-inspired interface.

### What's New
- 🏗️ **Foundation**: Flask backend + Docker setup with qBittorrent integration
- 🎨 **Jellyfin UI**: Dark theme with purple accents, responsive media grid
- 🔒 **Security**: Secure API key management with `.env` files
- 📱 **Responsive**: Works perfectly on mobile and desktop
- ⚡ **Performance**: Optimized with lazy loading and smooth animations

### Key Features
- Search interface with loading states
- Media card grid (2-6 columns responsive)
- Toast notifications
- Keyboard shortcuts (Ctrl/Cmd + K)
- Docker Compose for easy deployment

### Technical Stack
- Backend: Flask 3.0 + Gunicorn
- Frontend: Vanilla JS + Tailwind CSS
- Containerization: Docker + Docker Compose
- Design: Jellyfin-inspired dark theme

### API Endpoints
- `GET /` - Frontend
- `GET /api/health` - Health check
- `POST /api/search` - Search (scaffolded)
- `POST /api/download` - Download (scaffolded)

### Testing
```bash
docker-compose up -d
# Visit http://localhost:5000
```

### Next: Sprint 2
Prowlarr integration for real torrent search results.

Closes #1 