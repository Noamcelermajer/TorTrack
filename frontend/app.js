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
    // Use a film icon as default for torrents
    const torrentIcon = `
        <svg class="w-16 h-16 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 4v16M17 4v16M3 8h4m10 0h4M3 12h18M3 16h4m10 0h4M4 20h16a1 1 0 001-1V5a1 1 0 00-1-1H4a1 1 0 00-1 1v14a1 1 0 001 1z"></path>
        </svg>
    `;
    
    // Determine seeder health color
    const seederColor = result.seeders > 10 ? 'text-green-500' : 
                       result.seeders > 5 ? 'text-yellow-500' : 
                       'text-red-500';
    
    // Escape single quotes in data for onclick
    const safeTitle = (result.title || '').replace(/'/g, "\\'");
    const safeCategory = (result.category || '').replace(/'/g, "\\'");
    const safeMagnet = (result.magnet_link || result.download_url || '').replace(/'/g, "\\'");
    
    return `
        <div class="media-card group">
            <div class="poster-container bg-gray-900 flex items-center justify-center">
                ${torrentIcon}
                <div class="absolute top-2 right-2 bg-jellyfin-purple text-white text-xs px-2 py-1 rounded">
                    ${result.quality || 'Unknown'}
                </div>
                <div class="play-overlay">
                    <button 
                        onclick="downloadTorrent('${safeMagnet}', '${safeTitle}', '${safeCategory}')"
                        class="bg-jellyfin-purple hover:bg-jellyfin-purple-dark text-white p-4 rounded-full transition-all transform hover:scale-110"
                        title="Download ${result.title || 'this item'}"
                        ${!result.magnet_link && !result.download_url ? 'disabled' : ''}
                    >
                        <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M9 19l3 3m0 0l3-3m-3 3V10"></path>
                        </svg>
                    </button>
                </div>
            </div>
            <div class="info">
                <h3 class="title" title="${result.title || 'Unknown Title'}">${result.title || 'Unknown Title'}</h3>
                <div class="text-xs text-gray-400 space-y-1 mt-2">
                    <div class="flex justify-between">
                        <span>${result.category || 'Unknown'}</span>
                        <span>${result.size || '0 MB'}</span>
                    </div>
                    <div class="flex justify-between items-center">
                        <span class="text-gray-500">${result.indexer || 'Unknown'}</span>
                        <div class="flex items-center space-x-2">
                            <span class="${seederColor}" title="Seeders">
                                <svg class="w-3 h-3 inline" fill="currentColor" viewBox="0 0 20 20">
                                    <path fill-rule="evenodd" d="M3.293 9.707a1 1 0 010-1.414l6-6a1 1 0 011.414 0l6 6a1 1 0 01-1.414 1.414L11 5.414V17a1 1 0 11-2 0V5.414L4.707 9.707a1 1 0 01-1.414 0z" clip-rule="evenodd"></path>
                                </svg>
                                ${result.seeders || 0}
                            </span>
                            <span class="text-red-500" title="Leechers">
                                <svg class="w-3 h-3 inline" fill="currentColor" viewBox="0 0 20 20">
                                    <path fill-rule="evenodd" d="M16.707 10.293a1 1 0 010 1.414l-6 6a1 1 0 01-1.414 0l-6-6a1 1 0 111.414-1.414L9 14.586V3a1 1 0 012 0v11.586l4.293-4.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                                </svg>
                                ${result.leechers || 0}
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

// Handle download button click
async function downloadTorrent(magnetLink, title, category) {
    if (!magnetLink) {
        showError('No magnet link available for this torrent.');
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/api/download`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                magnet: magnetLink,
                title: title || 'Unknown',
                category: category || 'Unknown'
            }),
        });
        
        if (!response.ok) {
            throw new Error(`Download failed: ${response.statusText}`);
        }
        
        const data = await response.json();
        
        if (data.success) {
            showSuccess(data.message || 'Download started successfully!');
        } else {
            showError(data.error || 'Download failed');
        }
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