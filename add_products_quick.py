import sqlite3

conn = sqlite3.connect('C:/FreeLancing/dynamic-pricing-system/backend/data/pricing_system.db')
cursor = conn.cursor()

products = [
    ('Wireless Bluetooth Headphones', 'Electronics', 79.99, 45.00, 79.99, 50),
    ('Smart Fitness Watch', 'Electronics', 199.99, 120.00, 199.99, 30),
    ('Laptop Backpack', 'Accessories', 49.99, 25.00, 49.99, 75),
    ('Portable Power Bank 20000mAh', 'Electronics', 39.99, 18.00, 39.99, 100),
    ('Mechanical Gaming Keyboard', 'Gaming', 89.99, 50.00, 89.99, 40),
    ('Wireless Gaming Mouse', 'Gaming', 59.99, 30.00, 59.99, 60),
    ('4K Webcam', 'Electronics', 129.99, 70.00, 129.99, 25),
    ('USB-C Hub 7-in-1', 'Accessories', 34.99, 15.00, 34.99, 80),
    ('Noise Cancelling Earbuds', 'Electronics', 149.99, 85.00, 149.99, 45),
    ('LED Desk Lamp', 'Home', 29.99, 12.00, 29.99, 90),
    ('Smartphone Stand', 'Accessories', 14.99, 5.00, 14.99, 150),
    ('External SSD 1TB', 'Electronics', 119.99, 65.00, 119.99, 35),
]

print("Adding products to database...")
for p in products:
    cursor.execute('''
        INSERT INTO products (name, category, base_price, cost_price, current_price, inventory)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', p)
    print(f"  ✓ {p[0]} - ${p[2]}")

conn.commit()

# Show all products
all_products = cursor.execute('SELECT product_id, name, base_price, inventory FROM products ORDER BY product_id').fetchall()
print(f"\nTotal products in database: {len(all_products)}")
print("="*70)
for p in all_products:
    print(f"ID {p[0]:3d}: {p[1]:40s} ${p[2]:7.2f} (Stock: {p[3]:3d})")

conn.close()
print("\n✓ Products added successfully!")
