// Competitors Page JavaScript

let priceComparisonChart;
let allProducts = [];

document.addEventListener('DOMContentLoaded', function() {
    loadCompetitorPage();
});

async function loadCompetitorPage() {
    try {
        // Load products for dropdown
        const response = await getProducts();
        
        if (response.success) {
            allProducts = response.products;
            populateProductDropdowns();
            updateCompetitorStats();
        }
    } catch (error) {
        console.error('Error loading competitor page:', error);
        showAlert('Failed to load competitor data: ' + error.message, 'danger');
    }
}

function populateProductDropdowns() {
    const selectors = ['productSelector', 'modalProductSelector'];
    
    selectors.forEach(selectorId => {
        const selector = document.getElementById(selectorId);
        
        selector.innerHTML = '<option value="">Select a product...</option>' +
            allProducts.map(product => 
                `<option value="${product.product_id}">${product.name} - ${formatCurrency(product.current_price)}</option>`
            ).join('');
    });
}

async function updateCompetitorStats() {
    try {
        // Get all competitor prices
        let totalCompetitors = new Set();
        let monitoredProducts = 0;
        let totalPriceDiff = 0;
        let priceCount = 0;
        
        for (const product of allProducts) {
            const response = await getCompetitorPrices(product.product_id, 30);
            
            if (response.success && response.competitor_prices.length > 0) {
                monitoredProducts++;
                
                response.competitor_prices.forEach(cp => {
                    totalCompetitors.add(cp.competitor_name);
                    
                    const diff = ((product.current_price - cp.competitor_price) / cp.competitor_price) * 100;
                    totalPriceDiff += diff;
                    priceCount++;
                });
            }
        }
        
        document.getElementById('monitoredProducts').textContent = monitoredProducts;
        document.getElementById('totalCompetitors').textContent = totalCompetitors.size;
        
        // Calculate position
        const avgDiff = priceCount > 0 ? totalPriceDiff / priceCount : 0;
        
        let position = 'Neutral';
        let positionText = 'vs market avg';
        
        if (avgDiff < -5) {
            position = 'Lower';
            positionText = `${Math.abs(avgDiff).toFixed(1)}% below`;
            document.getElementById('pricePosition').style.color = 'var(--success-color)';
        } else if (avgDiff > 5) {
            position = 'Higher';
            positionText = `${avgDiff.toFixed(1)}% above`;
            document.getElementById('pricePosition').style.color = 'var(--danger-color)';
        }
        
        document.getElementById('pricePosition').textContent = position;
        document.getElementById('positionChange').textContent = positionText;
        
        // Last update time
        document.getElementById('lastUpdate').textContent = new Date().toLocaleTimeString();
        
    } catch (error) {
        console.error('Error updating competitor stats:', error);
    }
}

async function loadCompetitorPrices() {
    const productId = parseInt(document.getElementById('productSelector').value);
    const days = parseInt(document.getElementById('timeRange').value);
    
    if (!productId) {
        document.getElementById('competitorPricesTable').innerHTML = 
            '<tr><td colspan="7" class="text-center">Please select a product</td></tr>';
        document.getElementById('comparisonCard').style.display = 'none';
        return;
    }
    
    try {
        const [competitorResponse, productResponse] = await Promise.all([
            getCompetitorPrices(productId, days),
            getProduct(productId)
        ]);
        
        if (competitorResponse.success && productResponse.success) {
            const product = productResponse.product;
            const prices = competitorResponse.competitor_prices;
            
            // Update product name
            document.getElementById('selectedProductName').textContent = product.name;
            
            // Render table
            renderCompetitorPricesTable(prices, product.current_price);
            
            // Create chart
            createPriceComparisonChart(prices, product);
            
            // Generate insights
            generatePricingInsights(prices, product);
            
            // Show comparison card
            document.getElementById('comparisonCard').style.display = 'block';
        }
    } catch (error) {
        console.error('Error loading competitor prices:', error);
        showAlert('Failed to load competitor prices: ' + error.message, 'danger');
    }
}

function renderCompetitorPricesTable(prices, ourPrice) {
    const tbody = document.getElementById('competitorPricesTable');
    
    if (prices.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="text-center">No competitor prices found for this product</td></tr>';
        return;
    }
    
    tbody.innerHTML = prices.map(price => {
        const diff = price.competitor_price - ourPrice;
        const diffPercent = (diff / ourPrice) * 100;
        
        let position = 'Equal';
        let badge = 'badge-success';
        
        if (diffPercent < -5) {
            position = 'We\'re Higher';
            badge = 'badge-danger';
        } else if (diffPercent > 5) {
            position = 'We\'re Lower';
            badge = 'badge-success';
        }
        
        return `
            <tr>
                <td>${formatDate(price.scraped_at)}</td>
                <td>Product #${price.product_id}</td>
                <td><strong>${price.competitor_name}</strong></td>
                <td>${formatCurrency(price.competitor_price)}</td>
                <td><strong>${formatCurrency(ourPrice)}</strong></td>
                <td>
                    <span class="badge ${diff >= 0 ? 'badge-success' : 'badge-danger'}">
                        ${diff >= 0 ? '+' : ''}${formatCurrency(diff)} (${diffPercent.toFixed(1)}%)
                    </span>
                </td>
                <td><span class="badge ${badge}">${position}</span></td>
            </tr>
        `;
    }).join('');
}

