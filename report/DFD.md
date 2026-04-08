# DATA FLOW DIAGRAM (DFD)
## AI-Driven Dynamic Pricing System

---

## LEVEL 0 - CONTEXT DIAGRAM

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         CONTEXT LEVEL DFD (Level 0)                          │
└─────────────────────────────────────────────────────────────────────────────┘


                              Product Requests
                              Sales Data
                   ┌─────────────────────────────────┐
                   │                                 │
                   ▼                                 │
        ┌──────────────────┐                        │
        │                  │    Products, Prices    │
        │   CUSTOMERS      │◄───────────────────────┘
        │                  │
        └──────────────────┘
                   │
                   │ Purchase Orders
                   │ Shopping Cart Actions
                   │
                   ▼
╔══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║         AI-DRIVEN DYNAMIC PRICING SYSTEM                         ║
║                                                                   ║
║    • Demand Forecasting                                          ║
║    • Price Optimization                                          ║
║    • Inventory Management                                        ║
║    • Analytics & Reporting                                       ║
║                                                                   ║
╚══════════════════════════════════════════════════════════════════╝
                   │                        ▲
                   │                        │
                   │ Analytics              │ System Configuration
                   │ Price Controls         │ Product Management
                   │ Reports                │ Manual Price Overrides
                   │                        │
                   ▼                        │
        ┌──────────────────┐                │
        │                  │────────────────┘
        │ ADMINISTRATORS   │
        │                  │
        └──────────────────┘
                   │
                   │ Competitor Data
                   ▼                        
        ┌──────────────────┐    Market Prices
        │                  │◄───────────────────────┐
        │  COMPETITORS     │                        │
        │                  │────────────────────────┘
        └──────────────────┘    Price Monitoring


                               EXTERNAL ENTITIES:
                               
                               1. CUSTOMERS
                               2. ADMINISTRATORS  
                               3. COMPETITORS
