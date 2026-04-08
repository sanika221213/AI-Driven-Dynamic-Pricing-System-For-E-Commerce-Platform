# CHAPTER 5: METHODOLOGY

---

## 5.1 RESEARCH AND DEVELOPMENT METHODOLOGY

### 5.1.1 Development Approach

The development of the AI-Driven Dynamic Pricing System follows an iterative, component-based methodology combining elements of agile software development with machine learning research best practices. This hybrid approach acknowledges that building ML systems differs from traditional software engineering—model development requires experimentation, hyperparameter tuning, and validation that don't fit strictly into predefined specifications.

**Development Phases:**

**Phase 1: Research and Requirements (Weeks 1-3)**
- Literature review identifying relevant techniques and prior art
- Stakeholder requirements gathering (simulated for academic project)
- Feasibility analysis across technical, economic, operational dimensions
- Technology selection and environment setup
- Preliminary system architecture design

**Phase 2: Data Infrastructure (Weeks 4-6)**
- Database schema design and implementation
- Sample data generation scripts for testing
- Data preprocessing pipelines
- Database indexing and optimization
- API framework setup

**Phase 3: Machine Learning Development (Weeks 7-14)**
- LSTM forecaster implementation and training
- RL agent implementation
- Elasticity calculator development
- Component-level testing and validation
- Hyperparameter tuning
- Model evaluation and metrics

**Phase 4: Integration and Business Logic (Weeks 15-17)**
- Dynamic Pricing Engine implementation
- Multi-component integration
- Business rules implementation
- End-to-end workflow testing
- API endpoint development

**Phase 5: User Interfaces (Weeks 18-20)**
- Frontend interface development
- Dashboard and analytics visualizations
- Customer shop interface
- Usability testing
- Responsive design implementation

**Phase 6: Testing and Validation (Weeks 21-23)**
- Unit testing
- Integration testing
- Performance testing
- Security testing
- Comparative evaluation vs. baselines

**Phase 7: Documentation and Deployment (Weeks 24-26)**
- Technical documentation
- User manuals
- This project report
- Deployment preparation
- Demonstration setup

### 5.1.2 Iterative Refinement Process

Rather than waterfall approach where each phase completes before next begins, development uses iterative cycles:

1. **Implement** minimal viable version of component
2. **Test** functionality and performance
3. **Evaluate** against requirements and metrics
4. **Refine** based on test results
5. **Iterate** until component meets quality standards

This approach particularly benefits ML components where initial implementations rarely perform optimally and require tuning.

### 5.1.3 Version Control and Code Management

All code maintained in Git repository with structured commit history:
- Feature branches for major developments
- Regular commits with descriptive messages
- Code reviews (self-review for solo project, peer review if team)
- Tagged releases marking major milestones

### 5.1.4 Documentation Philosophy

Documentation developed concurrently with code (not as afterthought):
- Inline code comments explaining complex logic
- Function/method docstrings (Google style)
- README files in each module directory
- Architecture decision records (ADRs) documenting key choices
- This comprehensive project report

## 5.2 LSTM DEMAND FORECASTING METHODOLOGY

### 5.2.1 Data Preparation and Feature Engineering

**Data Collection:**
Historical sales data extracted from sales_history table:
```sql
SELECT product_id, DATE(timestamp) as date, SUM(quantity) as daily_quantity
FROM sales_history
WHERE product_id = ? AND timestamp >= DATE('now', '-180 days')
GROUP BY product_id, DATE(timestamp)
ORDER BY date;
```

**Missing Data Handling:**
Sales data often has gaps (days with zero sales). Strategy:
- Fill missing dates with quantity=0 (distinguish between "no sales" and "no data")
- Validate continuous date range without large gaps
- If gaps exceed 30 days, flag product as potentially inactive

**Feature Engineering:**

*Temporal Features:*
- Day of week (one-hot encoded: Monday=1,0,0,0,0,0,0, Tuesday=0,1,0,0,0,0,0, etc.)
- Month (encoded 1-12, normalized to [0,1])
- Day of month (1-31)
- Is_weekend (binary: 0 for weekday, 1 for weekend)
- Is_holiday (binary, based on defined holiday calendar)

