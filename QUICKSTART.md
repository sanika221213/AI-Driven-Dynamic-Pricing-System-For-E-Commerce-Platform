# 🚀 Quick Start Guide

## AI-Driven Dynamic Pricing System

### Setup in 3 Easy Steps

---

## Step 1: Install Dependencies

Open PowerShell/Terminal in the project directory:

```powershell
pip install -r requirements.txt
```

**Required packages:**
- Flask (Web framework)
- TensorFlow (Deep learning)
- Scikit-learn (Machine learning)
- NumPy & Pandas (Data processing)

---

## Step 2: Start the Backend Server

```powershell
cd backend
python app.py
```

You should see:
```
AI-Driven Dynamic Pricing System - Backend Server
Starting Flask server on http://localhost:5000
```

**Keep this terminal window open!**

---

## Step 3: Open the Frontend

**Option A: Direct File Access**
- Navigate to the `frontend` folder
- Double-click `index.html`

**Option B: Local Web Server (Recommended)**
```powershell
cd frontend
python -m http.server 8000
```
Then open: `http://localhost:8000`

---

## First Time Usage

1. **Dashboard will load** - You'll see the main interface

2. **Generate Sample Data**:
   - Click the "Generate Sample Data" button
   - Wait 5-10 seconds for data creation
   - Page will refresh automatically

3. **Explore Features**:
   - **Dashboard**: View metrics and revenue trends
   - **Products**: Manage products and optimize prices
   - **Analytics**: View detailed performance reports
   - **Competitors**: Track competitor pricing
   - **Settings**: Configure AI behavior

---

## Key Features to Try

### 🎯 AI Price Optimization

1. Go to **Products** page
2. Click **🪄 Optimize** button on any product
3. View AI recommendation
4. Apply the optimized price

### 📊 Batch Optimization

1. Click **Optimize All Prices** button
2. See suggestions for all products
3. Apply changes in one click

### 📈 Analytics Dashboard

- View revenue trends (last 7 days)
- Track product performance
- Monitor sales metrics

### 👥 Competitor Monitoring

1. Go to **Competitors** page
2. Select a product
3. Add competitor prices
4. Get AI pricing recommendations

---

## System Architecture

```
┌─────────────────────────────────────────────┐
│         Frontend (HTML/CSS/JS)              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │Dashboard │  │Products  │  │Analytics │ │
│  └──────────┘  └──────────┘  └──────────┘ │
└────────────────┬────────────────────────────┘
                 │ REST API
┌────────────────▼────────────────────────────┐
│      Backend (Python/Flask)                 │
│  ┌──────────────┐  ┌──────────────┐        │
│  │ LSTM Forecast│  │ RL Agent     │        │
│  └──────────────┘  └──────────────┘        │
│  ┌──────────────┐  ┌──────────────┐        │
│  │ Elasticity   │  │ Database     │        │
│  └──────────────┘  └──────────────┘        │
└─────────────────────────────────────────────┘
```

---

## Research Implementation

This system implements:

✅ **LSTM Time-Series Forecasting**
- Predicts future demand
- 30-day lookback window
- Seasonality detection

✅ **Reinforcement Learning (RL)**
- Contextual Bandit algorithm
- ε-greedy exploration (20%)
- Q-Learning optimization

✅ **Price Elasticity Analysis**
- Demand response estimation
- Revenue optimization
- Constraint satisfaction

✅ **Competitor Intelligence**
- Real-time price tracking
- Market position analysis
- Adaptive pricing

---

## Troubleshooting

### ❌ Backend won't start

**Problem**: Port 5000 already in use
**Solution**: 
```powershell
# Use different port
flask run --port 5001
```
Update `frontend/js/config.js` with new port.

### ❌ Import errors

**Problem**: Missing packages
**Solution**:
```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

### ❌ No data showing

**Problem**: Database not initialized
**Solution**:
1. Click "Generate Sample Data" on Dashboard
2. Wait for completion
3. Refresh page

### ❌ CORS errors in browser

**Problem**: Frontend can't connect to backend
**Solution**:
- Ensure backend is running
- Check console for exact error
- Verify URL in `config.js` matches backend

---

## Configuration

### Adjust AI Behavior

Go to **Settings** page to configure:

- **Pricing Strategy**: Aggressive/Balanced/Conservative
- **Exploration Rate**: 0-100% (default 20%)
- **Min Margin**: Minimum profit percentage
- **Max Discount**: Maximum price reduction
- **Update Frequency**: How often to recalculate

### Business Rules

Set constraints to ensure:
- Minimum profit margins
- Maximum price changes
- Inventory-aware pricing
- Competitor-based limits

---

## API Endpoints

Test the API directly:

```bash
# Health check
curl http://localhost:5000/api/health

# Get products
curl http://localhost:5000/api/products

# Get dashboard stats
curl http://localhost:5000/api/analytics/dashboard

# Optimize product price
curl -X POST http://localhost:5000/api/pricing/optimize/1
```

---

## Expected Results

Based on research paper findings:

📈 **Revenue Growth**: +22% vs static pricing
📊 **Conversion Rate**: +18% improvement
⚡ **Adaptability**: Real-time market response
⚖️ **Balance**: Profit + Customer satisfaction

---

## Next Steps

1. **Add Your Products**: Replace sample data with real products
2. **Import Sales History**: Load historical sales data
3. **Configure Competitors**: Add competitor price tracking
4. **Adjust Settings**: Fine-tune AI parameters
5. **Monitor Performance**: Track metrics over time

---

## Support

📖 **Full Documentation**: See `README.md`
🔧 **Technical Details**: Check research paper PDF
💻 **Code Structure**: Review inline comments

---

## Technology Stack

| Component | Technology |
|-----------|------------|
| Backend | Python 3.8+, Flask |
| ML/AI | TensorFlow, Keras, Scikit-learn |
| Database | SQLite |
| Frontend | HTML5, CSS3, JavaScript |
| Visualization | Chart.js |
| Design | Responsive, Mobile-friendly |

---

## Success Checklist

- [ ] Backend server running on port 5000
- [ ] Frontend accessible in browser
- [ ] Sample data generated successfully
- [ ] Can view dashboard metrics
- [ ] AI optimization works on products
- [ ] Analytics charts display correctly
- [ ] Competitor prices can be added
- [ ] Settings save successfully

---

**🎉 You're all set! Start optimizing prices with AI!**

For detailed information, refer to the complete README.md documentation.