```

---

## LEVEL 1 - MAJOR PROCESSES

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              LEVEL 1 DFD                                     │
└─────────────────────────────────────────────────────────────────────────────┘


    CUSTOMERS                                                    ADMINISTRATORS
        │                                                              │
        │ Product Browse                              Product Data    │
        │ Requests                                    Management      │
        │                                                              │
        ▼                                                              ▼
┌─────────────────┐                                       ┌─────────────────┐
│                 │   Product Data                        │                 │
│   PROCESS 1.0   │◄──────────────────────────────────────│   PROCESS 2.0   │
│                 │                                       │                 │
│ PRODUCT         │   Updated Products                    │ PRODUCT         │
│ MANAGEMENT      │───────────────────────────────────────►│ CATALOG         │
│                 │                                       │ MAINTENANCE     │
└─────────────────┘                                       └─────────────────┘
        │                                                              │
        │ Product Info                                  Product Data  │
        │                                                              │
        ▼                                                              ▼
    ═══════════                                              ═══════════
    ║ D1      ║                                              ║ D2      ║
    ║ PRODUCTS║◄─────────────────────────────────────────────║ INVENTORY║
    ═══════════                                              ═══════════
        │                                                              │
        │ Historical Data                                 Stock Levels │
        │                                                              │
        ▼                                                              ▼
┌─────────────────┐                                       ┌─────────────────┐
│                 │                                       │                 │
│   PROCESS 3.0   │   Demand Forecasts                    │   PROCESS 4.0   │
│                 │───────────────────────────────────────►│                 │
│ DEMAND          │                                       │ DYNAMIC         │
│ FORECASTING     │   Current Demand                      │ PRICING         │
│ (LSTM)          │───────────────────────────────────────►│ ENGINE          │
│                 │                                       │                 │
└─────────────────┘                                       └─────────────────┘
        │                                                              │
        │                                                              │
        │ Store Forecasts                              Price Updates  │
        ▼                                                              ▼
    ═══════════                                              ═══════════
    ║ D3      ║                                              ║ D4      ║
    ║FORECASTS║                                              ║ PRICES  ║
    ═══════════                                              ═══════════
        │                                                              │
        │                                                              │
        │                                                Price History │
        ▼                                                              ▼
┌─────────────────┐                                       ┌─────────────────┐
│                 │   Learning Data                       │                 │
│   PROCESS 5.0   │◄──────────────────────────────────────│   PROCESS 6.0   │
│                 │                                       │                 │
│ REINFORCEMENT   │   Price Actions                       │ SALES           │
│ LEARNING        │───────────────────────────────────────►│ RECORDING       │
│ AGENT           │                                       │                 │
└─────────────────┘                                       └─────────────────┘
        │                                                              │
        │ Q-Values                                      Sales Data    │
        │ Policy Updates                                              │
        ▼                                                              ▼
    ═══════════                                              ═══════════
    ║ D5      ║                                              ║ D6      ║
    ║ RL MODEL║                                              ║ SALES   ║
    ═══════════                                              ═══════════
                                                                       │
                                                   Sales History      │
                                                                       │
                                                                       ▼
                                                          ┌─────────────────┐
    COMPETITORS                                           │                 │
        │                                                 │   PROCESS 7.0   │
        │ Market Prices                                   │                 │
        │                                                 │ ANALYTICS &     │
        │                                                 │ REPORTING       │
        ▼                                                 │                 │
┌─────────────────┐                                       └─────────────────┘
│                 │                                                  │
│   PROCESS 8.0   │   Competitor Data                                │
│                 │──────────────────────────────────────┐           │
│ COMPETITOR      │                                      │           │
│ MONITORING      │                                      ▼           │
│                 │                                  ═══════════     │
└─────────────────┘                                  ║ D7      ║     │
                                                     ║COMPETITOR║    │
                                                     ═══════════     │
                                                                      │
                                                     Reports &        │
                                                     Analytics        │
                                                                      │
                                                                      ▼
                                                          ADMINISTRATORS


═══════════════════════════════════════════════════════════════════════════
                                DATA STORES
═══════════════════════════════════════════════════════════════════════════

D1: PRODUCTS         - Product master data (name, category, base price)
D2: INVENTORY        - Stock levels and inventory data
D3: FORECASTS        - LSTM demand predictions
D4: PRICES           - Current and historical prices
D5: RL MODEL         - Q-Learning model data
D6: SALES            - Sales transaction history
D7: COMPETITOR       - Competitor pricing data
```

---

## LEVEL 2 - DETAILED PROCESS DECOMPOSITION

### PROCESS 3.0 - DEMAND FORECASTING (LSTM)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                  PROCESS 3.0 - DEMAND FORECASTING (Detailed)                 │
└─────────────────────────────────────────────────────────────────────────────┘


    ═══════════
    ║ D6      ║
    ║ SALES   ║
    ═══════════
        │
        │ Historical Sales Data
        │
        ▼
┌─────────────────┐
│                 │
│   PROCESS 3.1   │
│                 │
│ DATA            │   Cleaned Data
│ PREPROCESSING   │───────────────────┐
│                 │                   │
└─────────────────┘                   │
                                      ▼
                              ┌─────────────────┐
                              │                 │
                              │   PROCESS 3.2   │
                              │                 │
                              │ SEQUENCE        │   Training Sequences
                              │ GENERATION      │───────────────────┐
                              │                 │                   │
                              └─────────────────┘                   │
                                                                    ▼
                                                        ┌─────────────────┐
                                                        │                 │
                                                        │   PROCESS 3.3   │
                                                        │                 │
                                                        │ LSTM MODEL      │
                                                        │ TRAINING        │
                                                        │                 │
                                                        └─────────────────┘
                                                                    │
                                                   Trained Model    │
                                                                    │
                                                                    ▼
                                                            ═══════════
                                                            ║ D8      ║
                                                            ║ LSTM    ║
                                                            ║ MODELS  ║
                                                            ═══════════
                                                                    │
                                                   Model Parameters │
                                                                    │
                                                                    ▼
