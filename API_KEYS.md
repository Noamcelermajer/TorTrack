# API Keys Setup Guide

## 🔐 Keeping Your API Keys Secure

This project uses environment variables to keep API keys secure and out of version control.

⚠️ **IMPORTANT**: Never put actual API keys in any file that gets committed to Git!

## Setup Instructions

### For Docker (Recommended)

1. **Create a `.env` file in the root directory with:**
   ```
   PROWLARR_API_KEY=your_api_key_here
   TMDB_API_KEY=your_api_key_here
   QBITTORRENT_USERNAME=admin
   QBITTORRENT_PASSWORD=your_password_here
   ```

2. **Fill in your API keys:**
   - `PROWLARR_API_KEY`: Get from Prowlarr Settings → General → API Key
   - `TMDB_API_KEY`: Get from https://www.themoviedb.org/settings/api
   - `QBITTORRENT_PASSWORD`: Change this to a secure password

### For Local Development

1. **Create a `backend/.env` file with:**
   ```
   PROWLARR_URL=http://localhost:9696
   PROWLARR_API_KEY=your_api_key_here
   TMDB_API_KEY=your_api_key_here
   QBITTORRENT_URL=http://localhost:8080
   QBITTORRENT_USERNAME=admin
   QBITTORRENT_PASSWORD=adminpass
   FLASK_ENV=development
   FLASK_DEBUG=1
   ```

## Required .env Format

Your `backend/.env` file should look like this (with your actual keys):

```bash
# Prowlarr Configuration
PROWLARR_URL=http://localhost:9696
PROWLARR_API_KEY=<your-actual-prowlarr-key>

# TMDb Configuration  
TMDB_API_KEY=<your-actual-tmdb-key>

# qBittorrent Configuration
QBITTORRENT_URL=http://localhost:8080
QBITTORRENT_USERNAME=admin
QBITTORRENT_PASSWORD=adminpass

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=1
```

⚠️ **Remember**: The `.env` files are ignored by Git, so your keys stay private!

## Getting API Keys

### TMDb API Key
1. Sign up at https://www.themoviedb.org/signup
2. Go to Settings → API
3. Request an API key (choose "Developer" option)
4. Copy your API Key (v3 auth)

### Prowlarr API Key
1. Access your Prowlarr instance
2. Go to Settings → General
3. Copy the API Key

## Security Notes

✅ **DO:**
- Keep your `.env` file local only
- Use different API keys for development and production
- Rotate keys periodically

❌ **DON'T:**
- Commit `.env` files to Git
- Share API keys in issues or pull requests
- Use the example values in production
- Put actual API keys in any file that gets tracked by Git

## Verification

The `.gitignore` file is configured to exclude:
- `.env`
- `backend/.env`
- Any `.env.*` files

This ensures your API keys stay safe and won't be accidentally pushed to GitHub. 