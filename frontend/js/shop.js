/**
 * Shop Page JavaScript
 * Handles customer product browsing, dynamic pricing display, and shopping cart
 */

let currentUser = null;
let products = [];
let cartItems = [];
let priceUpdateInterval = null;
let searchTimeout = null;
let filteredProducts = [];

// Initialize page
document.addEventListener('DOMContentLoaded', () => {
    // Check if user is logged in
    const userStr = localStorage.getItem('user');
    if (!userStr) {
        window.location.href = 'login.html';
        return;
    }
    
    currentUser = JSON.parse(userStr);
    
    // If admin, redirect to dashboard
    if (currentUser.is_admin) {
        window.location.href = 'index.html';
        return;
    }
    
    // Display user name
    document.getElementById('userName').textContent = currentUser.full_name || currentUser.username;
    
    // Load products and cart
    loadProducts();
    loadCart();
    
    // Auto-refresh prices every 10 seconds
    priceUpdateInterval = setInterval(refreshPrices, 10000);
});

function logout() {
    localStorage.removeItem('user');
    window.location.href = 'login.html';
}

async function loadProducts() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/products`);
        const data = await response.json();
        
        if (data.success) {
            products = data.products;
            displayProducts();
        }
    } catch (error) {
        console.error('Error loading products:', error);
    }
}

function displayProducts() {
    const grid = document.getElementById('productsGrid');
    
    if (products.length === 0) {
        grid.innerHTML = '<p style="text-align:center;color:var(--text-secondary);grid-column: 1 / -1;">No products available</p>';
        return;
    }
    
    grid.innerHTML = products.map(product => {
        const priceChange = ((product.current_price - product.base_price) / product.base_price * 100).toFixed(1);
        const isIncreased = priceChange > 0;
        const stockLow = product.inventory < 20;
        
        return `
            <div class="product-card" data-product-id="${product.product_id}">
                <span class="product-category">${product.category || 'General'}</span>
                
                <h3 class="product-name">${product.name}</h3>
                <p class="product-description">${product.description || ''}</p>
                
                <div class="product-stats">
                    <div class="stat-item">
                        <div class="stat-value" id="searches-${product.product_id}">${product.search_count || 0}</div>
                        <div class="stat-label">Searches</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value" id="views-${product.product_id}">${product.view_count || 0}</div>
                        <div class="stat-label">Views</div>
                    </div>
                </div>
                
                <div class="product-price">
                    <span class="current-price" id="price-${product.product_id}">$${product.current_price.toFixed(2)}</span>
                    ${product.current_price !== product.base_price ? 
                        `<span class="base-price">$${product.base_price.toFixed(2)}</span>` : ''}
                    ${priceChange != 0 ? 
                        `<span class="price-change ${isIncreased ? 'price-up' : 'price-down'}">
                            ${isIncreased ? '↑' : '↓'} ${Math.abs(priceChange)}%
                        </span>` : ''}
                </div>
                
                <div class="stock-info ${stockLow ? 'stock-low' : 'stock-ok'}">
                    ${stockLow ? '⚠️' : '✓'} 
                    ${product.inventory} in stock
                    ${stockLow ? ' - Low Stock!' : ''}
                </div>
                
                <button class="add-to-cart-btn" 
                        onclick="addToCart(${product.product_id})"
                        ${product.inventory === 0 ? 'disabled' : ''}>
                    ${product.inventory === 0 ? 'Out of Stock' : '<i class="fas fa-shopping-cart btn-icon"></i><span class="btn-text">Add to Cart</span>'}
                </button>
                
                <div class="viewing-indicator" id="viewers-${product.product_id}" style="display:none;">
                    <span class="pulse">👀</span>
                    <span id="viewer-count-${product.product_id}">0</span> others viewing
                </div>
            </div>
        `;
    }).join('');
    
    // Track views for all products
    products.forEach(product => {
        trackProductView(product.product_id);
        updateConcurrentViewers(product.product_id);
    });
}

async function trackProductView(productId) {
    try {
        await fetch(`${API_BASE_URL}/api/products/${productId}/track/view`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                user_id: currentUser.user_id
            })
        });
    } catch (error) {
        console.error('Error tracking view:', error);
    }
}

async function updateConcurrentViewers(productId) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/products/${productId}/engagement`);
        const data = await response.json();
        
        if (data.success && data.concurrent_users > 1) {
            const indicator = document.getElementById(`viewers-${productId}`);
            const count = document.getElementById(`viewer-count-${productId}`);
            
            if (indicator && count) {
                count.textContent = data.concurrent_users - 1; // Exclude current user
                indicator.style.display = 'flex';
            }
        }
    } catch (error) {
        console.error('Error updating viewers:', error);
    }
}

