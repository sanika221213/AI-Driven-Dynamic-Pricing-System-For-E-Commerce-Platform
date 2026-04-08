"""
Create demo user accounts for the e-commerce platform
"""
from database import DatabaseManager

def create_demo_users():
    db = DatabaseManager()
    
    # Check existing users
    conn = db.get_connection()
    existing_users = conn.execute('SELECT username FROM users').fetchall()
    print(f"\nExisting users in database: {len(existing_users)}")
    for user in existing_users:
        print(f"  - {user[0]}")
    conn.close()
    
    # Demo accounts to create
    demo_accounts = [
        {
            'username': 'customer1',
            'password': 'password123',
            'email': 'customer1@example.com',
            'is_admin': False
        },
        {
            'username': 'customer2',
            'password': 'password123',
            'email': 'customer2@example.com',
            'is_admin': False
        },
        {
            'username': 'customer3',
            'password': 'password123',
            'email': 'customer3@example.com',
            'is_admin': False
        },
        {
            'username': 'admin',
            'password': 'admin123',
            'email': 'admin@example.com',
            'is_admin': True
        }
    ]
    
    print("\n" + "="*50)
    print("Creating demo user accounts...")
    print("="*50)
    
    for account in demo_accounts:
        try:
            # Check if user already exists
            conn = db.get_connection()
            existing = conn.execute(
                'SELECT user_id FROM users WHERE username = ?', 
                (account['username'],)
            ).fetchone()
            conn.close()
            
            if existing:
                print(f"✓ {account['username']} already exists")
            else:
                result = db.create_user(
                    username=account['username'],
                    password=account['password'],
                    email=account['email'],
                    is_admin=account['is_admin']
                )
                if result['success']:
                    print(f"✓ Created {account['username']} (ID: {result['user_id']})")
                else:
                    print(f"✗ Error creating {account['username']}: {result.get('error', 'Unknown error')}")
        except Exception as e:
            print(f"✗ Error creating {account['username']}: {str(e)}")
    
    # Verify all accounts
    print("\n" + "="*50)
    print("Verification - All users in database:")
    print("="*50)
    conn = db.get_connection()
    all_users = conn.execute('SELECT user_id, username, email, is_admin FROM users').fetchall()
    conn.close()
    for user in all_users:
        role = "Admin" if user[3] else "Customer"
        print(f"  ID: {user[0]} | {user[1]} ({user[2]}) - {role}")
    
    print("\n" + "="*50)
    print("Login Credentials:")
    print("="*50)
    print("Customer Accounts:")
    print("  Username: customer1  |  Password: password123")
    print("  Username: customer2  |  Password: password123")
    print("  Username: customer3  |  Password: password123")
    print("\nAdmin Account:")
    print("  Username: admin      |  Password: admin123")
    print("="*50)

if __name__ == '__main__':
    create_demo_users()
