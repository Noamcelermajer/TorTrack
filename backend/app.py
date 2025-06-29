from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables from .env file
# This will load from backend/.env in development or /app/.env in Docker
load_dotenv()

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

# Configuration
app.config['PROWLARR_URL'] = os.getenv('PROWLARR_URL', 'http://localhost:9696')
app.config['PROWLARR_API_KEY'] = os.getenv('PROWLARR_API_KEY', '')
app.config['TMDB_API_KEY'] = os.getenv('TMDB_API_KEY', '')
app.config['QBITTORRENT_URL'] = os.getenv('QBITTORRENT_URL', 'http://localhost:8080')
app.config['QBITTORRENT_USERNAME'] = os.getenv('QBITTORRENT_USERNAME', 'admin')
app.config['QBITTORRENT_PASSWORD'] = os.getenv('QBITTORRENT_PASSWORD', 'adminpass')


@app.route('/')
def index():
    """Serve the frontend application"""
    return send_from_directory('../frontend', 'index.html')


@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'TorTrack API'})


@app.route('/api/search', methods=['POST'])
def search():
    """Search for torrents using Prowlarr"""
    data = request.get_json()
    query = data.get('query', '')
    
    if not query:
        return jsonify({'error': 'No search query provided'}), 400
    
    # TODO: Implement Prowlarr search in Sprint 2
    return jsonify({
        'message': 'Search endpoint ready for implementation',
        'query': query,
        'results': []
    })


@app.route('/api/download', methods=['POST'])
def download():
    """Trigger download via qBittorrent"""
    data = request.get_json()
    magnet_link = data.get('magnet', '')
    
    if not magnet_link:
        return jsonify({'error': 'No magnet link provided'}), 400
    
    # TODO: Implement qBittorrent download trigger in Sprint 4
    return jsonify({
        'message': 'Download endpoint ready for implementation',
        'magnet': magnet_link
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 