# 🎯 AI-Driven Dynamic Pricing E-Commerce System

A complete e-commerce platform with AI-powered real-time dynamic pricing that adjusts based on demand, search patterns, user behavior, and concurrent activity.

## 🌟 Key Features

### Customer-Facing Features
- **Multi-User Shopping Experience** - 4 pre-configured user accounts (3 customers + 1 admin)
- **Real-Time Dynamic Pricing** - Prices change based on:
  - Product searches and views
  - Shopping cart additions
  - Concurrent users viewing the same product
  - Purchase trends and demand
  - Inventory levels
- **Shopping Cart System** - Full cart functionality with real-time price updates
- **Concurrent Purchase Simulation** - Visual demonstration of how prices change when multiple users interact simultaneously

### Admin Features
- **Price Monitoring Dashboard** - Real-time tracking of all price changes
- **Product Management** - CRUD operations for products
- **Analytics & Reporting** - Revenue tracking, sales trends, performance metrics
- **Competitor Monitoring** - Track and respond to competitor pricing
- **AI Optimization** - LSTM forecasting + Reinforcement Learning pricing agents
- **Simulation Tool** - Demonstrate dynamic pricing with configurable scenarios

## 🏗️ Architecture

### Backend (Python/Flask)
- **Dynamic Pricing Engine** - Real-time price calculation based on 6 factors:
  - Demand velocity (sales trends)
  - Search frequency
  - Product views
  - Cart additions
  - Concurrent users
  - Inventory levels
- **Machine Learning Models**:
  - LSTM neural network for demand forecasting
  - Contextual Bandit (ε-greedy) for price optimization
  - Price elasticity calculator
- **RESTful API** - 25+ endpoints for all operations
- **SQLite Database** - 12 tables including users, carts, searches, views, sessions

### Frontend (HTML/CSS/JavaScript)
- **Login Page** - Authentication with demo accounts
- **Customer Shop** - E-commerce interface with real-time pricing
- **Shopping Cart** - Modal-based cart with quantity management
- **Admin Dashboard** - Metrics, charts, and quick actions
- **Product Management** - Full CRUD interface
- **Analytics** - Charts and reports
- **Competitor Tracking** - Price comparison and insights
- **Simulation Page** - Visual demonstration of concurrent purchase scenarios
- **Settings** - Configuration for pricing algorithms

## 📋 Database Schema

### New Tables for E-Commerce
```sql
users               -- Customer & admin accounts
shopping_cart       -- User shopping carts
product_searches    -- Search tracking for pricing
product_views       -- View tracking for pricing
active_sessions     -- Concurrent user tracking
```

### Original Tables
```sql
products            -- Product catalog with pricing
sales_history       -- Historical sales data
price_history       -- Price change tracking
competitor_prices   -- Competitor monitoring
demand_forecasts    -- LSTM predictions
system_settings     -- Configuration
performance_metrics -- Analytics
```

## 🚀 Quick Start

### Option 1: Automated Setup
```bash
python start.py
```

### Option 2: Manual Setup

1. **Install Dependencies**
```bash
pip install Flask Flask-CORS tensorflow keras scikit-learn numpy pandas
```

2. **Start Backend**
```bash
cd backend
python app.py
```
Server runs on `http://localhost:5000`

3. **Open Frontend**
Open `frontend/login.html` in your browser

## 👥 Demo Accounts

| Username | Password | Role | Purpose |
|----------|----------|------|---------|
| customer1 | password123 | Customer | Shopping user 1 |
| customer2 | password123 | Customer | Shopping user 2 |
| customer3 | password123 | Customer | Shopping user 3 |
| admin | admin123 | Admin | Dashboard access |

## 🎮 How to Use

### Customer Experience

1. **Login** - Use any customer account (customer1, customer2, customer3)
2. **Browse Products** - View real-time prices that change based on activity
3. **View Engagement** - See how many other users are viewing the same product
4. **Add to Cart** - Watch prices increase as demand grows
5. **Checkout** - Complete purchase (demo mode)

### Concurrent Purchase Demo

1. **Open Multiple Windows** - Login with different accounts in separate browser windows
2. **View Same Product** - Navigate to the same product across windows
3. **Watch Price Change** - See price increase as concurrent viewers grow
4. **Add to Cart** - Observe price jumps when multiple users add to cart