┌─────────────────┐                                       ┌─────────────────┐
│                 │   Recent Data                         │                 │
│   PROCESS 3.4   │◄──────────────────────────────────────│   PROCESS 3.5   │
│                 │                                       │                 │
│ FORECAST        │                                       │ MODEL           │
│ GENERATION      │   Predictions                         │ EVALUATION      │
│                 │───────────────────────────────────────►│                 │
└─────────────────┘                                       └─────────────────┘
        │                                                          │
        │ Demand Forecasts                         Accuracy       │
        │                                          Metrics         │
        ▼                                                          ▼
    ═══════════                                          ADMINISTRATORS
    ║ D3      ║                                          (Performance
    ║FORECASTS║                                           Reports)
    ═══════════
```

### PROCESS 4.0 - DYNAMIC PRICING ENGINE

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                 PROCESS 4.0 - DYNAMIC PRICING ENGINE (Detailed)              │
└─────────────────────────────────────────────────────────────────────────────┘


    ═══════════         ═══════════         ═══════════
    ║ D3      ║         ║ D2      ║         ║ D7      ║
    ║FORECASTS║         ║INVENTORY║         ║COMPETITOR║
    ═══════════         ═══════════         ═══════════
        │                    │                    │
        │ Demand             │ Stock              │ Market
        │ Predictions        │ Levels             │ Prices
        │                    │                    │
        └────────────┬───────┴──────────┬─────────┘
                     │                  │
                     ▼                  ▼
            ┌─────────────────────────────────┐
            │                                 │
            │      PROCESS 4.1                │
            │                                 │
            │  STATE EXTRACTION               │
            │  (Collect Market Signals)       │
            │                                 │
            └─────────────────────────────────┘
                            │
                            │ Market State Vector
                            │
                            ▼
            ┌─────────────────────────────────┐
            │                                 │
            │      PROCESS 4.2                │
            │                                 │
            │  PRICING FACTOR CALCULATION     │
            │  • Demand Factor                │
            │  • Inventory Factor             │
            │  • Competitor Factor            │
            │  • Engagement Factors           │
            │                                 │
            └─────────────────────────────────┘
                            │
                            │ Pricing Factors
                            │
                            ▼
            ┌─────────────────────────────────┐
            │                                 │
            │      PROCESS 4.3                │        ═══════════
            │                                 │        ║ D5      ║
            │  RL AGENT CONSULTATION          │◄───────║ RL MODEL║
            │  (Q-Learning Decision)          │        ═══════════
            │                                 │
            └─────────────────────────────────┘
                            │
                            │ Price Action
                            │
                            ▼
            ┌─────────────────────────────────┐
            │                                 │
            │      PROCESS 4.4                │
            │                                 │
            │  PRICE CALCULATION              │        ═══════════
            │  • Apply Factors                │───────►║ D9      ║
            │  • Enforce Constraints          │        ║ELASTICITY║
            │  • Validate Bounds              │◄───────║ DATA    ║
            │                                 │        ═══════════
            └─────────────────────────────────┘
                            │
                            │ New Price
                            │
                            ▼
            ┌─────────────────────────────────┐
            │                                 │
            │      PROCESS 4.5                │
            │                                 │
            │  PRICE UPDATE & RECORDING       │
            │                                 │
            └─────────────────────────────────┘
                            │
                ┌───────────┴───────────┐
                │                       │
                ▼                       ▼
        ═══════════              ═══════════
        ║ D1      ║              ║ D4      ║
        ║ PRODUCTS║              ║ PRICES  ║
        ║(current) ║              ║(history)║
        ═══════════              ═══════════
```