*Trend Features:*
- Linear trend (days since start)
- Moving average (7-day MA, 30-day MA)
- Exponentially weighted moving average

*Cyclical Features:*
- Sine/cosine encoding of day-of-year (captures seasonality while maintaining continuity)
  - sin(2π × day_of_year / 365)
  - cos(2π × day_of_year / 365)

*Lag Features:*
- Previous day sales: qty(t-1)
- Previous week same day: qty(t-7)
- Previous month same day: qty(t-30)

*Price Features:*
- Current price
- Price change from previous period
- Price relative to historical average

*External Features:*
- Promotion flag (binary)
- Marketing campaign flag
- Competitor price index

**Normalization:**
Min-Max scaling applied to ensure all features in [0,1] range:
```
X_normalized = (X - X_min) / (X_max - X_min)
```

Scaling parameters (min, max) saved for later inverse transformation during inference.

Alternative: StandardScaler (zero mean, unit variance) considered but Min-Max preferred for LSTM as it preserves zero values and bounds outputs naturally.

### 5.2.2 Sequence Creation for LSTM Training

LSTM requires fixed-length input sequences. Sliding window approach:

**Parameters:**
- Sequence length (lookback): 30 days
- Forecast horizon: 7 days
- Stride: 1 day (overlapping windows maximize training data)

**Window Creation:**
```python
def create_sequences(data, seq_length=30, forecast_horizon=7):
    X, y = [], []
    for i in range(len(data) - seq_length - forecast_horizon + 1):
        X.append(data[i:i+seq_length])  # Input: days t to t+29
        y.append(data[i+seq_length:i+seq_length+forecast_horizon, target_col])  
                                         # Output: days t+30 to t+36
    return np.array(X), np.array(y)
```

**Example:**
Given 100 days of data, with seq_length=30 and horizon=7:
- Window 1: Days 0-29 predict days 30-36
- Window 2: Days 1-30 predict days 31-37
- ...
- Window 64: Days 63-92 predict days 93-99
- Total windows: 100 - 30 - 7 + 1 = 64

### 5.2.3 LSTM Architecture and Training

**Network Architecture:**
```python
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

model = Sequential([
    LSTM(64, return_sequences=True, input_shape=(sequence_length, num_features)),
    Dropout(0.2),
    LSTM(32, return_sequences=False),
    Dropout(0.2),
    Dense(16, activation='relu'),
    Dense(forecast_horizon, activation='linear')
])

model.compile(optimizer='adam', loss='mse', metrics=['mae', 'mape'])
```

**Training Configuration:**
```python
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

early_stop = EarlyStopping(
    monitor='val_loss',
    patience=10,
    restore_best_weights=True
)

checkpoint = ModelCheckpoint(
    'models/lstm_forecaster_best.h5',
    monitor='val_loss',
    save_best_only=True
)

history = model.fit(
    X_train, y_train,
    validation_split=0.2,
    epochs=100,
    batch_size=32,
    callbacks=[early_stop, checkpoint],
    verbose=1
)
```

**Hyperparameter Tuning:**

Initial hyperparameters based on literature review. Tuning via grid search:

| Hyperparameter | Tested Values | Selected |
|----------------|---------------|----------|
| LSTM units (layer 1) | [32, 64, 128] | 64 |
| LSTM units (layer 2) | [16, 32, 64] | 32 |
| Dense units | [8, 16, 32] | 16 |
| Dropout rate | [0.1, 0.2, 0.3] | 0.2 |
| Learning rate | [0.0001, 0.001, 0.01] | 0.001 |
| Batch size | [16, 32, 64] | 32 |
| Sequence length | [14, 30, 60] | 30 |

Selection criterion: Minimize validation MAE while avoiding overfitting (training vs. validation loss gap <10%).

**Overfitting Prevention:**
- Dropout layers (0.2 rate)
- Early stopping (patience=10 epochs)
- L2 regularization considered but not needed given dropout effectiveness
- Validation split (20%) for monitoring generalization

### 5.2.4 Forecast Generation and Uncertainty Quantification

