/**
 * Simulation Page JavaScript
 * Demonstrates concurrent user purchases and dynamic pricing
 */

let products = [];

// Load products when page loads
document.addEventListener('DOMContentLoaded', async () => {
    await loadProducts();
});

async function loadProducts() {
    try {
        const response = await fetch(`${API_BASE_URL}/products`);
        const data = await response.json();
        
        if (data.success) {
            products = data.products;
            populateProductSelect();
        }
    } catch (error) {
        console.error('Error loading products:', error);
        showError('Failed to load products. Make sure the backend server is running.');
    }
}

function populateProductSelect() {
    const select = document.getElementById('productSelect');
    
    if (products.length === 0) {
        select.innerHTML = '<option value="">No products available</option>';
        return;
    }
    
    select.innerHTML = '<option value="">Select a product...</option>' + 
        products.map(p => `
            <option value="${p.product_id}">
                ${p.name} - $${p.current_price.toFixed(2)} (${p.inventory} in stock)
            </option>
        `).join('');
}

async function runSimulation() {
    const productId = document.getElementById('productSelect').value;
    const numUsers = parseInt(document.getElementById('numUsers').value);
    
    if (!productId) {
        showError('Please select a product');
        return;
    }
    
    if (numUsers < 2 || numUsers > 5) {
        showError('Number of users must be between 2 and 5');
        return;
    }
    
    // Disable button
    const runBtn = document.getElementById('runBtn');
    runBtn.disabled = true;
    runBtn.textContent = '⏳ Running Simulation...';
    
    try {
        const response = await fetch(`${API_BASE_URL}/simulation/concurrent-purchase/${productId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ num_users: numUsers })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displaySimulationResults(data);
            animateTimeline(data.simulation_steps);
        } else {
            showError(data.error || 'Simulation failed');
        }
    } catch (error) {
        console.error('Simulation error:', error);
        showError('Simulation failed. Make sure the backend server is running.');
    } finally {
        runBtn.disabled = false;
        runBtn.textContent = '▶️ Run Simulation';
    }
}

function displaySimulationResults(data) {
    // Show results section
    const resultsDiv = document.getElementById('results');
    resultsDiv.classList.add('active');
    resultsDiv.scrollIntoView({ behavior: 'smooth' });
    
    // Update header
    document.getElementById('resultProductName').textContent = data.product_name;
    document.getElementById('resultDescription').textContent = 
        `Simulated ${data.simulation_steps.length - 1} user interactions`;
    
    // Update price summary
    document.getElementById('basePrice').textContent = `$${data.base_price.toFixed(2)}`;
    document.getElementById('initialPrice').textContent = `$${data.initial_price.toFixed(2)}`;
    document.getElementById('finalPrice').textContent = `$${data.final_price.toFixed(2)}`;
    document.getElementById('totalIncrease').textContent = 
        `+$${data.total_increase.toFixed(2)} (${data.increase_percent}%)`;
    
    // Build timeline
    const timeline = document.getElementById('timeline');
    timeline.innerHTML = data.simulation_steps.map((step, index) => {
        const isInitial = step.step === 0;
        const priceChange = index > 0 ? step.price - data.simulation_steps[index - 1].price : 0;
        
        return `
            <div class="timeline-step" data-step="${step.step}">
                <div class="step-header">
                    <span class="step-number">Step ${step.step}</span>
                    <span class="step-price">$${step.price.toFixed(2)}</span>
                </div>
                
                <div class="step-action">
                    ${step.action}
                    ${priceChange > 0 ? 
                        `<span class="price-change-indicator">
                            ↑ +$${priceChange.toFixed(2)}
                        </span>` : ''}
                </div>
                
                <div class="step-details">
                    ${step.active_users !== undefined ? 
                        `<div class="detail-item">
                            <span>Active Users:</span>
                            <span class="detail-value">${step.active_users}</span>
                        </div>` : ''}
                    
                    ${step.concurrent_factor !== undefined ? 
                        `<div class="detail-item">
                            <span>Concurrent Factor:</span>
                            <span class="detail-value">${(step.concurrent_factor * 100).toFixed(1)}%</span>
                        </div>` : ''}
                    
                    ${step.cart_factor !== undefined ? 
                        `<div class="detail-item">
                            <span>Cart Factor:</span>
                            <span class="detail-value">${(step.cart_factor * 100).toFixed(1)}%</span>
                        </div>` : ''}
                    
                    ${step.price_change_from_initial !== undefined ? 
                        `<div class="detail-item">
                            <span>Total Change:</span>
                            <span class="detail-value">+$${step.price_change_from_initial.toFixed(2)}</span>
                        </div>` : ''}
                    
                    ${step.factors ? 
                        `<div class="detail-item" style="grid-column: 1 / -1;">
                            <span>Pricing Factors:</span>
                            <span class="detail-value">
                                Demand: ${(step.factors.demand * 100).toFixed(0)}% | 
                                Views: ${(step.factors.views * 100).toFixed(0)}% | 
                                Concurrent: ${(step.factors.concurrent_users * 100).toFixed(0)}%
                            </span>
                        </div>` : ''}
                </div>
            </div>
        `;
    }).join('');
}

function animateTimeline(steps) {
    const stepElements = document.querySelectorAll('.timeline-step');
    
    // Reset all steps
    stepElements.forEach(el => el.classList.remove('highlight'));
    
    // Animate each step
    steps.forEach((step, index) => {
        setTimeout(() => {
            const stepEl = document.querySelector(`[data-step="${step.step}"]`);
            if (stepEl) {
                stepEl.classList.add('highlight');
                stepEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
                
                // Remove highlight after 1 second
                setTimeout(() => {
                    stepEl.classList.remove('highlight');
                }, 1000);
            }
        }, index * 800);
    });
}

function showError(message) {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        background: var(--danger-color);
        color: white;
        border-radius: 5px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
        z-index: 10000;
        animation: slideIn 0.3s ease-out;
    `;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 5000);
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(400px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(400px); opacity: 0; }
    }
`;
document.head.appendChild(style);
