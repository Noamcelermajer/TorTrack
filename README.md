# Torrent Downloader Web App with Metadata – Project Overview

## 🔰 Project Purpose

A lightweight, self-hosted web application that enables users to:

- Search for movies or TV shows
- View metadata (posters, release year, overview)
- Download content via magnet links using qBittorrent Web API
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
  - Title
  - Year
  - Poster image
  - Short plot/description
- "Download" button per result
- Optional: Status feedback (e.g., "Download started")

#### Technologies:
- HTML + CSS (Tailwind, Bootstrap, or similar)
- JavaScript (plain or with a lightweight framework like Alpine.js or Vue if needed)
- Responsive design for mobile devices

---

### 2. **Backend (API Server)**

**Purpose:** Serve the frontend, handle torrent search, metadata fetch, and control qBittorrent.

#### Responsibilities:
- Accept search queries from frontend
- Query **Prowlarr** API to search across multiple torrent indexers and return torrent results
- Fetch metadata (poster, overview, year) from TMDb or OMDb API
- Normalize and enrich search results with metadata
- Trigger download via qBittorrent Web API when requested

#### Technologies:
- Python (Flask / FastAPI) or Node.js (Express)
- RESTful API design
- API key config for TMDb / OMDb and Prowlarr
- Environment variable or config file for qBittorrent credentials

---

### 3. **Torrent Indexer Integration**

**Purpose:** Source magnet links or torrent files for requested media.

#### Approach:
- Use **Prowlarr** as a unified torrent indexer proxy, aggregating results from multiple torrent indexers via a single API
- Requires running and configuring Prowlarr separately
- Your backend queries Prowlarr's API for torrent search results, eliminating the need for direct site scraping

#### Requirements:
- Handle Prowlarr API authentication and query formatting
- Normalize torrent results (title cleaning, ranking by seeds/peers, resolution, size)

---

### 4. **Metadata Fetching**

**Purpose:** Enhance UI with recognizable data like images, synopsis, and release date.

#### Options:
- **TMDb API** (preferred for rich images and structure)
- **OMDb API** (simpler JSON structure, limited image support)

#### Workflow:
- Clean title from torrent filename (e.g. `Movie.2024.1080p`) to `Movie`
- Query metadata API
- Extract and return: poster URL, title, year, overview

---

### 5. **qBittorrent Integration**

**Purpose:** Automatically download magnet links through the local or remote qBittorrent client.

#### Requirements:
- Authenticate with qBittorrent Web API
- Submit magnet link with optional category/path
- Handle basic error cases (e.g., invalid link, auth failure)
- Optional: Return download status to frontend

---

### 6. **Deployment & Networking**

#### Requirements:
- Dockerized app with:
  - API server
  - Static frontend
- Runs alongside Jellyfin on the same machine or server
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

## 🚀 Optional Enhancements

- Download history or queue tracking
- Torrent health stats (seeds/peers) in UI
- Category selection (e.g., Movies vs TV)
- Integration with Jellyfin to trigger metadata refresh or media scan
- Persistent metadata caching (e.g., SQLite or Redis)
- Notifications (Telegram, Pushover, etc.)

---

## 📁 Folder Structure (Conceptual)
