# AI-Driven Dynamic Pricing System for E-commerce Platforms

## Overview

This is a complete implementation of an AI-powered dynamic pricing system based on academic research. The system uses machine learning techniques including LSTM neural networks for demand forecasting and Reinforcement Learning for optimal pricing decisions.

## Research Implementation

This project implements the methodology from the research paper "AI-Driven Dynamic Pricing System for E-commerce Platforms" including:

### Core Components

1. **LSTM Demand Forecasting**
   - Time-series analysis of historical sales data
   - Predicts future demand patterns
   - Accounts for seasonality and trends

2. **Reinforcement Learning Pricing Agent**
   - Contextual Bandit (ε-greedy) algorithm
   - Q-Learning for price optimization
   - Balances exploration (20%) and exploitation (80%)

3. **Price Elasticity Calculator**
   - Estimates demand response to price changes
   - Calculates optimal revenue-maximizing prices

4. **Competitor Monitoring**
   - Track competitor prices in real-time
   - Adaptive pricing based on market position

## Project Structure

```
dynamic-pricing-system/
├── backend/
│   ├── app.py                      # Flask API server
│   ├── database.py                 # Database manager (SQLite)
│   ├── models/
│   │   ├── lstm_forecaster.py     # LSTM demand forecasting
│   │   ├── reinforcement_learning.py  # RL pricing agent
│   │   └── price_elasticity.py    # Elasticity calculator
│   └── utils/
├── frontend/
│   ├── index.html                 # Dashboard
│   ├── products.html              # Product management
│   ├── analytics.html             # Analytics & reporting
│   ├── competitors.html           # Competitor monitoring
│   ├── settings.html              # System settings
│   ├── css/
│   │   └── style.css             # Main stylesheet
│   └── js/
│       ├── config.js             # API configuration
│       ├── api.js                # API helper functions
│       ├── dashboard.js          # Dashboard logic
│       ├── products.js           # Product management
│       ├── analytics.js          # Analytics visualization
│       ├── competitors.js        # Competitor tracking
│       └── settings.js           # Settings management
├── data/
│   └── pricing_system.db         # SQLite database (auto-created)
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- Modern web browser (Chrome, Firefox, Edge)

### Step 1: Install Python Dependencies

```bash
# Navigate to project directory
cd dynamic-pricing-system

# Install required packages
pip install -r requirements.txt
```

### Step 2: Start the Backend Server

```bash
# Navigate to backend directory
cd backend

# Run Flask server
python app.py
```

The server will start on `http://localhost:5000`

### Step 3: Open the Frontend

Open `frontend/index.html` in your web browser, or use a local server:

```bash
# Using Python's built-in HTTP server
cd frontend
python -m http.server 8000
```

Then navigate to `http://localhost:8000` in your browser.

### Step 4: Initialize Sample Data

1. Open the application in your browser
2. Go to Dashboard
3. Click "Generate Sample Data" button
4. Wait for sample products and sales history to be created

## Features

### 1. Dashboard
- Real-time revenue and sales metrics
- Product performance overview
- Revenue trend visualization
- Quick actions for price optimization

### 2. Product Management
- Add/edit products
- View inventory levels
- Manual price adjustments
- AI-powered price optimization per product
- Batch optimization for all products

### 3. Analytics
- Revenue and sales trends
- Product performance rankings
- Category-wise revenue breakdown
- Sales history with detailed metrics
- Exportable reports

### 4. Competitor Monitoring
- Track competitor prices
- Price comparison visualization
- Market position analysis
- AI-powered pricing recommendations based on competition

### 5. Settings
- Configure AI pricing strategy (Aggressive/Balanced/Conservative)
- Set business rules (margins, discounts)
- Adjust ML model parameters
- Configure notification preferences

## AI Methodology

### Demand Forecasting (LSTM)

The system uses Long Short-Term Memory neural networks to predict future demand:

```python
Model Architecture:
- LSTM Layer 1: 64 units
- Dropout: 0.2
- LSTM Layer 2: 32 units
- Dropout: 0.2
- Dense Layer: 32 units (ReLU)
- Output Layer: 1 unit (demand prediction)
```

### Reinforcement Learning (Contextual Bandit)

Pricing decisions use ε-greedy exploration:

