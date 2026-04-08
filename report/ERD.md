# ENTITY RELATIONSHIP DIAGRAM (ERD)
## AI-Driven Dynamic Pricing System

---

## Database Schema Visualization

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         DATABASE SCHEMA - ERD                                │
└─────────────────────────────────────────────────────────────────────────────┘


╔═══════════════════════════════════════╗
║            USERS                       ║
╠═══════════════════════════════════════╣
║ PK  user_id          INTEGER          ║
║     username         TEXT (UNIQUE)    ║
║     email            TEXT (UNIQUE)    ║
║     password         TEXT             ║
║     full_name        TEXT             ║
║     is_admin         BOOLEAN          ║
║     created_at       TIMESTAMP        ║
╚═══════════════════════════════════════╝
          │
          │ 1
          │
          │ *
          ▼
┌───────────────────────────────────────┐         ┌───────────────────────────────────────┐
│       SHOPPING_CART                   │         │          PRODUCT_SEARCHES              │
├───────────────────────────────────────┤         ├───────────────────────────────────────┤
│ PK  cart_id          INTEGER         │         │ PK  search_id        INTEGER          │
│ FK  user_id          INTEGER         │────┐    │ FK  user_id          INTEGER          │
│ FK  product_id       INTEGER         │    │    │ FK  product_id       INTEGER          │
│     quantity         INTEGER         │    └────│     search_query     TEXT             │
│     price_at_add     REAL            │         │     searched_at      TIMESTAMP        │
│     added_at         TIMESTAMP       │         └───────────────────────────────────────┘
└───────────────────────────────────────┘
          │                                       ┌───────────────────────────────────────┐
          │                                       │         PRODUCT_VIEWS                  │
          │                                       ├───────────────────────────────────────┤
          │                                       │ PK  view_id          INTEGER          │
          │                                       │ FK  user_id          INTEGER          │
          │                                       │ FK  product_id       INTEGER          │
          │                                       │     viewed_at        TIMESTAMP        │
          ▼                                       └───────────────────────────────────────┘
╔═══════════════════════════════════════╗                   │
║            PRODUCTS                    ║                   │
╠═══════════════════════════════════════╣                   │
║ PK  product_id       INTEGER          ║◄──────────────────┘
║     name             TEXT             ║
║     category         TEXT             ║◄──────────────────┐
║     base_price       REAL             ║                   │
║     cost_price       REAL             ║                   │
║     current_price    REAL             ║                   │
║     inventory        INTEGER          ║                   │
║     min_price        REAL             ║                   │
║     max_price        REAL             ║                   │
║     description      TEXT             ║                   │
║     demand_score     REAL             ║                   │
║     search_count     INTEGER          ║                   │
║     view_count       INTEGER          ║                   │
║     created_at       TIMESTAMP        ║                   │
║     updated_at       TIMESTAMP        ║                   │
╚═══════════════════════════════════════╝                   │
          │                                                  │
          │ 1                                                │
          │                                                  │
          │ *                                                │
          ├──────────────────────────────────┐              │
          │                                  │              │
          ▼                                  ▼              │
┌───────────────────────────────────────┐  ┌───────────────────────────────────────┐
│       SALES_HISTORY                   │  │         PRICE_HISTORY                  │
├───────────────────────────────────────┤  ├───────────────────────────────────────┤
│ PK  sale_id          INTEGER         │  │ PK  price_id         INTEGER          │
│ FK  product_id       INTEGER         │  │ FK  product_id       INTEGER          │
│     quantity_sold    INTEGER         │  │     old_price        REAL             │
│     price            REAL            │  │     new_price        REAL             │
│     revenue          REAL            │  │     reason           TEXT             │
│     sale_date        TIMESTAMP       │  │     changed_at       TIMESTAMP        │
└───────────────────────────────────────┘  └───────────────────────────────────────┘
          │                                                  │
          │                                                  │
          ▼                                                  ▼
┌───────────────────────────────────────┐  ┌───────────────────────────────────────┐
│      COMPETITOR_PRICES                │  │        DEMAND_FORECASTS                │
├───────────────────────────────────────┤  ├───────────────────────────────────────┤
│ PK  comp_id          INTEGER         │  │ PK  forecast_id      INTEGER          │
│ FK  product_id       INTEGER         │  │ FK  product_id       INTEGER          │
│     competitor_name  TEXT            │  │     forecast_date    DATE             │
│     competitor_price REAL            │  │     predicted_demand REAL             │
│     competitor_url   TEXT            │  │     confidence_lower REAL             │
│     updated_at       TIMESTAMP       │  │     confidence_upper REAL             │
└───────────────────────────────────────┘  │     created_at       TIMESTAMP        │
                                            │     actual_demand    REAL             │
                                            └───────────────────────────────────────┘

