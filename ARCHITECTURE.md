# System Architecture Diagram

## AI-Driven Dynamic Pricing E-Commerce System

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         USERS (4 ACCOUNTS)                               │
├─────────────────────────────────────────────────────────────────────────┤
│  Customer 1  │  Customer 2  │  Customer 3  │  Admin                     │
│  (shop.html) │  (shop.html) │  (shop.html) │  (index.html)              │
└──────┬───────┴──────┬───────┴──────┬───────┴──────┬────────────────────┘
       │              │              │              │
       └──────────────┴──────────────┴──────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     FRONTEND (HTML/CSS/JS)                               │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────────┐  ┌─────────────┐        │
│  │  Login   │  │   Shop   │  │  Simulation  │  │   Admin     │        │
│  │  Page    │  │  Page    │  │    Page      │  │  Dashboard  │        │
│  └──────────┘  └──────────┘  └──────────────┘  └─────────────┘        │
│       │             │               │                  │                │
│       │             │               │                  │                │
│  ┌────┴─────────────┴───────────────┴──────────────────┴───────┐      │
│  │            shop.js  /  simulation.js  /  dashboard.js        │      │
│  │                   API Helper Functions                       │      │
│  └────────────────────────────┬──────────────────────────────────┘      │
└───────────────────────────────┼─────────────────────────────────────────┘
                                │
                         REST API Calls
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    BACKEND (Flask/Python)                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌───────────────────────────────────────────────────────────────┐     │
│  │                    app.py (Flask Server)                       │     │
│  │                      30+ API Endpoints                         │     │
│  └─────┬──────────────┬──────────────┬─────────────┬─────────────┘     │
│        │              │              │             │                    │
│        ▼              ▼              ▼             ▼                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐           │
│  │   Auth   │  │   Cart   │  │ Product  │  │   Dynamic    │           │
│  │ Endpoints│  │Endpoints │  │Tracking  │  │   Pricing    │           │
│  └──────────┘  └──────────┘  └──────────┘  └──────────────┘           │
│                                                     │                    │
│                                                     ▼                    │
│  ┌────────────────────────────────────────────────────────────┐        │
│  │          DynamicPricingEngine (dynamic_pricing_engine.py)  │        │
│  │                                                             │        │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │        │
│  │  │   Demand    │  │   Search    │  │    View     │        │        │
│  │  │   Factor    │  │   Factor    │  │   Factor    │        │        │
│  │  └─────────────┘  └─────────────┘  └─────────────┘        │        │
│  │                                                             │        │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │        │
│  │  │    Cart     │  │ Concurrent  │  │  Inventory  │        │        │
│  │  │   Factor    │  │   Factor    │  │   Factor    │        │        │
│  │  └─────────────┘  └─────────────┘  └─────────────┘        │        │
│  │                                                             │        │
│  │              Weighted Average → New Price                  │        │
│  └────────────────────────────────────────────────────────────┘        │
│                                                                          │
│  ┌────────────────────────────────────────────────────────────┐        │
│  │              Machine Learning Models                        │        │
│  │  ┌─────────────────┐  ┌──────────────┐  ┌──────────────┐  │        │
│  │  │ LSTM Forecaster │  │  RL Agent    │  │ Elasticity   │  │        │
│  │  │ (Demand Pred.)  │  │(Q-Learning)  │  │ Calculator   │  │        │
│  │  └─────────────────┘  └──────────────┘  └──────────────┘  │        │
│  └────────────────────────────────────────────────────────────┘        │
│                                                                          │
│  ┌────────────────────────────────────────────────────────────┐        │
│  │                  DatabaseManager (database.py)              │        │
│  └──────────────────────────────┬─────────────────────────────┘        │
└─────────────────────────────────┼──────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     DATABASE (SQLite)                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌────────────┐  ┌──────────────┐  ┌─────────────────┐                │
│  │   Users    │  │ Shopping Cart│  │ Product Searches│                │
│  │   Table    │  │    Table     │  │     Table       │                │
│  └────────────┘  └──────────────┘  └─────────────────┘                │
│                                                                          │
│  ┌────────────┐  ┌──────────────┐  ┌─────────────────┐                │
│  │  Product   │  │   Active     │  │  Sales History  │                │
│  │   Views    │  │  Sessions    │  │     Table       │                │
│  └────────────┘  └──────────────┘  └─────────────────┘                │
│                                                                          │
│  ┌────────────┐  ┌──────────────┐  ┌─────────────────┐                │
│  │  Products  │  │Price History │  │   Competitor    │                │
│  │   Table    │  │    Table     │  │     Prices      │                │
│  └────────────┘  └──────────────┘  └─────────────────┘                │
│                                                                          │
│  ┌────────────┐  ┌──────────────┐  ┌─────────────────┐                │
│  │  Demand    │  │   System     │  │  Performance    │                │
│  │ Forecasts  │  │  Settings    │  │    Metrics      │                │
│  └────────────┘  └──────────────┘  └─────────────────┘                │
└─────────────────────────────────────────────────────────────────────────┘
```

## Data Flow: User Action → Price Change

```
┌─────────────────┐
│  User Action    │  (View, Search, Add to Cart)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Track Event    │  (POST /api/products/<id>/track/view)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Database Update │  (product_views, product_searches tables)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Start Session   │  (active_sessions table)
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│   Calculate Dynamic Price               │
│                                         │
│   1. Get Engagement Stats (24h)         │
│   2. Count Concurrent Users (5min)      │
│   3. Calculate Sales Velocity (7d)      │
│   4. Apply 6 Weighted Factors           │
│   5. Ensure Min/Max Bounds              │
└─────────┬───────────────────────────────┘
          │
          ▼
