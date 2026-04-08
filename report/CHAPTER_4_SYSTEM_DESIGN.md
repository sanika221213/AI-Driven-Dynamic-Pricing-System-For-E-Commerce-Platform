# CHAPTER 4: SYSTEM DESIGN

---

## 4.1 ARCHITECTURE OVERVIEW

### 4.1.1 Architectural Style and Patterns

The AI-Driven Dynamic Pricing System employs a modern three-tier architecture separating concerns across presentation, application logic, and data persistence layers. This architectural pattern offers several critical advantages: clear separation of responsibilities enabling independent development and testing of each layer, scalability through horizontal replication of stateless application servers, and maintainability through modular organization.

**Presentation Tier (Frontend):**
- Web-based user interfaces implemented using HTML5, CSS3, and vanilla JavaScript
- Separate interfaces for different user roles: administrator dashboard, product management, analytics, customer shop
- Responsive design adapting to various screen sizes and devices
- Client-side interactivity using Chart.js for data visualizations
- Communicates with application tier exclusively through REST API

**Application Tier (Backend):**
- Python-based API server using Flask framework
- RESTful endpoints exposing system functionality
- Business logic implementation including pricing algorithms, data processing, validation
- Machine learning model hosting and inference
- Session management and authentication
- Integration point for external data sources

**Data Tier:**
- Relational database (SQLite for development/demonstration, PostgreSQL/MySQL for production scaling)
- Stores all persistent data: products, sales, prices, forecasts, users, configurations
- ACID transaction support ensuring data integrity
- Indexed for query performance
- Backup and recovery capabilities

### 4.1.2 Architectural Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         PRESENTATION TIER                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────┐ │
│  │  Admin       │  │  Products    │  │  Analytics   │  │  Shop  │ │
│  │  Dashboard   │  │  Management  │  │  & Reports   │  │        │ │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └────┬───┘ │
│         │                 │                  │               │      │
│         └─────────────────┴──────────────────┴───────────────┘      │
│                                    │                                 │
│                                HTTPS/REST API                        │
│                                    │                                 │
└────────────────────────────────────┼─────────────────────────────────┘
                                     │
┌────────────────────────────────────┼─────────────────────────────────┐
│                           APPLICATION TIER                           │
├────────────────────────────────────┴─────────────────────────────────┤
│                                                                       │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                     Flask API Server                          │  │
│  │  ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐    │  │
│  │  │   Product   │  │    Sales     │  │   Analytics      │    │  │
│  │  │   Routes    │  │    Routes    │  │   Routes         │    │  │
│  │  └─────────────┘  └──────────────┘  └──────────────────┘    │  │
│  │  ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐    │  │
│  │  │   Pricing   │  │     Auth     │  │   Competitor     │    │  │
│  │  │   Routes    │  │    Routes    │  │   Routes         │    │  │
│  │  └─────────────┘  └──────────────┘  └──────────────────┘    │  │
│  └──────────────────────────┬───────────────────────────────────┘  │
│                             │                                        │
│  ┌──────────────────────────┴───────────────────────────────────┐  │
│  │                   Business Logic Layer                        │  │
│  │  ┌──────────────────────────────────────────────────────┐    │  │
│  │  │            Dynamic Pricing Engine (Core)             │    │  │
│  │  │  • Integrates ML models and business rules            │    │  │
│  │  │  • Orchestrates pricing decision workflow             │    │  │
│  │  │  • Enforces constraints and safeguards                │    │  │
│  │  └─────────────┬────────────────────────────────────────┘    │  │
│  │                │                                               │  │
│  │    ┌───────────┴────────────┬──────────────────┬──────────┐  │  │
│  │    │                        │                  │          │  │  │
│  │  ┌─▼──────────────────┐  ┌─▼────────────┐  ┌─▼────────┐ │  │  │
│  │  │  LSTM Demand       │  │  RL Pricing  │  │  Price    │ │  │  │
│  │  │  Forecaster        │  │  Agent       │  │  Elasticity│ │  │  │
│  │  │  • Time series     │  │  • Q-Learning│  │  • Log-log │ │  │  │
│  │  │    forecasting     │  │  • ε-greedy  │  │    regr.   │ │  │  │
│  │  │  • LSTM neural net │  │  • Optimal   │  │  • Demand  │ │  │  │
│  │  │  • Multi-step pred │  │    policy    │  │    response│ │  │  │
│  │  └────────────────────┘  └──────────────┘  └───────────┘ │  │  │
│  └────────────────────────────────────────────────────────────┘  │  │
│                                                                      │
└──────────────────────────────────┬───────────────────────────────────┘
                                   │
