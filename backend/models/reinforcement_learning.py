"""
Reinforcement Learning Agent for Dynamic Pricing
Based on research methodology: RL for optimal pricing decisions
Implements Q-Learning and Contextual Bandits
"""

import numpy as np
import pandas as pd
from collections import defaultdict
import json
import os


class ContextualBandit:
    """
    Contextual Bandit algorithm for dynamic pricing
    Implements ε-greedy strategy for exploration-exploitation balance
    """
    
    def __init__(self, price_actions, epsilon=0.2, learning_rate=0.1):
        """
        Initialize Contextual Bandit
        
        Args:
            price_actions: List of possible price multipliers (e.g., [0.8, 0.9, 1.0, 1.1, 1.2])
            epsilon: Exploration rate (20% exploration as per research)
            learning_rate: Learning rate for Q-value updates
        """
        self.price_actions = price_actions
        self.epsilon = epsilon
        self.learning_rate = learning_rate
        
        # Q-values for state-action pairs
        self.Q = defaultdict(lambda: defaultdict(float))
        
        # Action counts for exploration
        self.action_counts = defaultdict(lambda: defaultdict(int))
        
    def get_state_key(self, state):
        """Convert state dictionary to hashable key"""
        return tuple(sorted(state.items()))
    
    def select_action(self, state):
        """
        Select pricing action using ε-greedy policy
        
        Args:
            state: Current market state (dict with demand, competitor_price, etc.)
            
        Returns:
            Selected price multiplier
        """
        state_key = self.get_state_key(state)
        
        # Exploration: random action
        if np.random.random() < self.epsilon:
            return np.random.choice(self.price_actions)
        
        # Exploitation: best known action
        q_values = [self.Q[state_key][action] for action in self.price_actions]
        
        if all(q == 0 for q in q_values):
            # No experience yet, choose randomly
            return np.random.choice(self.price_actions)
        
        best_action_idx = np.argmax(q_values)
        return self.price_actions[best_action_idx]
    
    def update(self, state, action, reward, next_state):
        """
        Update Q-values based on observed reward
        
        Args:
            state: Current state
            action: Action taken
            reward: Reward received
            next_state: Resulting state
        """
        state_key = self.get_state_key(state)
        next_state_key = self.get_state_key(next_state)
        
        # Get max Q-value for next state
        next_q_values = [self.Q[next_state_key][a] for a in self.price_actions]
        max_next_q = max(next_q_values) if next_q_values else 0
        
        # Q-learning update
        current_q = self.Q[state_key][action]
        new_q = current_q + self.learning_rate * (reward + 0.9 * max_next_q - current_q)
        
        self.Q[state_key][action] = new_q
        self.action_counts[state_key][action] += 1
    
    def save(self, filepath):
        """Save bandit state to file"""
        state = {
            'Q': {str(k): dict(v) for k, v in self.Q.items()},
            'action_counts': {str(k): dict(v) for k, v in self.action_counts.items()},
            'price_actions': self.price_actions,
            'epsilon': self.epsilon,
            'learning_rate': self.learning_rate
        }
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2)
    
    def load(self, filepath):
        """Load bandit state from file"""
        with open(filepath, 'r') as f:
            state = json.load(f)
        
        self.Q = defaultdict(lambda: defaultdict(float))
        for k, v in state['Q'].items():
            state_key = eval(k)
            for action, q_val in v.items():
                self.Q[state_key][float(action)] = q_val
        
        self.action_counts = defaultdict(lambda: defaultdict(int))
        for k, v in state['action_counts'].items():
            state_key = eval(k)
            for action, count in v.items():
                self.action_counts[state_key][float(action)] = count
        
        self.price_actions = state['price_actions']
        self.epsilon = state['epsilon']
        self.learning_rate = state['learning_rate']