┌─────────────────┐
│  Update Price   │  (products.current_price)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Record Change   │  (price_history table)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Return to UI   │  (JSON response with new price)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Auto-Refresh   │  (Every 10 seconds)
└─────────────────┘
```

## Concurrent User Scenario

```
Time: 00:00  ┌──────────────┐
             │ Product      │  Price: $25.99
             │ Base State   │
             └──────────────┘

Time: 00:01  ┌──────────────┐
             │ User 1 Views │  → Track View → Price: $26.50 (+2%)
             └──────────────┘       ↓
                              ┌──────────┐
                              │ +1 View  │
                              └──────────┘

Time: 00:02  ┌──────────────┐
             │ User 2 Views │  → Track View → Price: $27.10 (+4.3%)
             └──────────────┘       ↓
                              ┌──────────┐
                              │ +2 Views │
                              │ Concurrent│
                              │ Factor +5%│
                              └──────────┘

Time: 00:03  ┌──────────────┐
             │ User 3 Views │  → Track View → Price: $28.20 (+8.5%)
             └──────────────┘       ↓
                              ┌──────────┐
                              │ +3 Views │
                              │ Concurrent│
                              │ Factor+10%│
                              └──────────┘

Time: 00:10  ┌──────────────┐
             │ User 1 Adds  │  → Add to Cart → Price: $30.15 (+16%)
             │   to Cart    │       ↓
             └──────────────┘  ┌──────────┐
                               │ Cart     │
                               │ Factor   │
                               │  +10%    │
                               └──────────┘

Time: 00:15  ┌──────────────┐
             │ User 2 Adds  │  → Add to Cart → Price: $32.50 (+25%)
             │   to Cart    │       ↓
             └──────────────┘  ┌──────────┐
                               │ +2 Carts │
                               │ Factor   │
                               │  +15%    │
                               └──────────┘

Time: 00:20  ┌──────────────┐
             │ User 3 Adds  │  → Add to Cart → Price: $35.00 (+35%)
             │   to Cart    │       ↓
             └──────────────┘  ┌──────────┐
                               │ +3 Carts │
                               │ Factor   │
                               │  +15%    │
                               │ + High   │
                               │ Demand   │
                               └──────────┘

RESULT: Base Price $25.99 → Final Price $35.00 (35% increase!)
```

## Component Interaction

```
┌─────────────────────────────────────────────────────────────┐
│                    When Customer Shops                       │
└─────────────────────────────────────────────────────────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
        ┌─────────┐    ┌─────────┐    ┌─────────┐
        │  View   │    │ Search  │    │Add Cart │
        │ Product │    │ Product │    │ Product │
        └────┬────┘    └────┬────┘    └────┬────┘
             │              │              │
             ▼              ▼              ▼
        POST /track/view  /track/search  /cart/add
             │              │              │
             └──────────────┼──────────────┘
                            │
                            ▼
              ┌──────────────────────────┐
              │   Database Records       │
              │  - Increment counters    │
              │  - Create sessions       │
              │  - Update cart           │
              └────────────┬─────────────┘
                           │
                           ▼
              ┌──────────────────────────┐
              │ DynamicPricingEngine     │
              │  calculate_dynamic_price()│
              └────────────┬─────────────┘
                           │
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
    ┌──────────────┐         ┌──────────────┐
    │ Get Factors  │         │Apply Weights │
    │ - Searches   │         │  25% Demand  │
    │ - Views      │         │  20% Search  │
    │ - Carts      │         │  20% Cart    │
    │ - Concurrent │         │  15% Conc.   │
    │ - Demand     │         │  15% View    │
    │ - Inventory  │         │   5% Inv.    │
    └──────┬───────┘         └──────┬───────┘
           │                        │
           └───────────┬────────────┘
                       │
                       ▼
              ┌─────────────────┐
              │  New Price      │
              │  = Base × (1+Σ) │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Update Database │
              │ Return to User  │
              └─────────────────┘
```

## Tech Stack

```
┌─────────────────────────────────────────┐
│          Frontend Layer                 │
├─────────────────────────────────────────┤
│  HTML5  │  CSS3  │  JavaScript ES6+     │
│  Chart.js for Visualization             │
└─────────────────────────────────────────┘
                    │
                    │ REST API (JSON)
                    │
┌─────────────────────────────────────────┐
│          Backend Layer                  │
├─────────────────────────────────────────┤
│  Python 3.11  │  Flask 2.3.3            │
│  Flask-CORS for CORS support            │
└─────────────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
        ▼                       ▼
┌─────────────────┐   ┌─────────────────┐
│ ML/AI Layer     │   │ Database Layer  │
├─────────────────┤   ├─────────────────┤
│ TensorFlow 2.20 │   │ SQLite3         │
│ Keras 3.13      │   │ 12 Tables       │
│ Scikit-learn    │   │ Pandas for I/O  │
│ NumPy, Pandas   │   │                 │
└─────────────────┘   └─────────────────┘
```

---

This architecture enables:
✅ Real-time price updates
✅ Concurrent user tracking
✅ Scalable pricing algorithms
✅ Complete e-commerce functionality
✅ ML-powered predictions
✅ Comprehensive analytics
