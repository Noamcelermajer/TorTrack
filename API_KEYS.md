# API Keys Setup Guide

## 🔐 Keeping Your API Keys Secure

This project uses environment variables to keep API keys secure and out of version control.

## Setup Instructions

### For Docker (Recommended)

1. **Copy the environment template:**
   ```bash
   cp env.example .env
   ```

2. **Edit `.env` file with your actual API keys:**
   ```bash
   # Open with your favorite editor
   nano .env  # or vim, code, notepad, etc.
   ```

3. **Fill in your API keys:**
   - `PROWLARR_API_KEY`: Get from Prowlarr Settings → General → API Key
   - `TMDB_API_KEY`: Get from https://www.themoviedb.org/settings/api
   - `QBITTORRENT_PASSWORD`: Change this to a secure password

### For Local Development

1. **Copy the backend environment template:**
   ```bash
   cp backend/env.example backend/.env
   ```

2. **Edit `backend/.env` with your API keys**

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

## Verification

The `.gitignore` file is configured to exclude:
- `.env`
- `backend/.env`
- Any `.env.*` files

This ensures your API keys stay safe and won't be accidentally pushed to GitHub. 