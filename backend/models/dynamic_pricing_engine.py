"""
Enhanced Dynamic Pricing Engine
Adjusts prices based on demand, searches, trends, and concurrent user activity
"""

import numpy as np
from datetime import datetime, timedelta


class DynamicPricingEngine:
    """
    Real-time dynamic pricing engine that considers:
    - Product demand (sales velocity)
    - Search frequency
    - Product views
    - Cart additions
    - Concurrent users viewing/buying
    - Time of day
    - Inventory levels
    """
    
    def __init__(self, database_manager):
        """Initialize with database connection"""
        self.db = database_manager
        
        # Pricing factors (weights)
        self.weights = {
            'demand_factor': 0.25,
            'search_factor': 0.20,
            'view_factor': 0.15,
            'cart_factor': 0.20,
            'concurrent_factor': 0.15,
            'inventory_factor': 0.05
        }
    
    def calculate_dynamic_price(self, product_id, base_price, min_price, max_price, inventory):
        """
        Calculate optimal price based on real-time factors
        
        Args:
            product_id: Product ID
            base_price: Original base price
            min_price: Minimum allowed price
            max_price: Maximum allowed price
            inventory: Current inventory level
        
        Returns:
            dict: New price and factor breakdown
        """
        # Get recent engagement stats (last 24 hours)
        engagement = self.db.get_product_engagement_stats(product_id, hours=24)
        
        # Get concurrent users (last 5 minutes)
        concurrent_users = self.db.get_concurrent_users(product_id, minutes=5)
        
        # Get sales velocity (last 7 days)
        sales_velocity = self.get_sales_velocity(product_id, days=7)
        
        # Calculate individual factors
        demand_multiplier = self.calculate_demand_factor(sales_velocity)
        search_multiplier = self.calculate_search_factor(engagement['search_count'])
        view_multiplier = self.calculate_view_factor(engagement['view_count'])
        cart_multiplier = self.calculate_cart_factor(engagement['cart_count'])
        concurrent_multiplier = self.calculate_concurrent_factor(concurrent_users)
        inventory_multiplier = self.calculate_inventory_factor(inventory)
        
        # Weighted average of all factors
        total_multiplier = 1.0 + (
            demand_multiplier * self.weights['demand_factor'] +
            search_multiplier * self.weights['search_factor'] +
            view_multiplier * self.weights['view_factor'] +
            cart_multiplier * self.weights['cart_factor'] +
            concurrent_multiplier * self.weights['concurrent_factor'] +
            inventory_multiplier * self.weights['inventory_factor']
        )
        
        # Calculate new price
        new_price = base_price * total_multiplier
        
        # Ensure price within bounds
        new_price = max(min_price, min(max_price, new_price))
        
        # Round to 2 decimals
        new_price = round(new_price, 2)
        
        return {
            'new_price': new_price,
            'base_price': base_price,
            'multiplier': round(total_multiplier, 4),
            'price_change_percent': round(((new_price - base_price) / base_price) * 100, 2),
            'factors': {
                'demand': round(demand_multiplier, 4),
                'searches': round(search_multiplier, 4),
                'views': round(view_multiplier, 4),
                'cart_additions': round(cart_multiplier, 4),
                'concurrent_users': round(concurrent_multiplier, 4),
                'inventory': round(inventory_multiplier, 4)
            },
            'stats': {
                'searches_24h': engagement['search_count'],
                'views_24h': engagement['view_count'],
                'cart_adds_24h': engagement['cart_count'],
                'concurrent_users': concurrent_users,
                'sales_velocity': sales_velocity,
                'inventory': inventory
            }
        }
    
    def calculate_demand_factor(self, sales_velocity):
        """
        Calculate price adjustment based on sales velocity
        Higher sales = higher price (up to +20%)
        """
        if sales_velocity == 0:
            return -0.10  # Decrease price by 10% for no sales
        elif sales_velocity < 5:
            return 0.0  # Normal price
        elif sales_velocity < 15:
            return 0.10  # Increase by 10%
        else:
            return 0.20  # Increase by 20%
    
    def calculate_search_factor(self, search_count):
        """
        Calculate price adjustment based on search frequency
        More searches = higher interest = potential price increase
        """
        if search_count == 0:
            return -0.05
        elif search_count < 10:
            return 0.0
        elif search_count < 30:
            return 0.05
        elif search_count < 50:
            return 0.10
        else:
            return 0.15  # High interest, increase price
    
    def calculate_view_factor(self, view_count):
        """
        Calculate price adjustment based on product views
        """
        if view_count == 0:
            return -0.05
        elif view_count < 20:
            return 0.0
        elif view_count < 50:
            return 0.05
        else:
            return 0.10
    
    def calculate_cart_factor(self, cart_count):
        """
        Calculate price adjustment based on cart additions
        More cart additions = high buying intent = price increase
        """
        if cart_count == 0:
            return 0.0
        elif cart_count < 5:
            return 0.05
        elif cart_count < 10:
            return 0.10
        else:
            return 0.15  # Very high demand
    
    def calculate_concurrent_factor(self, concurrent_users):
        """
        Calculate price adjustment based on concurrent users
        Multiple users viewing simultaneously = scarcity signal
        """
        if concurrent_users <= 1:
            return 0.0
        elif concurrent_users == 2:
            return 0.05
        elif concurrent_users == 3:
            return 0.10
        else:
            return 0.15  # Multiple users competing
    
    def calculate_inventory_factor(self, inventory):
        """
        Calculate price adjustment based on inventory levels
        Low inventory = increase price
        High inventory = decrease price
        """
        if inventory == 0:
            return 0.0  # Out of stock
        elif inventory < 10:
            return 0.10  # Low stock, increase price
        elif inventory < 50:
            return 0.0  # Normal price
        else:
            return -0.10  # High stock, decrease to move inventory
    
    def get_sales_velocity(self, product_id, days=7):
        """
        Calculate sales velocity (average daily sales)
        """
        sales_history = self.db.get_sales_history(product_id)
        
        if sales_history.empty:
            return 0
        
        # Filter to last N days
        cutoff_date = datetime.now() - timedelta(days=days)
        sales_history['sale_date'] = pd.to_datetime(sales_history['sale_date'])
        recent_sales = sales_history[sales_history['sale_date'] >= cutoff_date]
        
        if recent_sales.empty:
            return 0
        
        # Calculate average daily sales
        total_quantity = recent_sales['quantity_sold'].sum()
        velocity = total_quantity / days
        
        return velocity
    
    def update_product_prices(self, product_ids=None):
        """
        Update prices for all products or specific products
        
        Args:
            product_ids: List of product IDs to update (None = all products)
        
        Returns:
            dict: Summary of price updates
        """
        if product_ids is None:
            # Get all products
            products = self.db.get_all_products()
            product_ids = products['product_id'].tolist()
        
        updates = []
        
        for product_id in product_ids:
            product = self.db.get_product(product_id)
            
            if product is None:
                continue
            
            # Calculate min/max prices if not set
            cost_price = product.get('cost_price', product['base_price'] * 0.6)
            min_price = product.get('min_price') or max(cost_price * 1.1, product['base_price'] * 0.7)
            max_price = product.get('max_price') or product['base_price'] * 1.5
            
            # Calculate new price
            pricing_result = self.calculate_dynamic_price(
                product_id,
                product['base_price'],
                min_price,
                max_price,
                product['inventory']
            )
            
            # Update price in database
            self.db.update_product_price(product_id, pricing_result['new_price'])
            
            # Record price change
            updates.append({
                'product_id': product_id,
                'product_name': product['name'],
                'old_price': product['current_price'],
                'new_price': pricing_result['new_price'],
                'change_percent': pricing_result['price_change_percent'],
                'factors': pricing_result['factors']
            })
        
        return {
            'success': True,
            'updated_count': len(updates),
            'updates': updates
        }
    
    def simulate_concurrent_purchases(self, product_id, num_users=3):
        """
        Simulate multiple users trying to purchase the same product
        Shows how price increases with concurrent activity
        
        Args:
            product_id: Product to simulate
            num_users: Number of concurrent users
        
        Returns:
            list: Price progression as users interact
        """
        import time
        
        product = self.db.get_product(product_id)
        if product is None:
            return {'error': 'Product not found'}
        
        simulation_steps = []
        
        # Initial price
        initial_pricing = self.calculate_dynamic_price(
            product_id,
            product['base_price'],
            product['min_price'],
            product['max_price'],
            product['inventory']
        )
        
        simulation_steps.append({
            'step': 0,
            'action': 'Initial state',
            'active_users': 0,
            'price': initial_pricing['new_price'],
            'factors': initial_pricing['factors']
        })
        
        # Simulate users joining
        session_ids = []
        for i in range(1, num_users + 1):
            # User starts viewing product
            session_id = self.db.start_active_session(100 + i, product_id, 'viewing')
            session_ids.append(session_id)
            
            # Track view
            self.db.track_product_view(product_id, 100 + i)
            
            # Calculate new price
            pricing = self.calculate_dynamic_price(
                product_id,
                product['base_price'],
                product['min_price'],
                product['max_price'],
                product['inventory']
            )
            
            simulation_steps.append({
                'step': i,
                'action': f'User {i} starts viewing',
                'active_users': i,
                'price': pricing['new_price'],
                'concurrent_factor': pricing['factors']['concurrent_users'],
                'price_change_from_previous': round(pricing['new_price'] - simulation_steps[-1]['price'], 2)
            })
        
        # Simulate users adding to cart
        for i in range(num_users):
            self.db.add_to_cart(100 + i + 1, product_id, 1)
            
            pricing = self.calculate_dynamic_price(
                product_id,
                product['base_price'],
                product['min_price'],
                product['max_price'],
                product['inventory']
            )
            
            simulation_steps.append({
                'step': num_users + i + 1,
                'action': f'User {i + 1} adds to cart',
                'active_users': num_users,
                'price': pricing['new_price'],
                'cart_factor': pricing['factors']['cart_additions'],
                'price_change_from_initial': round(pricing['new_price'] - simulation_steps[0]['price'], 2)
            })
        
        # Clean up sessions
        for session_id in session_ids:
            self.db.end_active_session(session_id)
        
        return {
            'product_id': product_id,
            'product_name': product['name'],
            'base_price': product['base_price'],
            'initial_price': simulation_steps[0]['price'],
            'final_price': simulation_steps[-1]['price'],
            'total_increase': round(simulation_steps[-1]['price'] - simulation_steps[0]['price'], 2),
            'increase_percent': round(((simulation_steps[-1]['price'] - simulation_steps[0]['price']) / simulation_steps[0]['price']) * 100, 2),
            'simulation_steps': simulation_steps
        }


# Import pandas for data operations
import pandas as pd
