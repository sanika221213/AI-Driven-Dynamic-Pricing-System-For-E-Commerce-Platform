// API Configuration
const API_BASE_URL = 'http://localhost:5000';

const config = {
    API_BASE_URL,
    API_ENDPOINTS: {
        HEALTH: `${API_BASE_URL}/api/health`,
        PRODUCTS: `${API_BASE_URL}/api/products`,
        PRICING_OPTIMIZE: `${API_BASE_URL}/api/pricing/optimize`,
        PRICING_BATCH: `${API_BASE_URL}/api/pricing/batch-optimize`,
        SALES: `${API_BASE_URL}/api/sales`,
        ANALYTICS_REVENUE: `${API_BASE_URL}/api/analytics/revenue`,
        ANALYTICS_PRODUCT: `${API_BASE_URL}/api/analytics/product`,
        ANALYTICS_DASHBOARD: `${API_BASE_URL}/api/analytics/dashboard`,
        COMPETITORS: `${API_BASE_URL}/api/competitors`,
        SETTINGS: `${API_BASE_URL}/api/settings`,
        INITIALIZE_DATA: `${API_BASE_URL}/api/initialize-sample-data`
    }
};
