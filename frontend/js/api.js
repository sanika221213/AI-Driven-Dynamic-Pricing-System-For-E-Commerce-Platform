// API Helper Functions

async function apiRequest(url, options = {}) {
    try {
        const response = await fetch(url, {
            ...options,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            }
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'API request failed');
        }
        
        return data;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Product API calls
async function getProducts() {
    return apiRequest(config.API_ENDPOINTS.PRODUCTS);
}

async function getProduct(id) {
    return apiRequest(`${config.API_ENDPOINTS.PRODUCTS}/${id}`);
}

async function addProduct(productData) {
    return apiRequest(config.API_ENDPOINTS.PRODUCTS, {
        method: 'POST',
        body: JSON.stringify(productData)
    });
}

async function updateProductPrice(id, price, reason = '') {
    return apiRequest(`${config.API_ENDPOINTS.PRODUCTS}/${id}/price`, {
        method: 'PUT',
        body: JSON.stringify({ price, reason })
    });
}

// Pricing optimization API calls
async function optimizeProductPrice(id) {
    return apiRequest(`${config.API_ENDPOINTS.PRICING_OPTIMIZE}/${id}`, {
        method: 'POST'
    });
}

// Sales API calls
async function getSales(days = 30, productId = null) {
    const params = new URLSearchParams({ days });
    if (productId) params.append('product_id', productId);
    
    return apiRequest(`${config.API_ENDPOINTS.SALES}?${params}`);
}

async function recordSale(saleData) {
    return apiRequest(config.API_ENDPOINTS.SALES, {
        method: 'POST',
        body: JSON.stringify(saleData)
    });
}

// Analytics API calls
async function getRevenueAnalytics(days = 30) {
    return apiRequest(`${config.API_ENDPOINTS.ANALYTICS_REVENUE}?days=${days}`);
}

async function getProductAnalytics(id, days = 30) {
    return apiRequest(`${config.API_ENDPOINTS.ANALYTICS_PRODUCT}/${id}?days=${days}`);
}

async function getDashboardStats() {
    return apiRequest(config.API_ENDPOINTS.ANALYTICS_DASHBOARD);
}

// Competitor API calls
async function getCompetitorPrices(productId, days = 7) {
    return apiRequest(`${config.API_ENDPOINTS.COMPETITORS}/${productId}?days=${days}`);
}

async function addCompetitorPrice(competitorData) {
    return apiRequest(config.API_ENDPOINTS.COMPETITORS, {
        method: 'POST',
        body: JSON.stringify(competitorData)
    });
}

// Settings API calls
async function getSettings() {
    return apiRequest(config.API_ENDPOINTS.SETTINGS);
}

async function updateSettings(settings) {
    return apiRequest(config.API_ENDPOINTS.SETTINGS, {
        method: 'POST',
        body: JSON.stringify(settings)
    });
}

// Initialize sample data
async function initializeSampleData() {
    return apiRequest(config.API_ENDPOINTS.INITIALIZE_DATA, {
        method: 'POST'
    });
}

// Utility functions
function showAlert(message, type = 'success') {
    const alertContainer = document.getElementById('alertContainer');
    if (!alertContainer) return;
    
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.innerHTML = `
        <strong>${type === 'success' ? '✓' : type === 'danger' ? '✗' : 'ℹ'}</strong>
        ${message}
    `;
    
    alertContainer.innerHTML = '';
    alertContainer.appendChild(alertDiv);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

function formatDateTime(dateString) {
    return new Date(dateString).toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function formatPercentage(value, decimals = 1) {
    return `${value.toFixed(decimals)}%`;
}
