# UML DIAGRAMS
## AI-Driven Dynamic Pricing System

---

## TABLE OF CONTENTS

1. [Class Diagram](#class-diagram)
2. [Sequence Diagrams](#sequence-diagrams)
   - Product Price Optimization
   - Customer Purchase Flow
   - Demand Forecast Generation
   - Admin Analytics Request
3. [Use Case Diagram](#use-case-diagram)
4. [Activity Diagram](#activity-diagram)
5. [Component Diagram](#component-diagram)
6. [Deployment Diagram](#deployment-diagram)

---

## CLASS DIAGRAM

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            MAIN CLASS DIAGRAM                                │
└─────────────────────────────────────────────────────────────────────────────┘


╔══════════════════════════════════════╗
║         DatabaseManager               ║
╠══════════════════════════════════════╣
║ - db_path: str                        ║
║ - connection: Connection              ║
╠══════════════════════════════════════╣
║ + __init__(db_path: str)              ║
║ + get_connection(): Connection        ║
║ + init_database(): void               ║
║ + add_product(...): int               ║
║ + get_product(id): dict               ║
║ + get_all_products(): DataFrame       ║
║ + update_product(...): bool           ║
║ + record_sale(...): int               ║
║ + get_sales_history(...): DataFrame   ║
║ + record_price_change(...): int       ║
║ + get_price_history(...): DataFrame   ║
║ + add_competitor_price(...): int      ║
║ + get_competitor_prices(...): list    ║
║ + save_demand_forecast(...): int      ║
║ + get_demand_forecasts(...): list     ║
║ + create_user(...): int               ║
║ + authenticate_user(...): dict        ║
║ + add_to_cart(...): int               ║
║ + get_cart(...): list                 ║
║ + track_product_view(...): void       ║
║ + track_product_search(...): void     ║
╚══════════════════════════════════════╝
                │
                │ uses
                │
                ▼
╔══════════════════════════════════════╗
║      LSTMDemandForecaster             ║
╠══════════════════════════════════════╣
║ - model: Sequential                   ║
║ - scaler: MinMaxScaler                ║
║ - lookback_window: int = 30           ║
║ - epochs: int = 50                    ║
║ - batch_size: int = 32                ║
╠══════════════════════════════════════╣
║ + __init__(lookback: int)             ║
║ + prepare_data(df): tuple             ║
║ + build_model(): Sequential           ║
║ + train(X, y): History                ║
║ + predict(X): ndarray                 ║
║ + forecast(data, steps): list         ║
║ + evaluate(X, y): dict                ║
║ + save_model(path): void              ║
║ + load_model(path): void              ║
╚══════════════════════════════════════╝
                │
                │
                │
╔══════════════════════════════════════╗
║    DynamicPricingAgent                ║
╠══════════════════════════════════════╣
║ - Q_table: dict                       ║
║ - learning_rate: float = 0.1          ║
║ - discount_factor: float = 0.9        ║
║ - epsilon: float = 0.3                ║
║ - actions: list                       ║
║ - episode_count: int = 0              ║
╠══════════════════════════════════════╣
║ + __init__(actions: list)             ║
║ + extract_state(...): tuple           ║
║ + select_action(state): float         ║
║ + get_q_value(state, action): float   ║
║ + update_q_values(...): void          ║
║ + get_reward(revenue, ...): float     ║
║ + decay_epsilon(): void               ║
║ + save_agent(path): void              ║
║ + load_agent(path): void              ║
╚══════════════════════════════════════╝
                │
                │
                │
╔══════════════════════════════════════╗
║   PriceElasticityCalculator           ║
╠══════════════════════════════════════╣
║ - min_samples: int = 30               ║
║ - elasticity_cache: dict              ║
╠══════════════════════════════════════╣
║ + __init__()                          ║
║ + calculate_elasticity(df): float     ║
║ + estimate_demand(price, ...): float  ║
║ + optimize_price(...): float          ║
║ + get_revenue_curve(...): list        ║
╚══════════════════════════════════════╝
                │
                │ uses all
                │
                ▼
╔══════════════════════════════════════╗
║     DynamicPricingEngine              ║
╠══════════════════════════════════════╣
║ - db_manager: DatabaseManager         ║
║ - forecaster: LSTMDemandForecaster    ║
║ - rl_agent: DynamicPricingAgent       ║
║ - elasticity_calc: PriceElasticity... ║
║ - factor_weights: dict                ║
╠══════════════════════════════════════╣
║ + __init__(db: DatabaseManager)       ║
║ + calculate_dynamic_price(...): float ║
║ + get_demand_factor(...): float       ║
║ + get_inventory_factor(...): float    ║
║ + get_competitor_factor(...): float   ║
║ + get_search_factor(...): float       ║
║ + get_view_factor(...): float         ║
║ + get_cart_factor(...): float         ║
║ + get_concurrent_factor(...): float   ║
║ + optimize_all_prices(): list         ║
║ + apply_price_constraints(...): float ║
╚══════════════════════════════════════╝
                │
                │ uses
                │
                ▼
╔══════════════════════════════════════╗
║          FlaskApp                     ║
╠══════════════════════════════════════╣
║ - app: Flask                          ║
║ - db: DatabaseManager                 ║
║ - pricing_engine: DynamicPricing...   ║
║ - rl_agent: DynamicPricingAgent       ║
╠══════════════════════════════════════╣
║ + health_check(): Response            ║
║ + get_products(): Response            ║
║ + get_product(id): Response           ║
║ + add_product(): Response             ║
║ + update_product(id): Response        ║
║ + optimize_price(id): Response        ║
║ + record_sale(): Response             ║
║ + get_analytics(): Response           ║
║ + login(): Response                   ║
║ + get_cart(): Response                ║
║ + add_to_cart(): Response             ║
╚══════════════════════════════════════╝


═══════════════════════════════════════════════════════════════════════════
                            SUPPORTING CLASSES
═══════════════════════════════════════════════════════════════════════════

┌──────────────────────────────────────┐
│           Product                     │
├──────────────────────────────────────┤
│ + product_id: int                     │
│ + name: str                           │
│ + category: str                       │
│ + base_price: float                   │
│ + cost_price: float                   │
│ + current_price: float                │
│ + inventory: int                      │
│ + min_price: float                    │
│ + max_price: float                    │
│ + description: str                    │
│ + demand_score: float                 │
│ + created_at: datetime                │
│ + updated_at: datetime                │
├──────────────────────────────────────┤
│ + to_dict(): dict                     │
│ + from_dict(data): Product            │
│ + validate(): bool                    │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│             Sale                      │
├──────────────────────────────────────┤
│ + sale_id: int                        │
│ + product_id: int                     │
│ + quantity_sold: int                  │
│ + price: float                        │
│ + revenue: float                      │
│ + sale_date: datetime                 │
├──────────────────────────────────────┤
│ + calculate_revenue(): float          │
│ + to_dict(): dict                     │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│          PriceChange                  │
├──────────────────────────────────────┤
│ + price_id: int                       │
│ + product_id: int                     │
│ + old_price: float                    │
│ + new_price: float                    │
│ + reason: str                         │
│ + changed_at: datetime                │
├──────────────────────────────────────┤
│ + get_change_percentage(): float      │
│ + to_dict(): dict                     │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│        DemandForecast                 │
├──────────────────────────────────────┤
│ + forecast_id: int                    │
│ + product_id: int                     │
│ + forecast_date: date                 │
│ + predicted_demand: float             │
│ + confidence_lower: float             │
│ + confidence_upper: float             │
│ + actual_demand: float                │
├──────────────────────────────────────┤
│ + calculate_error(): float            │
│ + to_dict(): dict                     │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│             User                      │
├──────────────────────────────────────┤
│ + user_id: int                        │
│ + username: str                       │
│ + email: str                          │
│ + password_hash: str                  │
│ + full_name: str                      │
│ + is_admin: bool                      │
│ + created_at: datetime                │
├──────────────────────────────────────┤
│ + verify_password(pwd): bool          │
│ + hash_password(pwd): str             │
│ + to_dict(): dict                     │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│          CartItem                     │
├──────────────────────────────────────┤
│ + cart_id: int                        │
│ + user_id: int                        │
│ + product_id: int                     │
│ + quantity: int                       │
│ + price_at_add: float                 │
│ + added_at: datetime                  │
├──────────────────────────────────────┤
│ + calculate_subtotal(): float         │
│ + to_dict(): dict                     │
└──────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════
                           RELATIONSHIPS
═══════════════════════════════════════════════════════════════════════════

DatabaseManager "1" ──── "0..*" Product
DatabaseManager "1" ──── "0..*" Sale  
DatabaseManager "1" ──── "0..*" User
Product "1" ──── "0..*" Sale
Product "1" ──── "0..*" PriceChange
Product "1" ──── "0..*" DemandForecast
User "1" ──── "0..*" CartItem
Product "1" ──── "0..*" CartItem
DynamicPricingEngine ──► DatabaseManager
DynamicPricingEngine ──► LSTMDemandForecaster
DynamicPricingEngine ──► DynamicPricingAgent
DynamicPricingEngine ──► PriceElasticityCalculator
FlaskApp ──► DatabaseManager
FlaskApp ──► DynamicPricingEngine
```

---

## SEQUENCE DIAGRAMS

### 1. Product Price Optimization Sequence

```
┌─────────────────────────────────────────────────────────────────────────────┐
│               SEQUENCE: Product Price Optimization                           │
└─────────────────────────────────────────────────────────────────────────────┘


Admin          API           Pricing         LSTM          RL           Database
              Server        Engine        Forecaster     Agent
  │              │             │              │            │               │
  │──Request────►│             │              │            │               │
  │ Optimize     │             │              │            │               │
  │ Price(pid)   │             │              │            │               │
  │              │             │              │            │               │
  │              │──Get────────────────────────────────────│               │
  │              │  Product   │              │            │               │
  │              │  Data(pid) │              │            │               │
  │              │             │              │            │               │
  │              │             │◄─────────────────────────────Product──────│
  │              │             │              │            │      Data     │
  │              │             │              │            │               │
  │              │──Calculate──►              │            │               │
  │              │  Price(pid) │              │            │               │
  │              │             │              │            │               │
  │              │             │──Get Sales───────────────────────────────►│
  │              │             │  History     │            │               │
  │              │             │              │            │               │
  │              │             │◄────────────────────────────Sales Data────│
  │              │             │              │            │               │
  │              │             │              │            │               │
  │              │             │──Forecast────►            │               │
  │              │             │  Demand      │            │               │
  │              │             │              │            │               │
  │              │             │              │──Build──►  │               │
  │              │             │              │  Sequences │               │
  │              │             │              │            │               │
  │              │             │              │◄─Predict───│               │
  │              │             │              │  Demand    │               │
  │              │             │              │            │               │
  │              │             │◄─Forecast────│            │               │
  │              │             │  Result      │            │               │
  │              │             │              │            │               │
  │              │             │──Get Competitor────────────────────────────►│
  │              │             │  Prices      │            │               │
  │              │             │              │            │               │
  │              │             │◄───────────────────────────Competitor─────│
  │              │             │              │            │    Prices     │
  │              │             │              │            │               │
  │              │             │──Extract─────────────────►│               │
  │              │             │  State       │            │               │
  │              │             │  (demand,    │            │               │
  │              │             │   inventory, │            │               │
  │              │             │   competitor)│            │               │
  │              │             │              │            │               │
  │              │             │              │            │──Lookup Q─►   │
  │              │             │              │            │  Values       │
  │              │             │              │            │               │
  │              │             │◄─Select──────────────────│               │
  │              │             │  Action      │            │               │
  │              │             │  (price mult)│            │               │
  │              │             │              │            │               │
  │              │             │──Calculate───►            │               │
  │              │             │  Factors     │            │               │
  │              │             │              │            │               │
  │              │             │◄─Factors─────│            │               │
  │              │             │              │            │               │
  │              │             │──Compute──►  │            │               │
  │              │             │  New Price   │            │               │
  │              │             │              │            │               │
  │              │             │──Validate────►            │               │
  │              │             │  Constraints │            │               │
  │              │             │              │            │               │
  │              │             │──Record Price──────────────────────────────►│
  │              │             │  Change      │            │               │
  │              │             │              │            │               │
  │              │             │──Update Product─────────────────────────────►│
  │              │             │  Price       │            │               │
  │              │             │              │            │               │
  │              │◄─New Price──│              │            │               │
  │              │             │              │            │               │
  │◄─Response────│             │              │            │               │
  │  {new_price, │             │              │            │               │
  │   old_price, │             │              │            │               │
  │   reason}    │             │              │            │               │
  │              │             │              │            │               │
```

### 2. Customer Purchase Flow Sequence

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                  SEQUENCE: Customer Purchase Flow                            │
└─────────────────────────────────────────────────────────────────────────────┘


Customer       Frontend        API          Database       Pricing        RL
                               Server                      Engine        Agent
  │              │              │              │              │            │
  │──Browse──────►              │              │              │            │
  │  Products    │              │              │              │            │
  │              │              │              │              │            │
  │              │──Get─────────►              │              │            │
  │              │  Products    │              │              │            │
  │              │              │              │              │            │
  │              │              │──Query───────►              │            │
  │              │              │  Products    │              │            │
  │              │              │              │              │            │
  │              │              │◄─Product─────│              │            │
  │              │              │  List        │              │            │
  │              │              │              │              │            │
  │              │◄─Products────│              │              │            │
  │              │  (JSON)      │              │              │            │
  │              │              │              │              │            │
  │◄─Display─────│              │              │              │            │
  │  Products    │              │              │              │            │
  │  with Prices │              │              │              │            │
  │              │              │              │              │            │
  │──View Product►              │              │              │            │
  │  Details     │              │              │              │            │
  │              │              │              │              │            │
  │              │──Track View──►              │              │            │
  │              │              │              │              │            │
  │              │              │──Record──────►              │            │
  │              │              │  View        │              │            │
  │              │              │              │              │            │
  │──Add to Cart─►              │              │              │            │
  │              │              │              │              │            │
  │              │──Add Cart────►              │              │            │
  │              │  Item        │              │              │            │
  │              │              │              │              │            │
  │              │              │──Insert──────►              │            │
  │              │              │  Cart        │              │            │
  │              │              │              │              │            │
  │              │              │──Track Cart──►              │            │
  │              │              │  Addition    │              │            │
  │              │              │              │              │            │
  │              │◄─Cart Updated│              │              │            │
  │              │              │              │              │            │
  │◄─Confirmation│              │              │              │            │
  │              │              │              │              │            │
  │──Checkout────►              │              │              │            │
  │              │              │              │              │            │
  │              │──Purchase────►              │              │            │
  │              │  Request     │              │              │            │
  │              │              │              │              │            │
  │              │              │──Validate────►              │            │
  │              │              │  Inventory   │              │            │
  │              │              │              │              │            │
  │              │              │◄─Available───│              │            │
  │              │              │              │              │            │
  │              │              │──Record Sale─►              │            │
  │              │              │              │              │            │
  │              │              │──Update──────►              │            │
  │              │              │  Inventory   │              │            │
  │              │              │              │              │            │
  │              │              │──Clear Cart──►              │            │
  │              │              │              │              │            │
  │              │              │──Trigger─────────────────────►           │
  │              │              │  Price       │              │            │
  │              │              │  Update      │              │            │
  │              │              │  (async)     │              │            │
  │              │              │              │              │            │
  │              │              │              │              │──Update────►
  │              │              │              │              │  Q-Values  │
  │              │              │              │              │  (reward)  │
  │              │              │              │              │            │
  │              │◄─Purchase────│              │              │            │
  │              │  Confirmed   │              │              │            │
  │              │              │              │              │            │
  │◄─Receipt─────│              │              │              │            │
  │  & Thank You │              │              │              │            │
  │              │              │              │              │            │
```

### 3. Demand Forecast Generation Sequence

```
┌─────────────────────────────────────────────────────────────────────────────┐
│              SEQUENCE: Demand Forecast Generation (Batch)                    │
└─────────────────────────────────────────────────────────────────────────────┘


Scheduler      LSTM           Database       Pricing         Admin
             Forecaster                      Engine        Dashboard
  │              │              │              │              │
  │──Daily───────►              │              │              │
  │  Trigger     │              │              │              │
  │  (2:00 AM)   │              │              │              │
  │              │              │              │              │
  │              │──Get All─────►              │              │
  │              │  Products    │              │              │
  │              │              │              │              │
  │              │◄─Product─────│              │              │
  │              │  List        │              │              │
  │              │              │              │              │
  │              │──For each────┐              │              │
  │              │  product     │              │              │
  │              │              │              │              │
  │              │  ┌───────────▼───────────┐  │              │
  │              │  │ Get Sales History    │  │              │
  │              │  │ (last 180 days)      │  │              │
  │              │  └───────────┬───────────┘  │              │
  │              │              │              │              │
  │              │◄─Sales Data──│              │              │
  │              │              │              │              │
  │              │──Prepare─────┐              │              │
  │              │  Data        │              │              │
  │              │              │              │              │
  │              │  ┌───────────▼───────────┐  │              │
  │              │  │ Normalize            │  │              │
  │              │  │ Create Sequences     │  │              │
  │              │  └───────────┬───────────┘  │              │
  │              │              │              │              │
  │              │──Build Model─┐              │              │
  │              │              │              │              │
  │              │  ┌───────────▼───────────┐  │              │
  │              │  │ LSTM Architecture    │  │              │
  │              │  │ - Layer 1: 64 units  │  │              │
  │              │  │ - Layer 2: 32 units  │  │              │
  │              │  │ - Output: 1 unit     │  │              │
  │              │  └───────────┬───────────┘  │              │
  │              │              │              │              │
  │              │──Train Model─┐              │              │
  │              │              │              │              │
  │              │  ┌───────────▼───────────┐  │              │
  │              │  │ Fit on data          │  │              │
  │              │  │ Epochs: 50           │  │              │
  │              │  │ Batch size: 32       │  │              │
  │              │  └───────────┬───────────┘  │              │
  │              │              │              │              │
  │              │──Predict Next►              │              │
  │              │  7 Days      │              │              │
  │              │              │              │              │
  │              │  ┌───────────▼───────────┐  │              │
  │              │  │ Generate forecasts   │  │              │
  │              │  │ Day 1-7 ahead        │  │              │
  │              │  └───────────┬───────────┘  │              │
  │              │              │              │              │
  │              │──Calculate───┐              │              │
  │              │  Confidence  │              │              │
  │              │  Intervals   │              │              │
  │              │              │              │              │
  │              │──Save────────►              │              │
  │              │  Forecasts   │              │              │
  │              │              │              │              │
  │              │              │──Insert──────┐              │
  │              │              │  Forecast    │              │
  │              │              │  Records     │              │
  │              │              │              │              │
  │              │◄─Saved───────│              │              │
  │              │              │              │              │
  │              │──Notify──────────────────────────────────────►
  │              │  Pricing     │              │              │
  │              │  Engine      │              │              │
  │              │              │              │              │
  │              │              │              │◄─Updated─────│
  │              │              │              │  Forecasts   │
  │              │              │              │              │
  │              │──Log─────────►              │              │
  │              │  Completion  │              │              │
  │              │              │              │              │
  │◄─Complete────│              │              │              │
  │              │              │              │              │
```

### 4. Admin Analytics Request Sequence

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                 SEQUENCE: Admin Analytics Request                            │
└─────────────────────────────────────────────────────────────────────────────┘


Admin        Frontend       API          Analytics        Database
Dashboard                  Server        Module
  │              │            │              │              │
  │──Request─────►            │              │              │
  │  Dashboard   │            │              │              │
  │  Analytics   │            │              │              │
  │              │            │              │              │
  │              │──GET───────►              │              │
  │              │  /analytics│              │              │
  │              │  /dashboard│              │              │
  │              │            │              │              │
  │              │            │──Generate────►              │
  │              │            │  Analytics   │              │
  │              │            │              │              │
  │              │            │              │──Query───────►
  │              │            │              │  Total       │
  │              │            │              │  Revenue     │
  │              │            │              │              │
  │              │            │              │◄─Revenue─────│
  │              │            │              │  Sum         │
  │              │            │              │              │
  │              │            │              │──Query───────►
  │              │            │              │  Product     │
  │              │            │              │  Count       │
  │              │            │              │              │
  │              │            │              │◄─Count───────│
  │              │            │              │              │
  │              │            │              │──Query───────►
  │              │            │              │  Sales       │
  │              │            │              │  Volume      │
  │              │            │              │              │
  │              │            │              │◄─Volume──────│
  │              │            │              │              │
  │              │            │              │──Query───────►
  │              │            │              │  Top         │
  │              │            │              │  Products    │
  │              │            │              │              │
  │              │            │              │◄─Top 10──────│
  │              │            │              │  List        │
  │              │            │              │              │
  │              │            │              │──Query───────►
  │              │            │              │  Revenue     │
  │              │            │              │  Trend (30d) │
  │              │            │              │              │
  │              │            │              │◄─Daily───────│
  │              │            │              │  Revenue     │
  │              │            │              │              │
  │              │            │              │──Query───────►
  │              │            │              │  Category    │
  │              │            │              │  Performance │
  │              │            │              │              │
  │              │            │              │◄─Category────│
  │              │            │              │  Stats       │
  │              │            │              │              │
  │              │            │              │──Calculate───┐
  │              │            │              │  KPIs        │
  │              │            │              │              │
  │              │            │              │  ┌───────────▼──┐
  │              │            │              │  │ Avg Price   │
  │              │            │              │  │ Conv. Rate  │
  │              │            │              │  │ Growth %    │
  │              │            │              │  └───────────┬──┘
  │              │            │              │              │
  │              │            │◄─Analytics───│              │
  │              │            │  Payload     │              │
  │              │            │  (JSON)      │              │
  │              │            │              │              │
  │              │◄─Response──│              │              │
  │              │  {stats,   │              │              │
  │              │   trends,  │              │              │
  │              │   products}│              │              │
  │              │            │              │              │
  │◄─Render──────│            │              │              │
  │  Charts &    │            │              │              │
  │  Dashboards  │            │              │              │
  │              │            │              │              │
```

---

## USE CASE DIAGRAM

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            USE CASE DIAGRAM                                  │
└─────────────────────────────────────────────────────────────────────────────┘


                    ┌────────────────────────────────────────┐
                    │  AI-Driven Dynamic Pricing System      │
                    │                                        │
   ┌──────────┐     │                                        │
   │          │     │  ┌──────────────────────────┐         │
   │ Customer │────────│ Browse Products           │         │
   │          │     │  └──────────────────────────┘         │
   └──────────┘     │                                        │
        │           │  ┌──────────────────────────┐         │
        │           │  │ View Product Details      │         │
        └──────────────│ (with dynamic price)      │         │
                    │  └──────────────────────────┘         │
                    │              │                         │
                    │              │ <<include>>             │
                    │              ▼                         │
                    │  ┌──────────────────────────┐         │
                    │  │ Track User Engagement     │         │
                    │  └──────────────────────────┘         │
                    │                                        │
   ┌──────────┐     │  ┌──────────────────────────┐         │
   │          │     │  │ Add to Shopping Cart      │         │
   │ Customer │────────│                           │         │
   │          │     │  └──────────────────────────┘         │
   └──────────┘     │                                        │
        │           │  ┌──────────────────────────┐         │
        │           │  │ Complete Purchase         │         │
        └──────────────│                           │         │
                    │  └──────────────────────────┘         │
                    │              │                         │
                    │              │ <<include>>             │
                    │              ▼                         │
                    │  ┌──────────────────────────┐         │
                    │  │ Update Inventory          │         │
                    │  └──────────────────────────┘         │
                    │              │                         │
                    │              │ <<extend>>              │
                    │              ▼                         │
                    │  ┌──────────────────────────┐         │
                    │  │ Trigger Price             │         │
                    │  │ Recalculation             │         │
                    │  └──────────────────────────┘         │
                    │                                        │
                    │                                        │
   ┌──────────┐     │  ┌──────────────────────────┐         │
   │          │     │  │ Manage Products           │         │
   │  Admin   │────────│ (Add/Edit/Delete)         │         │
   │          │     │  └──────────────────────────┘         │
   └──────────┘     │                                        │
        │           │  ┌──────────────────────────┐         │
        │           │  │ Set Price Constraints     │         │
        ├──────────────│ (Min/Max Bounds)          │         │
        │           │  └──────────────────────────┘         │
        │           │                                        │
        │           │  ┌──────────────────────────┐         │
        │           │  │ View Analytics Dashboard  │         │
        ├──────────────│                           │         │
        │           │  └──────────────────────────┘         │
        │           │              │                         │
        │           │              │ <<include>>             │
        │           │              ▼                         │
        │           │  ┌──────────────────────────┐         │
        │           │  │ Generate Reports          │         │
        │           │  └──────────────────────────┘         │
        │           │                                        │
        │           │  ┌──────────────────────────┐         │
        │           │  │ Monitor Competitors       │         │
        ├──────────────│                           │         │
        │           │  └──────────────────────────┘         │
        │           │                                        │
        │           │  ┌──────────────────────────┐         │
        │           │  │ Configure System          │         │
        ├──────────────│ Parameters                │         │
        │           │  └──────────────────────────┘         │
        │           │                                        │
        │           │  ┌──────────────────────────┐         │
        │           │  │ Override Automated        │         │
        └──────────────│ Pricing                   │         │
                    │  └──────────────────────────┘         │
                    │                                        │
                    │                                        │
                    │  ┌──────────────────────────┐         │
                    │  │ Forecast Demand           │◄────────┤ LSTM
                    │  │ (LSTM Model)              │         │ Scheduler
                    │  └──────────────────────────┘         │
                    │              │                         │
                    │              │ <<include>>             │
                    │              ▼                         │
                    │  ┌──────────────────────────┐         │
                    │  │ Optimize Prices           │         │
                    │  │ (RL Agent)                │         │
                    │  └──────────────────────────┘         │
                    │              │                         │
                    │              │ <<include>>             │
                    │              ▼                         │
                    │  ┌──────────────────────────┐         │
                    │  │ Calculate Price           │         │
                    │  │ Elasticity                │         │
                    │  └──────────────────────────┘         │
                    │                                        │
                    └────────────────────────────────────────┘


                    ACTORS:
                    • Customer - End user browsing and purchasing
                    • Admin - System administrator managing pricing
                    • LSTM Scheduler - Automated forecasting process
```

---

## ACTIVITY DIAGRAM

### Dynamic Price Calculation Activity

```
┌─────────────────────────────────────────────────────────────────────────────┐
│              ACTIVITY DIAGRAM: Dynamic Price Calculation                     │
└─────────────────────────────────────────────────────────────────────────────┘


                            ┌───────────┐
                            │  START    │
                            └─────┬─────┘
                                  │
                                  ▼
                        ┌─────────────────┐
                        │ Retrieve Product│
                        │ Data from DB    │
                        └────────┬────────┘
                                 │
                        ╔════════╧════════╗
                        ║ Product Exists? ║
                        ╚════════╤════════╝
                          No     │     Yes
                    ┌────────────┴────────────┐
                    │                         │
                    ▼                         ▼
            ┌───────────────┐      ┌──────────────────┐
            │ Return Error  │      │ Get Historical   │
            │ Message       │      │ Sales Data       │
            └───────┬───────┘      └────────┬─────────┘
                    │                       │
                    │                       ▼
                    │            ┌──────────────────────┐
                    │            │ Generate Demand      │
                    │            │ Forecast (LSTM)      │
                    │            └──────────┬───────────┘
                    │                       │
                    │                       ▼
                    │            ┌──────────────────────┐
                    │            │ Get Competitor Prices│
                    │            └──────────┬───────────┘
                    │                       │
                    │            ╔══════════╧══════════╗
                    │            ║ Competitors Found?  ║
                    │            ╚══════════╤══════════╝
                    │                 No    │    Yes
                    │           ┌───────────┴─────────────┐
                    │           │                         │
                    │           ▼                         ▼
                    │   ┌───────────────┐      ┌──────────────────┐
                    │   │ Use Default   │      │ Calculate        │
                    │   │ Factor (1.0)  │      │ Competitor Factor│
                    │   └───────┬───────┘      └────────┬─────────┘
                    │           │                       │
                    │           └───────────┬───────────┘
                    │                       │
                    │                       ▼
                    │            ══════════════════════════
                    │            ║ PARALLEL ACTIVITIES    ║
                    │            ══════════════════════════
                    │                       │
                    │       ┌───────────────┼───────────────┐
                    │       │               │               │
                    │       ▼               ▼               ▼
                    │  ┌─────────┐   ┌─────────┐   ┌─────────────┐
                    │  │Calculate│   │Calculate│   │ Calculate   │
                    │  │ Demand  │   │Inventory│   │ Search/View │
                    │  │ Factor  │   │ Factor  │   │ Factor      │
                    │  └────┬────┘   └────┬────┘   └──────┬──────┘
                    │       │             │               │
                    │       └─────────────┼───────────────┘
                    │                     │
                    │            ══════════════════════════
                    │                     │
                    │                     ▼
                    │          ┌──────────────────────┐
                    │          │ Calculate Weighted   │
                    │          │ Average of Factors   │
                    │          └──────────┬───────────┘
                    │                     │
                    │                     ▼
                    │          ┌──────────────────────┐
                    │          │ Apply Factor to      │
                    │          │ Base Price           │
                    │          │ new_price = base *   │
                    │          │ weighted_avg         │
                    │          └──────────┬───────────┘
                    │                     │
                    │                     ▼
                    │          ┌──────────────────────┐
                    │          │ Extract Market State │
                    │          │ for RL Agent         │
                    │          └──────────┬───────────┘
                    │                     │
                    │                     ▼
                    │          ┌──────────────────────┐
                    │          │ RL Agent Selects     │
                    │          │ Action (ε-greedy)    │
                    │          └──────────┬───────────┘
                    │                     │
                    │                     ▼
                    │          ╔═══════════════════════╗
                    │          ║ Random < epsilon?     ║
                    │          ╚═══════════════════════╝
                    │               Yes   │    No
                    │          ┌──────────┴──────────┐
                    │          │                     │
                    │          ▼                     ▼
                    │  ┌───────────────┐   ┌─────────────────┐
                    │  │ Explore:      │   │ Exploit:        │
                    │  │ Random Action │   │ Best Q-Value    │
                    │  │               │   │ Action          │
                    │  └───────┬───────┘   └────────┬────────┘
                    │          │                     │
                    │          └──────────┬──────────┘
                    │                     │
                    │                     ▼
                    │          ┌──────────────────────┐
                    │          │ Apply RL Action      │
                    │          │ (price multiplier)   │
                    │          └──────────┬───────────┘
                    │                     │
                    │                     ▼
                    │          ╔═══════════════════════╗
                    │          ║ Price < Min Bound?    ║
                    │          ╚═══════════════════════╝
                    │               Yes   │    No
                    │          ┌──────────┴──────────┐
                    │          │                     │
                    │          ▼                     ▼
                    │  ┌───────────────┐   ╔═════════════════╗
                    │  │ Set to        │   ║ Price > Max     ║
                    │  │ Min Price     │   ║ Bound?          ║
                    │  └───────┬───────┘   ╚═════════════════╝
                    │          │             Yes │    No
                    │          │        ┌────────┴────────┐
                    │          │        │                 │
                    │          │        ▼                 ▼
                    │          │  ┌──────────┐   ┌────────────┐
                    │          │  │ Set to   │   │ Accept     │
                    │          │  │ Max Price│   │ Price      │
                    │          │  └─────┬────┘   └──────┬─────┘
                    │          │        │               │
                    │          └────────┴───────────────┘
                    │                     │
                    │                     ▼
                    │          ┌──────────────────────┐
                    │          │ Record Price Change  │
                    │          │ in Database          │
                    │          └──────────┬───────────┘
                    │                     │
                    │                     ▼
                    │          ┌──────────────────────┐
                    │          │ Update Product       │
                    │          │ Current Price        │
                    │          └──────────┬───────────┘
                    │                     │
                    └─────────────────────┘
                                  │
                                  ▼
                            ┌───────────┐
                            │    END    │
                            │ Return    │
                            │ New Price │
                            └───────────┘
```

---

## COMPONENT DIAGRAM

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           COMPONENT DIAGRAM                                  │
└─────────────────────────────────────────────────────────────────────────────┘


┌────────────────────────────────────────────────────────────────────────────┐
│                        PRESENTATION LAYER                                   │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐           │
│  │  Dashboard UI   │  │   Shop UI       │  │  Analytics UI   │           │
│  │  (HTML/JS/CSS)  │  │  (HTML/JS/CSS)  │  │  (HTML/JS/CSS)  │           │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘           │
│           │                    │                     │                     │
│           └────────────────────┼─────────────────────┘                     │
│                                │                                           │
│                     ┌──────────▼──────────┐                                │
│                     │     API Client      │                                │
│                     │    (api.js)         │                                │
│                     └──────────┬──────────┘                                │
│                                │                                           │
└────────────────────────────────┼───────────────────────────────────────────┘
                                 │ HTTP/REST
                                 │ (JSON)
┌────────────────────────────────▼───────────────────────────────────────────┐
│                         APPLICATION LAYER                                   │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐ │
│  │                      Flask API Server                                 │ │
│  │                         (app.py)                                      │ │
│  └─────┬─────────────────────────┬─────────────────────────┬────────────┘ │
│        │                         │                         │               │
│        │ Uses                    │ Uses                    │ Uses          │
│        │                         │                         │               │
│        ▼                         ▼                         ▼               │
│  ┌──────────────┐      ┌──────────────────┐      ┌─────────────────────┐ │
│  │ Auth Module  │      │   Pricing        │      │   Analytics         │ │
│  │              │      │   Controller     │      │   Module            │ │
│  └──────┬───────┘      └────────┬─────────┘      └──────────┬──────────┘ │
│         │                       │                            │             │
│         │ Uses                  │ Uses                       │ Uses        │
│         │                       │                            │             │
└─────────┼───────────────────────┼────────────────────────────┼─────────────┘
          │                       │                            │
          │                       ▼                            │
          │         ┌─────────────────────────────┐           │
          │         │   Dynamic Pricing Engine    │           │
          │         │                             │           │
          │         │  ┌────────────────────────┐ │           │
          │         │  │ Factor Calculation     │ │           │
          │         │  └────────────────────────┘ │           │
          │         │  ┌────────────────────────┐ │           │
          │         │  │ Price Optimization     │ │           │
          │         │  └────────────────────────┘ │           │
          │         └──────────┬──────────────────┘           │
          │                    │ Uses                          │
          │                    │                               │
┌─────────┼────────────────────┼───────────────────────────────┼─────────────┐
│         │       MACHINE LEARNING LAYER                       │             │
├─────────┼────────────────────┼───────────────────────────────┼─────────────┤
│         │                    │                               │             │
│         │         ┌──────────▼──────────┐                    │             │
│         │         │  LSTM Forecaster    │                    │             │
│         │         │                     │                    │             │
│         │         │  ┌────────────────┐ │                    │             │
│         │         │  │ Data Prep      │ │                    │             │
│         │         │  │ Model Training │ │                    │             │
│         │         │  │ Prediction     │ │                    │             │
│         │         │  └────────────────┘ │                    │             │
│         │         └─────────────────────┘                    │             │
│         │                                                    │             │
│         │         ┌─────────────────────┐                    │             │
│         │         │  RL Pricing Agent   │                    │             │
│         │         │                     │                    │             │
│         │         │  ┌────────────────┐ │                    │             │
│         │         │  │ State Extract  │ │                    │             │
│         │         │  │ Action Select  │ │                    │             │
│         │         │  │ Q-Learning     │ │                    │             │
│         │         │  └────────────────┘ │                    │             │
│         │         └─────────────────────┘                    │             │
│         │                                                    │             │
│         │         ┌─────────────────────┐                    │             │
│         │         │ Elasticity Calc     │                    │             │
│         │         │                     │                    │             │
│         │         │  ┌────────────────┐ │                    │             │
│         │         │  │ Regression     │ │                    │             │
│         │         │  │ Estimation     │ │                    │             │
│         │         │  └────────────────┘ │                    │             │
│         │         └─────────────────────┘                    │             │
│         │                    │                               │             │
└─────────┼────────────────────┼───────────────────────────────┼─────────────┘
          │                    │                               │
          │ Uses               │ Uses                          │ Uses
          │                    │                               │
┌─────────▼────────────────────▼───────────────────────────────▼─────────────┐
│                          DATA ACCESS LAYER                                  │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌────────────────────────────────────────────────────────────────────┐   │
│  │                      Database Manager                               │   │
│  │                                                                     │   │
│  │  ┌───────────────┐  ┌───────────────┐  ┌──────────────────┐       │   │
│  │  │ Product CRUD  │  │ Sales Manager │  │ Analytics Queries│       │   │
│  │  └───────────────┘  └───────────────┘  └──────────────────┘       │   │
│  │  ┌───────────────┐  ┌───────────────┐  ┌──────────────────┐       │   │
│  │  │ User Manager  │  │ Price Manager │  │ Forecast Manager │       │   │
│  │  └───────────────┘  └───────────────┘  └──────────────────┘       │   │
│  └────────────────────────────┬───────────────────────────────────────┘   │
│                               │                                            │
└───────────────────────────────┼────────────────────────────────────────────┘
                                │
┌───────────────────────────────▼────────────────────────────────────────────┐
│                          DATA STORAGE LAYER                                 │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌────────────────────────────────────────────────────────────────────┐   │
│  │                      SQLite Database                                │   │
│  │                                                                     │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐              │   │
│  │  │ Products │ │ Sales    │ │ Prices   │ │ Users    │              │   │
│  │  │ Table    │ │ Table    │ │ Table    │ │ Table    │              │   │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘              │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐              │   │
│  │  │Forecasts │ │Competitor│ │  Cart    │ │ Settings │              │   │
│  │  │  Table   │ │  Table   │ │  Table   │ │  Table   │              │   │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘              │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


EXTERNAL COMPONENTS:

┌────────────────┐         ┌────────────────┐
│  TensorFlow/   │────────►│  NumPy/Pandas  │
│  Keras Library │         │  Libraries     │
└────────────────┘         └────────────────┘

┌────────────────┐         ┌────────────────┐
│  Flask         │────────►│  Scikit-Learn  │
│  Framework     │         │  Library       │
└────────────────┘         └────────────────┘
```

---

## DEPLOYMENT DIAGRAM

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          DEPLOYMENT DIAGRAM                                  │
└─────────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│                            CLIENT DEVICES                                    │
│                                                                              │
│  ┌────────────────────┐    ┌────────────────────┐    ┌────────────────────┐│
│  │   Desktop PC       │    │   Laptop           │    │   Mobile Device    ││
│  │                    │    │                    │    │                    ││
│  │  ┌──────────────┐  │    │  ┌──────────────┐  │    │  ┌──────────────┐  ││
│  │  │ Web Browser  │  │    │  │ Web Browser  │  │    │  │ Web Browser  │  ││
│  │  │ (Chrome/     │  │    │  │ (Firefox/    │  │    │  │ (Safari/     │  ││
│  │  │  Firefox)    │  │    │  │  Edge)       │  │    │  │  Chrome)     │  ││
│  │  └──────┬───────┘  │    │  └──────┬───────┘  │    │  └──────┬───────┘  ││
│  │         │          │    │         │          │    │         │          ││
│  └─────────┼──────────┘    └─────────┼──────────┘    └─────────┼──────────┘│
│            │                         │                         │            │
└────────────┼─────────────────────────┼─────────────────────────┼────────────┘
             │                         │                         │
             └─────────────────────────┼─────────────────────────┘
                                       │ HTTPS
                                       │ Port 443
┌──────────────────────────────────────▼──────────────────────────────────────┐
│                            WEB SERVER TIER                                   │
│                         ┌────────────────────┐                               │
│                         │  Nginx / Apache    │                               │
│                         │  Reverse Proxy     │                               │
│                         │                    │                               │
│                         │  • SSL Termination │                               │
│                         │  • Load Balancing  │                               │
│                         │  • Static Files    │                               │
│                         └──────────┬─────────┘                               │
│                                    │                                         │
└────────────────────────────────────┼─────────────────────────────────────────┘
                                     │ HTTP
                                     │ Port 5000
┌────────────────────────────────────▼─────────────────────────────────────────┐
│                        APPLICATION SERVER TIER                                │
│                                                                               │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │              Application Server (Gunicorn / uWSGI)                     │  │
│  │                                                                        │  │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐       │  │
│  │  │ Flask Worker 1  │  │ Flask Worker 2  │  │ Flask Worker 3  │       │  │
│  │  │                 │  │                 │  │                 │       │  │
│  │  │  ┌───────────┐  │  │  ┌───────────┐  │  │  ┌───────────┐  │       │  │
│  │  │  │  API      │  │  │  │  API      │  │  │  │  API      │  │       │  │
│  │  │  │  Routes   │  │  │  │  Routes   │  │  │  │  Routes   │  │       │  │
│  │  │  └───────────┘  │  │  └───────────┘  │  │  └───────────┘  │       │  │
│  │  │  ┌───────────┐  │  │  ┌───────────┐  │  │  ┌───────────┐  │       │  │
│  │  │  │ Business  │  │  │  │ Business  │  │  │  │ Business  │  │       │  │
│  │  │  │ Logic     │  │  │  │ Logic     │  │  │  │ Logic     │  │       │  │
│  │  │  └───────────┘  │  │  └───────────┘  │  │  └───────────┘  │       │  │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘       │  │
│  │                                                                        │  │
│  └────────────────────────────────────┬───────────────────────────────────┘  │
│                                       │                                      │
│  ┌────────────────────────────────────▼───────────────────────────────────┐ │
│  │                   ML Processing Engine                                  │ │
│  │                                                                         │ │
│  │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐     │ │
│  │  │ LSTM Forecaster  │  │ RL Pricing Agent │  │ Elasticity Calc  │     │ │
│  │  │                  │  │                  │  │                  │     │ │
│  │  │ • TensorFlow     │  │ • NumPy Q-Table  │  │ • Scikit-Learn   │     │ │
│  │  │ • Keras Models   │  │ • ε-greedy       │  │ • Linear Regress │     │ │
│  │  └──────────────────┘  └──────────────────┘  └──────────────────┘     │ │
│  │                                                                         │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
│                                       │                                      │
└───────────────────────────────────────┼──────────────────────────────────────┘
                                        │
                                        │ SQL Queries
                                        │
┌───────────────────────────────────────▼──────────────────────────────────────┐
│                          DATABASE SERVER TIER                                 │
│                                                                               │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                      Database Server                                   │  │
│  │                                                                        │  │
│  │  ┌──────────────────────────────────────────────────────────────────┐ │  │
│  │  │              SQLite / PostgreSQL / MySQL                          │ │  │
│  │  │                                                                   │ │  │
│  │  │  pricing_system.db                                                │ │  │
│  │  │                                                                   │ │  │
│  │  │  • products                  • sales_history                     │ │  │
│  │  │  • price_history             • demand_forecasts                  │ │  │
│  │  │  • competitor_prices         • users                             │ │  │
│  │  │  • shopping_cart             • system_settings                   │ │  │
│  │  │                                                                   │ │  │
│  │  └──────────────────────────────────────────────────────────────────┘ │  │
│  │                                                                        │  │
│  └────────────────────────────────────┬───────────────────────────────────┘  │
│                                       │                                      │
└───────────────────────────────────────┼──────────────────────────────────────┘
                                        │
                                        │ Backup
                                        │
┌───────────────────────────────────────▼──────────────────────────────────────┐
│                        BACKUP & STORAGE TIER                                  │
│                                                                               │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                    File Storage System                                 │  │
│  │                                                                        │  │
│  │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐    │  │
│  │  │ ML Model Files   │  │ Database Backups │  │ Log Files        │    │  │
│  │  │                  │  │                  │  │                  │    │  │
│  │  │ • lstm_model.h5  │  │ • Daily dumps    │  │ • app.log        │    │  │
│  │  │ • rl_agent.json  │  │ • Hourly txn log │  │ • error.log      │    │  │
│  │  │ • scaler.pkl     │  │                  │  │ • access.log     │    │  │
│  │  └──────────────────┘  └──────────────────┘  └──────────────────┘    │  │
│  │                                                                        │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                                                               │
└───────────────────────────────────────────────────────────────────────────────┘


┌───────────────────────────────────────────────────────────────────────────────┐
│                      EXTERNAL SERVICES (Optional)                              │
│                                                                                │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────────────┐  │
│  │ Monitoring      │  │ CDN Service     │  │ Competitor Price API        │  │
│  │ (Prometheus/    │  │ (CloudFront)    │  │ (External Data Source)      │  │
│  │  Grafana)       │  │                 │  │                             │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────────────────┘  │
│                                                                                │
└────────────────────────────────────────────────────────────────────────────────┘


DEPLOYMENT SPECIFICATIONS:

┌──────────────────────────────────────────────────────────────────┐
│ Development Environment                                          │
├──────────────────────────────────────────────────────────────────┤
│ • Local Machine (Windows/Mac/Linux)                              │
│ • Python 3.8+                                                    │
│ • Flask Development Server                                       │
│ • SQLite Database                                                │
│ • No reverse proxy                                               │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│ Production Environment                                           │
├──────────────────────────────────────────────────────────────────┤
│ • Cloud Server (AWS EC2 / DigitalOcean / Azure VM)              │
│ • Ubuntu Server 20.04 LTS                                        │
│ • Nginx (Reverse Proxy)                                          │
│ • Gunicorn (WSGI Server) - 3-5 workers                          │
│ • PostgreSQL / MySQL (for larger scale)                          │
│ • SSL/TLS Encryption (Let's Encrypt)                            │
│ • Firewall (UFW / Security Groups)                              │
└──────────────────────────────────────────────────────────────────┘
```

---

*This comprehensive UML documentation provides complete system design visualization for the AI-Driven Dynamic Pricing System.*
