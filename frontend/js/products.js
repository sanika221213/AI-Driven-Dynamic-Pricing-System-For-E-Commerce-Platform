// Products Page JavaScript

let allProducts = [];
let filteredProducts = [];

document.addEventListener('DOMContentLoaded', function() {
    loadProducts();
});

async function loadProducts() {
    try {
        const response = await getProducts();
        
        if (response.success) {
            allProducts = response.products;
            filteredProducts = allProducts;
            renderProductsTable();
        }
    } catch (error) {
        console.error('Error loading products:', error);
        showAlert('Failed to load products: ' + error.message, 'danger');
    }
}

function renderProductsTable() {
    const tbody = document.getElementById('productsTableBody');
    
    if (filteredProducts.length === 0) {
        tbody.innerHTML = '<tr><td colspan="9" class="text-center">No products found</td></tr>';
        return;
    }
    
    tbody.innerHTML = filteredProducts.map(product => `
        <tr>
            <td>${product.product_id}</td>
            <td><strong>${product.name}</strong></td>
            <td><span class="badge badge-primary">${product.category}</span></td>
            <td>${formatCurrency(product.base_price)}</td>
            <td><strong>${formatCurrency(product.current_price)}</strong></td>
            <td>${formatCurrency(product.cost_price)}</td>
            <td>
                <span class="badge ${getInventoryBadge(product.inventory)}">
                    ${product.inventory} units
                </span>
            </td>
            <td>${getPriceStatusBadge(product.current_price, product.base_price)}</td>
            <td>
                <div class="flex gap-1">
                    <button class="btn btn-sm btn-primary" onclick="showOptimizeModal(${product.product_id})" title="AI Optimize">
                        <i class="fas fa-magic"></i>
                    </button>
                    <button class="btn btn-sm btn-warning" onclick="showEditPriceModal(${product.product_id})" title="Edit Price">
                        <i class="fas fa-edit"></i>
                    </button>
                </div>
            </td>
        </tr>
    `).join('');
}

function filterProducts() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const category = document.getElementById('categoryFilter').value;
    const inventory = document.getElementById('inventoryFilter').value;
    
    filteredProducts = allProducts.filter(product => {
        // Search filter
        const matchesSearch = product.name.toLowerCase().includes(searchTerm) || 
                            product.category.toLowerCase().includes(searchTerm);
        
        // Category filter
        const matchesCategory = !category || product.category === category;
        
        // Inventory filter
        let matchesInventory = true;
        if (inventory === 'low') matchesInventory = product.inventory < 50;
        else if (inventory === 'medium') matchesInventory = product.inventory >= 50 && product.inventory <= 100;
        else if (inventory === 'high') matchesInventory = product.inventory > 100;
        
        return matchesSearch && matchesCategory && matchesInventory;
    });
    
    renderProductsTable();
}

function getInventoryBadge(inventory) {
    if (inventory < 50) return 'badge-danger';
    if (inventory < 100) return 'badge-warning';
    return 'badge-success';
}

function getPriceStatusBadge(current, base) {
    const diff = ((current - base) / base) * 100;
    
    if (Math.abs(diff) < 2) {
        return '<span class="badge badge-success">Optimal</span>';
    } else if (diff > 0) {
        return `<span class="badge badge-warning">+${diff.toFixed(1)}%</span>`;
    } else {
        return `<span class="badge badge-danger">${diff.toFixed(1)}%</span>`;
    }
}

// Modal functions
function showAddProductModal() {
    document.getElementById('addProductModal').classList.add('active');
}

function closeAddProductModal() {
    document.getElementById('addProductModal').classList.remove('active');
    document.getElementById('addProductForm').reset();
}

async function handleAddProduct(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const productData = {
        name: formData.get('name'),
        category: formData.get('category'),
        base_price: parseFloat(formData.get('base_price')),
        cost_price: parseFloat(formData.get('cost_price')),
        inventory: parseInt(formData.get('inventory')),
        description: formData.get('description')
    };
    
    try {
        const result = await addProduct(productData);
        
        if (result.success) {
            showAlert('Product added successfully!', 'success');
            closeAddProductModal();
            loadProducts();
        }
    } catch (error) {
        showAlert('Failed to add product: ' + error.message, 'danger');
    }
}

function showEditPriceModal(productId) {
    const product = allProducts.find(p => p.product_id === productId);
    
    if (!product) return;
    
    document.getElementById('editProductId').value = product.product_id;
    document.getElementById('editProductName').value = product.name;
    document.getElementById('editCurrentPrice').value = product.current_price;
    document.getElementById('editNewPrice').value = product.current_price;
    document.getElementById('editReason').value = '';
    
    document.getElementById('editPriceModal').classList.add('active');
}