function createPriceComparisonChart(prices, product) {
    const ctx = document.getElementById('priceComparisonChart');
    
    if (priceComparisonChart) {
        priceComparisonChart.destroy();
    }
    
    // Group by competitor
    const competitorData = {};
    
    prices.forEach(price => {
        if (!competitorData[price.competitor_name]) {
            competitorData[price.competitor_name] = [];
        }
        competitorData[price.competitor_name].push(price.competitor_price);
    });
    
    // Calculate averages
    const labels = Object.keys(competitorData);
    const avgPrices = labels.map(comp => {
        const prices = competitorData[comp];
        return prices.reduce((a, b) => a + b, 0) / prices.length;
    });
    
    // Add our price
    labels.push('Our Price');
    avgPrices.push(product.current_price);
    
    priceComparisonChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Average Price',
                data: avgPrices,
                backgroundColor: avgPrices.map((price, index) => 
                    index === avgPrices.length - 1 ? 'rgba(37, 99, 235, 0.8)' : 'rgba(156, 163, 175, 0.8)'
                ),
                borderColor: avgPrices.map((price, index) => 
                    index === avgPrices.length - 1 ? 'rgb(37, 99, 235)' : 'rgb(156, 163, 175)'
                ),
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: (context) => 'Price: ' + formatCurrency(context.parsed.y)
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: (value) => '$' + value.toLocaleString()
                    }
                }
            }
        }
    });
}

function generatePricingInsights(prices, product) {
    const insightsDiv = document.getElementById('pricingInsights');
    
    if (prices.length === 0) {
        insightsDiv.innerHTML = `
            <div class="alert alert-warning">
                <strong>⚠️ No competitor data available</strong><br>
                Add competitor prices to receive AI-powered pricing insights.
            </div>
        `;
        return;
    }
    
    // Calculate market average
    const avgCompetitorPrice = prices.reduce((sum, p) => sum + p.competitor_price, 0) / prices.length;
    const minCompetitorPrice = Math.min(...prices.map(p => p.competitor_price));
    const maxCompetitorPrice = Math.max(...prices.map(p => p.competitor_price));
    
    const ourPrice = product.current_price;
    const pricePosition = ((ourPrice - avgCompetitorPrice) / avgCompetitorPrice) * 100;
    
    let recommendation = '';
    let alertType = 'info';
    
    if (pricePosition < -10) {
        recommendation = `
            <strong>💰 Price Increase Opportunity:</strong><br>
            Your price is ${Math.abs(pricePosition).toFixed(1)}% below market average. 
            Consider increasing price to ${formatCurrency(avgCompetitorPrice * 0.95)} to maximize revenue while staying competitive.
        `;
        alertType = 'success';
    } else if (pricePosition > 10) {
        recommendation = `
            <strong>⚠️ Price Too High:</strong><br>
            Your price is ${pricePosition.toFixed(1)}% above market average. 
            Consider reducing to ${formatCurrency(avgCompetitorPrice * 1.05)} to improve competitiveness and sales volume.
        `;
        alertType = 'warning';
    } else {
        recommendation = `
            <strong>✓ Optimal Pricing:</strong><br>
            Your price is well-positioned at ${pricePosition >= 0 ? '+' : ''}${pricePosition.toFixed(1)}% 
            relative to market average. Current strategy is balanced.
        `;
        alertType = 'success';
    }
    
    insightsDiv.innerHTML = `
        <div class="alert alert-${alertType}">
            ${recommendation}
        </div>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-top: 1rem;">
            <div style="background: var(--light-bg); padding: 1rem; border-radius: 0.5rem;">
                <div style="color: var(--text-secondary); font-size: 0.875rem; margin-bottom: 0.25rem;">Market Average</div>
                <div style="font-size: 1.5rem; font-weight: 700;">${formatCurrency(avgCompetitorPrice)}</div>
            </div>
            <div style="background: var(--light-bg); padding: 1rem; border-radius: 0.5rem;">
                <div style="color: var(--text-secondary); font-size: 0.875rem; margin-bottom: 0.25rem;">Price Range</div>
                <div style="font-size: 1.5rem; font-weight: 700;">
                    ${formatCurrency(minCompetitorPrice)} - ${formatCurrency(maxCompetitorPrice)}
                </div>
            </div>
            <div style="background: var(--light-bg); padding: 1rem; border-radius: 0.5rem;">
                <div style="color: var(--text-secondary); font-size: 0.875rem; margin-bottom: 0.25rem;">Our Position</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: ${pricePosition >= 0 ? 'var(--danger-color)' : 'var(--success-color)'};">
                    ${pricePosition >= 0 ? '+' : ''}${pricePosition.toFixed(1)}%
                </div>
            </div>
        </div>
    `;
}

function showAddCompetitorModal() {
    document.getElementById('addCompetitorModal').classList.add('active');
}

function closeAddCompetitorModal() {
    document.getElementById('addCompetitorModal').classList.remove('active');
    document.getElementById('addCompetitorForm').reset();
}

async function handleAddCompetitorPrice(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const competitorData = {
        product_id: parseInt(formData.get('product_id')),
        competitor_name: formData.get('competitor_name'),
        price: parseFloat(formData.get('price')),
        url: formData.get('url')
    };
    
    try {
        const result = await addCompetitorPrice(competitorData);
        
        if (result.success) {
            showAlert('Competitor price added successfully!', 'success');
            closeAddCompetitorModal();
            
            // Reload if this product is selected
            const selectedProduct = parseInt(document.getElementById('productSelector').value);
            if (selectedProduct === competitorData.product_id) {
                loadCompetitorPrices();
            }
            
            updateCompetitorStats();
        }
    } catch (error) {
        showAlert('Failed to add competitor price: ' + error.message, 'danger');
    }
}

function refreshCompetitorData() {
    loadCompetitorPage();
    showAlert('Competitor data refreshed!', 'success');
}
