## 📅 Updated Project Development Plan – Sprints

### 🧪 Sprint 1 – Project Scaffold (1–2 days)
- Setup project repo and folder structure
- Scaffold backend Flask server and static frontend
- Configure environment variables for Prowlarr, TMDb, qBittorrent
- Docker setup for backend + qBittorrent

### 🔍 Sprint 2 – Prowlarr Integration for Torrent Search (3–4 days)
- Implement backend endpoint to query Prowlarr search API with user queries
- Handle authentication and error cases with Prowlarr API
- Parse and normalize torrent results from Prowlarr response
- Return magnet links and basic torrent info to frontend
- Display search results with minimal UI (title + download button)

### 🖼️ Sprint 3 – Metadata Fetching & Enrichment (2–3 days)
- Clean titles from torrent names for metadata query
- Query TMDb API for metadata (poster, year, overview)
- Merge metadata with Prowlarr torrent results
- Update frontend to display enriched metadata in search results

### ⬇️ Sprint 4 – Download Trigger via qBittorrent API (2–3 days)
- Implement backend API to send magnet URIs to qBittorrent Web API
- Add frontend “Download” button triggers calling this API
- Handle error and success feedback on UI

### 🌍 Sprint 5 – Deployment & Mobile Access (1–2 days)
- Finalize Docker Compose for backend and qBittorrent (assumes Prowlarr runs externally)
- Setup secure remote access (Ngrok or Nginx reverse proxy with HTTPS)
- Implement simple authentication (basic auth or token) for frontend

### 🔄 Sprint 6 – Polish + Optional Features (2–4 days)
- Add download queue status or history display (poll qBittorrent API)
- Cache metadata results to reduce API calls
- Download category filtering or selection
- Optional Jellyfin integration triggers (library scan refresh)
- Notifications (Telegram, email, etc.)

---
