// DOM elements
const searchForm = document.getElementById('searchForm');
const searchInput = document.getElementById('searchInput');
const categoryFilter = document.getElementById('categoryFilter');
const qualityFilter = document.getElementById('qualityFilter');
const sizeFilter = document.getElementById('sizeFilter');
const seedersFilter = document.getElementById('seedersFilter');
const seasonTypeFilter = document.getElementById('seasonTypeFilter');
const resultsLimit = document.getElementById('resultsLimit');
const sortBy = document.getElementById('sortBy');
const resultsContainer = document.getElementById('results');
const resultsSection = document.getElementById('resultsSection');
const resultCount = document.getElementById('resultCount');
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
    showLoading(true);
    
    try {
        const filters = getFilters();
        console.log('Searching with filters:', filters);
        
        const response = await fetch('/api/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: query,
                filters: filters
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error);
        }
        
        displayResults(data.results, query);
        showNotification(`Found ${data.results.length} results for "${query}"`, 'success');
        
    } catch (error) {
        console.error('Search error:', error);
        showNotification(`Search failed: ${error.message}`, 'error');
    } finally {
        showLoading(false);
    }
});

// Display search results
function displayResults(results, query) {
    const resultsContainer = document.getElementById('searchResults');
    
    if (!results || results.length === 0) {
        resultsContainer.innerHTML = `
            <div class="text-center py-12">
                <div class="text-gray-400 text-lg mb-2">No results found</div>
                <div class="text-gray-600">Try adjusting your search terms or filters</div>
            </div>
        `;
        return;
    }
    
    const resultsHTML = results.map(result => {
        const size = result.size || 'Unknown';
        const seeders = result.seeders || 0;
        const leechers = result.leechers || 0;
        const quality = result.quality || 'Unknown';
        const category = result.category || 'Unknown';
        
        // Use original title for display, TMDb title only for metadata
        const displayTitle = result.title; // Always use original torrent title
        const year = result.tmdb_year || 'Unknown';
        const overview = result.tmdb_overview || 'No overview available.';
        const poster = result.tmdb_poster;
        const contentType = result.content_type || (category.toLowerCase().includes('tv') ? 'tv' : 'movie');
        
        // Quality badge color
        const qualityColors = {
            '4K': 'bg-purple-600',
            '1080p': 'bg-green-600',
            '720p': 'bg-blue-600',
            'BluRay': 'bg-yellow-600',
            'WEB-DL': 'bg-indigo-600',
            'WEBRip': 'bg-pink-600',
            'HDTV': 'bg-orange-600'
        };
        
        const qualityColor = qualityColors[quality] || 'bg-gray-600';
        
        // Seeder indicator
        const seederColor = seeders > 50 ? 'text-green-400' : seeders > 10 ? 'text-yellow-400' : 'text-red-400';
        
        return `
            <div class="bg-jellyfin-card border border-gray-800 rounded-lg p-6 hover:border-jellyfin-purple transition-all cursor-pointer" 
                 onclick="showTorrentDetails('${result.title.replace(/'/g, "\\'")}', '${result.magnet_link || result.download_url}', '${category}', '${result.indexer}', '${size}', '${seeders}', '${leechers}', '${quality}', '${result.publishDate || ''}', '${result.info_url || ''}')">
                <div class="flex gap-4">
                    ${poster ? `
                        <div class="flex-shrink-0">
                            <img src="${poster}" alt="${displayTitle}" class="w-20 h-30 object-cover rounded-md shadow-lg">
                        </div>
                    ` : `
                        <div class="flex-shrink-0 w-20 h-30 bg-gray-800 rounded-md flex items-center justify-center">
                            <svg class="w-8 h-8 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                            </svg>
                        </div>
                    `}
                    
                    <div class="flex-1 min-w-0">
                        <div class="flex items-start justify-between mb-2">
                            <div class="flex-1 min-w-0">
                                <h3 class="text-lg font-medium text-white truncate" title="${displayTitle}">${displayTitle}</h3>
                                <div class="flex items-center gap-2 mt-1">
                                    <span class="text-sm text-gray-400">${year}</span>
                                    <span class="text-xs px-2 py-1 ${qualityColor} text-white rounded-full">${quality}</span>
                                    <span class="text-xs px-2 py-1 bg-gray-700 text-gray-300 rounded-full">${category}</span>
                                </div>
                            </div>
                            <button 
                                onclick="event.stopPropagation(); downloadTorrent('${result.magnet_link || result.download_url}', '${category}', '${displayTitle.replace(/'/g, "\\'")}')"
                                class="px-4 py-2 bg-jellyfin-purple text-white rounded-md hover:bg-jellyfin-purple-dark transition-all text-sm font-medium"
                            >
                                Download
                            </button>
                        </div>
                        
                        <p class="text-gray-400 text-sm mb-3 line-clamp-2">${overview}</p>
                        
                        <div class="flex items-center gap-4 text-sm text-gray-500">
                            <div class="flex items-center gap-1">
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4"></path>
                                </svg>
                                <span class="${seederColor} font-medium">${seeders}</span>
                                <span>seeders</span>
                            </div>
                            <div class="flex items-center gap-1">
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                </svg>
                                <span>${size}</span>
                            </div>
                            <div class="flex items-center gap-1">
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                                </svg>
                                <span>${leechers}</span>
                                <span>leechers</span>
                            </div>
                        </div>
                        
                        <div class="mt-2 text-xs text-gray-600">
                            <span>Indexer: ${result.indexer || 'Unknown'}</span>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }).join('');
    
    resultsContainer.innerHTML = resultsHTML;
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
function showLoading(show) {
    const loadingElement = document.getElementById('loading');
    if (loadingElement) {
        loadingElement.style.display = show ? 'block' : 'none';
    }
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

    // Initialize the application
    initializeApp();
});

function initializeApp() {
    // Initialize filter toggle
    const filterToggleBtn = document.getElementById('filterToggleBtn');
    const filtersSection = document.getElementById('filtersSection');
    
    if (filterToggleBtn && filtersSection) {
        filterToggleBtn.addEventListener('click', function() {
            const isHidden = filtersSection.classList.contains('hidden');
            if (isHidden) {
                filtersSection.classList.remove('hidden');
                filterToggleBtn.classList.add('bg-jellyfin-purple');
                filterToggleBtn.classList.remove('bg-gray-700');
            } else {
                filtersSection.classList.add('hidden');
                filterToggleBtn.classList.remove('bg-jellyfin-purple');
                filterToggleBtn.classList.add('bg-gray-700');
            }
        });
    }

    // Initialize search form
    const searchForm = document.getElementById('searchForm');
    if (searchForm) {
        searchForm.addEventListener('submit', handleSearch);
    }

    // Initialize download form
    const downloadForm = document.getElementById('downloadForm');
    if (downloadForm) {
        downloadForm.addEventListener('submit', handleDownload);
    }

    // Add automatic filter updates
    const sizeFilter = document.getElementById('sizeFilter');
    const seedersFilter = document.getElementById('seedersFilter');
    
    if (sizeFilter) {
        sizeFilter.addEventListener('change', function() {
            if (currentSearchQuery) {
                handleSearch(new Event('submit'));
            }
        });
    }
    
    if (seedersFilter) {
        seedersFilter.addEventListener('change', function() {
            if (currentSearchQuery) {
                handleSearch(new Event('submit'));
            }
        });
    }

    // Load downloads on page load
    loadDownloads();
}

// Global variable to store current search query
let currentSearchQuery = '';
let currentSearchController = null;

function getFilters() {
    return {
        size: document.getElementById('sizeFilter')?.value || '',
        seeders: document.getElementById('seedersFilter')?.value || ''
    };
}

async function handleSearch(event) {
    event.preventDefault();
    
    const searchInput = document.getElementById('searchInput');
    const query = searchInput.value.trim();
    
    if (!query) {
        showNotification('Please enter a search query', 'error');
        return;
    }
    
    // Cancel previous search if running
    if (currentSearchController) {
        currentSearchController.abort();
    }
    
    // Create new abort controller for this search
    currentSearchController = new AbortController();
    
    // Store current query for filter updates
    currentSearchQuery = query;
    
    // Show loading state
    showLoading(true);
    clearResults();
    
    try {
        const filters = getFilters();
        console.log('Searching with filters:', filters);
        
        const response = await fetch('/api/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: query,
                filters: filters
            }),
            signal: currentSearchController.signal
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error);
        }
        
        displayResults(data.results, query);
        showNotification(`Found ${data.results.length} results for "${query}"`, 'success');
        
    } catch (error) {
        if (error.name === 'AbortError') {
            console.log('Search was cancelled');
            return;
        }
        console.error('Search error:', error);
        showNotification(`Search failed: ${error.message}`, 'error');
    } finally {
        showLoading(false);
        currentSearchController = null;
    }
}

function clearResults() {
    const resultsContainer = document.getElementById('searchResults');
    if (resultsContainer) {
        resultsContainer.innerHTML = '';
    }
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 z-50 px-6 py-4 rounded-lg shadow-lg transition-all transform translate-x-full ${
        type === 'error' ? 'bg-red-600 text-white' :
        type === 'success' ? 'bg-green-600 text-white' :
        'bg-blue-600 text-white'
    }`;
    notification.textContent = message;
    
    // Add to page
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.classList.remove('translate-x-full');
    }, 100);
    
    // Remove after 5 seconds
    setTimeout(() => {
        notification.classList.add('translate-x-full');
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 5000);
}

function showTorrentDetails(title, magnetLink, category, indexer, size, seeders, leechers, quality, publishDate, infoUrl) {
    // Create modal with full torrent information
    const modal = document.createElement('div');
    modal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50';
    modal.innerHTML = `
        <div class="bg-jellyfin-card border border-gray-800 rounded-lg p-6 max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
            <div class="flex justify-between items-start mb-4">
                <h2 class="text-xl font-medium text-white">Torrent Details</h2>
                <button onclick="this.closest('.fixed').remove()" class="text-gray-400 hover:text-white">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                    </svg>
                </button>
            </div>
            
            <div class="space-y-4">
                <div>
                    <label class="block text-sm font-medium text-gray-400 mb-1">Title</label>
                    <p class="text-white break-words">${title}</p>
                </div>
                
                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-400 mb-1">Category</label>
                        <p class="text-white">${category}</p>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-400 mb-1">Quality</label>
                        <p class="text-white">${quality}</p>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-400 mb-1">Size</label>
                        <p class="text-white">${size}</p>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-400 mb-1">Indexer</label>
                        <p class="text-white">${indexer}</p>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-400 mb-1">Seeders</label>
                        <p class="text-white">${seeders}</p>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-400 mb-1">Leechers</label>
                        <p class="text-white">${leechers}</p>
                    </div>
                </div>
                
                ${publishDate ? `
                    <div>
                        <label class="block text-sm font-medium text-gray-400 mb-1">Published Date</label>
                        <p class="text-white">${publishDate}</p>
                    </div>
                ` : ''}
                
                ${infoUrl ? `
                    <div>
                        <label class="block text-sm font-medium text-gray-400 mb-1">Info URL</label>
                        <a href="${infoUrl}" target="_blank" class="text-jellyfin-purple hover:underline break-all">${infoUrl}</a>
                    </div>
                ` : ''}
                
                <div>
                    <label class="block text-sm font-medium text-gray-400 mb-1">Magnet Link</label>
                    <div class="bg-gray-900 p-3 rounded text-xs text-gray-300 break-all font-mono">${magnetLink}</div>
                </div>
            </div>
            
            <div class="flex gap-3 mt-6">
                <button 
                    onclick="downloadTorrent('${magnetLink}', '${category}', '${title.replace(/'/g, "\\'")}'); this.closest('.fixed').remove();"
                    class="flex-1 px-4 py-2 bg-jellyfin-purple text-white rounded-md hover:bg-jellyfin-purple-dark transition-all font-medium"
                >
                    Download
                </button>
                <button 
                    onclick="this.closest('.fixed').remove()"
                    class="px-4 py-2 bg-gray-700 text-white rounded-md hover:bg-gray-600 transition-all"
                >
                    Close
                </button>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Close modal when clicking outside
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            modal.remove();
        }
    });
} 