- **Exploration (20%)**: Try new pricing strategies
- **Exploitation (80%)**: Use best-known pricing strategies
- **State Features**: demand_level, inventory_level, competitor_ratio, seasonality
- **Actions**: Price multipliers from 0.7x to 1.3x base price
- **Reward**: Revenue improvement percentage

### Price Optimization Workflow

1. **Collect Data**: Historical sales, competitor prices, inventory
2. **Forecast Demand**: LSTM predicts future demand at different price points
3. **Estimate Elasticity**: Calculate demand response to price changes
4. **RL Decision**: Agent selects optimal price multiplier
5. **Apply Constraints**: Ensure business rules (min margin, max discount)
6. **Update Price**: Deploy new price to platform
7. **Learn**: Update model based on actual sales performance

## API Endpoints

### Products
- `GET /api/products` - Get all products
- `POST /api/products` - Add new product
- `PUT /api/products/<id>/price` - Update product price

### Pricing
- `POST /api/pricing/optimize/<id>` - Optimize single product
- `POST /api/pricing/batch-optimize` - Optimize all products

### Analytics
- `GET /api/analytics/revenue?days=30` - Revenue analytics
- `GET /api/analytics/product/<id>?days=30` - Product performance
- `GET /api/analytics/dashboard` - Dashboard statistics

### Competitors
- `GET /api/competitors/<id>?days=7` - Competitor prices
- `POST /api/competitors` - Add competitor price

### Settings
- `GET /api/settings` - Get system settings
- `POST /api/settings` - Update settings

## Research Paper Implementation Notes

This system implements the following concepts from the research:

✅ **LSTM Demand Forecasting** - Implemented with configurable lookback window
✅ **Reinforcement Learning** - Contextual Bandit with ε-greedy exploration
✅ **Price Elasticity** - Regression-based elasticity estimation
✅ **Competitor Monitoring** - Real-time price tracking and comparison
✅ **Business Constraints** - Min margin, max discount, inventory-aware pricing
✅ **Fairness & Transparency** - Explainable pricing decisions
✅ **Scalability** - Stateless API design, efficient database queries
✅ **Performance Metrics** - Revenue growth, conversion rate, adaptability

## Performance Expectations

Based on the research paper, the system achieves:

- **22% revenue growth** vs. static pricing
- **18% conversion rate improvement** vs. rule-based pricing
- **Real-time adaptability** to market changes
- **Balanced profitability and customer satisfaction**

## Configuration

Key settings can be adjusted in `frontend/settings.html`:

- **Pricing Strategy**: Aggressive/Balanced/Conservative
- **Exploration Rate**: 0-100% (default 20%)
- **Min Profit Margin**: Ensure minimum profitability
- **Update Frequency**: How often to recalculate prices
- **RL Algorithm**: Bandit/Q-Learning/DQN

## Troubleshooting

### Backend won't start
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.8+)
- Verify port 5000 is not in use

### Frontend can't connect to backend
- Ensure backend is running on `http://localhost:5000`
- Check browser console for CORS errors
- Verify API_BASE_URL in `frontend/js/config.js`

### No data showing
- Click "Generate Sample Data" on Dashboard
- Wait for initialization to complete
- Refresh the page

## Future Enhancements

Potential improvements based on research directions:

- Explainable AI visualizations for pricing decisions
- Blockchain integration for transparent pricing records
- Advanced fairness-aware pricing models
- Integration with real e-commerce platforms
- A/B testing framework
- Mobile application

## Technology Stack

**Backend:**
- Python 3.8+
- Flask (Web framework)
- TensorFlow/Keras (Deep learning)
- Scikit-learn (ML algorithms)
- SQLite (Database)

**Frontend:**
- HTML5, CSS3, JavaScript (ES6+)
- Chart.js (Data visualization)
- Font Awesome (Icons)
- Responsive design (Mobile-friendly)

## License

This project is created for educational and research purposes.

## Credits

Based on research methodology from:
"AI-Driven Dynamic Pricing System for E-commerce Platforms"
Authors: Miss. Shrushti Pawar, Miss. Anisha
Guide: Prof. N. R. Shinde
Shivaji University, Kolhapur (2025-2026)

## Contact

For questions or support, please refer to the research paper documentation.

---

**Version:** 1.0.0  
**Last Updated:** January 2026