┌──────────────────────────────────┼───────────────────────────────────┐
│                              DATA TIER                                │
├──────────────────────────────────┴───────────────────────────────────┤
│                                                                       │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                 Relational Database (SQLite/PostgreSQL)      │  │
│  │                                                               │  │
│  │  ┌─────────────┐  ┌──────────────┐  ┌───────────────────┐  │  │
│  │  │  Products   │  │ Sales History│  │  Price History    │  │  │
│  │  │  • id       │  │ • id         │  │  • id             │  │  │
│  │  │  • name     │  │ • product_id │  │  • product_id     │  │  │
│  │  │  • price    │  │ • quantity   │  │  • price          │  │  │
│  │  │  • cost     │  │ • price      │  │  • timestamp      │  │  │
│  │  │  • stock    │  │ • timestamp  │  │  • reason         │  │  │
│  │  └─────────────┘  └──────────────┘  └───────────────────┘  │  │
│  │                                                               │  │
│  │  ┌─────────────┐  ┌──────────────┐  ┌───────────────────┐  │  │
│  │  │   Users     │  │  Demand      │  │  Competitor       │  │  │
│  │  │  • id       │  │  Forecasts   │  │  Prices           │  │  │
│  │  │  • username │  │ • product_id │  │  • id             │  │  │
│  │  │  • password │  │ • forecast   │  │  • product_name   │  │  │
│  │  │  • role     │  │ • timestamp  │  │  • price          │  │  │
│  │  └─────────────┘  └──────────────┘  └───────────────────┘  │  │
│  │                                                               │  │
│  │  [Additional tables: shopping_cart, product_searches,        │  │
│  │   product_views, active_sessions, system_settings,           │  │
│  │   performance_metrics]                                        │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
```

### 4.1.3 Component Interaction Flow

**Price Optimization Flow:**

1. Administrator requests price optimization (or scheduled job triggers)
2. API endpoint receives request, validates authentication/authorization
3. Dynamic Pricing Engine initiated for specified products
4. Engine queries database for product data, sales history, inventory, competitor prices
5. LSTM Forecaster generates demand predictions for forecast horizon
6. RL Agent evaluates Q-values for different price actions given current state
7. Price Elasticity Calculator estimates demand-price relationship
8. Engine synthesizes recommendations, applying business rules and constraints
9. Optimized prices validated against bounds, rate limits
10. Approved prices written to database, price history recorded
11. Response returned to client with optimization results
12. Frontend updates to display new prices

**Customer Purchase Flow:**

1. Customer browses shop interface, views products
2. Frontend requests product catalog via API
3. API queries database for active products with current prices
4. Product data with prices returned and displayed
5. Customer adds items to cart
6. Cart stored in session/database
7. Customer proceeds to checkout
8. Purchase transaction processed via API
9. Sale record created in database
10. Inventory decremented
11. RL Agent observes transaction outcome (price, quantity sold)
12. Q-values updated based on observed reward
13. Confirmation returned to customer

**Forecasting Flow:**

1. Scheduled job triggers forecast generation
2. LSTM Forecaster retrieves historical sales data from database
3. Data preprocessed: normalization, feature engineering
4. Model performs forward pass generating predictions
5. Forecasts with confidence intervals stored in database
6. Forecast metrics (MAE, MAPE) calculated and logged
7. Anomalies or poor performance trigger alerts

### 4.1.4 Design Principles Applied

**Separation of Concerns:**
Each component has well-defined responsibility. LSTM handles forecasting, RL handles sequential decision-making, elasticity handles price-response quantification, Dynamic Pricing Engine orchestrates integration. This separation allows independent development, testing, and potential replacement of components.

**Modularity:**
System is decomposed into loosely coupled, highly cohesive modules. Changes to one module (e.g., swapping LSTM for different forecasting method) don't cascade through entire system.

**Scalability:**
Stateless API design enables horizontal scaling—multiple API server instances can serve requests independently. Database can be replicated/sharded for read scalability.

**Extensibility:**
Architecture accommodates future enhancements. New ML models can be added alongside existing ones. Additional data sources can be integrated. New API endpoints extend functionality without modifying existing endpoints.

**Resilience:**
Graceful degradation ensures partial failures don't crash entire system. If LSTM forecasting fails, system can fallback to simpler methods. If RL agent hasn't learned yet, system uses elasticity-based optimization.

**Security:**
Authentication and authorization implemented at API layer. Sensitive operations require authentication. SQL injection prevented through parameterized queries. Input validation prevents malformed data.

**Observability:**
Comprehensive logging records significant events, errors, and decisions. Performance metrics tracked. Monitoring enables proactive issue detection.

## 4.2 DATABASE DESIGN

### 4.2.1 Entity-Relationship Model

The database schema implements a normalized relational design (Third Normal Form) minimizing redundancy while maintaining query performance through strategic indexing.

**Core Entities:**

1. **Products:** Represents items available for sale
2. **Sales_History:** Records each sale transaction
3. **Price_History:** Tracks all price changes with rationale
4. **Demand_Forecasts:** Stores forecast predictions
5. **Users:** System users with authentication credentials
6. **Shopping_Cart:** Temporary storage of customer shopping sessions
7. **Competitor_Prices:** Tracks competitor pricing data
8. **Product_Searches:** Logs customer search queries
9. **Product_Views:** Records product page views for engagement tracking
10. **Active_Sessions:** Manages user session state
11. **System_Settings:** Configuration parameters
12. **Performance_Metrics:** System health and performance data

### 4.2.2 Detailed Table Specifications

**Products Table:**
```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    category VARCHAR(100),
    base_price DECIMAL(10,2) NOT NULL,
    current_price DECIMAL(10,2) NOT NULL,
    cost DECIMAL(10,2) NOT NULL,
    stock_quantity INTEGER DEFAULT 0,
    min_price DECIMAL(10,2),
    max_price DECIMAL(10,2),
    max_price_change_rate DECIMAL(5,2) DEFAULT 0.20,
    image_url VARCHAR(500),
    status VARCHAR(20) DEFAULT 'active',
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_price_positive CHECK (current_price >= 0),
    CONSTRAINT chk_cost_positive CHECK (cost >= 0),
    CONSTRAINT chk_stock_nonnegative CHECK (stock_quantity >= 0),
    CONSTRAINT chk_price_bounds CHECK (min_price IS NULL OR max_price IS NULL 
                                        OR min_price <= max_price)
);

