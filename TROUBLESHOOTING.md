# 🔧 Troubleshooting Guide

## Common Issues and Solutions

---

## ❌ CORS Error: "Access blocked by CORS policy"

**Error Message:**
```
Access to fetch at 'http://localhost:5000/auth/login' from origin 'http://localhost:8000' 
has been blocked by CORS policy
```

### **Problem:**
Your frontend is trying to access the backend from a different origin (port), and CORS (Cross-Origin Resource Sharing) is blocking it.

### **Solution:**

#### Option 1: Open Frontend Directly (Recommended)
**Instead of using a local server, open the HTML file directly:**

1. **Close any local server** (like `python -m http.server`)
2. **Navigate to your project folder**
3. **Double-click** `frontend/login.html`
4. Or **drag and drop** `login.html` into your browser

This will use the `file://` protocol which bypasses CORS issues.

#### Option 2: Restart Backend Server
If you modified the CORS settings:

1. **Stop the backend** (Ctrl+C in the terminal)
2. **Restart it:**
```bash
cd backend
python app.py
```

#### Option 3: Use the Correct URL
Make sure your `frontend/js/config.js` has:
```javascript
const API_BASE_URL = 'http://localhost:5000/api';
```

#### Option 4: Serve Frontend from Backend
**Add static file serving to Flask:**

```python
# In backend/app.py, add:
@app.route('/')
def serve_frontend():
    return app.send_static_file('login.html')
```

Then access via: `http://localhost:5000/login.html`

---

## ❌ "Cannot connect to backend" / Network Error

### **Problem:**
Frontend cannot reach the backend server.

### **Solution:**

1. **Check if backend is running:**
```bash
# You should see this output:
Starting Flask server on http://localhost:5000
```

2. **Test backend directly:**
Open browser and go to: `http://localhost:5000/api/health`

You should see: `{"status": "healthy"}`

3. **Check port 5000 is not blocked:**
```powershell
# Windows PowerShell
netstat -ano | findstr :5000
```

4. **Restart backend:**
```bash
cd backend
python app.py
```

---

## ❌ "Login Failed" / Invalid Credentials

### **Problem:**
Cannot login with demo accounts.

### **Solution:**

1. **Use correct credentials:**
   - Username: `customer1` (lowercase)
   - Password: `password123`

2. **Check backend logs** - Should show login attempt

3. **Regenerate database:**
```bash
# Delete old database
del data\pricing_system.db

# Restart backend (will regenerate)
cd backend
python app.py
```

4. **Manually create users via Python:**
```python
from backend.database import DatabaseManager
import hashlib

db = DatabaseManager()
password = hashlib.sha256('password123'.encode()).hexdigest()
db.create_user('customer1', 'customer1@example.com', password, 'Customer One', 0)
```

---

## ❌ Backend Won't Start / Import Errors

### **Problem:**
```
ModuleNotFoundError: No module named 'flask'
```

### **Solution:**

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Or install manually:**
```bash
pip install Flask Flask-CORS tensorflow keras scikit-learn numpy pandas
```

3. **Check Python version:**
```bash
python --version
# Should be 3.8 or higher
```

4. **Use pip with Python:**
```bash
python -m pip install -r requirements.txt
```

---

## ❌ Prices Don't Change

### **Problem:**
Prices remain static even with user activity.

### **Solution:**

1. **Wait for auto-refresh** (10 seconds)

2. **Manually refresh page** (F5)

3. **Check backend logs** for price calculations

4. **Trigger update manually:**
   - Click "Optimize Price" in admin dashboard
   - Or call: `POST /api/pricing/update-all`

5. **Verify activity is tracked:**
```python
# Check in backend terminal for messages like:
"Tracking product view"
"Product added to cart"
```

---

## ❌ Shopping Cart Empty After Adding

### **Problem:**
Items disappear from cart.

### **Solution:**

1. **Check localStorage:**
```javascript
// In browser console (F12):
localStorage.getItem('user')
```

2. **Verify user is logged in:**
   - Top right should show username
   - Cart badge should show count

3. **Check API response:**
```javascript
// In browser console (F12) → Network tab
// Look for /api/cart/add request
// Check response status
```

4. **Clear cache and reload:**
   - Ctrl+Shift+R (hard reload)
   - Or clear browser cache

---

## ❌ Database Errors

### **Problem:**
```
sqlite3.OperationalError: no such table: users
```

### **Solution:**

1. **Delete and regenerate database:**
```bash
# Windows
del data\pricing_system.db

# Linux/Mac
rm data/pricing_system.db

# Restart backend
python backend/app.py
```