┌───────────────────────────────────────┐
│       ACTIVE_SESSIONS                 │
├───────────────────────────────────────┤
│ PK  session_id       INTEGER         │
│ FK  user_id          INTEGER         │──────┐
│ FK  product_id       INTEGER         │      │
│     action_type      TEXT            │      │
│     started_at       TIMESTAMP       │      │
│     ended_at         TIMESTAMP       │      │
└───────────────────────────────────────┘      │
                                               │
                                               ▼
╔═══════════════════════════════════════╗
║        SYSTEM_SETTINGS                 ║
╠═══════════════════════════════════════╣
║ PK  setting_id       INTEGER          ║
║     setting_name     TEXT (UNIQUE)    ║
║     setting_value    TEXT             ║
║     data_type        TEXT             ║
║     updated_at       TIMESTAMP        ║
╚═══════════════════════════════════════╝


╔═══════════════════════════════════════╗
║      PERFORMANCE_METRICS               ║
╠═══════════════════════════════════════╣
║ PK  metric_id        INTEGER          ║
║     metric_name      TEXT             ║
║     metric_value     REAL             ║
║     metric_category  TEXT             ║
║     recorded_at      TIMESTAMP        ║
╚═══════════════════════════════════════╝


═══════════════════════════════════════════════════════════════════════════
                         LEGEND
═══════════════════════════════════════════════════════════════════════════