CREATE INDEX idx_products_category ON products(category);
CREATE INDEX idx_products_status ON products(status);
CREATE INDEX idx_products_price ON products(current_price);
```

**Rationale:**
- `id` as surrogate key for efficient joins and foreign key references
- `base_price` and `current_price` separated—base provides reference point, current reflects dynamic pricing
- `cost` enables profit margin calculations
- `min_price` and `max_price` enforce product-specific pricing boundaries
- `max_price_change_rate` limits volatility (e.g., 0.20 = max 20% change per update)
- `status` supports product lifecycle (active, discontinued, out-of-stock)
- Constraints ensure data integrity
- Indexes accelerate common queries (filtering by category, status, price range)

**Sales_History Table:**
```sql
CREATE TABLE sales_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    revenue DECIMAL(10,2) NOT NULL,
    cost DECIMAL(10,2),
    profit DECIMAL(10,2),
    customer_id INTEGER,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    session_id VARCHAR(100),
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (customer_id) REFERENCES users(id),
    CONSTRAINT chk_quantity_positive CHECK (quantity > 0),
    CONSTRAINT chk_sale_price_positive CHECK (price >= 0)
);

CREATE INDEX idx_sales_product ON sales_history(product_id);
CREATE INDEX idx_sales_timestamp ON sales_history(timestamp DESC);
CREATE INDEX idx_sales_customer ON sales_history(customer_id);
```

**Rationale:**
- Each row represents single sale transaction
- `product_id` foreign key links to products table
- `price` captures actual price charged (historical snapshot even if product price later changes)
- `revenue`, `cost`, `profit` denormalized for query performance (could be computed but frequently accessed)
- `timestamp` enables time-series analysis
- Indexes accelerate product-specific queries, time-based queries, customer purchase history

**Price_History Table:**
```sql
CREATE TABLE price_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    old_price DECIMAL(10,2),
    new_price DECIMAL(10,2) NOT NULL,
    price_change_pct DECIMAL(5,2),
    reason VARCHAR(500),
    changed_by VARCHAR(100),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id)
);