### Admin Dashboard

1. **Login as Admin** - Use admin/admin123
2. **Monitor Pricing** - Track all price changes in real-time
3. **Run Simulation** - Click "Simulation" to see automated demo
4. **Manage Products** - Add, edit, or optimize product prices
5. **View Analytics** - Track revenue, sales, and performance

### Simulation Tool

1. **Navigate to Simulation** - From admin dashboard or directly
2. **Select Product** - Choose any product from dropdown
3. **Set User Count** - Configure 2-5 concurrent users
4. **Run Simulation** - Watch automated price progression
5. **Analyze Results** - See step-by-step price changes with factors

## 📊 API Endpoints

### Authentication
```
POST /api/auth/login          - User login
POST /api/auth/register       - User registration
GET  /api/users               - Get all users
```

### Shopping Cart
```
GET    /api/cart/<user_id>           - Get user's cart
POST   /api/cart/add                 - Add item to cart
DELETE /api/cart/remove/<cart_id>    - Remove item
PUT    /api/cart/update               - Update quantity
DELETE /api/cart/clear/<user_id>     - Clear cart
```

### Product Tracking
```
POST /api/products/<id>/track/search - Track product search
POST /api/products/<id>/track/view   - Track product view
GET  /api/products/<id>/engagement   - Get engagement stats
```

### Dynamic Pricing
```
GET  /api/pricing/dynamic/<id>              - Get real-time price
POST /api/pricing/update-all                - Update all prices
POST /api/simulation/concurrent-purchase    - Run simulation
```

### Product Management
```
GET    /api/products           - Get all products
POST   /api/products           - Add new product
PUT    /api/products/<id>      - Update product
```

## 🧮 Dynamic Pricing Algorithm

### Price Calculation Formula
```
New Price = Base Price × (1 + Weighted Factors)

Weighted Factors:
- Demand Factor (25%)    - Sales velocity trends
- Search Factor (20%)    - Search frequency
- View Factor (15%)      - Product view count
- Cart Factor (20%)      - Cart additions
- Concurrent Factor (15%) - Simultaneous users
- Inventory Factor (5%)   - Stock levels
```

### Factor Calculations

**Demand Factor** (based on sales velocity):
- 0 sales/day: -10% (decrease price)
- 5-15 sales/day: +10%
- 15+ sales/day: +20% (high demand)

**Search Factor** (24-hour window):
- 0 searches: -5%
- 10-30 searches: +5%
- 50+ searches: +15% (high interest)

**Cart Factor** (24-hour window):
- 0 carts: 0%
- 5-10 carts: +10%
- 10+ carts: +15% (very high intent)

**Concurrent Factor** (5-minute window):
- 1 user: 0%
- 2 users: +5%
- 3+ users: +15% (scarcity signal)

**Inventory Factor**:
- <10 units: +10% (low stock)
- 10-50 units: 0%
- 50+ units: -10% (clear inventory)

## 🎯 Use Cases Demonstrated

### 1. Demand-Based Pricing
Products with higher search/view counts automatically increase in price

### 2. Scarcity Pricing
When multiple users view simultaneously, price increases to reflect demand

### 3. Inventory Clearance
High inventory items get price reductions

### 4. Flash Sales Effect
Low inventory + high views = significant price increase

### 5. Concurrent Purchase Competition
Multiple users adding to cart triggers rapid price increases

## 🔧 Configuration

### Adjust Pricing Weights
Edit `backend/models/dynamic_pricing_engine.py`:
```python
self.weights = {
    'demand_factor': 0.25,      # Adjust these
    'search_factor': 0.20,      # values to
    'cart_factor': 0.20,        # change pricing
    'concurrent_factor': 0.15,  # sensitivity
    ...
}
```

### Change Price Refresh Rate
Edit `frontend/js/shop.js`:
```javascript
// Auto-refresh prices every 10 seconds
priceUpdateInterval = setInterval(refreshPrices, 10000); // milliseconds
```

## 📁 Project Structure