PK  = Primary Key
FK  = Foreign Key
1   = One (Relationship Cardinality)
*   = Many (Relationship Cardinality)
║   = Double line box indicates Primary/Core entity
│   = Single line box indicates Secondary/Supporting entity
─── = Relationship line
```

---

## DETAILED RELATIONSHIPS

### 1. USERS ──< SHOPPING_CART
- **Type:** One-to-Many
- **Description:** One user can have multiple items in shopping cart
- **Foreign Key:** shopping_cart.user_id → users.user_id
- **Cascade:** ON DELETE CASCADE (deleting user removes cart items)

### 2. USERS ──< PRODUCT_SEARCHES
- **Type:** One-to-Many
- **Description:** One user can perform multiple product searches
- **Foreign Key:** product_searches.user_id → users.user_id
- **Cascade:** ON DELETE SET NULL (searches remain for analytics even if user deleted)

### 3. USERS ──< PRODUCT_VIEWS
- **Type:** One-to-Many
- **Description:** One user can view multiple products
- **Foreign Key:** product_views.user_id → users.user_id
- **Cascade:** ON DELETE SET NULL (views remain for analytics)

### 4. USERS ──< ACTIVE_SESSIONS
- **Type:** One-to-Many
- **Description:** One user can have multiple sessions
- **Foreign Key:** active_sessions.user_id → users.user_id
- **Cascade:** ON DELETE CASCADE (user deletion removes sessions)

### 5. PRODUCTS ──< SHOPPING_CART
- **Type:** One-to-Many
- **Description:** One product can appear in multiple shopping carts
- **Foreign Key:** shopping_cart.product_id → products.product_id
- **Cascade:** ON DELETE CASCADE (deleting product removes from carts)

### 6. PRODUCTS ──< SALES_HISTORY
- **Type:** One-to-Many
- **Description:** One product can have multiple sales transactions
- **Foreign Key:** sales_history.product_id → products.product_id
- **Cascade:** ON DELETE RESTRICT (cannot delete product with sales history)

### 7. PRODUCTS ──< PRICE_HISTORY
- **Type:** One-to-Many
- **Description:** One product can have multiple price changes
- **Foreign Key:** price_history.product_id → products.product_id
- **Cascade:** ON DELETE CASCADE (price history deleted with product)

### 8. PRODUCTS ──< COMPETITOR_PRICES
- **Type:** One-to-Many
- **Description:** One product can have prices from multiple competitors
- **Foreign Key:** competitor_prices.product_id → products.product_id
- **Cascade:** ON DELETE CASCADE (competitor data removed with product)

### 9. PRODUCTS ──< DEMAND_FORECASTS
- **Type:** One-to-Many
- **Description:** One product can have multiple demand forecasts
- **Foreign Key:** demand_forecasts.product_id → products.product_id
- **Cascade:** ON DELETE CASCADE (forecasts removed with product)

### 10. PRODUCTS ──< PRODUCT_SEARCHES
- **Type:** One-to-Many
- **Description:** One product can be searched multiple times
- **Foreign Key:** product_searches.product_id → products.product_id
- **Cascade:** ON DELETE CASCADE (searches removed with product)

### 11. PRODUCTS ──< PRODUCT_VIEWS
- **Type:** One-to-Many
- **Description:** One product can be viewed multiple times
- **Foreign Key:** product_views.product_id → products.product_id
- **Cascade:** ON DELETE CASCADE (views removed with product)

### 12. PRODUCTS ──< ACTIVE_SESSIONS
- **Type:** One-to-Many
- **Description:** One product can appear in multiple active sessions
- **Foreign Key:** active_sessions.product_id → products.product_id
- **Cascade:** ON DELETE CASCADE (sessions removed with product)

---

## ENTITY DESCRIPTIONS

### Core Entities

**USERS**
- Stores user account information for authentication and authorization
- Supports both customer and administrator roles via is_admin flag
- All user activity (cart, searches, views) linked via user_id

**PRODUCTS**
- Central entity containing all product master data
- Maintains both base_price (reference) and current_price (dynamic)
- Tracks engagement metrics (search_count, view_count, demand_score)
- Most tables have foreign key relationships to products

### Transaction Entities

**SALES_HISTORY**
- Records completed purchase transactions
- Critical for training ML models and calculating revenue
- Immutable audit trail (no updates, only inserts)

**SHOPPING_CART**
- Temporary storage for products selected but not purchased
- Captures price_at_add for price consistency during checkout
- Provides data on cart abandonment behavior

### Analytics Entities

**PRICE_HISTORY**
- Audit trail of all price changes
- Includes reason for change (algorithm, manual, competitor)
- Enables analysis of pricing strategy effectiveness

**COMPETITOR_PRICES**
- Tracks competitor pricing for market positioning
- Supports competitive pricing strategies
- Updated periodically via manual entry or API integration

**DEMAND_FORECASTS**
- Stores LSTM model predictions
- Includes confidence intervals for uncertainty quantification
- actual_demand filled after forecast_date for accuracy evaluation

**PRODUCT_SEARCHES**
- Captures product search behavior
- Early demand signal (searches precede purchases)
- Enables search trend analysis

**PRODUCT_VIEWS**
- Tracks product detail page views
- Indicates later-stage purchase interest
- Supports engagement analytics

**ACTIVE_SESSIONS**
- Real-time tracking of concurrent user activity
- Enables congestion-aware pricing
- Sessions marked ended_at when complete

### System Entities

**SYSTEM_SETTINGS**
- Configurable parameters for system operation
- Enables runtime configuration changes without code deployment
- Includes ML hyperparameters, pricing bounds, update frequencies

**PERFORMANCE_METRICS**
- Time-series data on system performance
- Supports dashboards and trend analysis
- Categories include revenue, accuracy, sales, efficiency

---

## NORMALIZATION ANALYSIS

**Normal Form:** The schema achieves Third Normal Form (3NF)

**1NF (First Normal Form):**
✓ All attributes contain atomic values
✓ No repeating groups or arrays
✓ Each table has a primary key

**2NF (Second Normal Form):**
✓ All non-key attributes fully dependent on primary key
✓ No partial dependencies (all PKs are single columns)

**3NF (Third Normal Form):**
✓ No transitive dependencies
✓ Example: revenue in sales_history is stored denormalized for query performance (acceptable trade-off as it's derived from price × quantity)

**Denormalization Decisions:**
- revenue stored in sales_history (can be calculated from price × quantity) for query performance
- demand_score, search_count, view_count stored in products (can be calculated from related tables) for dashboard performance
- These calculated fields are updated via triggers or application logic

---

## INDEXES

**Primary Indexes (Automatic):**
- All primary keys automatically indexed

**Foreign Key Indexes (Recommended):**
```sql
CREATE INDEX idx_shopping_cart_user ON shopping_cart(user_id);
CREATE INDEX idx_shopping_cart_product ON shopping_cart(product_id);
CREATE INDEX idx_sales_history_product ON sales_history(product_id);
CREATE INDEX idx_sales_history_date ON sales_history(sale_date);
CREATE INDEX idx_price_history_product ON price_history(product_id);
CREATE INDEX idx_competitor_prices_product ON competitor_prices(product_id);
CREATE INDEX idx_demand_forecasts_product ON demand_forecasts(product_id);
CREATE INDEX idx_product_searches_product ON product_searches(product_id);
CREATE INDEX idx_product_views_product ON product_views(product_id);
```

**Composite Indexes (Performance Optimization):**
```sql
CREATE INDEX idx_sales_product_date ON sales_history(product_id, sale_date);
CREATE INDEX idx_price_product_changed ON price_history(product_id, changed_at);
CREATE INDEX idx_forecast_product_date ON demand_forecasts(product_id, forecast_date);
```

**Text Search Indexes:**
```sql
CREATE INDEX idx_products_name ON products(name);
CREATE INDEX idx_products_category ON products(category);
```

---

## CONSTRAINTS

**Primary Key Constraints:**
- All tables have auto-increment integer primary keys
- Ensures unique identification of records

**Foreign Key Constraints:**
- Maintain referential integrity
- Prevent orphaned records
- Define cascade behavior on delete/update

**Unique Constraints:**
```sql
UNIQUE(users.username)
UNIQUE(users.email)
UNIQUE(system_settings.setting_name)
```

**Check Constraints (Recommended):**
```sql
CHECK(products.current_price >= products.min_price)
CHECK(products.current_price <= products.max_price)
CHECK(products.inventory >= 0)
CHECK(sales_history.quantity_sold > 0)
CHECK(sales_history.price > 0)
```

**Not Null Constraints:**
- Applied to essential fields (name, price, user credentials, etc.)
- Ensures data completeness

---

## DATA FLOW PATTERNS

### Write Patterns

**Product Creation:**
1. Insert into PRODUCTS table
2. Initialize related settings in SYSTEM_SETTINGS (optional)
3. Generate initial forecast in DEMAND_FORECASTS (optional)

**Sale Transaction:**
1. Insert into SALES_HISTORY
2. Update PRODUCTS.inventory (decrement)
3. Potentially trigger PRICE_HISTORY update
4. Update PERFORMANCE_METRICS

**Price Change:**
1. Insert into PRICE_HISTORY (old and new price)
2. Update PRODUCTS.current_price
3. Record reason for change

### Read Patterns

**Dashboard Query:**
```sql
SELECT 
    p.product_id,
    p.name,
    p.current_price,
    p.inventory,
    SUM(sh.revenue) as total_revenue,
    COUNT(sh.sale_id) as total_sales