**Inference Process:**
```python
def generate_forecast(product_id, model, scaler):
    # 1. Retrieve recent 30 days of data
    recent_data = get_recent_sales(product_id, days=30)
    
    # 2. Preprocess and normalize
    features = engineer_features(recent_data)
    features_scaled = scaler.transform(features)
    
    # 3. Reshape for LSTM input (1, sequence_length, num_features)
    X = features_scaled.reshape(1, sequence_length, num_features)
    
    # 4. Model prediction
    forecast_scaled = model.predict(X)
    
    # 5. Inverse transform to original scale
    forecast = scaler.inverse_transform(forecast_scaled)
    
    # 6. Compute confidence intervals
    historical_errors = compute_validation_errors(model)
    confidence_interval = 1.96 * np.std(historical_errors)
    lower_bound = forecast - confidence_interval
    upper_bound = forecast + confidence_interval
    
    return forecast, lower_bound, upper_bound
```

**Uncertainty Quantification Methods:**

*Empirical Approach (Current):*
- Compute prediction errors on validation set
- Assume errors approximately normal (validated via Q-Q plot)
- Confidence interval: forecast ± 1.96 × σ_error (95% CI)

*Alternative Approaches (Future Work):*
- **Monte Carlo Dropout:** Run multiple forward passes with dropout enabled during inference, generating distribution of predictions
- **Quantile Regression:** Train model to predict quantiles (5th, 50th, 95th percentile) directly
- **Bayesian Neural Networks:** Model weight uncertainty, propagate through predictions

### 5.2.5 Model Evaluation Metrics

**Point Forecast Accuracy:**

*Mean Absolute Error (MAE):*
```
MAE = (1/n) Σ |actual_i - forecast_i|
```
Interpretation: Average magnitude of forecast errors in original units (e.g., units sold)

*Mean Absolute Percentage Error (MAPE):*
```
MAPE = (1/n) Σ |(actual_i - forecast_i) / actual_i| × 100%
```
Interpretation: Average percentage error. Target: MAPE < 15% indicates good forecast

*Root Mean Squared Error (RMSE):*
```
RMSE = √[(1/n) Σ (actual_i - forecast_i)²]
```
Interpretation: Penalizes large errors more than MAE. Useful for detecting problematic outliers.

**Directional Accuracy:**
```
Directional_Accuracy = (1/n) Σ sign(actual_change_i) == sign(forecast_change_i)
```
Percentage of times forecast correctly predicts direction of change (up vs. down).

**Uncertainty Calibration:**
```
Coverage = (1/n) Σ (actual_i within confidence_interval_i)
```
For 95% confidence interval, coverage should be approximately 95%. If coverage < 95%, intervals too narrow (underconfident). If coverage > 95%, intervals too wide (overconfident).

**Forecast Horizon Analysis:**
Accuracy typically degrades with longer horizons. Evaluate separately for:
- 1-day ahead
- 3-day ahead
- 7-day ahead

Allows understanding how much we can trust forecasts at different horizons.

### 5.2.6 Continuous Model Updating

Forecasting models must adapt as data distributions evolve:

**Update Schedule:**
- **Daily:** Incremental update adding previous day's actual sales to training data (fast)
- **Weekly:** Full retrain from scratch on recent 180 days (comprehensive but slower)

**Incremental Update Process:**
```python
def incremental_update(model, new_data_point):
    # 1. Add new data to training set
    X_new, y_new = create_sequences([new_data_point])
    
    # 2. Perform single epoch training
    model.fit(X_new, y_new, epochs=1, verbose=0)
    
    # 3. Save updated model
    model.save('models/lstm_forecaster_updated.h5')
```

**Full Retrain Trigger Conditions:**
- Scheduled weekly retrain
- Forecast accuracy degrades below threshold (MAPE > 25%)
- Significant concept drift detected (distribution tests fail)
- New product seasonal pattern emerges

**Model Version Management:**
- Each retrain creates new version (versioned file names)
- Forecast metadata records which model version generated it
- A/B testing can compare model versions

## 5.3 REINFORCEMENT LEARNING METHODOLOGY

### 5.3.1 Problem Formulation as MDP

**Markov Decision Process Components:**

