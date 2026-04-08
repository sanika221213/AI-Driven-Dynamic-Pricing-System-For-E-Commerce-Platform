# 🚀 Quick Start Guide - E-Commerce Dynamic Pricing System

## ✅ System Overview

You now have a complete AI-powered e-commerce system with:
- **Customer Shopping Portal** with real-time dynamic pricing
- **4 Demo User Accounts** (3 customers + 1 admin)
- **Shopping Cart** with live price updates
- **Concurrent Purchase Simulation** 
- **Admin Dashboard** for monitoring and management

---

## 📋 Prerequisites

✅ **Python 3.8+** - Check with: `python --version`  
✅ **Dependencies Installed** - Already done!  
✅ **Backend Running** - Server on http://localhost:5000

---

## 🎮 How to Get Started (3 Steps)

### Step 1: Start the Backend (If not already running)

```bash
cd backend
python app.py
```

You should see:
```
============================================================
AI-Driven Dynamic Pricing System - Backend Server
============================================================
Starting Flask server on http://localhost:5000
```

**Keep this terminal open!**

---

### Step 2: Open the Application

Open `frontend/login.html` in your web browser:

**Windows:**
- Double-click `frontend/login.html`
- Or drag the file into your browser

**Or use the full path:**
- `C:\FreeLancing\dynamic-pricing-system\frontend\login.html`

---

### Step 3: Login with Demo Account

Use any of these accounts:

| Username | Password | Access |
|----------|----------|--------|
| **customer1** | password123 | Customer Shop |
| **customer2** | password123 | Customer Shop |
| **customer3** | password123 | Customer Shop |
| **admin** | admin123 | Admin Dashboard |

---

## 🛒 Testing Dynamic Pricing (3 Scenarios)

### Scenario A: Single User Shopping (Basic)

1. Login as `customer1`
2. Browse products on the shop page
3. Click on products to view details
4. Add items to cart
5. Open cart (🛒 icon)
6. Notice prices may change slightly

**What to observe:**
- Product view counts increase
- Prices update based on your activity

---

### Scenario B: Concurrent Users (Advanced)

**You'll need 3 browser windows/tabs:**

**Window 1:**
1. Open `frontend/login.html`
2. Login as `customer1`
3. Navigate to "Wireless Mouse" product

**Window 2:**
1. Open `frontend/login.html` (new window)
2. Login as `customer2`
3. Navigate to same "Wireless Mouse" product

**Window 3:**
1. Open `frontend/login.html` (new window)
2. Login as `customer3`
3. Navigate to same "Wireless Mouse" product

**In all windows (one by one):**
4. Add "Wireless Mouse" to cart
5. Watch the price increase with each addition!

**What to observe:**
- "X others viewing" indicator appears
- Price increases as more users view
- Bigger price jump when users add to cart
- Real-time price synchronization

---

### Scenario C: Automated Simulation (Easiest!)

1. Login as `admin` (admin/admin123)
2. Click "Simulation" in left sidebar
3. Select any product
4. Set "Number of Concurrent Users" to 3
5. Click "▶️ Run Simulation"
6. Watch the automated price progression!

**What you'll see:**
- Step-by-step price increases
- Concurrent user factors
- Cart addition impacts
- Final vs. initial price comparison

---

## 📊 Admin Dashboard Features

After logging in as **admin**:

### Dashboard (index.html)
- Revenue statistics
- Product count
- Sales metrics
- Quick optimization buttons

### Products (products.html)
- View all products
- Add new products
- Edit prices
- AI price optimization

### Analytics (analytics.html)
- Revenue charts
- Sales trends
- Category analysis

### Simulation (simulation.html)
- Run concurrent user demos
- Visual price progression
- Factor breakdowns

---

## 🎯 Key Features to Try

### 1. Price Changes Based on Activity
- **Search a product** → Price may increase
- **View a product** → View count increases
- **Add to cart** → Price increases more
- **Multiple users** → Significant price jumps

### 2. Shopping Cart
- Add multiple products
- Update quantities
- See price changes
- Checkout (demo mode)

### 3. Real-Time Updates
- Prices refresh every 10 seconds automatically
- Cart updates immediately
- Concurrent viewer counts update live

### 4. Admin Controls
- Optimize all prices with one click
- View detailed analytics
- Monitor competitor prices
- Configure pricing settings

---

## 📈 Understanding Dynamic Pricing

The system adjusts prices based on:

| Factor | Weight | Impact |
|--------|--------|--------|
| **Search Count** | 20% | More searches = higher price |
| **View Count** | 15% | More views = higher price |
| **Cart Additions** | 20% | High buying intent = higher price |
| **Concurrent Users** | 15% | Multiple viewers = scarcity pricing |
| **Demand Velocity** | 25% | Sales trends influence price |
| **Inventory** | 5% | Low stock = higher price |

**Example:**
- Base Price: $25.99
- 3 concurrent users viewing: +15%
- 10 cart additions (24h): +15%
- 30 searches (24h): +10%
- **New Price: ~$35.00** (35% increase!)

---

## 🔧 Customization

### Change Price Sensitivity

Edit `backend/models/dynamic_pricing_engine.py`:

```python
self.weights = {
    'demand_factor': 0.25,      # ← Change these
    'search_factor': 0.20,      # ← to adjust
    'cart_factor': 0.20,        # ← pricing
    'concurrent_factor': 0.15,  # ← sensitivity
}
```

### Change Auto-Refresh Rate

Edit `frontend/js/shop.js`:

```javascript
// Refresh every 10 seconds (10000 ms)
priceUpdateInterval = setInterval(refreshPrices, 10000);
```

---

## 🐛 Troubleshooting

### "Cannot connect to backend"
→ Make sure backend is running: `python backend/app.py`

### "Login failed"
→ Use correct credentials (username: customer1, password: password123)

### "Prices don't change"
→ Wait 10 seconds for auto-refresh, or refresh page manually

### Database errors
→ Delete `data/pricing_system.db` and restart backend (will regenerate)

---

## 📚 Documentation

- **Complete README**: `README_ECOMMERCE.md`
- **Original README**: `README.md`
- **API Reference**: See backend console output
- **Quick Setup**: `QUICKSTART.md`

---

## 🎓 What This Demonstrates

✅ Real-time dynamic pricing algorithms  
✅ Multi-user concurrent systems  
✅ Machine learning integration (LSTM, RL)  
✅ Full-stack e-commerce development  
✅ RESTful API design  
✅ Session management  
✅ Real-time data visualization  

---

## 🌟 Next Steps

1. **Try all 3 scenarios** above
2. **Explore the admin dashboard**
3. **Run simulations** with different products
4. **Customize pricing weights**
5. **Add your own products**

---

## 💡 Pro Tips

- Open browser console (F12) to see API calls
- Watch backend terminal for real-time logs
- Try adding the same product multiple times
- Compare prices between customer accounts
- Use simulation page to understand algorithm

---

## 🎉 You're All Set!

The system is ready to demonstrate AI-driven dynamic pricing in action.

**Start with Scenario C (Simulation)** for the easiest demonstration!

---

**Questions?** Check `README_ECOMMERCE.md` for detailed documentation.

**Happy Testing! 🚀**
