// Dashboard JavaScript

let revenueChart = null;

// Load dashboard on page load
document.addEventListener('DOMContentLoaded', function() {
    loadDashboard();
});

async function loadDashboard() {
    try {
        // Load dashboard statistics
        const stats = await getDashboardStats();
        
        if (stats.success) {
            updateDashboardStats(stats.stats);
            createRevenueChart(stats.stats.revenue_trend);
            await loadProducts();
        }
    } catch (error) {
        console.error('Error loading dashboard:', error);
        showAlert('Failed to load dashboard data. ' + error.message, 'danger');
    }
}

function updateDashboardStats(stats) {
    // Update stat cards
    document.getElementById('totalRevenue').textContent = formatCurrency(stats.total_revenue_30d);
    document.getElementById('totalProducts').textContent = stats.total_products;
    document.getElementById('totalSales').textContent = stats.total_sales_30d;
    document.getElementById('avgPriceChange').textContent = formatPercentage(stats.avg_price_change);
    
    // Update change indicators
    const revenueChange = Math.abs(stats.avg_price_change);
    document.getElementById('revenueChange').textContent = `+${formatPercentage(revenueChange)}`;
    
    if (stats.low_inventory_count > 0) {
        document.getElementById('productsInfo').textContent = `${stats.low_inventory_count} need restocking`;
        document.getElementById('productsInfo').style.color = 'var(--warning-color)';
    }
}

function createRevenueChart(trendData) {
    let ctx = document.getElementById('revenueTrendChart');
    
    // If the canvas was removed, recreate it
    if (!ctx) {
        const chartContainer = document.querySelector('.chart-container');
        if (chartContainer) {
            chartContainer.innerHTML = '<canvas id="revenueTrendChart"></canvas>';
            ctx = document.getElementById('revenueTrendChart');
        } else {
            return;
        }
    }
    
    if (!trendData || trendData.length === 0) {
        ctx.style.display = 'none';
        let noDataMsg = ctx.parentElement.querySelector('.no-data-message');
        if (!noDataMsg) {
            noDataMsg = document.createElement('p');
            noDataMsg.className = 'text-center no-data-message';
            noDataMsg.style.padding = '2rem';
            noDataMsg.textContent = 'No revenue data available';
            ctx.parentElement.appendChild(noDataMsg);
        }
        return;
    }
    
    // Show canvas and remove any no-data message
    ctx.style.display = '';
    const noDataMsg = ctx.parentElement.querySelector('.no-data-message');
    if (noDataMsg) noDataMsg.remove();
    
    // Destroy existing chart
    if (revenueChart) {
        revenueChart.destroy();
    }
    
    const labels = trendData.map(d => formatDate(d.date));
    const data = trendData.map(d => d.daily_revenue);
    
    revenueChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Daily Revenue',
                data: data,
                borderColor: 'rgb(37, 99, 235)',
                backgroundColor: 'rgba(37, 99, 235, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return 'Revenue: ' + formatCurrency(context.parsed.y);
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return '$' + value.toLocaleString();
                        }
                    }
                }
            }
        }
    });
}

async function loadProducts() {
    try {
        const response = await getProducts();
        
        if (response.success) {
            const tbody = document.getElementById('productsTableBody');
            
            if (response.products.length === 0) {
                tbody.innerHTML = '<tr><td colspan="7" class="text-center">No products found. Add products to get started.</td></tr>';
                return;
            }
            
            // Show only first 5 products
            const displayProducts = response.products.slice(0, 5);
            
            tbody.innerHTML = displayProducts.map(product => `
                <tr>
                    <td><strong>${product.name}</strong></td>
                    <td><span class="badge badge-primary">${product.category}</span></td>
                    <td><strong>${formatCurrency(product.current_price)}</strong></td>
                    <td>${formatCurrency(product.base_price)}</td>
                    <td>
                        <span class="badge ${getInventoryBadge(product.inventory)}">
                            ${product.inventory}
                        </span>
                    </td>
                    <td>
                        ${getPriceStatus(product.current_price, product.base_price)}
                    </td>
                    <td>
                        <button class="btn btn-sm btn-primary" onclick="optimizeSinglePrice(${product.product_id})">
                            <i class="fas fa-magic"></i> Optimize
                        </button>
                    </td>
                </tr>
            `).join('');
        }
    } catch (error) {
        console.error('Error loading products:', error);
    }
}

function getInventoryBadge(inventory) {
    if (inventory < 50) return 'badge-danger';
    if (inventory < 100) return 'badge-warning';
    return 'badge-success';
}

function getPriceStatus(current, base) {
    const diff = ((current - base) / base) * 100;
    
    if (Math.abs(diff) < 2) {
        return '<span class="badge badge-success">Optimal</span>';
    } else if (diff > 0) {
        return `<span class="badge badge-warning">+${diff.toFixed(1)}%</span>`;
    } else {
        return `<span class="badge badge-danger">${diff.toFixed(1)}%</span>`;
    }
}

async function optimizeSinglePrice(productId) {
    try {
        showAlert('Calculating optimal price...', 'info');
        
        const result = await optimizeProductPrice(productId);
        
        if (result.success) {
            const optimization = result.optimization;
            const insights = result.market_insights;
            
            const message = `
                Optimal price for this product: ${formatCurrency(optimization.optimal_price)}<br>
                Current price: ${formatCurrency(insights.current_price)}<br>
                Suggested change: ${formatPercentage((optimization.optimal_price - insights.current_price) / insights.current_price * 100)}
            `;
            
            showAlert(message, 'success');
            
            // Ask user to apply
            if (confirm(`Apply new price ${formatCurrency(optimization.optimal_price)}?`)) {
                await updateProductPrice(productId, optimization.optimal_price, 'AI Optimization');
                showAlert('Price updated successfully!', 'success');
                loadDashboard();
            }
        }
    } catch (error) {
        showAlert('Failed to optimize price: ' + error.message, 'danger');
    }
}

async function generateSampleData() {
    if (!confirm('This will generate sample products and sales data. Continue?')) {
        return;
    }
    
    try {
        showAlert('Generating sample data...', 'info');
        
        const result = await initializeSampleData();
        
        if (result.success) {
            showAlert('Sample data generated successfully!', 'success');
            setTimeout(() => {
                loadDashboard();
            }, 1000);
        }
    } catch (error) {
        showAlert('Failed to generate sample data: ' + error.message, 'danger');
    }
}

function refreshDashboard() {
    loadDashboard();
    showAlert('Dashboard refreshed!', 'success');
}