2. **Manually initialize:**
```python
from backend.database import DatabaseManager

db = DatabaseManager()
db.init_database()
db.generate_sample_data()
```

---

## ❌ Simulation Page Not Loading

### **Problem:**
Simulation page shows errors.

### **Solution:**

1. **Verify API endpoint exists:**
```bash
# Check backend logs for:
POST /api/simulation/concurrent-purchase/<id>
```

2. **Test endpoint directly:**
```bash
curl -X POST http://localhost:5000/api/simulation/concurrent-purchase/1 \
  -H "Content-Type: application/json" \
  -d '{"num_users": 3}'
```

3. **Check JavaScript console** (F12) for errors

---

## ❌ Port Already in Use

### **Problem:**
```
OSError: [Errno 48] Address already in use
```

### **Solution:**

1. **Find process using port 5000:**
```powershell
# Windows
netstat -ano | findstr :5000
taskkill /PID <process_id> /F
```

2. **Use different port:**
```python
# In backend/app.py, change last line:
app.run(host='0.0.0.0', port=5001, debug=True)
```

Then update `frontend/js/config.js`:
```javascript
const API_BASE_URL = 'http://localhost:5001/api';
```

---

## ❌ Charts Not Displaying

### **Problem:**
Dashboard/analytics charts don't show.

### **Solution:**

1. **Check Chart.js is loaded:**
```html
<!-- Should be in HTML file: -->
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
```

2. **Check browser console** (F12) for errors

3. **Verify data is returned:**
```javascript
// In browser console:
fetch('http://localhost:5000/api/analytics/dashboard')
  .then(r => r.json())
  .then(console.log)
```

---

## 🔍 Debugging Tips

### **1. Browser Console (F12)**
- **Console tab:** See JavaScript errors
- **Network tab:** View API requests/responses
- **Application tab:** Check localStorage

### **2. Backend Logs**
Watch the terminal running `python app.py`:
```
127.0.0.1 - - [04/Jan/2026 16:33:45] "POST /api/auth/login HTTP/1.1" 200
```

### **3. Test API Directly**
Use browser or curl:
```bash
# Test health endpoint
curl http://localhost:5000/api/health

# Test login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"customer1","password":"password123"}'
```

### **4. Check File Paths**
Ensure you're in the correct directory:
```bash
# Should see:
# backend/
# frontend/
# data/
# etc.
```

---

## 📞 Quick Fixes

### Reset Everything:
```bash
# 1. Stop backend (Ctrl+C)
# 2. Delete database
del data\pricing_system.db

# 3. Restart backend
cd backend
python app.py

# 4. Hard reload frontend (Ctrl+Shift+R)
```

### Fresh Start:
```bash
# 1. Close all browser windows
# 2. Stop backend
# 3. Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# 4. Delete database
del data\pricing_system.db

# 5. Start backend
python backend/app.py

# 6. Open frontend/login.html in browser
```

---

## ✅ Verification Checklist

Before reporting issues, verify:

- [ ] Backend is running (`python backend/app.py`)
- [ ] Backend shows: "Starting Flask server on http://localhost:5000"
- [ ] Can access: http://localhost:5000/api/health
- [ ] Frontend opened correctly (not from localhost:8000 if causing CORS issues)
- [ ] Browser console (F12) checked for errors
- [ ] Correct credentials used (customer1/password123)
- [ ] Database file exists: `data/pricing_system.db`
- [ ] Python 3.8+ installed
- [ ] All dependencies installed

---

## 🆘 Still Having Issues?

1. **Check backend terminal** for error messages
2. **Check browser console** (F12) for JavaScript errors
3. **Try the "Fresh Start" steps above**
4. **Review GETTING_STARTED.md** for proper setup

---

## 📝 Common Configuration Issues

### Config.js Wrong URL:
```javascript
// ❌ WRONG
const API_BASE_URL = 'http://localhost:5000';

// ✅ CORRECT
const API_BASE_URL = 'http://localhost:5000/api';
```

### Opening from Wrong Location:
```
❌ WRONG: http://localhost:8000/login.html (causes CORS)
✅ CORRECT: file:///C:/FreeLancing/dynamic-pricing-system/frontend/login.html
```

### Backend Not in Debug Mode:
```python
# Make sure app.py ends with:
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    #                                  ^^^^^^^^^^^^
```

---

**Most issues are solved by:**
1. ✅ Opening HTML files directly (not via localhost:8000)
2. ✅ Making sure backend is running
3. ✅ Using correct credentials
4. ✅ Hard refreshing browser (Ctrl+Shift+R)