### PROCESS 6.0 - SALES RECORDING

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                   PROCESS 6.0 - SALES RECORDING (Detailed)                   │
└─────────────────────────────────────────────────────────────────────────────┘


    CUSTOMERS
        │
        │ Purchase Order
        │ (Product, Quantity)
        │
        ▼
┌─────────────────┐
│                 │
│   PROCESS 6.1   │      ═══════════
│                 │      ║ D1      ║
│ VALIDATE        │◄─────║ PRODUCTS║
│ ORDER           │      ║ D2      ║
│                 │◄─────║INVENTORY║
└─────────────────┘      ═══════════
        │
        │ Validated Order
        │
        ▼
┌─────────────────┐
│                 │
│   PROCESS 6.2   │      ═══════════
│                 │      ║ D4      ║
│ CALCULATE       │◄─────║ PRICES  ║
│ REVENUE         │      ║(current)║
│                 │      ═══════════
└─────────────────┘
        │
        │ Order + Revenue
        │
        ▼
┌─────────────────┐
│                 │
│   PROCESS 6.3   │
│                 │      ═══════════
│ RECORD SALE     │─────►║ D6      ║
│                 │      ║ SALES   ║
│                 │      ═══════════
└─────────────────┘
        │
        │ Sale Confirmation
        │
        ▼
┌─────────────────┐
│                 │
│   PROCESS 6.4   │
│                 │      ═══════════
│ UPDATE          │─────►║ D2      ║
│ INVENTORY       │      ║INVENTORY║
│                 │      ║ (reduce)║
└─────────────────┘      ═══════════
        │
        │ Transaction Complete
        │
        ▼
    CUSTOMERS
    (Confirmation)
```

### PROCESS 7.0 - ANALYTICS & REPORTING

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                PROCESS 7.0 - ANALYTICS & REPORTING (Detailed)                │
└─────────────────────────────────────────────────────────────────────────────┘


    ═══════════      ═══════════      ═══════════      ═══════════
    ║ D6      ║      ║ D4      ║      ║ D3      ║      ║ D7      ║
    ║ SALES   ║      ║ PRICES  ║      ║FORECASTS║      ║COMPETITOR║
    ═══════════      ═══════════      ═══════════      ═══════════
        │                 │                 │                 │
        │ Sales Data      │ Price Data      │ Predictions     │ Market Data
        │                 │                 │                 │
        └─────────┬───────┴────────┬────────┴─────────┬───────┘
                  │                │                  │
                  ▼                ▼                  ▼
        ┌──────────────────────────────────────────────────┐
        │                                                  │
        │           PROCESS 7.1                            │
        │                                                  │
        │     DATA AGGREGATION & TRANSFORMATION            │
        │                                                  │
        └──────────────────────────────────────────────────┘
                            │
                            │ Aggregated Data
                            │
                ┌───────────┴───────────┬──────────────────┐
                │                       │                  │
                ▼                       ▼                  ▼
    ┌─────────────────┐    ┌─────────────────┐   ┌─────────────────┐
    │                 │    │                 │   │                 │
    │  PROCESS 7.2    │    │  PROCESS 7.3    │   │  PROCESS 7.4    │
    │                 │    │                 │   │                 │
    │ REVENUE         │    │ PRODUCT         │   │ COMPETITIVE     │
    │ ANALYSIS        │    │ PERFORMANCE     │   │ ANALYSIS        │
    │                 │    │                 │   │                 │
    └─────────────────┘    └─────────────────┘   └─────────────────┘
                │                       │                  │
                │ Revenue Reports       │ Product Reports  │ Market Reports
                │                       │                  │
                └───────────┬───────────┴──────────────────┘
                            │
                            ▼
                ┌─────────────────────────┐
                │                         │
                │     PROCESS 7.5         │
                │                         │
                │  VISUALIZATION          │
                │  GENERATION             │
                │  • Charts               │
                │  • Graphs               │
                │  • Dashboards           │
                │                         │
                └─────────────────────────┘
                            │
                            │ Visual Reports
                            │
                            ▼
                    ADMINISTRATORS
                    (Dashboard Display)
```

