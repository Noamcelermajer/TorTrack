# Torrent Downloader Web App with Metadata – Project Overview

## 🔰 Project Purpose

A lightweight, self-hosted web application that enables users to:

- Search for movies or TV shows across 275+ torrent indexers via Prowlarr
- View torrent details (quality, size, seeders, category)
- Download content via magnet links using qBittorrent Web API
- Automatic file organization (TV shows → C:/shows, Movies → C:/movies)
- Use on mobile or desktop browsers
- Integrate with existing media server setups like Jellyfin

The goal is to offer a clean and reliable way to manage torrent downloads remotely without relying on complex or unstable third-party solutions like Sonarr/Radarr.

---

## 📦 Components Overview

### 1. **Frontend (Web Interface)**

**Purpose:** Provide a user-friendly, mobile-compatible UI to perform searches and trigger downloads.

#### Features:
- Search bar for movie/show titles
- Display search results with:
  - Title and quality badges (4K, 1080p, BluRay, etc.)
  - File size and category
  - Seeder/leecher counts with health indicators
  - Indexer information
- "Download" button per result with automatic categorization
- Success/error feedback messages
- Responsive design for mobile devices

#### Technologies:
- HTML + CSS (Tailwind CSS)
- Vanilla JavaScript
- Jellyfin-inspired dark theme

---

### 2. **Backend (API Server)**

**Purpose:** Serve the frontend, handle torrent search, metadata fetch, and control qBittorrent.

#### Responsibilities:
- Accept search queries from frontend
- Query **Prowlarr** API to search across multiple torrent indexers and return torrent results
- Parse and normalize torrent results from Prowlarr response
- Trigger download via qBittorrent Web API with automatic categorization
- Handle error cases and provide feedback

#### Technologies:
- Python (Flask 3.0)
- RESTful API design
- API key config for Prowlarr and TMDb
- Environment variable configuration

---

### 3. **Prowlarr Integration**

**Purpose:** Source magnet links or torrent files for requested media.

#### Approach:
- Use **Prowlarr** as a unified torrent indexer proxy, aggregating results from multiple torrent indexers via a single API
- Requires running and configuring Prowlarr separately
- Your backend queries Prowlarr's API for torrent search results
- Returns top 50 results sorted by quality and seeders

#### Features:
- Real-time search across 275+ indexers
- Quality detection (4K, 1080p, BluRay, WEB-DL, etc.)
- Category parsing and normalization
- Seeder health assessment

---

### 4. **qBittorrent Integration**

**Purpose:** Automatically download magnet links through the local or remote qBittorrent client.

#### Features:
- Authenticate with qBittorrent Web API
- Submit magnet link with automatic categorization
- Sequential download with first/last piece priority
- Smart file organization:
  - TV shows → C:/shows
  - Movies → C:/movies
- Handle basic error cases and provide feedback

---

### 5. **Deployment & Networking**

#### Requirements:
- Dockerized app with:
  - API server
  - Static frontend
  - qBittorrent client
- Runs alongside Prowlarr on the same machine or server
- Can be exposed securely via:
  - **Ngrok** (on-demand public access)
  - **Nginx reverse proxy** (if self-hosted with domain)
  - **Auth**: Simple password or IP whitelist

---

## 🔒 Security Considerations

- API keys are stored in `.env` files that are excluded from Git
- Protect access to the interface with basic auth or IP filtering
- Ensure qBittorrent Web API is not exposed publicly without protection
- Do not log sensitive information (e.g., API keys, magnet links)
- See `API_KEYS.md` for secure API key setup instructions

---

## 🚀 Current Status (Sprint 2 Complete)

### ✅ Implemented Features:
- **Prowlarr Integration**: Full API integration for real torrent search
- **Smart Downloads**: Automatic categorization with proper file paths
- **Search Optimization**: Top 50 results with quality-based sorting
- **Enhanced UI**: Quality badges, seeder indicators, better feedback
- **Sequential Downloads**: First/last piece priority for faster streaming
- **Error Handling**: Comprehensive error handling and logging

### 🔜 Coming in Sprint 3:
- TMDb metadata integration for posters and descriptions
- Title cleaning from torrent names
- Enhanced UI with rich media display

---

## 📁 Folder Structure

```
TorTrack/
├── backend/
│   ├── app.py              # Flask API with Prowlarr + qBittorrent integration
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile         # Backend container config
├── frontend/
│   ├── index.html         # Jellyfin-style UI
│   ├── app.js            # Frontend logic with torrent display
│   └── styles.css        # Custom Jellyfin-inspired styles
├── config/
│   └── qbittorrent/
│       └── qBittorrent.conf # qBittorrent configuration
├── PR_Messages/          # Documentation folder
├── docker-compose.yml    # Multi-container orchestration
├── .gitignore           # Git exclusions
├── README.md            # Project overview
├── SETUP.md            # Setup instructions
├── API_KEYS.md         # API key guide
└── Sprints.md          # Development plan
```

---

## 🛠️ Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/TorTrack.git
   cd TorTrack
   ```

2. **Configure API keys**
   - Copy `.env.example` to `.env`
   - Add your Prowlarr and TMDb API keys
   - See `API_KEYS.md` for detailed instructions

3. **Start the application**
   ```bash
   docker-compose up -d --build
   ```

4. **Access the application**
   - TorTrack Web UI: http://localhost:5000
   - qBittorrent Web UI: http://localhost:8080

---

## 📋 Requirements

- Docker and Docker Compose
- Prowlarr running on localhost:9696
- API keys for Prowlarr and TMDb
- C:/shows and C:/movies directories (auto-created)

---

## 🎯 Features

- **Real-time Search**: Search across 275+ torrent indexers
- **Smart Categorization**: Automatic TV/Movie organization
- **Quality Detection**: 4K, 1080p, BluRay, WEB-DL detection
- **Sequential Downloads**: Faster streaming with piece prioritization
- **Responsive Design**: Works on mobile and desktop
- **Jellyfin-inspired UI**: Beautiful dark theme with purple accents
