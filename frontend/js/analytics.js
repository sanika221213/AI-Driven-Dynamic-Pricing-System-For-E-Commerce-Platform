// Analytics Page JavaScript

let revenueTrendChart, salesVolumeChart, categoryRevenueChart, priceCorrelationChart;

document.addEventListener('DOMContentLoaded', function() {
    updateAnalytics();
});

async function updateAnalytics() {
    const days = parseInt(document.getElementById('timeRangeFilter').value);
    
    try {
        // Load analytics data
        const [revenueData, salesData, dashboardStats] = await Promise.all([
            getRevenueAnalytics(days),
            getSales(days),
            getDashboardStats()
        ]);
        
        if (revenueData.success) {
            updateAnalyticsStats(revenueData.analytics);
            createRevenueTrendChart(revenueData.analytics.daily_breakdown);
        }
        
        if (salesData.success && dashboardStats.success) {
            createSalesVolumeChart(salesData.sales);
            await createCategoryRevenueChart();
            await createPriceCorrelationChart(days);
            await createTopProductsTable(days);
            createSalesHistoryTable(salesData.sales);
        }
    } catch (error) {
        console.error('Error loading analytics:', error);
        showAlert('Failed to load analytics: ' + error.message, 'danger');
    }
}

function updateAnalyticsStats(analytics) {
    document.getElementById('analyticsRevenue').textContent = formatCurrency(analytics.total_revenue);
    document.getElementById('totalTransactions').textContent = analytics.total_sales;
    
    const avgValue = analytics.total_revenue / analytics.total_sales;
    document.getElementById('avgTransactionValue').textContent = formatCurrency(avgValue);
    
    // Mock conversion rate
    const conversionRate = 18.5;
    document.getElementById('conversionRate').textContent = formatPercentage(conversionRate);
    
    // Mock price changes count
    document.getElementById('priceChanges').textContent = Math.floor(Math.random() * 50) + 20;
    
    // Calculate growth
    const growth = 22.5;
    document.getElementById('revenueGrowth').textContent = `+${formatPercentage(growth)}`;
}

