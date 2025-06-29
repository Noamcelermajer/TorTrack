# TorTrack Setup Guide - Sprint 1

## Quick Start

### 1. Configure Environment Variables
```bash
cp config/config.example.txt config/.env
# Edit config/.env with your actual API keys
```

### 2. Run with Docker Compose
```bash
docker-compose up -d
```

### 3. Access the Application
- TorTrack Web UI: http://localhost:5000
- qBittorrent Web UI: http://localhost:8080

## Development Setup

### Backend
```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
python app.py
```

### Frontend
Frontend is served directly by Flask. Just open http://localhost:5000

## Sprint 1 Completed Features
- ✅ Flask backend scaffolding with API endpoints
- ✅ Responsive frontend with search UI
- ✅ Environment configuration for all services
- ✅ Docker setup for easy deployment
- ✅ qBittorrent integration ready

## Next Steps (Sprint 2)
- Implement Prowlarr API integration
- Connect search functionality to real torrent results
- Parse and normalize torrent data 