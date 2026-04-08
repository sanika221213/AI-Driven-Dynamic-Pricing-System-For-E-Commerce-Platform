"""
Database Manager for Dynamic Pricing System
Handles all data storage and retrieval operations
"""

import sqlite3
import json
import pandas as pd
from datetime import datetime, timedelta
import os


class DatabaseManager:
    """
    Manages all database operations for the dynamic pricing system
    """
    
    def __init__(self, db_path='data/pricing_system.db'):
        """Initialize database connection"""
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.init_database()
    
    def get_connection(self):
        """Get database connection with timeout and WAL mode for better concurrency"""
        conn = sqlite3.connect(self.db_path, timeout=30)
        conn.execute('PRAGMA journal_mode=WAL')
        conn.execute('PRAGMA busy_timeout=30000')
        return conn
    
    def init_database(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table - for customer authentication
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                full_name TEXT,
                is_admin BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Shopping cart table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS shopping_cart (
                cart_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER DEFAULT 1,
                price_at_add REAL NOT NULL,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (product_id) REFERENCES products(product_id)
            )
        ''')
        
        # Product search tracking table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS product_searches (
                search_id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                user_id INTEGER,
                search_query TEXT,
                searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products(product_id),
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        
        # Product views tracking
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS product_views (
                view_id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                user_id INTEGER,
                viewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products(product_id),
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        
        # Active sessions tracking for concurrent users
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS active_sessions (
                session_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                action_type TEXT,
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ended_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (product_id) REFERENCES products(product_id)
            )
        ''')
        
        # Products table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT,
                base_price REAL NOT NULL,
                cost_price REAL,
                current_price REAL,
                inventory INTEGER DEFAULT 0,
                min_price REAL,
                max_price REAL,
                description TEXT,
                demand_score REAL DEFAULT 0,
                search_count INTEGER DEFAULT 0,
                view_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Sales history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales_history (
                sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER,
                quantity_sold INTEGER,
                price REAL,
                revenue REAL,
                sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products(product_id)
            )
        ''')
        
        # Price history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS price_history (
                price_id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER,
                old_price REAL,
                new_price REAL,
                reason TEXT,
                changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products(product_id)
            )
        ''')
        
        # Competitor prices table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS competitor_prices (
                comp_id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER,
                competitor_name TEXT,
                competitor_price REAL,
                url TEXT,
                scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products(product_id)
            )
        ''')
        
        # Demand forecasts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS demand_forecasts (
                forecast_id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER,
                forecast_date DATE,
                predicted_demand REAL,
                confidence_level REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products(product_id)
            )
        ''')
        
        # System settings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_settings (
                setting_key TEXT PRIMARY KEY,
                setting_value TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Performance metrics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS performance_metrics (
                metric_id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE,
                total_revenue REAL,
                total_sales INTEGER,
                avg_conversion_rate REAL,
                price_changes INTEGER,
                recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    # Product operations
    def add_product(self, name, category, base_price, cost_price, inventory, description=''):
        """Add new product to database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        min_price = base_price * 0.7
        max_price = base_price * 1.3
        
        cursor.execute('''
            INSERT INTO products 
            (name, category, base_price, cost_price, current_price, inventory, 
             min_price, max_price, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, category, base_price, cost_price, base_price, inventory, 
              min_price, max_price, description))
        
        product_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return product_id
    
    def get_product(self, product_id):
        """Get product by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM products WHERE product_id = ?', (product_id,))
        columns = [desc[0] for desc in cursor.description]
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return dict(zip(columns, row))
        return None
    
    def get_all_products(self):
        """Get all products"""
        conn = self.get_connection()
        df = pd.read_sql_query('SELECT * FROM products ORDER BY product_id', conn)
        conn.close()
        return df
    
    def update_product_price(self, product_id, new_price, reason='AI Dynamic Pricing'):
        """Update product price"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get current price
        cursor.execute('SELECT current_price FROM products WHERE product_id = ?', (product_id,))
        result = cursor.fetchone()
        
        if result:
            old_price = result[0]
            
            # Update price
            cursor.execute('''
                UPDATE products 
                SET current_price = ?, updated_at = CURRENT_TIMESTAMP
                WHERE product_id = ?
            ''', (new_price, product_id))
            
            # Log price change
            cursor.execute('''
                INSERT INTO price_history (product_id, old_price, new_price, reason)
                VALUES (?, ?, ?, ?)
            ''', (product_id, old_price, new_price, reason))
            
            conn.commit()
        
        conn.close()
    
    def update_inventory(self, product_id, new_inventory):
        """Update product inventory"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE products SET inventory = ?, updated_at = CURRENT_TIMESTAMP
            WHERE product_id = ?
        ''', (new_inventory, product_id))
        
        conn.commit()
        conn.close()
    
    # Sales operations
    def record_sale(self, product_id, quantity, price):
        """Record a sale"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        revenue = quantity * price
        
        cursor.execute('''
            INSERT INTO sales_history (product_id, quantity_sold, price, revenue)
            VALUES (?, ?, ?, ?)
        ''', (product_id, quantity, price, revenue))
        
        # Update inventory
        cursor.execute('''
            UPDATE products 
            SET inventory = inventory - ?
            WHERE product_id = ?
        ''', (quantity, product_id))
        
        conn.commit()
        conn.close()
    
    def add_sale(self, product_id, quantity, price, revenue):
        """Add a sale record to sales history"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO sales_history (product_id, quantity_sold, price, revenue)
            VALUES (?, ?, ?, ?)
        ''', (product_id, quantity, price, revenue))
        
        conn.commit()
        sale_id = cursor.lastrowid
        conn.close()
        
        return sale_id
    
    def get_sales_history(self, product_id=None, days=30):
        """Get sales history"""
        conn = self.get_connection()
        
        if product_id:
            query = '''
                SELECT * FROM sales_history 
                WHERE product_id = ? AND sale_date >= date('now', '-{} days')
                ORDER BY sale_date DESC
            '''.format(days)
            df = pd.read_sql_query(query, conn, params=(product_id,))
        else:
            query = '''
                SELECT * FROM sales_history 
                WHERE sale_date >= date('now', '-{} days')
                ORDER BY sale_date DESC
            '''.format(days)
            df = pd.read_sql_query(query, conn)
        
        conn.close()
        return df
    
    # Competitor price operations
    def record_competitor_price(self, product_id, competitor_name, price, url=''):
        """Record competitor price"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO competitor_prices 
            (product_id, competitor_name, competitor_price, url)
            VALUES (?, ?, ?, ?)
        ''', (product_id, competitor_name, price, url))
        
        conn.commit()
        conn.close()
    
    def get_competitor_prices(self, product_id, days=7):
        """Get recent competitor prices"""
        conn = self.get_connection()
        
        query = '''
            SELECT * FROM competitor_prices 
            WHERE product_id = ? AND scraped_at >= date('now', '-{} days')
            ORDER BY scraped_at DESC
        '''.format(days)
        
        df = pd.read_sql_query(query, conn, params=(product_id,))
        conn.close()
        return df
    
    # Demand forecast operations
    def save_demand_forecast(self, product_id, forecast_data):
        """Save demand forecasts"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        for date, demand, confidence in forecast_data:
            cursor.execute('''
                INSERT INTO demand_forecasts 
                (product_id, forecast_date, predicted_demand, confidence_level)
                VALUES (?, ?, ?, ?)
            ''', (product_id, date, demand, confidence))
        
        conn.commit()
        conn.close()
    
    def get_demand_forecast(self, product_id, days_ahead=7):
        """Get demand forecasts"""
        conn = self.get_connection()
        
        query = '''
            SELECT * FROM demand_forecasts 
            WHERE product_id = ? AND forecast_date >= date('now')
            ORDER BY forecast_date
            LIMIT ?
        '''
        
        df = pd.read_sql_query(query, conn, params=(product_id, days_ahead))
        conn.close()
        return df
    
    # Analytics and reporting
    def get_revenue_report(self, days=30):
        """Get revenue report"""
        conn = self.get_connection()
        
        query = '''
            SELECT 
                DATE(sale_date) as date,
                SUM(revenue) as daily_revenue,
                SUM(quantity_sold) as daily_sales,
                COUNT(DISTINCT product_id) as products_sold
            FROM sales_history
            WHERE sale_date >= date('now', '-{} days')
            GROUP BY DATE(sale_date)
            ORDER BY date DESC
        '''.format(days)
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    
    def get_product_performance(self, product_id, days=30):
        """Get product performance metrics"""
        conn = self.get_connection()
        
        query = '''
            SELECT 
                COUNT(*) as total_transactions,
                SUM(quantity_sold) as total_units_sold,
                SUM(revenue) as total_revenue,
                AVG(price) as avg_price,
                MIN(price) as min_price,
                MAX(price) as max_price
            FROM sales_history
            WHERE product_id = ? AND sale_date >= date('now', '-{} days')
        '''.format(days)
        
        cursor = conn.cursor()
        cursor.execute(query, (product_id,))
        columns = [desc[0] for desc in cursor.description]
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return dict(zip(columns, row))
        return None
    
    # Settings operations
    def save_setting(self, key, value):
        """Save system setting"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO system_settings (setting_key, setting_value, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        ''', (key, json.dumps(value)))
        
        conn.commit()
        conn.close()
    
    def get_setting(self, key, default=None):
        """Get system setting"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT setting_value FROM system_settings WHERE setting_key = ?', (key,))
        result = cursor.fetchone()
        
        conn.close()
        
        if result:
            return json.loads(result[0])
        return default
    
    def generate_sample_data(self):
        """Generate sample data for demonstration"""
        # Add sample products
        products = [
            ('Wireless Mouse', 'Electronics', 25.99, 15.00, 150, 'High-quality wireless mouse with ergonomic design'),
            ('USB-C Cable', 'Electronics', 12.99, 5.00, 300, 'Durable USB-C charging cable'),
            ('Laptop Stand', 'Accessories', 39.99, 20.00, 80, 'Adjustable aluminum laptop stand'),
            ('Bluetooth Headphones', 'Electronics', 79.99, 40.00, 120, 'Noise-cancelling wireless headphones'),
            ('Phone Case', 'Accessories', 15.99, 6.00, 200, 'Protective phone case with shock absorption'),
            ('Mechanical Keyboard', 'Electronics', 129.99, 70.00, 60, 'RGB mechanical gaming keyboard'),
            ('Webcam HD', 'Electronics', 59.99, 30.00, 90, '1080p HD webcam for video calls'),
            ('Desk Organizer', 'Accessories', 24.99, 12.00, 110, 'Multi-compartment desk organizer'),
        ]
        
        for product in products:
            self.add_product(*product)
        
        # Generate sample sales history
        import random
        products_data = self.get_all_products()
        
        for _, product in products_data.iterrows():
            product_id = product['product_id']
            base_price = product['base_price']
            
            # Generate 60 days of sales history
            for day in range(60, 0, -1):
                # Random sales between 1-20 per day
                num_sales = random.randint(1, 20)
                
                for _ in range(num_sales):
                    # Price variation
                    price = base_price * random.uniform(0.85, 1.15)
                    quantity = random.randint(1, 5)
                    
                    conn = self.get_connection()
                    cursor = conn.cursor()
                    
                    sale_date = (datetime.now() - timedelta(days=day)).strftime('%Y-%m-%d %H:%M:%S')
                    revenue = price * quantity
                    
                    cursor.execute('''
                        INSERT INTO sales_history (product_id, quantity_sold, price, revenue, sale_date)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (product_id, quantity, price, revenue, sale_date))
                    
                    conn.commit()
                    conn.close()
        
        # Add sample competitor prices
        competitors = ['Amazon', 'eBay', 'Walmart', 'BestBuy']
        
        for _, product in products_data.iterrows():
            product_id = product['product_id']
            base_price = product['base_price']
            
            for competitor in competitors:
                comp_price = base_price * random.uniform(0.9, 1.1)
                self.record_competitor_price(product_id, competitor, comp_price)
        
        # Generate sample users
        import hashlib
        sample_users = [
            ('customer1', 'customer1@example.com', 'password123', 'John Doe', 0),
            ('customer2', 'customer2@example.com', 'password123', 'Jane Smith', 0),
            ('customer3', 'customer3@example.com', 'password123', 'Bob Johnson', 0),
            ('admin', 'admin@example.com', 'admin123', 'Admin User', 1),
        ]
        
        for username, email, password, full_name, is_admin in sample_users:
            # Simple hash (in production, use bcrypt or similar)
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            self.create_user(username, email, hashed_password, full_name, is_admin)
    
    # ==================== User Management Methods ====================
    
    def create_user(self, username, email, password, full_name='', is_admin=0):
        """Create a new user"""
        import hashlib
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Hash the password before storing
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            
            cursor.execute('''
                INSERT INTO users (username, email, password, full_name, is_admin)
                VALUES (?, ?, ?, ?, ?)
            ''', (username, email, hashed_password, full_name, is_admin))
            
            user_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return {'success': True, 'user_id': user_id}
        except sqlite3.IntegrityError as e:
            return {'success': False, 'error': 'Username or email already exists'}
    
    def authenticate_user(self, username, password):
        """Authenticate user login"""
        import hashlib
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT user_id, username, email, full_name, is_admin
            FROM users
            WHERE username = ? AND password = ?
        ''', (username, hashed_password))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'success': True,
                'user': {
                    'user_id': result[0],
                    'username': result[1],
                    'email': result[2],
                    'full_name': result[3],
                    'is_admin': bool(result[4])
                }
            }
        return {'success': False, 'error': 'Invalid credentials'}
    
    def get_all_users(self):
        """Get all users"""
        conn = self.get_connection()
        df = pd.read_sql_query('SELECT user_id, username, email, full_name, is_admin, created_at FROM users', conn)
        conn.close()
        return df
    
    # ==================== Shopping Cart Methods ====================
    
    def add_to_cart(self, user_id, product_id, quantity=1):
        """Add item to shopping cart"""
        # Get current price
        product = self.get_product(product_id)
        if product is None:
            return {'success': False, 'error': 'Product not found'}
        
        current_price = product['current_price']
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Check if item already in cart
        cursor.execute('''
            SELECT cart_id, quantity FROM shopping_cart
            WHERE user_id = ? AND product_id = ?
        ''', (user_id, product_id))
        
        existing = cursor.fetchone()
        
        if existing:
            # Update quantity
            new_quantity = existing[1] + quantity
            cursor.execute('''
                UPDATE shopping_cart
                SET quantity = ?, price_at_add = ?
                WHERE cart_id = ?
            ''', (new_quantity, current_price, existing[0]))
        else:
            # Add new item
            cursor.execute('''
                INSERT INTO shopping_cart (user_id, product_id, quantity, price_at_add)
                VALUES (?, ?, ?, ?)
            ''', (user_id, product_id, quantity, current_price))
        
        conn.commit()
        conn.close()
        
        return {'success': True}
    
    def get_user_cart(self, user_id):
        """Get user's shopping cart"""
        conn = self.get_connection()
        df = pd.read_sql_query('''
            SELECT c.cart_id, c.product_id, p.name, p.current_price, 
                   c.quantity, c.price_at_add, c.added_at,
                   (c.quantity * p.current_price) as total_price
            FROM shopping_cart c
            JOIN products p ON c.product_id = p.product_id
            WHERE c.user_id = ?
        ''', conn, params=(user_id,))
        conn.close()
        return df
    
    def remove_from_cart(self, cart_id):
        """Remove item from cart"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM shopping_cart WHERE cart_id = ?', (cart_id,))
        
        conn.commit()
        conn.close()
        
        return {'success': True}
    
    def clear_cart(self, user_id):
        """Clear user's entire cart"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM shopping_cart WHERE user_id = ?', (user_id,))
        
        conn.commit()
        conn.close()
        
        return {'success': True}
    
    def update_cart_quantity(self, cart_id, quantity):
        """Update item quantity in cart"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('UPDATE shopping_cart SET quantity = ? WHERE cart_id = ?', (quantity, cart_id))
        
        conn.commit()
        conn.close()
        
        return {'success': True}
    
    # ==================== Product Search Tracking Methods ====================
    
    def track_product_search(self, product_id, user_id=None, search_query=''):
        """Track when a product is searched"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO product_searches (product_id, user_id, search_query)
            VALUES (?, ?, ?)
        ''', (product_id, user_id, search_query))
        
        # Update search count in products table
        cursor.execute('''
            UPDATE products
            SET search_count = search_count + 1
            WHERE product_id = ?
        ''', (product_id,))
        
        conn.commit()
        conn.close()
        
        return {'success': True}
    
    def track_product_view(self, product_id, user_id=None):
        """Track when a product is viewed"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO product_views (product_id, user_id)
            VALUES (?, ?)
        ''', (product_id, user_id))
        
        # Update view count in products table
        cursor.execute('''
            UPDATE products
            SET view_count = view_count + 1
            WHERE product_id = ?
        ''', (product_id,))
        
        conn.commit()
        conn.close()
        
        return {'success': True}
    
    def get_product_engagement_stats(self, product_id, hours=24):
        """Get product engagement statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        time_threshold = (datetime.now() - timedelta(hours=hours)).strftime('%Y-%m-%d %H:%M:%S')
        
        # Get search count
        cursor.execute('''
            SELECT COUNT(*) FROM product_searches
            WHERE product_id = ? AND searched_at >= ?
        ''', (product_id, time_threshold))
        search_count = cursor.fetchone()[0]
        
        # Get view count
        cursor.execute('''
            SELECT COUNT(*) FROM product_views
            WHERE product_id = ? AND viewed_at >= ?
        ''', (product_id, time_threshold))
        view_count = cursor.fetchone()[0]
        
        # Get active cart count
        cursor.execute('''
            SELECT COUNT(*) FROM shopping_cart
            WHERE product_id = ? AND added_at >= ?
        ''', (product_id, time_threshold))
        cart_count = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'search_count': search_count,
            'view_count': view_count,
            'cart_count': cart_count,
            'engagement_score': search_count * 2 + view_count + cart_count * 3
        }
    
    # ==================== Session Tracking Methods ====================
    
    def start_active_session(self, user_id, product_id, action_type='viewing'):
        """Track when a user starts interacting with a product"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO active_sessions (user_id, product_id, action_type)
            VALUES (?, ?, ?)
        ''', (user_id, product_id, action_type))
        
        session_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return session_id
    
    def end_active_session(self, session_id):
        """End an active session"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE active_sessions
            SET ended_at = CURRENT_TIMESTAMP
            WHERE session_id = ?
        ''', (session_id,))
        
        conn.commit()
        conn.close()
    
    def get_concurrent_users(self, product_id, minutes=5):
        """Get number of users currently viewing/buying a product"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        time_threshold = (datetime.now() - timedelta(minutes=minutes)).strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute('''
            SELECT COUNT(DISTINCT user_id)
            FROM active_sessions
            WHERE product_id = ?
            AND started_at >= ?
            AND (ended_at IS NULL OR ended_at >= ?)
        ''', (product_id, time_threshold, time_threshold))
        
        count = cursor.fetchone()[0]
        conn.close()
        
        return count