function closeEditPriceModal() {
    document.getElementById('editPriceModal').classList.remove('active');
}

async function handleUpdatePrice(event) {
    event.preventDefault();
    
    const productId = parseInt(document.getElementById('editProductId').value);
    const newPrice = parseFloat(document.getElementById('editNewPrice').value);
    const reason = document.getElementById('editReason').value || 'Manual Update';
    
    try {
        const result = await updateProductPrice(productId, newPrice, reason);
        
        if (result.success) {
            showAlert('Price updated successfully!', 'success');
            closeEditPriceModal();
            loadProducts();
        }
    } catch (error) {
        showAlert('Failed to update price: ' + error.message, 'danger');
    }
}

async function showOptimizeModal(productId) {
    document.getElementById('optimizePriceModal').classList.add('active');
    document.getElementById('optimizationResults').innerHTML = '<div class="spinner"></div>';
    
    try {
        const result = await optimizeProductPrice(productId);
        
        if (result.success) {
            const optimization = result.optimization;
            const insights = result.market_insights;
            const product = allProducts.find(p => p.product_id === productId);
            
            const priceChange = optimization.optimal_price - insights.current_price;
            const changePercent = (priceChange / insights.current_price) * 100;
            
            document.getElementById('optimizationResults').innerHTML = `
                <div style="padding: 1rem;">
                    <h3>${product.name}</h3>
                    
                    <div style="background: var(--light-bg); padding: 1rem; border-radius: 0.5rem; margin: 1rem 0;">
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                            <div>
                                <label style="color: var(--text-secondary); font-size: 0.875rem;">Current Price</label>
                                <div style="font-size: 1.5rem; font-weight: 700;">${formatCurrency(insights.current_price)}</div>
                            </div>
                            <div>
                                <label style="color: var(--text-secondary); font-size: 0.875rem;">Optimal Price</label>
                                <div style="font-size: 1.5rem; font-weight: 700; color: var(--primary-color);">
                                    ${formatCurrency(optimization.optimal_price)}
                                </div>
                            </div>
                        </div>
                        
                        <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid var(--border-color);">
                            <div class="badge ${changePercent >= 0 ? 'badge-success' : 'badge-warning'}" 
                                 style="font-size: 1rem; padding: 0.5rem 1rem;">
                                ${changePercent >= 0 ? '+' : ''}${changePercent.toFixed(2)}% change
                            </div>
                        </div>
                    </div>
                    
                    <div style="margin-top: 1.5rem;">
                        <h4 style="margin-bottom: 0.75rem;">Market Insights</h4>
                        <ul style="list-style: none; padding: 0;">
                            <li style="padding: 0.5rem 0; border-bottom: 1px solid var(--border-color);">
                                <strong>Avg Competitor Price:</strong> ${formatCurrency(insights.avg_competitor_price)}
                            </li>
                            <li style="padding: 0.5rem 0; border-bottom: 1px solid var(--border-color);">
                                <strong>Recent Demand:</strong> ${insights.recent_demand.toFixed(0)} units
                            </li>
                            <li style="padding: 0.5rem 0; border-bottom: 1px solid var(--border-color);">
                                <strong>AI State:</strong> ${JSON.stringify(optimization.state)}
                            </li>
                            <li style="padding: 0.5rem 0;">
                                <strong>Multiplier:</strong> ${optimization.multiplier}x
                            </li>
                        </ul>
                    </div>
                    
                    <div class="alert alert-info" style="margin-top: 1rem;">
                        <strong>💡 AI Recommendation:</strong> Based on demand forecasting and reinforcement learning analysis.
                    </div>
                </div>
            `;
            
            // Store optimization data for applying
            window.currentOptimization = { productId, newPrice: optimization.optimal_price };
            document.getElementById('applyOptimizationBtn').style.display = 'inline-flex';
        }
    } catch (error) {
        document.getElementById('optimizationResults').innerHTML = `
            <div class="alert alert-danger">
                Failed to optimize price: ${error.message}
            </div>
        `;
    }
}

function closeOptimizePriceModal() {
    document.getElementById('optimizePriceModal').classList.remove('active');
    delete window.currentOptimization;
}

async function applyOptimization() {
    if (!window.currentOptimization) return;
    
    const { productId, newPrice } = window.currentOptimization;
    
    try {
        const result = await updateProductPrice(productId, newPrice, 'AI Dynamic Pricing Optimization');
        
        if (result.success) {
            showAlert('Optimized price applied successfully!', 'success');
            closeOptimizePriceModal();
            loadProducts();
        }
    } catch (error) {
        showAlert('Failed to apply optimization: ' + error.message, 'danger');
    }
}