---

## DATA FLOW DESCRIPTIONS

### Primary Data Flows

**1. Product Data Flow**
- **Source:** Administrators
- **Destination:** Product Database (D1)
- **Content:** Product name, category, base price, cost price, description
- **Volume:** Low frequency (product additions/updates)
- **Format:** JSON via REST API

**2. Sales Data Flow**
- **Source:** Customers
- **Destination:** Sales History (D6)
- **Content:** Product ID, quantity, price, timestamp
- **Volume:** High frequency (multiple per minute)
- **Format:** Transaction records

**3. Demand Forecast Flow**
- **Source:** LSTM Model (Process 3.0)
- **Destination:** Forecasts Database (D3), Pricing Engine (Process 4.0)
- **Content:** Predicted demand, confidence intervals
- **Volume:** Daily/hourly batch processing
- **Format:** Time-series predictions

**4. Price Update Flow**
- **Source:** Dynamic Pricing Engine (Process 4.0)
- **Destination:** Products (D1), Price History (D4)
- **Content:** New price, old price, reasoning
- **Volume:** Hourly/event-driven
- **Format:** Price update records

**5. Competitor Data Flow**
- **Source:** Competitor Monitoring (Process 8.0) / External APIs
- **Destination:** Competitor Database (D7), Pricing Engine (Process 4.0)
- **Content:** Competitor name, product match, price
- **Volume:** Daily batch updates
- **Format:** Structured price data

**6. Analytics Flow**
- **Source:** Various data stores (D1-D7)
- **Destination:** Analytics Module (Process 7.0), Administrators
- **Content:** Aggregated metrics, trends, comparisons
- **Volume:** On-demand queries
- **Format:** JSON reports, chart data

**7. RL Learning Flow**
- **Source:** Sales outcomes, price changes
- **Destination:** RL Agent (Process 5.0), RL Model (D5)
- **Content:** State-action-reward tuples, Q-value updates
- **Volume:** Continuous stream
- **Format:** Training data tuples

**8. User Engagement Flow**
- **Source:** Customers (browsing, searching, viewing)
- **Destination:** Engagement tracking, Pricing Engine
- **Content:** Search queries, page views, cart additions
- **Volume:** High frequency
- **Format:** Event logs

---

## DATA STORE SPECIFICATIONS

### D1: PRODUCTS
- **Type:** Relational database table
- **Size:** 1000-100,000 records
- **Update Frequency:** Low (product additions/modifications)
- **Access Pattern:** Read-heavy (10:1 read:write ratio)
- **Key Fields:** product_id, name, current_price, inventory

### D2: INVENTORY
- **Type:** Relational database table or in-memory cache
- **Size:** Matches product count
- **Update Frequency:** High (every sale)
- **Access Pattern:** Balanced read-write
- **Key Fields:** product_id, quantity, last_updated

### D3: FORECASTS
- **Type:** Relational database table
- **Size:** Product_count × forecast_horizon (e.g., 10K products × 7 days)
- **Update Frequency:** Daily batch
- **Access Pattern:** Read during pricing, write during forecast generation
- **Key Fields:** product_id, forecast_date, predicted_demand

### D4: PRICES
- **Type:** Relational database table (audit log)
- **Size:** Grows continuously (archival strategy needed)
- **Update Frequency:** Each price change
- **Access Pattern:** Write-heavy, historical reads
- **Key Fields:** price_id, product_id, old_price, new_price, timestamp

### D5: RL MODEL
- **Type:** File storage (JSON/pickle) or database
- **Size:** Model parameters (MB scale)
- **Update Frequency:** Continuous learning updates
- **Access Pattern:** Read for decisions, write for learning
- **Key Fields:** Q-table, learning_rate, epsilon

