"""
Flask API Server for Dynamic Pricing System
Provides REST endpoints for the frontend application
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import DatabaseManager
from models.lstm_forecaster import LSTMDemandForecaster
from models.reinforcement_learning import DynamicPricingAgent
from models.price_elasticity import PriceElasticityCalculator
from models.dynamic_pricing_engine import DynamicPricingEngine

# Initialize Flask app
app = Flask(__name__)

# Enable CORS with proper configuration
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:8000", "http://127.0.0.1:8000", "null"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})

# Initialize components
db = DatabaseManager()
pricing_agent = DynamicPricingAgent()
elasticity_calc = PriceElasticityCalculator()
dynamic_pricing = DynamicPricingEngine(db)

# Try to load pre-trained models
try:
    pricing_agent.load_agent('models/pricing_agent.json')
except:
    print("No pre-trained pricing agent found. Starting fresh.")


# Add CORS headers to all responses
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})


# Product endpoints
@app.route('/api/products', methods=['GET'])
def get_products():
    """Get all products"""
    try:
        products = db.get_all_products()
        # Replace NaN with None for valid JSON
        products_dict = products.replace({np.nan: None}).to_dict('records')
        return jsonify({
            'success': True,
            'products': products_dict
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get single product"""
    try:
        product = db.get_product(product_id)
        if product:
            return jsonify({'success': True, 'product': product})
        return jsonify({'success': False, 'error': 'Product not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/products', methods=['POST'])
def add_product():
    """Add new product"""
    try:
        data = request.json
        product_id = db.add_product(
            name=data['name'],
            category=data['category'],
            base_price=float(data['base_price']),
            cost_price=float(data['cost_price']),
            inventory=int(data['inventory']),
            description=data.get('description', '')
        )
        return jsonify({
            'success': True,
            'product_id': product_id,
            'message': 'Product added successfully'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/products/<int:product_id>/price', methods=['PUT'])
def update_price(product_id):
    """Update product price"""
    try:
        data = request.json
        new_price = float(data['price'])
        reason = data.get('reason', 'Manual Update')
        
        db.update_product_price(product_id, new_price, reason)
        
        return jsonify({
            'success': True,
            'message': 'Price updated successfully'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# Pricing optimization endpoints
@app.route('/api/pricing/optimize/<int:product_id>', methods=['POST'])
def optimize_price(product_id):
    """Calculate optimal price for a product"""
    try:
        # Get product data
        product = db.get_product(product_id)
        if not product:
            return jsonify({'success': False, 'error': 'Product not found'}), 404
        
        # Get market data
        sales_history = db.get_sales_history(product_id, days=30)
        competitor_prices = db.get_competitor_prices(product_id, days=7)
        
        # Calculate average competitor price
        avg_competitor_price = competitor_prices['competitor_price'].mean() if not competitor_prices.empty else product['base_price']
        
        # Forecast demand (simplified - using average recent sales)
        avg_recent_sales = sales_history['quantity_sold'].mean() if not sales_history.empty else 10
        
        # Prepare market data
        market_data = {
            'demand_forecast': avg_recent_sales,
            'competitor_price': avg_competitor_price,
            'seasonality': 'normal'
        }
        
        # Prepare product data
        product_data = {
            'base_price': product['base_price'],
            'inventory': product['inventory']
        }
        
        # Calculate min/max prices if not set
        cost_price = product.get('cost_price', product['base_price'] * 0.6)
        min_price = product.get('min_price') or max(cost_price * 1.1, product['base_price'] * 0.7)
        max_price = product.get('max_price') or product['base_price'] * 1.5
        
        # Business rules
        business_rules = {
            'min_price': min_price,
            'max_price': max_price,
            'min_margin': 0.15
        }
        
        # Calculate optimal price
        result = pricing_agent.calculate_optimal_price(
            product_data,
            market_data,
            business_rules
        )
        
        return jsonify({
            'success': True,
            'optimization': result,
            'market_insights': {
                'avg_competitor_price': round(avg_competitor_price, 2),
                'recent_demand': round(avg_recent_sales, 2),
                'current_price': product['current_price']
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/pricing/batch-optimize', methods=['POST'])
def batch_optimize_prices():
    """Optimize prices for all products"""
    try:
        products = db.get_all_products()
        results = []
        
        for _, product in products.iterrows():
            product_id = product['product_id']
            
            # Get market data
            sales_history = db.get_sales_history(product_id, days=30)
            competitor_prices = db.get_competitor_prices(product_id, days=7)
            
            avg_competitor_price = competitor_prices['competitor_price'].mean() if not competitor_prices.empty else product['base_price']
            avg_recent_sales = sales_history['quantity_sold'].mean() if not sales_history.empty else 10
            
            market_data = {
                'demand_forecast': avg_recent_sales,
                'competitor_price': avg_competitor_price,
                'seasonality': 'normal'
            }
            
            product_data = {
                'base_price': product['base_price'],
                'inventory': product['inventory']
            }
            
            business_rules = {
                'min_price': product['min_price'],
                'max_price': product['max_price'],
                'min_margin': 0.15
            }
            
            optimization = pricing_agent.calculate_optimal_price(
                product_data,
                market_data,
                business_rules
            )
            
            results.append({
                'product_id': product_id,
                'product_name': product['name'],
                'current_price': product['current_price'],
                'suggested_price': optimization['optimal_price'],
                'change_percentage': round(((optimization['optimal_price'] - product['current_price']) / product['current_price']) * 100, 2)
            })
        
        return jsonify({
            'success': True,
            'optimizations': results,
            'total_products': len(results)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# Sales endpoints
@app.route('/api/sales', methods=['GET'])
def get_sales():
    """Get sales history"""
    try:
        days = request.args.get('days', 30, type=int)
        product_id = request.args.get('product_id', None, type=int)
        
        sales = db.get_sales_history(product_id, days)
        
        return jsonify({
            'success': True,
            'sales': sales.to_dict('records'),
            'total_records': len(sales)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/sales', methods=['POST'])
def record_sale():
    """Record a new sale"""
    try:
        data = request.json
        
        db.record_sale(
            product_id=int(data['product_id']),
            quantity=int(data['quantity']),
            price=float(data['price'])
        )
        
        return jsonify({
            'success': True,
            'message': 'Sale recorded successfully'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# Analytics endpoints
@app.route('/api/analytics/revenue', methods=['GET'])
def get_revenue_analytics():
    """Get revenue analytics"""
    try:
        days = request.args.get('days', 30, type=int)
        revenue_data = db.get_revenue_report(days)
        
        total_revenue = revenue_data['daily_revenue'].sum() if not revenue_data.empty else 0
        total_sales = revenue_data['daily_sales'].sum() if not revenue_data.empty else 0
        
        return jsonify({
            'success': True,
            'analytics': {
                'total_revenue': round(total_revenue, 2),
                'total_sales': int(total_sales),
                'avg_daily_revenue': round(revenue_data['daily_revenue'].mean(), 2) if not revenue_data.empty else 0,
                'daily_breakdown': revenue_data.to_dict('records')
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/analytics/product/<int:product_id>', methods=['GET'])
def get_product_analytics(product_id):
    """Get product performance analytics"""
    try:
        days = request.args.get('days', 30, type=int)
        performance = db.get_product_performance(product_id, days)
        
        if performance:
            return jsonify({
                'success': True,
                'performance': performance
            })
        return jsonify({'success': False, 'error': 'No data found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/analytics/dashboard', methods=['GET'])
def get_dashboard_stats():
    """Get dashboard statistics"""
    try:
        # Get overall statistics
        products = db.get_all_products()
        revenue_data = db.get_revenue_report(30)
        
        total_products = len(products)
        total_revenue_30d = revenue_data['daily_revenue'].sum() if not revenue_data.empty else 0
        total_sales_30d = revenue_data['daily_sales'].sum() if not revenue_data.empty else 0
        
        # Calculate average price change
        avg_current_price = products['current_price'].mean()
        avg_base_price = products['base_price'].mean()
        avg_price_change = ((avg_current_price - avg_base_price) / avg_base_price) * 100 if avg_base_price > 0 else 0
        
        # Get low inventory products
        low_inventory = products[products['inventory'] < 50]['product_id'].count()
        
        return jsonify({
            'success': True,
            'stats': {
                'total_products': int(total_products),
                'total_revenue_30d': round(total_revenue_30d, 2),
                'total_sales_30d': int(total_sales_30d),
                'avg_price_change': round(avg_price_change, 2),
                'low_inventory_count': int(low_inventory),
                'revenue_trend': revenue_data.tail(7).to_dict('records')
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# Competitor monitoring endpoints
@app.route('/api/competitors/<int:product_id>', methods=['GET'])
def get_competitor_prices_endpoint(product_id):
    """Get competitor prices for a product"""
    try:
        days = request.args.get('days', 7, type=int)
        prices = db.get_competitor_prices(product_id, days)
        
        return jsonify({
            'success': True,
            'competitor_prices': prices.to_dict('records')
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/competitors', methods=['POST'])
def add_competitor_price():
    """Add competitor price"""
    try:
        data = request.json
        
        db.record_competitor_price(
            product_id=int(data['product_id']),
            competitor_name=data['competitor_name'],
            price=float(data['price']),
            url=data.get('url', '')
        )
        
        return jsonify({
            'success': True,
            'message': 'Competitor price recorded'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# Settings endpoints
@app.route('/api/settings', methods=['GET'])
def get_settings():
    """Get system settings"""
    try:
        settings = {
            'pricing_strategy': db.get_setting('pricing_strategy', 'balanced'),
            'auto_pricing': db.get_setting('auto_pricing', False),
            'price_update_frequency': db.get_setting('price_update_frequency', 'daily'),
            'min_margin': db.get_setting('min_margin', 15),
            'max_discount': db.get_setting('max_discount', 30),
            'exploration_rate': db.get_setting('exploration_rate', 20)
        }
        
        return jsonify({
            'success': True,
            'settings': settings
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/settings', methods=['POST'])
def update_settings():
    """Update system settings"""
    try:
        data = request.json
        
        for key, value in data.items():
            db.save_setting(key, value)
        
        return jsonify({
            'success': True,
            'message': 'Settings updated successfully'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# Initialize sample data
@app.route('/api/initialize-sample-data', methods=['POST'])
def initialize_sample_data():
    """Initialize database with sample data"""
    try:
        db.generate_sample_data()
        return jsonify({
            'success': True,
            'message': 'Sample data generated successfully'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== Authentication Endpoints ====================

@app.route('/api/auth/login', methods=['POST'])
def login():
    """User login endpoint"""
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'success': False, 'error': 'Missing credentials'}), 400
        
        result = db.authenticate_user(username, password)
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 401
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/auth/register', methods=['POST'])
def register():
    """User registration endpoint"""
    try:
        data = request.json
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        full_name = data.get('full_name', '')
        
        if not username or not email or not password:
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        # Pass plain password - create_user will hash it
        result = db.create_user(username, email, password, full_name)
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 400
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/users', methods=['GET'])
def get_users():
    """Get all users"""
    try:
        users = db.get_all_users()
        return jsonify({
            'success': True,
            'users': users.to_dict(orient='records')
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== Shopping Cart Endpoints ====================

@app.route('/api/cart/<int:user_id>', methods=['GET'])
def get_cart(user_id):
    """Get user's shopping cart"""
    try:
        cart = db.get_user_cart(user_id)
        
        cart_total = cart['total_price'].sum() if not cart.empty else 0
        
        return jsonify({
            'success': True,
            'cart': cart.to_dict(orient='records'),
            'total': float(cart_total),
            'item_count': len(cart)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/cart/add', methods=['POST'])
def add_to_cart():
    """Add item to cart"""
    try:
        data = request.json
        user_id = data.get('user_id')
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)
        
        if not user_id or not product_id:
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        # Get product details
        product = db.get_product(product_id)
        if not product:
            return jsonify({'success': False, 'error': 'Product not found'}), 404
        
        # Track product view
        db.track_product_view(product_id, user_id)
        
        # Start active session
        db.start_active_session(user_id, product_id, 'adding_to_cart')
        
        result = db.add_to_cart(user_id, product_id, quantity)
        
        # Calculate min/max prices if not set
        cost_price = product.get('cost_price', product['base_price'] * 0.6)
        min_price = product.get('min_price') or max(cost_price * 1.1, product['base_price'] * 0.7)
        max_price = product.get('max_price') or product['base_price'] * 1.5
        
        # Trigger price update based on new activity
        pricing_result = dynamic_pricing.calculate_dynamic_price(
            product_id,
            product['base_price'],
            min_price,
            max_price,
            product['inventory']
        )
        
        # Update price in database
        db.update_product_price(product_id, pricing_result['new_price'])
        
        return jsonify({
            'success': True,
            'new_price': pricing_result['new_price'],
            'price_increased': pricing_result['new_price'] > db.get_product(product_id)['current_price']
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/cart/remove/<int:cart_id>', methods=['DELETE'])
def remove_from_cart(cart_id):
    """Remove item from cart"""
    try:
        result = db.remove_from_cart(cart_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/cart/update', methods=['PUT'])
def update_cart():
    """Update cart item quantity"""
    try:
        data = request.json
        cart_id = data.get('cart_id')
        quantity = data.get('quantity')
        
        if not cart_id or quantity is None:
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        result = db.update_cart_quantity(cart_id, quantity)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/cart/clear/<int:user_id>', methods=['DELETE'])
def clear_cart(user_id):
    """Clear user's cart"""
    try:
        result = db.clear_cart(user_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/cart/checkout/<int:user_id>', methods=['POST'])
def checkout_cart(user_id):
    """Process checkout - record sales and clear cart"""
    try:
        # Get cart items (returns DataFrame)
        cart_df = db.get_user_cart(user_id)
        
        if cart_df.empty:
            return jsonify({'success': False, 'error': 'Cart is empty'}), 400
        
        cart_items = cart_df.to_dict('records')
        total_revenue = 0
        
        # Record each item as a sale
        for item in cart_items:
            sale_revenue = item['price_at_add'] * item['quantity']
            total_revenue += sale_revenue
            
            # Add to sales history
            db.add_sale(
                product_id=item['product_id'],
                quantity=item['quantity'],
                price=item['price_at_add'],
                revenue=sale_revenue
            )
            
            # Update inventory
            product = db.get_product(item['product_id'])
            if product:
                new_inventory = max(0, product['inventory'] - item['quantity'])
                conn = db.get_connection()
                conn.execute(
                    'UPDATE products SET inventory = ? WHERE product_id = ?',
                    (new_inventory, item['product_id'])
                )
                conn.commit()
                conn.close()
        
        # Clear the cart
        db.clear_cart(user_id)
        
        return jsonify({
            'success': True,
            'message': 'Purchase completed successfully',
            'total_items': len(cart_items),
            'total_revenue': round(total_revenue, 2)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== Product Tracking Endpoints ====================

@app.route('/api/products/<int:product_id>/track/search', methods=['POST'])
def track_search(product_id):
    """Track product search"""
    try:
        data = request.json or {}
        user_id = data.get('user_id')
        search_query = data.get('query', '')
        
        db.track_product_search(product_id, user_id, search_query)
        
        # Recalculate price based on increased search activity
        product = db.get_product(product_id)
        
        # Handle NULL min/max prices
        base_price = product['base_price']
        cost_price = product.get('cost_price', base_price * 0.7)
        min_price = product.get('min_price') or max(cost_price * 1.1, base_price * 0.7)
        max_price = product.get('max_price') or base_price * 1.5
        
        pricing_result = dynamic_pricing.calculate_dynamic_price(
            product_id,
            base_price,
            min_price,
            max_price,
            product['inventory']
        )
        
        db.update_product_price(product_id, pricing_result['new_price'])
        
        return jsonify({
            'success': True,
            'new_price': pricing_result['new_price'],
            'pricing_factors': pricing_result['factors']
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/products/<int:product_id>/track/view', methods=['POST'])
def track_view(product_id):
    """Track product view"""
    try:
        data = request.json or {}
        user_id = data.get('user_id')
        
        db.track_product_view(product_id, user_id)
        
        return jsonify({'success': True})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/products/<int:product_id>/engagement', methods=['GET'])
def get_engagement(product_id):
    """Get product engagement statistics"""
    try:
        stats = db.get_product_engagement_stats(product_id, hours=24)
        concurrent = db.get_concurrent_users(product_id, minutes=5)
        
        return jsonify({
            'success': True,
            'engagement': stats,
            'concurrent_users': concurrent
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== Dynamic Pricing Endpoints ====================

@app.route('/api/pricing/dynamic/<int:product_id>', methods=['GET'])
def get_dynamic_price(product_id):
    """Get real-time dynamic price for a product"""
    try:
        product = db.get_product(product_id)
        
        if product is None:
            return jsonify({'success': False, 'error': 'Product not found'}), 404
        
        pricing_result = dynamic_pricing.calculate_dynamic_price(
            product_id,
            product['base_price'],
            product['min_price'],
            product['max_price'],
            product['inventory']
        )
        
        return jsonify({
            'success': True,
            **pricing_result
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/pricing/update-all', methods=['POST'])
def update_all_prices():
    """Update prices for all products based on current activity"""
    try:
        result = dynamic_pricing.update_product_prices()
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/simulation/concurrent-purchase/<int:product_id>', methods=['POST'])
def simulate_concurrent_purchase(product_id):
    """Simulate multiple users purchasing the same product"""
    try:
        data = request.json or {}
        num_users = data.get('num_users', 3)
        
        result = dynamic_pricing.simulate_concurrent_purchases(product_id, num_users)
        
        return jsonify({
            'success': True,
            **result
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    print("=" * 60)
    print("AI-Driven Dynamic Pricing System - Backend Server")
    print("=" * 60)
    print("Starting Flask server on http://localhost:5000")
    print("API Documentation:")
    print("  - GET  /api/health - Health check")
    print("  - POST /api/auth/login - User login")
    print("  - POST /api/auth/register - User registration")
    print("  - GET  /api/products - Get all products")
    print("  - POST /api/products - Add new product")
    print("  - GET  /api/cart/<user_id> - Get shopping cart")
    print("  - POST /api/cart/add - Add to cart")
    print("  - POST /api/pricing/dynamic/<id> - Get dynamic price")
    print("  - POST /api/simulation/concurrent-purchase/<id> - Simulate concurrent users")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
