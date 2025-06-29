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


def search_prowlarr(query, filters=None):
    """Search for torrents using Prowlarr API with advanced filtering"""
    if not app.config['PROWLARR_API_KEY']:
        logger.warning("Prowlarr API key not configured")
        return []
    
    try:
        # Clean the search query using guessit for better results
        cleaned_query = clean_title_for_metadata(query, '')
        if cleaned_query and len(cleaned_query) > 2:
            search_query = cleaned_query
            logger.info(f"Using cleaned query: '{cleaned_query}' instead of original: '{query}'")
        else:
            search_query = query
        
        # Prowlarr search endpoint
        url = f"{app.config['PROWLARR_URL']}/api/v1/search"
        
        # Search parameters
        params = {
            'query': search_query,
            'type': 'search'
        }
        
        # Add category filter if specified
        if filters and filters.get('category'):
            category_id = get_category_id(filters['category'])
            if category_id:
                params['categories'] = [category_id]
        
        # Headers with API key
        headers = {
            'X-Api-Key': app.config['PROWLARR_API_KEY']
        }
        
        logger.info(f"Searching Prowlarr for: {search_query} with filters: {filters}")
        response = requests.get(url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        
        results = response.json()
        logger.info(f"Found {len(results)} raw results from Prowlarr")
        
        # Normalize results first
        normalized_results = []
        for torrent in results:
            normalized = {
                'title': torrent.get('title', 'Unknown'),  # Keep original title
                'indexer': torrent.get('indexer', 'Unknown'),
                'size': format_bytes(torrent.get('size', 0)),
                'size_bytes': torrent.get('size', 0),
                'seeders': torrent.get('seeders', 0),
                'leechers': torrent.get('leechers', 0),
                'magnet_link': torrent.get('magnetUrl', ''),
                'download_url': torrent.get('downloadUrl', ''),
                'info_url': torrent.get('infoUrl', ''),
                'publishDate': torrent.get('publishDate', ''),
                'category': parse_category(torrent.get('categories', [])),
                'quality': extract_quality(torrent.get('title', '')),
                'guid': torrent.get('guid', '')
            }
            
            # Only include torrents with magnet links or download URLs
            if normalized['magnet_link'] or normalized['download_url']:
                normalized_results.append(normalized)
        
        # Apply advanced filtering using the new filter_torrents function
        if filters:
            filtered_results = filter_torrents(normalized_results, filters)
        else:
            filtered_results = normalized_results
        
        logger.info(f"Filtered to {len(filtered_results)} results")
        return filtered_results
        
    except requests.exceptions.Timeout:
        logger.error("Prowlarr request timed out")
        return []
    except requests.exceptions.RequestException as e:
        logger.error(f"Prowlarr request failed: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error searching Prowlarr: {e}")
        return []


def get_category_id(category_name):
    """Convert category name to Prowlarr category ID"""
    category_map = {
        'Movies': 2000,
        'TV': 5000,
        'Movies/HD': 2040,
        'Movies/UHD': 2045,
        'TV/HD': 5040,
        'TV/UHD': 5045
    }
    return category_map.get(category_name)


def apply_filters(results, filters):
    """Apply all filters to the results"""
    if not filters:
        return results
    
    filtered_results = []
    
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
        
        # Apply filters
        if not passes_filters(normalized, filters):
            continue
        
        # Only include torrents with magnet links or download URLs
        if normalized['magnet_link'] or normalized['download_url']:
            filtered_results.append(normalized)
    
    logger.info(f"Filtered to {len(filtered_results)} results")
    return filtered_results


def passes_filters(torrent, filters):
    """Check if torrent passes all applied filters"""
    
    # Quality filter
    if filters.get('quality') and torrent['quality'] != filters['quality']:
        return False
    
    # Size filter
    if filters.get('min_size'):
        min_size_bytes = parse_size_to_bytes(filters['min_size'])
        if torrent['size_bytes'] < min_size_bytes:
            return False
    
    # Seeders filter
    if filters.get('min_seeders'):
        min_seeders = int(filters['min_seeders'])
        if torrent['seeders'] < min_seeders:
            return False
    
    # Season type filter
    if filters.get('season_type') and is_tv_show(torrent['category']):
        season_type = filters['season_type']
        if season_type == 'full_season' and not is_full_season(torrent['title']):
            return False
        elif season_type == 'single_episode' and is_full_season(torrent['title']):
            return False
        elif season_type == 'complete_series' and not is_complete_series(torrent['title']):
            return False
    
    return True


def parse_size_to_bytes(size_str):
    """Convert size string (e.g., '1GB') to bytes"""
    size_str = size_str.upper()
    if 'GB' in size_str:
        return int(float(size_str.replace('GB', '')) * 1024 * 1024 * 1024)
    elif 'MB' in size_str:
        return int(float(size_str.replace('MB', '')) * 1024 * 1024)
    elif 'KB' in size_str:
        return int(float(size_str.replace('KB', '')) * 1024)
    else:
        return int(size_str)


def is_complete_series(title):
    """Check if the torrent title indicates a complete series"""
    title_lower = title.lower()
    series_keywords = ['complete series', 'full series', 'series pack', 'complete collection']
    return any(keyword in title_lower for keyword in series_keywords)


def sort_results(results, sort_by):
    """Sort results based on the specified criteria"""
    if sort_by == 'seeders':
        return sorted(results, key=lambda x: x['seeders'], reverse=True)
    elif sort_by == 'size':
        return sorted(results, key=lambda x: x['size_bytes'], reverse=True)
    elif sort_by == 'date':
        return sorted(results, key=lambda x: x['published_date'], reverse=True)
    else:  # relevance (default)
        # Sort by seeders and quality score
        def relevance_score(x):
            quality_score = {
                '4K': 100, '2160p': 100, '1080p': 80, 'BluRay': 70,
                'WEB-DL': 60, '720p': 50, 'WEBRip': 40, 'HDTV': 30,
                '480p': 20, 'DVDRip': 10
            }.get(x['quality'], 0)
            return (x['seeders'] * 10) + quality_score
        
        return sorted(results, key=relevance_score, reverse=True)


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
    """Search for torrents using Prowlarr with advanced filtering"""
    data = request.get_json()
    query = data.get('query', '')
    filters = data.get('filters', {})
    
    if not query:
        return jsonify({'error': 'No search query provided'}), 400
    
    # Log the filters being applied
    logger.info(f"Search request - Query: '{query}', Filters: {filters}")
    
    # Check if Prowlarr is configured
    if not app.config['PROWLARR_API_KEY']:
        return jsonify({
            'error': 'Prowlarr not configured',
            'message': 'Please configure PROWLARR_API_KEY in your .env file'
        }), 503
    
    # Search using Prowlarr with filters
    results = search_prowlarr(query, filters)
    
    # Log the results count
    logger.info(f"Found {len(results)} results after filtering")
    
    # Enrich results with TMDb metadata AFTER filtering to preserve metadata
    if results:
        enriched_results = enrich_torrent_results(results)
    else:
        enriched_results = []
    
    return jsonify({
        'query': query,
        'results': enriched_results,
        'count': len(enriched_results),
        'filters_applied': filters
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


def is_tv_show(category):
    """Check if the torrent is a TV show"""
    return 'TV' in category if category else False


def is_full_season(title):
    """Check if the torrent title indicates a full season"""
    title_lower = title.lower()
    
    # Keywords that indicate full season
    season_keywords = [
        'complete season', 'full season', 'season pack', 'season 1-', 'season 2-',
        's01e01-e', 's02e01-e', 's03e01-e', 's04e01-e', 's05e01-e',
        'season 01', 'season 02', 'season 03', 'season 04', 'season 05',
        'complete series', 'full series', 'series pack'
    ]
    
    # Keywords that indicate single episodes (to exclude)
    episode_keywords = [
        's01e01', 's01e02', 's02e01', 's02e02', 'episode 1', 'episode 2',
        'e01', 'e02', 'e03', 'e04', 'e05', 'e06', 'e07', 'e08', 'e09', 'e10',
        'e11', 'e12', 'e13', 'e14', 'e15', 'e16', 'e17', 'e18', 'e19', 'e20',
        'e21', 'e22', 'e23', 'e24', 'e25', 'e26'
    ]
    
    # Check for season keywords
    has_season_keyword = any(keyword in title_lower for keyword in season_keywords)
    
    # Check for single episode keywords (exclude these)
    has_episode_keyword = any(keyword in title_lower for keyword in episode_keywords)
    
    # If it has season keywords but no episode keywords, it's likely a full season
    return has_season_keyword and not has_episode_keyword


def clean_title_for_metadata(title, category):
    """Clean torrent title for TMDb metadata search using parse-torrent-name"""
    if not title:
        return ""
    
    try:
        import PTN
        
        # Use parse-torrent-name to parse the scene title
        parsed = PTN.parse(title)
        
        # Extract the title from the parsed result
        clean_title = parsed.get('title', '')
        
        # If no title found, try alternative
        if not clean_title:
            # Fallback: try to extract title before any season/episode info
            import re
            # Remove common patterns that come after the title
            fallback_title = re.sub(r'\s*(?:S\d{1,2}E\d{1,2}|Season\s*\d+|Episode\s*\d+).*', '', title, flags=re.IGNORECASE)
            # Remove release group info
            fallback_title = re.sub(r'\s*(?:REPACK|PROPER|EXTENDED|DIRECTORS\s*CUT|UNRATED|LIMITED).*', '', fallback_title, flags=re.IGNORECASE)
            # Remove quality info
            fallback_title = re.sub(r'\s*(?:2160P|1080P|720P|480P|4K|UHD|HDTV|WEBRIP|WEB-DL|BLURAY|DVDRIP).*', '', fallback_title, flags=re.IGNORECASE)
            # Clean up
            fallback_title = re.sub(r'[^\w\s]', ' ', fallback_title)
            fallback_title = re.sub(r'\s+', ' ', fallback_title).strip()
            clean_title = fallback_title
        
        # If still no title, use the original title but clean it up
        if not clean_title:
            import re
            # Basic cleaning of the original title
            clean_title = re.sub(r'[^\w\s]', ' ', title)
            clean_title = re.sub(r'\s+', ' ', clean_title).strip()
            # Take first few words
            words = clean_title.split()
            clean_title = ' '.join(words[:4])  # Take first 4 words
        
        logger.info(f"Cleaned title '{title}' to '{clean_title}' using parse-torrent-name")
        return clean_title
        
    except ImportError:
        # Fallback if parse-torrent-name is not available
        logger.warning("parse-torrent-name not available, using fallback cleaning")
        import re
        
        # Basic cleaning
        cleaned = title.lower()
        
        # Remove common patterns
        cleaned = re.sub(r's\d{1,2}e\d{1,2}', ' ', cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r'season\s*\d+', ' ', cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r'episode\s*\d+', ' ', cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r'repack|proper|extended|directors\s*cut|unrated|limited', ' ', cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r'2160p|1080p|720p|480p|4k|uhd|hdtv|webrip|web-dl|bluray|dvdrip', ' ', cleaned, flags=re.IGNORECASE)
        
        # Clean up
        cleaned = re.sub(r'[^\w\s]', ' ', cleaned)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        
        # Take first few words
        words = cleaned.split()
        cleaned = ' '.join(words[:4])
        
        logger.info(f"Cleaned title '{title}' to '{cleaned}' using fallback")
        return cleaned
    except Exception as e:
        logger.error(f"Error cleaning title '{title}': {e}")
        return title[:50]  # Return first 50 characters as fallback


def search_tmdb_metadata(title, category):
    """Search TMDb for metadata with timeout"""
    if not app.config['TMDB_API_KEY']:
        logger.warning("TMDb API key not configured")
        return None
    
    try:
        # Clean title for better search results
        cleaned_title = clean_title_for_metadata(title, category)
        
        if not cleaned_title or len(cleaned_title) < 2:
            logger.info(f"Title too short after cleaning: '{cleaned_title}'")
            return None
        
        # Try to extract year from the original title using parse-torrent-name
        year = None
        try:
            import PTN
            parsed = PTN.parse(title)
            year = parsed.get('year')
        except:
            pass
        
        # Determine search type based on category
        search_type = 'tv' if 'tv' in category.lower() or 'show' in category.lower() else 'movie'
        
        # TMDb search endpoint
        url = f"https://api.themoviedb.org/3/search/{search_type}"
        params = {
            'api_key': app.config['TMDB_API_KEY'],
            'query': cleaned_title,
            'language': 'en-US',
            'page': 1
        }
        
        # Add year if available for more accurate search
        if year:
            params['year'] = year
        
        logger.info(f"Searching TMDb for: {cleaned_title} (type: {search_type}, year: {year})")
        response = requests.get(url, params=params, timeout=3)  # Reduced timeout to 3 seconds
        response.raise_for_status()
        
        data = response.json()
        results = data.get('results', [])
        
        if results:
            # Get the first (most relevant) result
            result = results[0]
            
            metadata = {
                'title': result.get('title') or result.get('name', 'Unknown'),
                'year': extract_year(result.get('release_date') or result.get('first_air_date')),
                'overview': result.get('overview', 'No overview available.'),
                'poster_url': f"https://image.tmdb.org/t/p/w500{result.get('poster_path')}" if result.get('poster_path') else None,
                'tmdb_id': result.get('id'),
                'type': search_type
            }
            
            logger.info(f"Found TMDb metadata for: {metadata['title']} ({metadata['year']})")
            return metadata
        else:
            logger.info(f"No TMDb results found for: {cleaned_title}")
            return None
            
    except requests.exceptions.Timeout:
        logger.warning("TMDb request timed out")
        return None
    except requests.exceptions.RequestException as e:
        logger.warning(f"TMDb request failed: {e}")
        return None
    except Exception as e:
        logger.warning(f"Unexpected error searching TMDb: {e}")
        return None


def extract_year(date_string):
    """Extract year from date string"""
    if date_string:
        try:
            return date_string.split('-')[0]
        except:
            pass
    return 'Unknown'


def enrich_torrent_results(results):
    """Enrich torrent results with TMDb metadata (optimized for filtered results)"""
    enriched_results = []
    
    # Process first 15 results for metadata (increased from 10)
    max_metadata_results = 15
    results_to_enrich = results[:max_metadata_results]
    
    # Simple cache to avoid duplicate API calls
    processed_titles = {}
    
    for result in results_to_enrich:
        # Create a cache key based on cleaned title and category
        cache_key = f"{result['title'][:30]}_{result['category']}"
        
        # Check if we already processed this title
        if cache_key in processed_titles:
            metadata = processed_titles[cache_key]
        else:
            # Try to get metadata for this torrent (with timeout)
            try:
                metadata = search_tmdb_metadata(result['title'], result['category'])
                processed_titles[cache_key] = metadata
            except Exception as e:
                logger.warning(f"Metadata fetch failed for {result['title']}: {e}")
                metadata = None
        
        # Merge metadata with torrent data
        enriched_result = result.copy()
        if metadata:
            enriched_result.update({
                'tmdb_title': metadata['title'],
                'tmdb_year': metadata['year'],
                'tmdb_overview': metadata['overview'],
                'tmdb_poster': metadata['poster_url'],
                'tmdb_id': metadata['tmdb_id'],
                'content_type': metadata['type']
            })
        else:
            # Fallback values if no metadata found
            enriched_result.update({
                'tmdb_title': result['title'],
                'tmdb_year': 'Unknown',
                'tmdb_overview': 'No overview available.',
                'tmdb_poster': None,
                'tmdb_id': None,
                'content_type': 'movie' if 'Movies' in result['category'] else 'tv'
            })
        
        enriched_results.append(enriched_result)
    
    # Add remaining results without metadata (for speed)
    for result in results[max_metadata_results:]:
        enriched_result = result.copy()
        enriched_result.update({
            'tmdb_title': result['title'],
            'tmdb_year': 'Unknown',
            'tmdb_overview': 'No overview available.',
            'tmdb_poster': None,
            'tmdb_id': None,
            'content_type': 'movie' if 'Movies' in result['category'] else 'tv'
        })
        enriched_results.append(enriched_result)
    
    logger.info(f"Enriched {len(enriched_results)} results (metadata for first {max_metadata_results})")
    return enriched_results


def parse_size(size_str):
    """Parse size string to bytes for comparison"""
    if isinstance(size_str, (int, float)):
        return size_str
    
    if not size_str:
        return 0
    
    size_str = str(size_str).upper().strip()
    
    # Handle common size formats
    multipliers = {
        'B': 1,
        'KB': 1024,
        'MB': 1024**2,
        'GB': 1024**3,
        'TB': 1024**4
    }
    
    # Try to extract number and unit
    for unit, multiplier in multipliers.items():
        if size_str.endswith(unit):
            try:
                # Extract the number part
                number_part = size_str[:-len(unit)].strip()
                number = float(number_part)
                return int(number * multiplier)
            except ValueError:
                continue
    
    # Try to parse as plain number (assume bytes)
    try:
        return int(float(size_str))
    except ValueError:
        return 0


def filter_torrents(torrents, filters):
    """Filter and sort torrents based on criteria - simplified for speed"""
    filtered = torrents.copy()
    
    # Apply size filter
    if filters.get('size'):
        size_filter = filters['size']
        if size_filter in ['asc', 'desc']:
            # Sort by size (ascending or descending)
            filtered.sort(key=lambda x: parse_size(x.get('size', '0 B')), reverse=(size_filter == 'desc'))
        else:
            # Filter by minimum size
            min_size = parse_size(size_filter)
            filtered = [t for t in filtered if parse_size(t.get('size', '0 B')) >= min_size]
    
    # Apply seeders filter
    if filters.get('seeders'):
        min_seeders = int(filters['seeders'])
        filtered = [t for t in filtered if t.get('seeders', 0) >= min_seeders]
    
    # If no filters applied, sort by relevance (seeders + quality)
    if not filters.get('size') and not filters.get('seeders'):
        def relevance_score(x):
            quality_score = {
                '4K': 100, '2160p': 100, '1080p': 80, 'BluRay': 70,
                'WEB-DL': 60, '720p': 50, 'WEBRip': 40, 'HDTV': 30,
                '480p': 20, 'DVDRip': 10
            }.get(x.get('quality', ''), 0)
            return (x.get('seeders', 0) * 10) + quality_score
        
        filtered.sort(key=relevance_score, reverse=True)
    
    # Limit results for faster response
    return filtered[:100]  # Limit to 100 results for speed


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 