// DOM elements
const searchForm = document.getElementById('searchForm');
const searchInput = document.getElementById('searchInput');
const resultsContainer = document.getElementById('results');
const resultsSection = document.getElementById('resultsSection');
const loadingDiv = document.getElementById('loading');
const errorDiv = document.getElementById('error');
const errorMessage = document.getElementById('errorMessage');
const emptyState = document.getElementById('emptyState');

// API base URL (will be same origin in production)
const API_URL = window.location.origin;

// Handle search form submission
searchForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const query = searchInput.value.trim();
    if (!query) return;
    
    // Clear previous results and errors
    resultsContainer.innerHTML = '';
    hideError();
    hideEmptyState();
    hideResults();
    
    // Show loading state
    showLoading();
    
    try {
        const response = await fetch(`${API_URL}/api/search`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query }),
        });
        
        if (!response.ok) {
            throw new Error(`Search failed: ${response.statusText}`);
        }
        
        const data = await response.json();
        hideLoading();
        
        if (data.results && data.results.length > 0) {
            displayResults(data.results);
        } else {
            showEmptyState();
            showError('No results found. Try a different search term.');
        }
    } catch (error) {
        hideLoading();
        showError(`Error: ${error.message}`);
        console.error('Search error:', error);
    }
});

// Display search results
function displayResults(results) {
    showResults();
    resultsContainer.innerHTML = results.map(result => createResultCard(result)).join('');
}

// Create a Jellyfin-style result card
function createResultCard(result) {
    const defaultPoster = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 300"%3E%3Crect fill="%23101010" width="200" height="300"/%3E%3Ctext x="50%25" y="50%25" text-anchor="middle" dy=".3em" fill="%23666" font-family="sans-serif" font-size="16"%3ENo Image%3C/text%3E%3C/svg%3E';
    
    return `
        <div class="media-card group">
            <div class="poster-container">
                <img 
                    src="${result.poster || defaultPoster}" 
                    alt="${result.title || 'Unknown Title'}"
                    loading="lazy"
                    onerror="this.src='${defaultPoster}'"
                >
                <div class="play-overlay">
                    <button 
                        onclick="downloadTorrent('${(result.magnet || '').replace(/'/g, "\\'")}')"
                        class="bg-jellyfin-purple hover:bg-jellyfin-purple-dark text-white p-4 rounded-full transition-all transform hover:scale-110"
                        title="Download ${result.title || 'this item'}"
                        ${!result.magnet ? 'disabled' : ''}
                    >
                        <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M9 19l3 3m0 0l3-3m-3 3V10"></path>
                        </svg>
                    </button>
                </div>
            </div>
            <div class="info">
                <h3 class="title" title="${result.title || 'Unknown Title'}">${result.title || 'Unknown Title'}</h3>
                <p class="year">${result.year || 'Year Unknown'}</p>
            </div>
        </div>
    `;
}

// Handle download button click
async function downloadTorrent(magnetLink) {
    if (!magnetLink) {
        showError('No magnet link available for this item.');
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/api/download`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ magnet: magnetLink }),
        });
        
        if (!response.ok) {
            throw new Error(`Download failed: ${response.statusText}`);
        }
        
        const data = await response.json();
        showSuccess('Download started successfully!');
    } catch (error) {
        showError(`Download error: ${error.message}`);
        console.error('Download error:', error);
    }
}

// Show success notification (Jellyfin style)
function showSuccess(message) {
    // Create toast notification
    const toast = document.createElement('div');
    toast.className = 'fixed bottom-4 right-4 bg-green-800/90 backdrop-blur-sm text-white px-6 py-4 rounded-lg shadow-lg flex items-center space-x-3 z-50';
    toast.innerHTML = `
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
        <span>${message}</span>
    `;
    document.body.appendChild(toast);
    
    // Remove after 3 seconds
    setTimeout(() => {
        toast.classList.add('opacity-0', 'transition-opacity', 'duration-300');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// UI helper functions
function showLoading() {
    loadingDiv.classList.remove('hidden');
}

function hideLoading() {
    loadingDiv.classList.add('hidden');
}

function showError(message) {
    errorMessage.textContent = message;
    errorDiv.classList.remove('hidden');
}

function hideError() {
    errorDiv.classList.add('hidden');
    errorMessage.textContent = '';
}

function showResults() {
    resultsSection.classList.remove('hidden');
}

function hideResults() {
    resultsSection.classList.add('hidden');
}

function showEmptyState() {
    emptyState.classList.remove('hidden');
}

function hideEmptyState() {
    emptyState.classList.add('hidden');
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    // Focus search input
    searchInput.focus();
    
    // Add keyboard shortcut for search (Ctrl+K or Cmd+K)
    document.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            searchInput.focus();
            searchInput.select();
        }
    });
}); 