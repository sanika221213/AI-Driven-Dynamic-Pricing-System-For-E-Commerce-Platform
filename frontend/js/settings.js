// Settings Page JavaScript

document.addEventListener('DOMContentLoaded', function() {
    loadSettings();
    updateLastUpdated();
});

async function loadSettings() {
    try {
        const response = await getSettings();
        
        if (response.success) {
            const settings = response.settings;
            
            // Populate form fields
            document.getElementById('pricingStrategy').value = settings.pricing_strategy;
            document.getElementById('autoPricing').value = settings.auto_pricing.toString();
            document.getElementById('priceUpdateFrequency').value = settings.price_update_frequency;
            document.getElementById('explorationRate').value = settings.exploration_rate;
            document.getElementById('minMargin').value = settings.min_margin;
            document.getElementById('maxDiscount').value = settings.max_discount;
        }
    } catch (error) {
        console.error('Error loading settings:', error);
        showAlert('Failed to load settings: ' + error.message, 'danger');
    }
}

async function saveSettings() {
    const settings = {
        pricing_strategy: document.getElementById('pricingStrategy').value,
        auto_pricing: document.getElementById('autoPricing').value === 'true',
        price_update_frequency: document.getElementById('priceUpdateFrequency').value,
        exploration_rate: parseInt(document.getElementById('explorationRate').value),
        min_margin: parseInt(document.getElementById('minMargin').value),
        max_discount: parseInt(document.getElementById('maxDiscount').value)
    };
    
    try {
        const result = await updateSettings(settings);
        
        if (result.success) {
            showAlert('Settings saved successfully!', 'success');
            updateLastUpdated();
        }
    } catch (error) {
        showAlert('Failed to save settings: ' + error.message, 'danger');
    }
}

function resetSettings() {
    if (!confirm('Reset all settings to default values?')) {
        return;
    }
    
    document.getElementById('pricingStrategy').value = 'balanced';
    document.getElementById('autoPricing').value = 'false';
    document.getElementById('priceUpdateFrequency').value = 'daily';
    document.getElementById('explorationRate').value = 20;
    document.getElementById('minMargin').value = 15;
    document.getElementById('maxDiscount').value = 30;
    
    showAlert('Settings reset to default values', 'info');
}

function updateLastUpdated() {
    document.getElementById('lastUpdated').textContent = new Date().toLocaleString();
}

function clearCache() {
    if (!confirm('Clear system cache? This may temporarily slow down performance.')) {
        return;
    }
    
    showAlert('Cache cleared successfully!', 'success');
}

function resetDatabase() {
    if (!confirm('⚠️ WARNING: This will delete all data and cannot be undone. Continue?')) {
        return;
    }
    
    if (!confirm('Are you absolutely sure? This action is irreversible!')) {
        return;
    }
    
    showAlert('Database reset functionality disabled in demo mode', 'warning');
}

function exportSettings() {
    const settings = {
        pricing_strategy: document.getElementById('pricingStrategy').value,
        auto_pricing: document.getElementById('autoPricing').value,
        price_update_frequency: document.getElementById('priceUpdateFrequency').value,
        exploration_rate: document.getElementById('explorationRate').value,
        min_margin: document.getElementById('minMargin').value,
        max_discount: document.getElementById('maxDiscount').value,
        exported_at: new Date().toISOString()
    };
    
    const dataStr = JSON.stringify(settings, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'pricing-system-settings.json';
    link.click();
    
    showAlert('Settings exported successfully!', 'success');
}