```
dynamic-pricing-system/
├── backend/
│   ├── app.py                          # Flask API server (25+ endpoints)
│   ├── database.py                     # Database manager with all CRUD
│   └── models/
│       ├── dynamic_pricing_engine.py   # Real-time pricing engine ⭐
│       ├── lstm_forecaster.py          # Demand forecasting
│       ├── reinforcement_learning.py   # RL pricing agent
│       └── price_elasticity.py         # Elasticity calculator
├── frontend/
│   ├── login.html                      # Authentication page ⭐
│   ├── shop.html                       # Customer e-commerce page ⭐
│   ├── simulation.html                 # Concurrent purchase demo ⭐
│   ├── index.html                      # Admin dashboard
│   ├── products.html                   # Product management
│   ├── analytics.html                  # Analytics & reports
│   ├── competitors.html                # Competitor tracking
│   ├── settings.html                   # Configuration
│   ├── css/
│   │   └── style.css                   # Complete styling
│   └── js/
│       ├── config.js                   # API configuration
│       ├── api.js                      # API helpers
│       ├── shop.js                     # Customer page logic ⭐
│       ├── simulation.js               # Simulation logic ⭐
│       ├── dashboard.js                # Dashboard logic
│       ├── products.js                 # Product management
│       ├── analytics.js                # Analytics logic
│       ├── competitors.js              # Competitor tracking
│       └── settings.js                 # Settings management
├── data/
│   └── pricing_system.db               # SQLite database (auto-created)
├── requirements.txt                    # Python dependencies
├── start.py                            # Automated setup script
└── README.md                           # This file
```

⭐ = New files for e-commerce functionality

## 🧪 Testing Scenarios

### Scenario 1: Single User Shopping
1. Login as customer1
2. Browse products
3. Add items to cart
4. Observe price stability

### Scenario 2: Concurrent Users (Manual)
1. Open 3 browser windows
2. Login with customer1, customer2, customer3
3. All navigate to same product
4. Watch price increase
5. All add to cart
6. See cumulative price jump

### Scenario 3: Automated Simulation
1. Login as admin
2. Navigate to Simulation page
3. Select product
4. Set 3 concurrent users
5. Run simulation
6. Analyze step-by-step price changes

### Scenario 4: Search Impact
1. Login as customer
2. Search for product multiple times
3. Refresh page
4. See price increase from search activity

## 📝 Technical Details

### Price Update Triggers
Prices are recalculated when:
- Product is viewed
- Product is searched
- Product is added to cart
- User starts/ends session
- Manual "Update All Prices" is clicked
- 10-second auto-refresh (frontend)

### Session Tracking
Active sessions are tracked for 5 minutes. Users are considered "concurrent" if their sessions overlap within this window.

### Data Persistence
All interactions (searches, views, cart additions) are stored in the database and factor into future price calculations.

## 🔍 Troubleshooting

### Backend won't start
```bash
# Check Python version (3.8+ required)
python --version

# Reinstall dependencies
pip install -r requirements.txt --no-cache-dir
```

### Prices don't change
- Check backend console for errors
- Verify API calls in browser console (F12)
- Ensure database has sample data (run generate_sample_data)

### Login doesn't work
- Verify backend is running on port 5000
- Check CORS is enabled
- Open browser console to see error messages

## 📚 Technologies Used

- **Backend**: Python 3.8+, Flask 2.3.3, SQLite3
- **Machine Learning**: TensorFlow 2.13+, Keras, Scikit-learn
- **Frontend**: HTML5, CSS3, JavaScript ES6+
- **Charts**: Chart.js
- **Architecture**: RESTful API, MVC pattern

## 🎓 Learning Outcomes

This project demonstrates:
1. Real-time dynamic pricing algorithms
2. Multi-user concurrent system design
3. Machine learning integration (LSTM, RL)
4. Full-stack web development
5. RESTful API design
6. Database design for e-commerce
7. User session management
8. Real-time data visualization

## 📄 License

This is a demonstration/educational project.

## 👨‍💻 Author

Created for dynamic pricing research and demonstration purposes.

---

**Note**: This is a demonstration system. For production use, add:
- Secure password hashing (bcrypt)
- JWT authentication tokens
- Payment gateway integration
- SSL/HTTPS
- Rate limiting
- Input validation
- Error logging
- Database backups
