"""
Add sample products to the database
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import DatabaseManager

def add_sample_products():
    db = DatabaseManager()
    
    # Sample products to add
    sample_products = [
        {
            'name': 'Wireless Bluetooth Headphones',
            'category': 'Electronics',
            'base_price': 79.99,
            'cost_price': 45.00,
            'inventory': 50,
            'description': 'Premium wireless headphones with noise cancellation'
        },
        {
            'name': 'Smart Fitness Watch',
            'category': 'Electronics',
            'base_price': 199.99,
            'cost_price': 120.00,
            'inventory': 30,
            'description': 'Track your health and fitness with style'
        },
        {
            'name': 'Laptop Backpack',
            'category': 'Accessories',
            'base_price': 49.99,
            'cost_price': 25.00,
            'inventory': 75,
            'description': 'Durable backpack with laptop compartment'
        },
        {
            'name': 'Portable Power Bank 20000mAh',
            'category': 'Electronics',
            'base_price': 39.99,
            'cost_price': 18.00,
            'inventory': 100,
            'description': 'Fast charging portable battery for all devices'
        },
        {
            'name': 'Mechanical Gaming Keyboard',
            'category': 'Gaming',
            'base_price': 89.99,
            'cost_price': 50.00,
            'inventory': 40,
            'description': 'RGB backlit mechanical keyboard with tactile switches'
        },
        {
            'name': 'Wireless Gaming Mouse',
            'category': 'Gaming',
            'base_price': 59.99,
            'cost_price': 30.00,
            'inventory': 60,
            'description': 'High-precision wireless mouse with programmable buttons'
        },
        {
            'name': '4K Webcam',
            'category': 'Electronics',
            'base_price': 129.99,
            'cost_price': 70.00,
            'inventory': 25,
            'description': 'Ultra HD webcam for streaming and video calls'
        },
        {
            'name': 'USB-C Hub 7-in-1',
            'category': 'Accessories',
            'base_price': 34.99,
            'cost_price': 15.00,
            'inventory': 80,
            'description': 'Multi-port USB-C adapter with HDMI and card reader'
        },
        {
            'name': 'Noise Cancelling Earbuds',
            'category': 'Electronics',
            'base_price': 149.99,
            'cost_price': 85.00,
            'inventory': 45,
            'description': 'True wireless earbuds with active noise cancellation'
        },
        {
            'name': 'LED Desk Lamp',
            'category': 'Home',
            'base_price': 29.99,
            'cost_price': 12.00,
            'inventory': 90,
            'description': 'Adjustable LED lamp with touch control and USB port'
        },
        {
            'name': 'Smartphone Stand',
            'category': 'Accessories',
            'base_price': 14.99,
            'cost_price': 5.00,
            'inventory': 150,
            'description': 'Adjustable phone holder for desk or bedside'
        },
        {
            'name': 'External SSD 1TB',
            'category': 'Electronics',
            'base_price': 119.99,
            'cost_price': 65.00,
            'inventory': 35,
            'description': 'Ultra-fast portable solid state drive'
        }
    ]
    
    print("=" * 60)
    print("ADDING SAMPLE PRODUCTS TO DATABASE")
    print("=" * 60)
    
    added_count = 0
    for product in sample_products:
        try:
            product_id = db.add_product(
                name=product['name'],
                category=product['category'],
                base_price=product['base_price'],
                cost_price=product['cost_price'],
                inventory=product['inventory'],
                description=product.get('description', '')
            )
            print(f"✓ Added: {product['name']} (ID: {product_id}) - ${product['base_price']}")
            added_count += 1
        except Exception as e:
            print(f"✗ Error adding {product['name']}: {str(e)}")
    
    print("\n" + "=" * 60)
    print(f"Successfully added {added_count} products!")
    print("=" * 60)
    
    # Display all products
    conn = db.get_connection()
    all_products = conn.execute('''
        SELECT product_id, name, category, base_price, inventory 
        FROM products 
        ORDER BY product_id
    ''').fetchall()
    conn.close()
    
    print("\nALL PRODUCTS IN DATABASE:")
    print("=" * 60)
    for p in all_products:
        print(f"ID: {p[0]:3d} | {p[1]:35s} | {p[2]:15s} | ${p[3]:7.2f} | Stock: {p[4]}")
    
    print("\n" + "=" * 60)
    print("HOW TO ADD MORE PRODUCTS:")
    print("=" * 60)
    print("""
# Method 1: Using Python Script
from database import DatabaseManager

db = DatabaseManager()
product_id = db.add_product(
    name='Product Name',
    category='Category',
    base_price=99.99,
    cost_price=50.00,
    inventory=100,
    description='Product description'
)

# Method 2: Direct SQL
import sqlite3
conn = sqlite3.connect('backend/data/pricing_system.db')
cursor = conn.cursor()
cursor.execute('''
    INSERT INTO products (name, category, base_price, cost_price, current_price, inventory)
    VALUES (?, ?, ?, ?, ?, ?)
''', ('Product Name', 'Category', 99.99, 50.00, 99.99, 100))
conn.commit()
conn.close()

# Method 3: Via API (when server is running)
import requests
response = requests.post('http://localhost:5000/api/products', json={
    'name': 'Product Name',
    'category': 'Category',
    'base_price': 99.99,
    'cost_price': 50.00,
    'inventory': 100,
    'description': 'Product description'
})
    """)
    print("=" * 60)

if __name__ == '__main__':
    add_sample_products()
