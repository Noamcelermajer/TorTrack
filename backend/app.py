from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
from dotenv import load_dotenv
import requests
import logging
from datetime import datetime
import json

# Load environment variables from .env file
# This will load from backend/.env in development or /app/.env in Docker
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='./frontend' if os.path.exists('./frontend') else '../frontend', static_url_path='')
CORS(app)

# Configuration
app.config['PROWLARR_URL'] = os.getenv('PROWLARR_URL', 'http://localhost:9696')
app.config['PROWLARR_API_KEY'] = os.getenv('PROWLARR_API_KEY', '')
app.config['TMDB_API_KEY'] = os.getenv('TMDB_API_KEY', '')
app.config['QBITTORRENT_URL'] = os.getenv('QBITTORRENT_URL', 'http://localhost:8080')
app.config['QBITTORRENT_USERNAME'] = os.getenv('QBITTORRENT_USERNAME', 'admin')
app.config['QBITTORRENT_PASSWORD'] = os.getenv('QBITTORRENT_PASSWORD', 'adminpass')


def search_prowlarr(query, category=None):
    """Search for torrents using Prowlarr API"""
    if not app.config['PROWLARR_API_KEY']:
        logger.warning("Prowlarr API key not configured")
        return []
    
    try:
        # Prowlarr search endpoint
        url = f"{app.config['PROWLARR_URL']}/api/v1/search"
        
        # Search parameters
        params = {
            'query': query,
            'type': 'search'
        }
        
        # Add category if specified (2000 = Movies, 5000 = TV)
        if category:
            params['categories'] = [category]
        
        # Headers with API key
        headers = {
            'X-Api-Key': app.config['PROWLARR_API_KEY']
        }
        
        logger.info(f"Searching Prowlarr for: {query}")
        logger.info(f"Prowlarr URL: {url}")
        response = requests.get(url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        
        results = response.json()
        logger.info(f"Found {len(results)} results from Prowlarr")
        
        # Log first result for debugging
        if results and len(results) > 0:
            logger.info(f"First result example: {results[0]}")
        
        # Normalize results
        normalized_results = []
        for torrent in results:
            normalized = {
                'title': torrent.get('title', 'Unknown'),
                'indexer': torrent.get('indexer', 'Unknown'),
                'size': format_bytes(torrent.get('size', 0)),
                'size_bytes': torrent.get('size', 0),
                'seeders': torrent.get('seeders', 0),
                'leechers': torrent.get('leechers', 0),
                'magnet_link': torrent.get('magnetUrl', ''),
                'download_url': torrent.get('downloadUrl', ''),
                'info_url': torrent.get('infoUrl', ''),
                'published_date': torrent.get('publishDate', ''),
                'category': parse_category(torrent.get('categories', [])),
                'quality': extract_quality(torrent.get('title', '')),
                'guid': torrent.get('guid', '')
            }
            
            # Only include torrents with magnet links or download URLs
            if normalized['magnet_link'] or normalized['download_url']:
                normalized_results.append(normalized)
        
        logger.info(f"Normalized {len(normalized_results)} results with magnet/download links")
        
        # Sort by seeders (descending) and quality score
        def sort_key(x):
            # Higher score for better quality
            quality_score = {
                '4K': 100,
                '2160p': 100,
                '1080p': 80,
                'BluRay': 70,
                'WEB-DL': 60,
                '720p': 50,
                'WEBRip': 40,
                'HDTV': 30,
                '480p': 20,
                'DVDRip': 10
            }.get(x['quality'], 0)
            
            # Combine seeders and quality for sorting
            return (x['seeders'] * 10) + quality_score
        
        normalized_results.sort(key=sort_key, reverse=True)
        
        # Limit to top 50 results for faster response
        return normalized_results[:50]
        
    except requests.exceptions.Timeout:
        logger.error("Prowlarr request timed out")
        return []
    except requests.exceptions.RequestException as e:
        logger.error(f"Prowlarr request failed: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error searching Prowlarr: {e}")
        logger.exception(e)  # This will log the full traceback
        return []


def format_bytes(bytes_value):
    """Format bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} PB"


def parse_category(categories):
    """Parse category IDs to human readable format"""
    if not categories:
        return "Unknown"
    
    # Common category mappings
    category_map = {
        2000: "Movies",
        2010: "Movies/Foreign",
        2020: "Movies/Other",
        2030: "Movies/SD",
        2040: "Movies/HD",
        2045: "Movies/UHD",
        2050: "Movies/BluRay",
        2060: "Movies/3D",
        5000: "TV",
        5020: "TV/Foreign",
        5030: "TV/SD",
        5040: "TV/HD",
        5045: "TV/UHD",
        5050: "TV/Other",
        5070: "TV/Anime"
    }
    
    # Check each category
    for cat in categories:
        if isinstance(cat, dict) and 'id' in cat:
            cat_id = cat['id']
            if cat_id in category_map:
                return category_map[cat_id]
        elif isinstance(cat, int):
            if cat in category_map:
                return category_map[cat]
    
    return "Other"


def extract_quality(title):
    """Extract quality information from torrent title"""
    title_lower = title.lower()
    
    if '2160p' in title_lower or '4k' in title_lower or 'uhd' in title_lower:
        return '4K'
    elif '1080p' in title_lower:
        return '1080p'
    elif '720p' in title_lower:
        return '720p'
    elif '480p' in title_lower:
        return '480p'
    elif 'hdtv' in title_lower:
        return 'HDTV'
    elif 'webrip' in title_lower or 'web-rip' in title_lower:
        return 'WEBRip'
    elif 'webdl' in title_lower or 'web-dl' in title_lower:
        return 'WEB-DL'
    elif 'bluray' in title_lower or 'blu-ray' in title_lower:
        return 'BluRay'
    elif 'dvdrip' in title_lower:
        return 'DVDRip'
    
    return 'Unknown'


def qbittorrent_login():
    """Login to qBittorrent and get session cookie"""
    try:
        login_url = f"{app.config['QBITTORRENT_URL']}/api/v2/auth/login"
        login_data = {
            'username': app.config['QBITTORRENT_USERNAME'],
            'password': app.config['QBITTORRENT_PASSWORD']
        }
        
        session = requests.Session()
        response = session.post(login_url, data=login_data)
        
        if response.text == 'Ok.':
            logger.info("Successfully logged into qBittorrent")
            return session
        else:
            logger.error(f"Failed to login to qBittorrent: {response.text}")
            return None
            
    except Exception as e:
        logger.error(f"Error connecting to qBittorrent: {e}")
        return None


def add_torrent_to_qbittorrent(magnet_link, category, title):
    """Add torrent to qBittorrent with proper settings"""
    session = qbittorrent_login()
    if not session:
        return False, "Failed to connect to qBittorrent"
    
    try:
        # Determine save path based on category
        if 'TV' in category or 'show' in title.lower():
            save_path = 'C:/shows'
            qb_category = 'tv'
        else:
            save_path = 'C:/movies'
            qb_category = 'movies'
        
        # Add torrent
        add_url = f"{app.config['QBITTORRENT_URL']}/api/v2/torrents/add"
        torrent_params = {
            'urls': magnet_link,
            'savepath': save_path,
            'category': qb_category,
            'sequentialDownload': 'true',  # Enable sequential download
            'firstLastPiecePrio': 'true',   # Prioritize first and last pieces
        }
        
        response = session.post(add_url, data=torrent_params)
        
        if response.status_code == 200:
            logger.info(f"Successfully added torrent: {title} to {save_path}")
            return True, f"Download started! Saving to {save_path}"
        else:
            logger.error(f"Failed to add torrent: {response.status_code} - {response.text}")
            return False, "Failed to add torrent to qBittorrent"
            
    except Exception as e:
        logger.error(f"Error adding torrent: {e}")
        return False, f"Error: {str(e)}"
    finally:
        # Logout
        try:
            session.get(f"{app.config['QBITTORRENT_URL']}/api/v2/auth/logout")
        except:
            pass


@app.route('/')
def index():
    """Serve the frontend application"""
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'TorTrack API'})


@app.route('/api/search', methods=['POST'])
def search():
    """Search for torrents using Prowlarr"""
    data = request.get_json()
    query = data.get('query', '')
    category = data.get('category', None)  # Optional: 2000 for movies, 5000 for TV
    
    if not query:
        return jsonify({'error': 'No search query provided'}), 400
    
    # Check if Prowlarr is configured
    if not app.config['PROWLARR_API_KEY']:
        return jsonify({
            'error': 'Prowlarr not configured',
            'message': 'Please configure PROWLARR_API_KEY in your .env file'
        }), 503
    
    # Search using Prowlarr
    results = search_prowlarr(query, category)
    
    return jsonify({
        'query': query,
        'results': results,
        'count': len(results)
    })


@app.route('/api/download', methods=['POST'])
def download():
    """Trigger download via qBittorrent"""
    data = request.get_json()
    magnet_link = data.get('magnet', '')
    title = data.get('title', 'Unknown')
    category = data.get('category', 'Unknown')
    
    if not magnet_link:
        return jsonify({'error': 'No magnet link provided'}), 400
    
    # Add torrent to qBittorrent
    success, message = add_torrent_to_qbittorrent(magnet_link, category, title)
    
    if success:
        return jsonify({
            'success': True,
            'message': message
        })
    else:
        return jsonify({
            'success': False,
            'error': message
        }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 