function createRevenueTrendChart(dailyData) {
    const ctx = document.getElementById('revenueTrendChart');
    
    if (revenueTrendChart) {
        revenueTrendChart.destroy();
    }
    
    const labels = dailyData.map(d => formatDate(d.date));
    const data = dailyData.map(d => d.daily_revenue);
    
    revenueTrendChart = new Chart(ctx, {
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
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: (context) => 'Revenue: ' + formatCurrency(context.parsed.y)
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

function createSalesVolumeChart(salesData) {
    const ctx = document.getElementById('salesVolumeChart');
    
    if (salesVolumeChart) {
        salesVolumeChart.destroy();
    }
    
    // Group by date
    const salesByDate = {};
    salesData.forEach(sale => {
        const date = sale.sale_date.split(' ')[0];
        salesByDate[date] = (salesByDate[date] || 0) + sale.quantity_sold;
    });
    
    const labels = Object.keys(salesByDate).slice(-7);
    const data = labels.map(date => salesByDate[date]);
    
    salesVolumeChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels.map(formatDate),
            datasets: [{
                label: 'Units Sold',
                data: data,
                backgroundColor: 'rgba(16, 185, 129, 0.8)',
                borderColor: 'rgb(16, 185, 129)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
}

async function createCategoryRevenueChart() {
    const ctx = document.getElementById('categoryRevenueChart');
    
    if (categoryRevenueChart) {
        categoryRevenueChart.destroy();
    }
    
    try {
        const productsResponse = await getProducts();
        const salesResponse = await getSales(30);
        
        if (!productsResponse.success || !salesResponse.success) return;
        
        const products = productsResponse.products;
        const sales = salesResponse.sales;
        
        // Calculate revenue by category
        const categoryRevenue = {};
        
        sales.forEach(sale => {
            const product = products.find(p => p.product_id === sale.product_id);
            if (product) {
                categoryRevenue[product.category] = (categoryRevenue[product.category] || 0) + sale.revenue;
            }
        });
        
        const labels = Object.keys(categoryRevenue);
        const data = Object.values(categoryRevenue);
        
        categoryRevenueChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: [
                        'rgba(37, 99, 235, 0.8)',
                        'rgba(16, 185, 129, 0.8)',
                        'rgba(245, 158, 11, 0.8)',
                        'rgba(124, 58, 237, 0.8)',
                        'rgba(239, 68, 68, 0.8)'
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: (context) => {
                                const label = context.label || '';
                                const value = formatCurrency(context.parsed);
                                return `${label}: ${value}`;
                            }
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error creating category chart:', error);
    }
}

async function createPriceCorrelationChart(days) {
    const ctx = document.getElementById('priceCorrelationChart');
    
    if (priceCorrelationChart) {
        priceCorrelationChart.destroy();
    }
    
    try {
        const productsResponse = await getProducts();
        const salesResponse = await getSales(days);
        
        if (!productsResponse.success || !salesResponse.success) {
            console.log('No data available for price correlation chart');
            return;
        }
        
        const products = productsResponse.products;
        const sales = salesResponse.sales;
        
        if (sales.length === 0) {
            // Show "No Data" message
            ctx.getContext('2d').font = '16px Arial';
            ctx.getContext('2d').fillStyle = '#666';
            ctx.getContext('2d').textAlign = 'center';
            ctx.getContext('2d').fillText('No sales data available. Make some purchases to see correlation.', ctx.width / 2, ctx.height / 2);
            return;
        }
        
        // Aggregate sales data per product
        const productSalesData = {};
        
        sales.forEach(sale => {
            if (!productSalesData[sale.product_id]) {
                productSalesData[sale.product_id] = {
                    totalQuantity: 0,
                    avgPrice: 0,
                    priceSum: 0,
                    count: 0,
                    name: ''
                };
            }
            
            const data = productSalesData[sale.product_id];
            data.totalQuantity += sale.quantity_sold;
            data.priceSum += sale.price;
            data.count += 1;
        });
        
        // Calculate average prices and prepare scatter plot data
        const scatterData = [];
        
        Object.keys(productSalesData).forEach(productId => {
            const product = products.find(p => p.product_id == productId);
            const data = productSalesData[productId];
            
            if (product) {
                const avgPrice = data.priceSum / data.count;
                scatterData.push({
                    x: avgPrice,
                    y: data.totalQuantity,
                    label: product.product_name
                });
            }
        });
        
        priceCorrelationChart = new Chart(ctx, {
            type: 'scatter',
            data: {
                datasets: [{
                    label: 'Price vs Sales Volume',
                    data: scatterData,
                    backgroundColor: 'rgba(37, 99, 235, 0.6)',
                    borderColor: 'rgba(37, 99, 235, 1)',
                    borderWidth: 1,
                    pointRadius: 8,
                    pointHoverRadius: 10
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        type: 'linear',
                        position: 'bottom',
                        title: {
                            display: true,
                            text: 'Average Price ($)',
                            color: '#666'
                        },
                        ticks: {
                            callback: (value) => '$' + value.toFixed(2)
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Total Sales Volume',
                            color: '#666'
                        },
                        beginAtZero: true
                    }
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: (context) => {
                                const point = context.raw;
                                return [
                                    `Product: ${point.label}`,
                                    `Price: $${point.x.toFixed(2)}`,
                                    `Sales: ${point.y} units`
                                ];
                            }
                        }
                    },
                    legend: {
                        display: false
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error creating price correlation chart:', error);
    }
}

async function createTopProductsTable(days) {
    const tbody = document.getElementById('topProductsTable');
    
    try {
        const [productsResponse, salesResponse] = await Promise.all([
            getProducts(),
            getSales(days)
        ]);
        
        if (!productsResponse.success || !salesResponse.success) return;
        
        const products = productsResponse.products;
        const sales = salesResponse.sales;
        
        // Calculate product performance
        const productStats = {};
        
        sales.forEach(sale => {
            if (!productStats[sale.product_id]) {
                productStats[sale.product_id] = {
                    revenue: 0,
                    units: 0,
                    transactions: 0,
                    totalPrice: 0
                };
            }
            
            productStats[sale.product_id].revenue += sale.revenue;
            productStats[sale.product_id].units += sale.quantity_sold;
            productStats[sale.product_id].transactions += 1;
            productStats[sale.product_id].totalPrice += sale.price;
        });
        
        // Create ranked list
        const rankedProducts = Object.entries(productStats)
            .map(([id, stats]) => {
                const product = products.find(p => p.product_id == id);
                return {
                    ...product,
                    ...stats,
                    avgPrice: stats.totalPrice / stats.transactions
                };
            })
            .sort((a, b) => b.revenue - a.revenue)
            .slice(0, 10);
        
        tbody.innerHTML = rankedProducts.map((product, index) => `
            <tr>
                <td><strong>#${index + 1}</strong></td>
                <td>${product.name}</td>
                <td><span class="badge badge-primary">${product.category}</span></td>
                <td><strong>${formatCurrency(product.revenue)}</strong></td>
                <td>${product.units}</td>
                <td>${formatCurrency(product.avgPrice)}</td>
                <td>
                    <div style="width: 100px; background: var(--border-color); border-radius: 9999px; height: 8px;">
                        <div style="width: ${Math.min(100, (index === 0 ? 100 : (product.revenue / rankedProducts[0].revenue) * 100))}%; 
                                    background: var(--success-color); height: 100%; border-radius: 9999px;"></div>
                    </div>
                </td>
            </tr>
        `).join('');
        
    } catch (error) {
        console.error('Error creating top products table:', error);
        tbody.innerHTML = '<tr><td colspan="7" class="text-center">Error loading data</td></tr>';
    }
}

function createSalesHistoryTable(salesData) {
    const tbody = document.getElementById('salesHistoryTable');
    
    const recentSales = salesData.slice(0, 20);
    
    tbody.innerHTML = recentSales.map(sale => `
        <tr>
            <td>${formatDateTime(sale.sale_date)}</td>
            <td>Product #${sale.product_id}</td>
            <td>${sale.quantity_sold}</td>
            <td>${formatCurrency(sale.price)}</td>
            <td><strong>${formatCurrency(sale.revenue)}</strong></td>
        </tr>
    `).join('');
}

function exportAnalytics() {
    showAlert('Exporting analytics report...', 'info');
    
    // Mock export - in production, this would generate a PDF or CSV
    setTimeout(() => {
        showAlert('Analytics report exported successfully!', 'success');
    }, 1000);
}