class DynamicPricingAgent:
    """
    Advanced RL agent for dynamic pricing with DQN capabilities
    Implements the core pricing optimization logic
    """
    
    def __init__(self, base_price_range=(10, 1000), discount_range=(0.7, 1.3)):
        """
        Initialize Dynamic Pricing Agent
        
        Args:
            base_price_range: Range of base prices
            discount_range: Range of price multipliers
        """
        self.base_price_range = base_price_range
        self.discount_range = discount_range
        
        # Price action space (multipliers)
        self.price_multipliers = np.linspace(discount_range[0], discount_range[1], 11)
        
        # Initialize contextual bandit
        self.bandit = ContextualBandit(
            price_actions=list(self.price_multipliers),
            epsilon=0.2,
            learning_rate=0.1
        )
        
        # Performance tracking
        self.performance_history = []
    
    def extract_state(self, product_data, market_data):
        """
        Extract state representation from product and market data
        
        Args:
            product_data: Dict with product info (inventory, base_price, etc.)
            market_data: Dict with market info (demand_forecast, competitor_price, etc.)
            
        Returns:
            State dictionary
        """
        # Discretize continuous values for state representation
        demand_level = self._discretize_demand(market_data.get('demand_forecast', 0))
        inventory_level = self._discretize_inventory(product_data.get('inventory', 0))
        competitor_price_ratio = self._get_competitor_ratio(
            product_data.get('base_price', 100),
            market_data.get('competitor_price', 100)
        )
        seasonality = market_data.get('seasonality', 'normal')
        
        state = {
            'demand_level': demand_level,
            'inventory_level': inventory_level,
            'competitor_ratio': competitor_price_ratio,
            'seasonality': seasonality
        }
        
        return state
    
    def _discretize_demand(self, demand):
        """Discretize demand into levels"""
        if demand < 10:
            return 'low'
        elif demand < 30:
            return 'medium'
        else:
            return 'high'
    
    def _discretize_inventory(self, inventory):
        """Discretize inventory into levels"""
        if inventory < 20:
            return 'low'
        elif inventory < 100:
            return 'medium'
        else:
            return 'high'
    
    def _get_competitor_ratio(self, our_price, competitor_price):
        """Calculate price ratio relative to competitor"""
        if competitor_price == 0:
            return 'equal'
        
        ratio = our_price / competitor_price
        
        if ratio < 0.9:
            return 'lower'
        elif ratio > 1.1:
            return 'higher'
        else:
            return 'equal'
    
    def calculate_optimal_price(self, product_data, market_data, business_rules=None):
        """
        Calculate optimal price using RL agent
        
        Args:
            product_data: Product information
            market_data: Market conditions
            business_rules: Optional constraints (min_price, max_price, min_margin)
            
        Returns:
            Optimal price and metadata
        """
        # Extract state
        state = self.extract_state(product_data, market_data)
        
        # Get base price
        base_price = product_data.get('base_price', 100)
        
        # Select action (price multiplier)
        price_multiplier = self.bandit.select_action(state)
        
        # Calculate suggested price
        suggested_price = base_price * price_multiplier
        
        # Apply business rules
        if business_rules:
            suggested_price = self._apply_business_rules(
                suggested_price,
                base_price,
                business_rules
            )
        
        # Calculate final multiplier after rules
        final_multiplier = suggested_price / base_price
        
        return {
            'optimal_price': round(suggested_price, 2),
            'base_price': base_price,
            'multiplier': round(final_multiplier, 3),
            'state': state,
            'action': price_multiplier
        }
    
    def _apply_business_rules(self, price, base_price, rules):
        """Apply business constraints to pricing"""
        min_price = rules.get('min_price', base_price * 0.7)
        max_price = rules.get('max_price', base_price * 1.3)
        min_margin = rules.get('min_margin', 0.1)
        
        # Ensure minimum margin
        cost = base_price * (1 - min_margin)
        if price < cost:
            price = cost
        
        # Ensure price bounds
        price = max(min_price, min(max_price, price))
        
        return price
    
    def update_from_feedback(self, product_data, market_data, action, sales, revenue):
        """
        Update agent based on observed sales and revenue
        
        Args:
            product_data: Product information
            market_data: Market conditions
            action: Action taken (price multiplier)
            sales: Number of units sold
            revenue: Revenue generated
        """
        # Calculate reward (combine revenue and conversion)
        base_revenue = product_data.get('base_price', 100) * sales
        reward = (revenue / max(base_revenue, 1)) * 100  # Percentage improvement
        
        # Extract current and next state
        current_state = self.extract_state(product_data, market_data)
        
        # Update market data with new sales info
        next_market_data = market_data.copy()
        next_market_data['recent_sales'] = sales
        next_state = self.extract_state(product_data, next_market_data)
        
        # Update bandit
        self.bandit.update(current_state, action, reward, next_state)
        
        # Track performance
        self.performance_history.append({
            'sales': sales,
            'revenue': revenue,
            'reward': reward,
            'action': action
        })
    
    def get_performance_stats(self):
        """Get performance statistics"""
        if not self.performance_history:
            return {}
        
        df = pd.DataFrame(self.performance_history)
        
        return {
            'total_revenue': df['revenue'].sum(),
            'avg_sales': df['sales'].mean(),
            'avg_reward': df['reward'].mean(),
            'total_interactions': len(self.performance_history)
        }
    
    def save_agent(self, filepath='models/pricing_agent.json'):
        """Save agent state"""
        self.bandit.save(filepath)
        
        # Save performance history
        perf_file = filepath.replace('.json', '_performance.json')
        with open(perf_file, 'w') as f:
            json.dump(self.performance_history, f, indent=2)
    
    def load_agent(self, filepath='models/pricing_agent.json'):
        """Load agent state"""
        self.bandit.load(filepath)
        
        # Load performance history
        perf_file = filepath.replace('.json', '_performance.json')
        if os.path.exists(perf_file):
            with open(perf_file, 'r') as f:
                self.performance_history = json.load(f)