### D6: SALES
- **Type:** Relational database table
- **Size:** Grows continuously (millions of records)
- **Update Frequency:** Each purchase
- **Access Pattern:** Write-heavy, batch reads for analytics
- **Key Fields:** sale_id, product_id, quantity, price, timestamp

### D7: COMPETITOR
- **Type:** Relational database table
- **Size:** Products × competitors (e.g., 10K × 5 = 50K records)
- **Update Frequency:** Daily/hourly scraping
- **Access Pattern:** Batch write, read during pricing
- **Key Fields:** product_id, competitor_name, price, timestamp

### D8: LSTM MODELS
- **Type:** File storage (HDF5/SavedModel format)
- **Size:** Model weights (MB-GB scale)
- **Update Frequency:** Weekly/monthly retraining
- **Access Pattern:** Read for predictions, write during training
- **Key Fields:** Model architecture, weights, training metadata

### D9: ELASTICITY DATA
- **Type:** Relational database table or cache
- **Size:** One record per product
- **Update Frequency:** Weekly/monthly recalculation
- **Access Pattern:** Read during pricing, write during estimation
- **Key Fields:** product_id, elasticity_coefficient, confidence_interval

---

## PROCESS TIMING AND SCHEDULING

### Real-Time Processes (< 1 second response)
- **Process 1.0:** Product Management - Immediate
- **Process 6.0:** Sales Recording - Immediate
- **User Queries:** Analytics display - Immediate

### Near Real-Time (1-60 seconds)
- **Process 4.0:** Dynamic Pricing (event-triggered) - 5-30 seconds
- **Process 8.0:** Competitor Monitoring (API-based) - 10-60 seconds

### Batch Processes (Scheduled)
- **Process 3.0:** Demand Forecasting - Daily at 2:00 AM
- **Process 5.0:** RL Model Updates - Continuous with batch aggregation
- **Process 7.0:** Analytics Aggregation - Hourly
- **Elasticity Calculation:** Weekly on Sunday

---

## ERROR HANDLING AND VALIDATION

### Input Validation Flows
```
External Input
    │
    ▼
┌──────────────┐
│  Validate    │──► Reject if invalid
│  Format      │    (Return error to source)
└──────────────┘
    │ Valid
    ▼
┌──────────────┐
│  Validate    │──► Reject if constraints violated
│  Business    │    (Log & notify)
│  Rules       │
└──────────────┘
    │ Valid
    ▼
Continue Processing
```

### Data Quality Checks
- **Sales Data:** Positive quantities, valid product IDs, reasonable prices
- **Forecasts:** Within historical range, not NaN/Inf
- **Prices:** Within min/max bounds, positive values
- **Competitor Data:** Valid URLs, current timestamps

### Failure Recovery
- **Database Write Failures:** Transaction rollback, retry logic
- **Model Prediction Failures:** Fall back to baseline (e.g., base price)
- **API Timeouts:** Cached data usage, degraded service mode

---

## SECURITY AND PRIVACY FLOWS

### Authentication Flow
```
User Login Request
    │
    ▼
┌──────────────┐
│  Validate    │──► Reject if invalid
│  Credentials │
└──────────────┘
    │
    ▼
┌──────────────┐
│  Generate    │
│  Session     │
│  Token       │
└──────────────┘
    │
    ▼
Return Token to User
```

### Authorization Flow
```
API Request + Token
    │
    ▼
┌──────────────┐
│  Validate    │──► Reject if invalid/expired
│  Token       │
└──────────────┘
    │
    ▼
┌──────────────┐
│  Check       │──► Deny if insufficient permissions
│  Permissions │
└──────────────┘
    │
    ▼
Process Request
```

### Data Privacy
- **Customer Data:** Anonymized for analytics
- **Payment Info:** Not stored (out of scope)
- **Admin Actions:** Audit logged
- **Price Strategies:** Protected from competitors

---

*This DFD provides comprehensive documentation of data flows in the AI-Driven Dynamic Pricing System across multiple levels of abstraction.*