async function addToCart(productId) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/cart/add`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                user_id: currentUser.user_id,
                product_id: productId,
                quantity: 1
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Show success message
            showNotification('Product added to cart!');
            
            // If price increased, show notification
            if (data.price_increased) {
                showNotification(`⚠️ Price increased to $${data.new_price.toFixed(2)} due to high demand!`, 'warning');
            }
            
            // Reload cart
            await loadCart();
            
            // Refresh product prices
            await refreshPrices();
        }
    } catch (error) {
        console.error('Error adding to cart:', error);
        showNotification('Error adding to cart', 'error');
    }
}

async function loadCart() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/cart/${currentUser.user_id}`);
        const data = await response.json();
        
        if (data.success) {
            cartItems = data.cart;
            updateCartBadge(data.item_count);
        }
    } catch (error) {
        console.error('Error loading cart:', error);
    }
}

function updateCartBadge(count) {
    const badge = document.getElementById('cartBadge');
    badge.textContent = count;
    badge.style.display = count > 0 ? 'flex' : 'none';
}

function openCart() {
    displayCart();
    document.getElementById('cartModal').style.display = 'block';
}

function closeCart() {
    document.getElementById('cartModal').style.display = 'none';
}

function displayCart() {
    const container = document.getElementById('cartItems');
    const totalEl = document.getElementById('cartTotal');
    
    if (cartItems.length === 0) {
        container.innerHTML = '<p style="text-align:center;color:var(--text-secondary);padding:40px;">Your cart is empty</p>';
        totalEl.textContent = '$0.00';
        return;
    }
    
    const total = cartItems.reduce((sum, item) => sum + item.total_price, 0);
    
    container.innerHTML = cartItems.map(item => `
        <div class="cart-item">
            <div class="cart-item-info">
                <div class="cart-item-name">${item.name}</div>
                <div class="cart-item-price">$${item.current_price.toFixed(2)} × ${item.quantity} = $${item.total_price.toFixed(2)}</div>
                ${item.current_price !== item.price_at_add ? 
                    `<small style="color:var(--warning-color);">Price changed from $${item.price_at_add.toFixed(2)}</small>` : ''}
            </div>
            <div class="cart-actions">
                <button class="qty-btn" onclick="updateQuantity(${item.cart_id}, ${item.quantity - 1})">-</button>
                <span id="qty-${item.cart_id}">${item.quantity}</span>
                <button class="qty-btn" onclick="updateQuantity(${item.cart_id}, ${item.quantity + 1})">+</button>
                <button class="remove-btn" onclick="removeFromCart(${item.cart_id})">
                    <i class="fas fa-trash-alt"></i>
                </button>
            </div>
        </div>
    `).join('');
    
    totalEl.textContent = `$${total.toFixed(2)}`;
}

