// DOM elements
const searchForm = document.getElementById('searchForm');
const searchInput = document.getElementById('searchInput');
const resultsContainer = document.getElementById('results');
const loadingDiv = document.getElementById('loading');
const errorDiv = document.getElementById('error');
const errorMessage = document.getElementById('errorMessage');

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
    resultsContainer.innerHTML = results.map(result => createResultCard(result)).join('');
}

// Create a result card HTML
function createResultCard(result) {
    // Placeholder card design - will be enhanced in Sprint 3 with metadata
    return `
        <div class="bg-gray-800 rounded-lg overflow-hidden shadow-lg hover:shadow-2xl transition-shadow">
            <div class="aspect-[2/3] bg-gray-700 flex items-center justify-center">
                ${result.poster ? 
                    `<img src="${result.poster}" alt="${result.title}" class="w-full h-full object-cover">` :
                    `<span class="text-gray-500">No Image</span>`
                }
            </div>
            <div class="p-4">
                <h3 class="font-bold text-lg mb-2 line-clamp-2">${result.title || 'Unknown Title'}</h3>
                <p class="text-gray-400 text-sm mb-2">${result.year || 'Year Unknown'}</p>
                <p class="text-gray-300 text-sm line-clamp-3 mb-4">${result.overview || 'No description available.'}</p>
                <button 
                    onclick="downloadTorrent('${result.magnet || ''}')"
                    class="w-full bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 transition-colors"
                    ${!result.magnet ? 'disabled' : ''}
                >
                    Download
                </button>
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
        // TODO: Show success notification in Sprint 4
        alert('Download started successfully!');
    } catch (error) {
        showError(`Download error: ${error.message}`);
        console.error('Download error:', error);
    }
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