CREATE INDEX idx_price_history_product ON price_history(product_id);
CREATE INDEX idx_price_history_timestamp ON price_history(timestamp DESC);
```

**Rationale:**
- Complete audit trail of all price changes
- `reason` provides explainability (e.g., "RL optimization: high demand forecast, low inventory")
- `changed_by` tracks whether change was algorithmic or manual override
- Supports analysis of pricing strategy effectiveness over time

**Demand_Forecasts Table:**
```sql
CREATE TABLE demand_forecasts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    forecast_date DATE NOT NULL,
    forecast_quantity DECIMAL(10,2) NOT NULL,
    confidence_lower DECIMAL(10,2),
    confidence_upper DECIMAL(10,2),
    model_version VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id),
    UNIQUE(product_id, forecast_date)
);

CREATE INDEX idx_forecasts_product ON demand_forecasts(product_id);
CREATE INDEX idx_forecasts_date ON demand_forecasts(forecast_date);
```

**Rationale:**
- Stores multi-step-ahead forecasts (one row per product per forecast date)
- `forecast_quantity` is point estimate
- `confidence_lower` and `confidence_upper` capture uncertainty
- `model_version` tracks which model generated forecast (useful if multiple models compared)
- UNIQUE constraint prevents duplicate forecasts for same product-date
- Indexes support querying forecasts for specific products and date ranges

**Users Table:**
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(200),
    role VARCHAR(50) DEFAULT 'customer',
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_role ON users(role);
```

**Rationale:**
- Supports both customer accounts and administrative users
- `password_hash` stores securely hashed passwords (never plaintext)
- `role` enables role-based access control (customer, admin, pricing_manager, analyst)
- `is_active` allows account disabling without deletion
- `last_login` tracks activity for security monitoring

**Shopping_Cart Table:**
```sql
CREATE TABLE shopping_cart (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id VARCHAR(100) NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    price_at_add DECIMAL(10,2) NOT NULL,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id),
    CONSTRAINT chk_cart_quantity_positive CHECK (quantity > 0)
);

CREATE INDEX idx_cart_session ON shopping_cart(session_id);
CREATE INDEX idx_cart_product ON shopping_cart(product_id);
```

**Rationale:**
- Supports customer shopping sessions
- `session_id` links cart items for same customer session
- `price_at_add` locks price when item added (preventing price changes during checkout from causing confusion)
- Temporary data—can be periodically purged for abandoned carts

**Competitor_Prices Table:**
```sql
CREATE TABLE competitor_prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    competitor_name VARCHAR(200) NOT NULL,
    product_name VARCHAR(200) NOT NULL,
    product_url VARCHAR(500),
    price DECIMAL(10,2) NOT NULL,
    currency VARCHAR(10) DEFAULT 'USD',
    last_checked TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    mapped_product_id INTEGER,
    FOREIGN KEY (mapped_product_id) REFERENCES products(id)
);

CREATE INDEX idx_competitor_name ON competitor_prices(competitor_name);
CREATE INDEX idx_competitor_product ON competitor_prices(mapped_product_id);
CREATE INDEX idx_competitor_timestamp ON competitor_prices(last_checked DESC);
```

**Rationale:**
- Tracks competitor pricing data
- `mapped_product_id` links competitor products to our products for direct comparison
- `last_checked` enables freshness filtering
- Supports competitive positioning analysis

**System_Settings Table:**
```sql
CREATE TABLE system_settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    setting_key VARCHAR(100) UNIQUE NOT NULL,
    setting_value TEXT,
    data_type VARCHAR(20),
    description TEXT,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(100)
);

CREATE INDEX idx_settings_key ON system_settings(setting_key);
```

**Rationale:**
- Flexible key-value store for configuration parameters
- `data_type` indicates how to parse `setting_value` (string, integer, float, boolean, json)
- Examples: `default_min_price_multiplier`, `rl_epsilon`, `forecast_update_frequency`, `pricing_objective`
- Enables configuration changes without code deployment

### 4.2.3 Relationships and Cardinality