async function updateQuantity(cartId, newQuantity) {
    if (newQuantity <= 0) {
        await removeFromCart(cartId);
        return;
    }
    
    // Optimistic update - update UI immediately
    const qtyElement = document.getElementById(`qty-${cartId}`);
    if (qtyElement) {
        qtyElement.textContent = newQuantity;
    }
    
    // Update the cart item in memory
    const item = cartItems.find(i => i.cart_id === cartId);
    if (item) {
        const oldQuantity = item.quantity;
        item.quantity = newQuantity;
        item.total_price = item.current_price * newQuantity;
        
        // Update total immediately
        const total = cartItems.reduce((sum, item) => sum + item.total_price, 0);
        document.getElementById('cartTotal').textContent = `$${total.toFixed(2)}`;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/cart/update`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                cart_id: cartId,
                quantity: newQuantity
            })
        });
        
        if (response.ok) {
            // Reload to get accurate data from server
            await loadCart();
            displayCart();
        } else {
            // Revert on error
            if (item) {
                item.quantity = oldQuantity;
                item.total_price = item.current_price * oldQuantity;
                displayCart();
            }
            showNotification('Failed to update quantity', 'error');
        }
    } catch (error) {
        console.error('Error updating quantity:', error);
        // Revert on error
        if (item) {
            item.quantity = oldQuantity;
            item.total_price = item.current_price * oldQuantity;
            displayCart();
        }
        showNotification('Error updating cart', 'error');
    }
}

async function removeFromCart(cartId) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/cart/remove/${cartId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            await loadCart();
            displayCart();
            showNotification('Item removed from cart');
        }
    } catch (error) {
        console.error('Error removing item:', error);
    }
}

async function checkout() {
    if (cartItems.length === 0) {
        showNotification('Your cart is empty', 'error');
        return;
    }
    
    try {
        // Process checkout - this will record sales and clear cart
        const response = await fetch(`${API_BASE_URL}/api/cart/checkout/${currentUser.user_id}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            showNotification(`Thank you for your purchase! Total: $${data.total_revenue.toFixed(2)}`, 'success');
            await loadCart();
            closeCart();
            await refreshPrices();
        } else {
            showNotification(data.error || 'Checkout failed', 'error');
        }
    } catch (error) {
        console.error('Error during checkout:', error);
        showNotification('Checkout error. Please try again.', 'error');
    }
}

async function refreshPrices() {
    try {
        // Update all product prices
        await fetch(`${API_BASE_URL}/api/pricing/update-all`, {
            method: 'POST'
        });
        
        // Reload products to show new prices
        await loadProducts();
        
        // Reload cart to show updated prices
        await loadCart();
    } catch (error) {
        console.error('Error refreshing prices:', error);
    }
}

function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        bottom: 30px;
        left: 50%;
        transform: translateX(-50%);
        padding: 15px 30px;
        background: ${type === 'success' ? 'var(--success-color)' : type === 'warning' ? 'var(--warning-color)' : 'var(--danger-color)'};
        color: white;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        z-index: 10000;
        animation: slideUp 0.3s ease-out;
        font-size: 15px;
        font-weight: 500;
        min-width: 300px;
        text-align: center;
    `;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideDown 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideUp {
        from { transform: translate(-50%, 100px); opacity: 0; }
        to { transform: translate(-50%, 0); opacity: 1; }
    }
    @keyframes slideDown {
        from { transform: translate(-50%, 0); opacity: 1; }
        to { transform: translate(-50%, 100px); opacity: 0; }
    }
`;
document.head.appendChild(style);

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    if (priceUpdateInterval) {
        clearInterval(priceUpdateInterval);
    }
});