FROM products p
LEFT JOIN sales_history sh ON p.product_id = sh.product_id
WHERE sh.sale_date >= date('now', '-30 days')
GROUP BY p.product_id;
```

**Demand Forecasting Data:**
```sql
SELECT 
    product_id,
    sale_date,
    quantity_sold,
    price
FROM sales_history
WHERE product_id = ? 
AND sale_date >= date('now', '-180 days')
ORDER BY sale_date;
```

**Competitive Analysis:**
```sql
SELECT 
    p.product_id,
    p.name,
    p.current_price,
    AVG(cp.competitor_price) as avg_competitor_price,
    COUNT(DISTINCT cp.competitor_name) as competitor_count
FROM products p
LEFT JOIN competitor_prices cp ON p.product_id = cp.product_id
WHERE cp.updated_at >= date('now', '-7 days')
GROUP BY p.product_id;
```

---

## BACKUP AND RECOVERY

**Backup Strategy:**
- Full database backup daily
- Transaction log backup hourly (for systems supporting it)
- Retain backups for 30 days minimum

**Critical Tables (Priority for Recovery):**
1. PRODUCTS - Master data
2. SALES_HISTORY - Revenue records
3. USERS - Customer data
4. PRICE_HISTORY - Audit trail

**Recoverable Tables (Can be regenerated):**
- DEMAND_FORECASTS (can be recalculated)
- PRODUCT_SEARCHES, PRODUCT_VIEWS (analytics data)
- PERFORMANCE_METRICS (can be recalculated)

---

*This ERD provides comprehensive documentation of the database structure supporting the AI-Driven Dynamic Pricing System.*