- **Products ↔ Sales_History:** One-to-Many (one product has many sales records)
- **Products ↔ Price_History:** One-to-Many (one product has many price change records)
- **Products ↔ Demand_Forecasts:** One-to-Many (one product has many forecasts)
- **Products ↔ Shopping_Cart:** One-to-Many (one product can be in many carts)
- **Products ↔ Competitor_Prices:** One-to-Many (our product mapped to multiple competitor listings)
- **Users ↔ Sales_History:** One-to-Many (one customer has many purchases)

### 4.2.4 Normalization and Data Integrity

**Third Normal Form (3NF) Compliance:**
- All tables have atomic attributes (no repeating groups)
- All non-key attributes fully dependent on primary key (no partial dependencies)
- No transitive dependencies (non-key attributes don't depend on other non-key attributes)

**Examples of Normalization:**
- Revenue, cost, profit in sales_history could theoretically be computed (price × quantity, cost × quantity, revenue - cost) but are stored for performance (denormalization for read optimization)
- Product category could be normalized to separate categories table with foreign key, but current design trades purity for simplicity given limited categories
- Future enhancement: Create separate tables for categories with attributes (category_id, category_name, parent_category) enabling hierarchical categories

**Constraints Ensuring Integrity:**
- PRIMARY KEY constraints ensure unique identifiers
- FOREIGN KEY constraints maintain referential integrity
- CHECK constraints enforce business rules (positive prices, valid bounds)
- UNIQUE constraints prevent duplicates where inappropriate
- NOT NULL constraints require essential data
- DEFAULT values provide sensible initial states

### 4.2.5 Indexing Strategy

Indexes dramatically improve query performance but have costs:
- Storage space overhead
- Insert/update performance degradation (indexes must be maintained)

**Indexing Decisions:**

*Indexed:*
- Foreign keys (accelerate joins)
- Columns frequently in WHERE clauses (category, status, timestamps)
- Columns in ORDER BY or GROUP BY operations
- Unique constraints (usernames)

*Not Indexed:*
- Low-cardinality columns rarely queried alone (boolean flags)
- Columns rarely in predicates
- Very small tables where full scan is fast enough

**Composite Indexes:**
Future optimization might add composite indexes for common query patterns:
```sql
CREATE INDEX idx_sales_product_time ON sales_history(product_id, timestamp DESC);
```
This accelerates queries like "recent sales for product X" without needing separate indexes.

### 4.2.6 Database Migration Strategy

**Development:** SQLite offers simplicity for single-user development and demonstration

**Production:** PostgreSQL or MySQL recommended for production deployment providing:
- Better concurrency control
- Advanced indexing options (partial indexes, expression indexes)
- Horizontal read scaling (replication)
- Backup and recovery tools
- Connection pooling

**Migration Path:**
1. Export data from SQLite using SQL dumps or pandas
2. Transform schema SQL for PostgreSQL/MySQL syntax compatibility
3. Import data into target database
4. Update application connection strings
5. Validate data integrity and application functionality
6. Performance testing and index optimization

## 4.3 MACHINE LEARNING COMPONENT DESIGN

### 4.3.1 LSTM Demand Forecaster Architecture

**Purpose:** Predict future demand (sales quantity) for products based on historical patterns.

**Input:** Time series of historical sales quantities plus external features (day-of-week, month, promotions, holidays)

**Output:** Multi-step-ahead forecast (7-day forecast horizon) with confidence intervals

**Architecture:**
```
Input Layer (Sequence Length × Features)
    ↓
LSTM Layer 1 (64 units, return sequences=True)
    ↓
Dropout Layer (0.2 dropout rate)
    ↓
LSTM Layer 2 (32 units, return sequences=False)
    ↓
Dropout Layer (0.2 dropout rate)
    ↓
Dense Layer (16 units, ReLU activation)
    ↓
Output Layer (7 units, linear activation) — 7-day forecast
```

**Design Rationale:**

- **Two LSTM layers:** First layer (64 units) extracts hierarchical temporal features. Second layer (32 units) refines representations. Stacking enables learning complex patterns.

- **Return sequences:** First LSTM returns full sequence (enabling second LSTM to process), final LSTM returns only final state (condensing sequence into fixed representation)

- **Dropout:** 20% dropout after each LSTM prevents overfitting by randomly deactivating neurons during training

- **Dense layer:** Provides non-linear transformation before output

- **Output size 7:** Direct multi-step forecasting (one output per forecast day)

**Hyperparameters:**
- Sequence length (lookback window): 30 days
- Batch size: 32
- Epochs: 100 with early stopping (patience=10)
- Optimizer: Adam with learning rate 0.001
- Loss function: Mean Squared Error (MSE)

**Training Process:**
1. Retrieve historical sales data from database (minimum 90 days required)
2. Create sliding windows: for each time point, look back 30 days to predict next 7 days
3. Normalize quantities using Min-Max scaling (preserving scale parameters)
4. Add engineered features (day-of-week one-hot, month, trend)
5. Split data: 80% training, 20% validation
6. Train model with early stopping monitoring validation loss
7. Save best model (lowest validation loss) to disk
8. Evaluate on validation set, compute MAE/MAPE/RMSE

**Inference Process:**
1. Load trained model from disk
2. Retrieve recent 30 days of sales data
3. Preprocess and normalize using saved scaling parameters
4. Model forward pass generates 7-day forecast
5. Denormalize predictions to original scale
6. Compute confidence intervals (empirical: forecast ± 1.96 × validation MAE)
7. Store forecasts in database

**Cold Start Handling:**
For new products with insufficient history, fallback methods:
- If <7 days data: Use category average
- If 7-30 days data: Use exponential smoothing
- If >30 days: LSTM forecasting

### 4.3.2 Reinforcement Learning Pricing Agent Design

**Purpose:** Learn optimal pricing policy maximizing long-term cumulative reward (revenue or profit).

**Approach:** Q-Learning with ε-greedy exploration

**State Space Representation:**
Each state is discrete tuple: `(demand_level, inventory_level, competitor_position, seasonality, trend)`

- **demand_level:** Categorized as 'low', 'medium', 'high' based on recent sales relative to historical average
- **inventory_level:** 'low' (<20% of max), 'medium' (20-80%), 'high' (>80%)
- **competitor_position:** 'below' (our price <95% of competitor avg), 'match' (95-105%), 'above' (>105%)
- **seasonality:** 'off-season', 'normal', 'peak-season' based on month
- **trend:** 'declining', 'stable', 'growing' based on recent sales trend

Total states: 3 × 3 × 3 × 3 × 3 = 243 discrete states

**Action Space:**
Price multipliers applied to base price: [0.85, 0.90, 0.95, 1.00, 1.05, 1.10, 1.15, 1.20]

Total actions: 8 discrete actions

**Q-Function:**
Q-table: 243 states × 8 actions = 1,944 (state, action) pairs
Stored as dictionary: Q[(state, action)] = expected cumulative reward

**Reward Function:**
`reward = revenue` or `reward = profit` depending on configuration

Where:
- revenue = price × quantity_sold
- profit = (price - cost) × quantity_sold

**Learning Algorithm (Q-Learning):**
```
Initialize Q(s, a) = 0 for all states s and actions a
For each transaction:
    1. Observe current state s
    2. Choose action a using ε-greedy:
       - With probability ε: random action (exploration)
       - With probability 1-ε: action with max Q(s, a) (exploitation)
    3. Apply action (set price = base_price × multiplier)
    4. Observe quantity sold, compute reward r
    5. Observe next state s'
    6. Update Q-value:
       Q(s, a) ← Q(s, a) + α [r + γ max_a' Q(s', a') - Q(s, a)]
    7. Decay ε if configured (reduce exploration over time)
```

**Hyperparameters:**
- Learning rate α: 0.10 (controls how much new information overrides old)
- Discount factor γ: 0.95 (balances immediate vs. future rewards)
- Initial ε: 0.30 (30% exploration initially)
- ε decay: 0.995 per episode (gradually reduce exploration)
- Min ε: 0.05 (maintain 5% minimum exploration)

**Design Rationale:**

- **Discrete states/actions:** Simplifies implementation and reduces sample complexity compared to continuous spaces. Function approximation (deep RL) deferred to future work.

- **ε-greedy:** Simple but effective exploration strategy. Alternatives (Thompson Sampling, UCB) could be tested.

- **Q-Learning:** Off-policy algorithm can learn from suboptimal exploration data. Converges to optimal policy under sufficient exploration.

- **Reward = revenue or profit:** Configurable based on business objective. Could be extended to incorporate inventory costs.

### 4.3.3 Price Elasticity Calculator Design

**Purpose:** Estimate how demand responds to price changes, quantified as elasticity coefficient.

**Approach:** Log-log linear regression

**Model:**
```
log(quantity) = α + β log(price) + ∑ γ_i control_i + ε
```

Where:
- β is price elasticity coefficient (percent change in quantity per 1% change in price)
- control_i are confounding variables (day-of-week, month, promotions, trend)

**Estimation Process:**
1. Retrieve sales history (minimum 30 observations required)
2. Extract quantity, price, and control variables
3. Take logarithms: log_qty = log(quantity), log_price = log(price)
4. Fit ordinary least squares regression: log_qty ~ log_price + controls
5. Extract coefficient β and standard error
6. Compute confidence interval: β ± 1.96 × SE(β)
7. Validate: check if elasticity is negative (demand decreases as price increases)

**Usage in Pricing:**
Elasticity enables revenue and profit optimization:

**Revenue = Price × Quantity = P × Q(P)**

Revenue maximization:
- If |elasticity| > 1 (elastic demand): lowering price increases revenue (quantity increase outweighs price decrease)
- If |elasticity| < 1 (inelastic demand): raising price increases revenue (quantity decrease is proportionally smaller than price increase)
- Revenue-maximizing price occurs where elasticity = -1

**Profit = (Price - Cost) × Quantity**

Profit maximization depends on margin and elasticity. Lerner index:
```
(P - MC) / P = -1 / elasticity
```
Optimal markup depends on demand elasticity—more elastic demand requires lower markups.

**Design Rationale:**

- **Log-log specification:** Constant elasticity assumption simplifies computation and interpretation. More flexible specifications (splines, non-parametric) deferred to future work.

- **Control variables:** Including confounders (seasonality, trends) reduces omitted variable bias in elasticity estimate.

- **Limitations acknowledged:** Endogeneity (price may be set in response to demand shocks) causes bias. Instrumental variables or randomized experiments would provide cleaner identification but require more sophisticated setup.

### 4.3.4 Dynamic Pricing Engine Integration Logic

**Purpose:** Orchestrate multiple ML components and business rules to determine final price recommendations.

**Integration Workflow:**

```
1. INPUT: Product ID, current context
2. Retrieve product data from database
3. Check if manual override active → if yes, use override price and STOP
4. Generate demand forecast (call LSTM Forecaster)
5. Estimate current state representation for RL agent
6. Query RL agent for recommended price multiplier
7. Calculate price elasticity (call Elasticity Calculator)
8. Compute elasticity-based optimal price
9. SYNTHESIS:
   a. RL recommendation: base_price × rl_multiplier
   b. Elasticity recommendation: elasticity-optimal price
   c. Weighted combination: 
      recommended_price = w1 × rl_price + w2 × elasticity_price + w3 × baseline_price
      (default weights: w1=0.5, w2=0.3, w3=0.2)
10. Apply business rules:
    a. Enforce min_price ≤ recommended_price ≤ max_price
    b. Check rate-of-change limit: 
       |recommended_price - current_price| / current_price ≤ max_change_rate
       If violated, cap change at maximum allowed
    c. Adjust for inventory:
       - If inventory < 10% of target: increase price by 5-10%
       - If inventory > 90% of target: decrease price by 5-10%
    d. Consider competitor prices:
       - If recommended_price > 1.2 × min_competitor_price: flag for review
11. OUTPUT: Final optimized price with explanation
12. Log decision rationale in price_history
13. Update product current_price in database
```

**Weighting Rationale:**
- RL gets highest weight (0.5) as it learns from actual outcomes
- Elasticity provides economic grounding (0.3)
- Baseline maintains stability and anchoring (0.2)
- Weights configurable via system_settings

**Business Rules Justification:**
- **Price bounds:** Prevent obviously wrong prices (too low hurts profit, too high hurts sales)
- **Rate limits:** Avoid customer confusion and price volatility
- **Inventory adjustment:** Balances supply and demand, accelerates clearance or moderates demand for scarce items
- **Competitor consideration:** Maintains competitive positioning

---

**END OF CHAPTER 4 (Part 1)**

*Current Word Count: ~6,800 words*

*Chapter 4 continues with sections on API Design, User Interface Design, and Security Design...*
