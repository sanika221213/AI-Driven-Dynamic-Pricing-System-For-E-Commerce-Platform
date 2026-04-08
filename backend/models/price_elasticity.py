"""
Price Elasticity Calculator
Estimates how demand changes with price changes
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


class PriceElasticityCalculator:
    """
    Calculate and estimate price elasticity of demand
    Based on historical pricing and sales data
    """
    
    def __init__(self):
        self.elasticity_models = {}
        
    def calculate_elasticity(self, prices, quantities):
        """
        Calculate price elasticity using historical data
        
        Args:
            prices: Array of historical prices
            quantities: Array of corresponding quantities sold
            
        Returns:
            Elasticity coefficient
        """
        if len(prices) < 2 or len(quantities) < 2:
            return -1.0  # Default elasticity
        
        # Convert to numpy arrays
        prices = np.array(prices)
        quantities = np.array(quantities)
        
        # Calculate percentage changes
        price_changes = np.diff(np.log(prices))
        quantity_changes = np.diff(np.log(quantities))
        
        # Elasticity = % change in quantity / % change in price
        if len(price_changes) > 0 and np.std(price_changes) > 0:
            elasticity = np.mean(quantity_changes / price_changes)
            return elasticity
        
        return -1.0
    
    def fit_elasticity_model(self, product_id, historical_data):
        """
        Fit elasticity model for a specific product
        
        Args:
            product_id: Product identifier
            historical_data: DataFrame with 'price' and 'quantity' columns
        """
        if len(historical_data) < 10:
            # Not enough data for reliable estimation
            self.elasticity_models[product_id] = {'elasticity': -1.0, 'model': None}
            return
        
        X = np.log(historical_data['price'].values).reshape(-1, 1)
        y = np.log(historical_data['quantity'].values)
        
        model = LinearRegression()
        model.fit(X, y)
        
        elasticity = model.coef_[0]
        
        self.elasticity_models[product_id] = {
            'elasticity': elasticity,
            'model': model,
            'r_squared': model.score(X, y)
        }
    
    def predict_demand_at_price(self, product_id, current_price, new_price, current_demand):
        """
        Predict demand at a new price point
        
        Args:
            product_id: Product identifier
            current_price: Current price
            new_price: Proposed new price
            current_demand: Current demand level
            
        Returns:
            Predicted demand
        """
        if product_id not in self.elasticity_models:
            # Use default elasticity
            elasticity = -1.0
        else:
            elasticity = self.elasticity_models[product_id]['elasticity']
        
        # Calculate predicted demand using elasticity
        price_change_pct = (new_price - current_price) / current_price
        demand_change_pct = elasticity * price_change_pct
        
        predicted_demand = current_demand * (1 + demand_change_pct)
        
        return max(0, predicted_demand)  # Demand can't be negative
    
    def get_optimal_price_for_revenue(self, product_id, base_price, base_demand, price_range):
        """
        Find price that maximizes revenue within a range
        
        Args:
            product_id: Product identifier
            base_price: Base price
            base_demand: Base demand
            price_range: Tuple of (min_price, max_price)
            
        Returns:
            Optimal price for maximum revenue
        """
        prices = np.linspace(price_range[0], price_range[1], 100)
        revenues = []
        
        for price in prices:
            demand = self.predict_demand_at_price(product_id, base_price, price, base_demand)
            revenue = price * demand
            revenues.append(revenue)
        
        optimal_idx = np.argmax(revenues)
        optimal_price = prices[optimal_idx]
        max_revenue = revenues[optimal_idx]
        
        return {
            'optimal_price': optimal_price,
            'expected_revenue': max_revenue,
            'expected_demand': self.predict_demand_at_price(product_id, base_price, optimal_price, base_demand)
        }