*State Space S:*
State representation as tuple of discrete features:
```python
state = (demand_level, inventory_level, competitor_position, seasonality, trend)
```

Discretization functions:
```python
def discretize_demand(recent_sales, historical_avg):
    if recent_sales < 0.7 * historical_avg:
        return 'low'
    elif recent_sales > 1.3 * historical_avg:
        return 'high'
    else:
        return 'medium'

def discretize_inventory(current_stock, max_stock):
    if current_stock < 0.2 * max_stock:
        return 'low'
    elif current_stock > 0.8 * max_stock:
        return 'high'
    else:
        return 'medium'

def discretize_competitor_position(our_price, competitor_avg):
    ratio = our_price / competitor_avg
    if ratio < 0.95:
        return 'below'
    elif ratio > 1.05:
        return 'above'
    else:
        return 'match'

def get_seasonality(month):
    if month in [11, 12]:  # Holiday season
        return 'peak'
    elif month in [1, 2]:  # Post-holiday
        return 'off'
    else:
        return 'normal'

def get_trend(recent_sales_list):
    if len(recent_sales_list) < 7:
        return 'stable'
    slope = np.polyfit(range(len(recent_sales_list)), recent_sales_list, 1)[0]
    if slope < -5:
        return 'declining'
    elif slope > 5:
        return 'growing'
    else:
        return 'stable'
```

*Action Space A:*
Discrete price multipliers:
```python
actions = [0.85, 0.90, 0.95, 1.00, 1.05, 1.10, 1.15, 1.20]
```

Action selection:
```python
def select_action(state, epsilon):
    if random.random() < epsilon:
        # Exploration: random action
        return random.choice(actions)
    else:
        # Exploitation: best known action
        q_values = [Q[(state, a)] for a in actions]
        return actions[np.argmax(q_values)]
```