// Search functionality
function handleSearch(event) {
    const searchTerm = event.target.value.toLowerCase().trim();
    const resultsDiv = document.getElementById('searchResults');
    
    // Clear previous timeout
    if (searchTimeout) {
        clearTimeout(searchTimeout);
    }
    
    if (searchTerm === '') {
        // Show all products
        filteredProducts = [];
        displayProducts();
        resultsDiv.textContent = '';
        return;
    }
    
    // Filter products
    filteredProducts = products.filter(product => 
        (product.name && product.name.toLowerCase().includes(searchTerm)) ||
        (product.category && product.category.toLowerCase().includes(searchTerm)) ||
        (product.description && product.description.toLowerCase().includes(searchTerm))
    );
    
    console.log('Search term:', searchTerm);
    console.log('Filtered products:', filteredProducts.length, filteredProducts);
    
    // Update display
    displayFilteredProducts();
    
    // Show results count
    resultsDiv.textContent = `Found ${filteredProducts.length} product${filteredProducts.length !== 1 ? 's' : ''}`;
    
    // Track search after a delay (debounce)
    searchTimeout = setTimeout(() => {
        trackSearches(searchTerm);
    }, 1000);
}

function displayFilteredProducts() {
    const grid = document.getElementById('productsGrid');
    const productsToShow = filteredProducts.length > 0 ? filteredProducts : products;
    
    if (productsToShow.length === 0) {
        grid.innerHTML = '<p style="text-align:center;color:var(--text-secondary);grid-column: 1 / -1;padding:40px;">No products found matching your search</p>';
        return;
    }
    
    grid.innerHTML = productsToShow.map(product => {
        const priceChange = ((product.current_price - product.base_price) / product.base_price * 100).toFixed(1);
        const isIncreased = priceChange > 0;
        const stockLow = product.inventory < 20;
        
        return `
            <div class="product-card" data-product-id="${product.product_id}">
                <span class="product-category">${product.category || 'General'}</span>
                
                <h3 class="product-name">${product.name}</h3>
                <p class="product-description">${product.description || ''}</p>
                
                <div class="product-stats">
                    <div class="stat-item">
                        <div class="stat-value" id="searches-${product.product_id}">${product.search_count || 0}</div>
                        <div class="stat-label">Searches</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value" id="views-${product.product_id}">${product.view_count || 0}</div>
                        <div class="stat-label">Views</div>
                    </div>
                </div>
                
                <div class="product-price">
                    <span class="current-price" id="price-${product.product_id}">$${product.current_price.toFixed(2)}</span>
                    ${product.current_price !== product.base_price ? 
                        `<span class="base-price">$${product.base_price.toFixed(2)}</span>` : ''}
                    ${priceChange != 0 ? 
                        `<span class="price-change ${isIncreased ? 'price-up' : 'price-down'}">
                            ${isIncreased ? '↑' : '↓'} ${Math.abs(priceChange)}%
                        </span>` : ''}
                </div>
                
                <div class="stock-info ${stockLow ? 'stock-low' : 'stock-ok'}">
                    ${stockLow ? '⚠️' : '✓'} 
                    ${product.inventory} in stock
                    ${stockLow ? ' - Low Stock!' : ''}
                </div>
                
                <button class="add-to-cart-btn" 
                        onclick="addToCart(${product.product_id})"
                        ${product.inventory === 0 ? 'disabled' : ''}>
                    ${product.inventory === 0 ? 'Out of Stock' : '<i class="fas fa-shopping-cart btn-icon"></i><span class="btn-text">Add to Cart</span>'}
                </button>
                
                <div class="viewing-indicator" id="viewers-${product.product_id}" style="display:none;">
                    <span class="pulse">👀</span>
                    <span id="viewer-count-${product.product_id}">0</span> others viewing
                </div>
            </div>
        `;
    }).join('');
}

async function trackSearches(searchTerm) {
    // Track search for products that match the search term
    const matchedProducts = products.filter(product => 
        (product.name && product.name.toLowerCase().includes(searchTerm)) ||
        (product.category && product.category.toLowerCase().includes(searchTerm))
    );
    
    // Track search for each matched product
    for (const product of matchedProducts) {
        try {
            await fetch(`${API_BASE_URL}/api/products/${product.product_id}/track/search`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    user_id: currentUser?.user_id || null,
                    query: searchTerm
                })
            });
        } catch (error) {
            console.error('Error tracking search:', error);
        }
    }
}
