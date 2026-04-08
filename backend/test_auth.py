"""
Test authentication to debug login issue
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import DatabaseManager
import hashlib

db = DatabaseManager()

# Check what's in the database
conn = db.get_connection()
cursor = conn.cursor()

print("=" * 60)
print("USERS IN DATABASE:")
print("=" * 60)
users = cursor.execute('SELECT user_id, username, password, is_admin FROM users').fetchall()
for user in users:
    print(f"ID: {user[0]}")
    print(f"Username: {user[1]}")
    print(f"Password Hash: {user[2][:20]}...")
    print(f"Is Admin: {user[3]}")
    print("-" * 60)

conn.close()

# Test authentication
print("\n" + "=" * 60)
print("TESTING AUTHENTICATION:")
print("=" * 60)

test_accounts = [
    ('customer1', 'password123'),
    ('customer2', 'password123'),
    ('customer3', 'password123'),
    ('admin', 'admin123')
]

for username, password in test_accounts:
    print(f"\nTesting: {username} / {password}")
    print(f"Password hash: {hashlib.sha256(password.encode()).hexdigest()}")
    
    result = db.authenticate_user(username, password)
    
    if result['success']:
        print(f"✓ SUCCESS - User: {result['user']['username']}, Admin: {result['user']['is_admin']}")
    else:
        print(f"✗ FAILED - {result.get('error', 'Unknown error')}")