*Transition Function P(s'|s,a):*
Not explicitly modeled (model-free RL). Transitions result from actual market dynamics—applying price action leads to sales outcome determining next state.

*Reward Function R(s,a,s'):*
```python
def compute_reward(price, quantity_sold, cost, objective='revenue'):
    if objective == 'revenue':
        return price * quantity_sold
    elif objective == 'profit':
        return (price - cost) * quantity_sold
    elif objective == 'hybrid':
        revenue = price * quantity_sold
        profit = (price - cost) * quantity_sold
        return 0.5 * revenue + 0.5 * profit
```

*Discount Factor γ:*
γ = 0.95 weights future rewards at 95% of immediate rewards per time step. Over horizon:
- 1-day ahead: weight = 0.95
- 7-day ahead: weight = 0.95^7 ≈ 0.70
- 30-day ahead: weight = 0.95^30 ≈ 0.21

This discounting reflects practical preference for near-term revenue and uncertainty about distant future.

### 5.3.2 Q-Learning Algorithm Implementation

**Q-Table Initialization:**
```python
import itertools
from collections import defaultdict

# Define all possible states
demand_levels = ['low', 'medium', 'high']
inventory_levels = ['low', 'medium', 'high']
competitor_positions = ['below', 'match', 'above']
seasonalities = ['off', 'normal', 'peak']
trends = ['declining', 'stable', 'growing']

states = list(itertools.product(demand_levels, inventory_levels, 
                                 competitor_positions, seasonalities, trends))

# Initialize Q-table with optimistic values to encourage exploration
Q = defaultdict(lambda: 1000.0)  # Optimistic initialization
for state in states:
    for action in actions:
        Q[(state, action)] = 1000.0
```

**Q-Learning Update Rule:**
```python
def q_learning_update(state, action, reward, next_state, alpha=0.1, gamma=0.95):
    """
    Update Q-value using TD learning:
    Q(s,a) ← Q(s,a) + α [r + γ max_a' Q(s',a') - Q(s,a)]
    """
    # Current Q-value
    current_q = Q[(state, action)]
    
    # Maximum Q-value in next state
    next_max_q = max([Q[(next_state, a)] for a in actions])
    
    # TD target
    target = reward + gamma * next_max_q
    
    # TD error
    td_error = target - current_q
    
    # Update
    Q[(state, action)] = current_q + alpha * td_error
    
    return td_error
```

**Learning Episode:**
```python
def pricing_episode(product_id, epsilon, alpha=0.1, gamma=0.95):
    # 1. Observe current state
    state = get_current_state(product_id)
    
    # 2. Select action (ε-greedy)
    action = select_action(state, epsilon)
    
    # 3. Apply action (set price)
    new_price = product.base_price * action
    update_product_price(product_id, new_price)
    
    # 4. Wait for transaction (or simulate)
    time.sleep(transaction_interval)  # In simulation, move to next time step
    
    # 5. Observe quantity sold
    quantity_sold = get_sales_since_price_change(product_id)
    
    # 6. Compute reward
    reward = compute_reward(new_price, quantity_sold, product.cost)
    
    # 7. Observe next state
    next_state = get_current_state(product_id)
    
    # 8. Q-learning update
    td_error = q_learning_update(state, action, reward, next_state, alpha, gamma)
    
    # 9. Log episode
    log_episode(product_id, state, action, reward, next_state, td_error)
    
    return reward, td_error
```

### 5.3.3 Exploration Strategy

**ε-Greedy with Decay:**
```python
class EpsilonGreedyPolicy:
    def __init__(self, epsilon_start=0.3, epsilon_min=0.05, epsilon_decay=0.995):
        self.epsilon = epsilon_start
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.episode_count = 0
    
    def select_action(self, state, Q, actions):
        if random.random() < self.epsilon:
            # Explore
            return random.choice(actions)
        else:
            # Exploit
            q_values = [Q[(state, a)] for a in actions]
            best_actions = [a for a, q in zip(actions, q_values) 
                           if q == max(q_values)]
            return random.choice(best_actions)  # Break ties randomly
    
    def decay(self):
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
        self.episode_count += 1
```

**Exploration Rationale:**
- Start with high ε (30%) to explore broadly
- Gradually reduce exploration as Q-values converge
- Maintain minimum ε (5%) to continue adapting to non-stationary environment
- Decay rate (0.995) means ε halves roughly every 140 episodes

**Alternative: Softmax Action Selection (Considered but not implemented):**
```python
def softmax_policy(state, Q, actions, temperature=1.0):
    q_values = np.array([Q[(state, a)] for a in actions])
    exp_q = np.exp(q_values / temperature)
    probabilities = exp_q / np.sum(exp_q)
    return np.random.choice(actions, p=probabilities)
```
Softmax provides more graded exploration but adds hyperparameter (temperature). ε-greedy simpler and equally effective for discrete action space.

### 5.3.4 Safe Exploration and Deployment

**Price Bounds Enforcement:**
```python
def apply_price_action(product, action, min_multiplier=0.70, max_multiplier=1.50):
    proposed_price = product.base_price * action
    
    # Apply product-specific bounds
    if product.min_price is not None:
        proposed_price = max(proposed_price, product.min_price)
    if product.max_price is not None:
        proposed_price = min(proposed_price, product.max_price)
    
    # Apply global safety bounds
    proposed_price = max(proposed_price, product.base_price * min_multiplier)
    proposed_price = min(proposed_price, product.base_price * max_multiplier)
    
    # Ensure price covers cost with minimum margin
    min_acceptable_price = product.cost * 1.10  # 10% minimum margin
    proposed_price = max(proposed_price, min_acceptable_price)
    
    return proposed_price
```

**Rate Limiting:**
```python
def check_price_change_rate(product, new_price, max_change_rate=0.20):
    price_change = abs(new_price - product.current_price) / product.current_price
    
    if price_change > max_change_rate:
        # Cap change at maximum rate
        if new_price > product.current_price:
            return product.current_price * (1 + max_change_rate)
        else:
            return product.current_price * (1 - max_change_rate)
    
    return new_price
```

**Gradual Rollout Strategy:**
1. **Simulation Phase:** Train RL agent on historical data simulated environment (no real price changes)
2. **Shadow Mode:** RL agent makes recommendations but doesn't execute (logged for evaluation)
3. **Partial Deployment:** Apply RL pricing to 10% of products (low-risk items)
4. **Monitored Expansion:** If performance metrics positive, expand to 25%, 50%, 100%
5. **Full Deployment:** RL pricing across catalog with continued monitoring

### 5.3.5 Model Persistence and Loading

**Saving Q-Table:**
```python
import pickle

def save_q_table(Q, filepath='models/q_table.pkl'):
    with open(filepath, 'wb') as f:
        pickle.dump(dict(Q), f)  # Convert defaultdict to regular dict

def load_q_table(filepath='models/q_table.pkl'):
    with open(filepath, 'rb') as f:
        Q_dict = pickle.load(f)
    Q = defaultdict(lambda: 0.0)
    Q.update(Q_dict)
    return Q
```

**Versioning:**
- Save Q-table after each training batch (e.g., every 100 episodes)
- Maintain multiple versions (q_table_v1.pkl, q_table_v2.pkl, ...)
- Metadata file records training episodes, date, performance metrics for each version

## 5.4 PRICE ELASTICITY METHODOLOGY

### 5.4.1 Log-Log Regression Specification

**Econometric Model:**
```
log(quantity_i) = α + β·log(price_i) + γ₁·controls₁ᵢ + ... + εᵢ
```

Where:
- quantity_i: units sold in transaction i
- price_i: price charged in transaction i
- β: price elasticity of demand
- controls: confounding variables (day-of-week, month, promotions, trend)
- ε_i: error term

**Interpretation:**
β represents % change in quantity for 1% change in price. For example:
- β = -2.0: 1% price increase → 2% quantity decrease (elastic demand)
- β = -0.5: 1% price increase → 0.5% quantity decrease (inelastic demand)

Typically expect β < 0 (demand curves slope downward).

### 5.4.2 Implementation Using Statsmodels

```python
import statsmodels.api as sm
import numpy as np
import pandas as pd

def estimate_price_elasticity(product_id, min_observations=30):
    # 1. Retrieve sales history
    sales = get_sales_history(product_id, min_obs=min_observations)
    
    if len(sales) < min_observations:
        return None, None  # Insufficient data
    
    # 2. Prepare data
    df = pd.DataFrame(sales)
    df['log_quantity'] = np.log(df['quantity'] + 1)  # Add 1 to handle zeros
    df['log_price'] = np.log(df['price'])
    
    # 3. Add control variables
    df['day_of_week'] = pd.to_datetime(df['timestamp']).dt.dayofweek
    df['month'] = pd.to_datetime(df['timestamp']).dt.month
    df['trend'] = range(len(df))
    
    # One-hot encode categorical variables
    df = pd.get_dummies(df, columns=['day_of_week', 'month'], drop_first=True)
    
    # 4. Specify regression
    y = df['log_quantity']
    X = df[['log_price', 'trend'] + 
           [col for col in df.columns if col.startswith('day_of_week_') or 
            col.startswith('month_')]]
    X = sm.add_constant(X)  # Add intercept
    
    # 5. Fit OLS regression
    model = sm.OLS(y, X)
    results = model.fit()
    
    # 6. Extract elasticity coefficient
    elasticity = results.params['log_price']
    elasticity_se = results.bse['log_price']
    confidence_interval = (
        elasticity - 1.96 * elasticity_se,
        elasticity + 1.96 * elasticity_se
    )
    
    # 7. Validate
    if elasticity > 0:
        # Unexpected positive elasticity (demand increases with price?)
        # Likely data quality issue or confounding
        print(f"Warning: Positive elasticity {elasticity:.2f} for product {product_id}")
    
    return elasticity, confidence_interval, results
```

### 5.4.3 Handling Estimation Challenges

**Zero Quantities:**
Log transformation undefined for zero. Solutions:
- Add small constant: log(quantity + 1)
- Use Poisson or negative binomial regression (count data models)
- Filter out zero-sales observations if infrequent

**Multicollinearity:**
If price highly correlated with controls, coefficient estimates unstable. Check:
```python
from statsmodels.stats.outliers_influence import variance_inflation_factor

vif_data = pd.DataFrame()
vif_data["feature"] = X.columns
vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(len(X.columns))]
print(vif_data)

# VIF > 10 indicates problematic multicollinearity
```

**Endogeneity:**
Prices may be set in response to demand shocks (e.g., lowering price when demand is low). This creates bias. Full solution requires instrumental variables. Partial mitigation:
- Include rich set of controls
- Use lagged price: log(quantity_t) ~ log(price_{t-1}) reducing simultaneity
- Acknowledge limitation in interpretation

**Heteroskedasticity:**
Error variance may not be constant. Check:
```python
from statsmodels.stats.diagnostic import het_breuschpagan

bp_test = het_breuschpagan(results.resid, results.model.exog)
print(f"Breusch-Pagan test p-value: {bp_test[1]}")

# If p < 0.05, heteroskedasticity present
# Use robust standard errors
results_robust = model.fit(cov_type='HC3')
```

### 5.4.4 Using Elasticity for Pricing Optimization

**Revenue Maximization:**
```python
def revenue_optimal_price(base_price, elasticity, current_quantity):
    """
    Revenue = Price × Quantity = P × Q(P)
    If Q(P) = k × P^elasticity, then:
    Revenue-maximizing price occurs where elasticity = -1
    
    Adjustment factor = elasticity / (elasticity + 1)
    """
    if elasticity >= -1:
        # Inelastic demand: increase price
        return base_price * 1.10  # Increase by 10%
    else:
        # Elastic demand: decrease price may increase revenue
        # But be cautious: large price drops risky
        return base_price * 0.95  # Decrease by 5%
```

**Profit Maximization:**
```python
def profit_optimal_price(cost, base_price, elasticity):
    """
    Optimal markup: (P - MC) / P = -1 / elasticity
    Solving: P = MC / (1 + 1/elasticity)
    """
    if elasticity == 0:
        return base_price  # Edge case
    
    optimal_price = cost / (1 + 1/elasticity)
    
    # Bound within reasonable range
    optimal_price = max(cost * 1.10, optimal_price)  # At least 10% margin
    optimal_price = min(base_price * 2.0, optimal_price)  # At most 2× base price
    
    return optimal_price
```

**Integration with Dynamic Pricing Engine:**
Elasticity estimate used as one input to pricing synthesis:
```python
def elasticity_recommendation(product, elasticity):
    if elasticity is None or np.isnan(elasticity):
        return product.base_price  # No estimate available
    
    if elasticity > -0.5:
        # Very inelastic: price can be increased without losing much demand
        return min(product.max_price, product.current_price * 1.15)
    elif elasticity < -2.0:
        # Very elastic: price decreases may substantially increase volume
        return max(product.min_price, product.current_price * 0.90)
    else:
        # Moderate elasticity: small adjustments
        if elasticity < -1.0:
            return product.current_price * 0.95
        else:
            return product.current_price * 1.05
```

### 5.4.5 Periodic Re-estimation

Elasticity estimates should be updated regularly:

**Update Schedule:**
- Monthly full re-estimation using recent 90 days
- Triggered re-estimation if product undergoes major changes (repositioning, competitor entry)

**Monitoring Stability:**
```python
def monitor_elasticity_stability(product_id, window_days=30):
    elasticities = []
    
    # Estimate elasticity using rolling windows
    for start_day in range(0, 180, window_days):
        sales = get_sales_history(product_id, 
                                   start_date=today - start_day - window_days,
                                   end_date=today - start_day)
        elasticity, _ = estimate_price_elasticity_from_data(sales)
        elasticities.append((start_day, elasticity))
    
    # Check coefficient of variation
    elasticity_values = [e for _, e in elasticities if e is not None]
    if len(elasticity_values) > 1:
        cv = np.std(elasticity_values) / abs(np.mean(elasticity_values))
        if cv > 0.5:
            print(f"Warning: Elasticity unstable (CV={cv:.2f}) for product {product_id}")
    
    return elasticities
```

If elasticity estimates vary widely over time, suggests either:
- True change in market conditions (demand becoming more/less elastic)
- Poor estimation due to confounding or insufficient data
- Need for more sophisticated time-varying elasticity model

---

**END OF CHAPTER 5**

*Total Word Count: ~5,800 words*

This comprehensive Methodology chapter details the techniques, algorithms, data processing, training procedures, and implementation approaches for all major ML components of the dynamic pricing system.
