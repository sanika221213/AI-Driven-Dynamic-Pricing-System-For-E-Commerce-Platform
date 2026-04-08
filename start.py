"""
Quick Start Guide for AI-Driven Dynamic Pricing System
Run this script to get started quickly
"""

import os
import sys
import subprocess

def print_header(text):
    print("\n" + "=" * 60)
    print(text.center(60))
    print("=" * 60 + "\n")

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✓ Python version: {version.major}.{version.minor}.{version.micro}")
    return True

def install_dependencies():
    """Install required Python packages"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def initialize_database():
    """Initialize the database"""
    print("\n💾 Initializing database...")
    try:
        from backend.database import DatabaseManager
        db = DatabaseManager()
        print("✓ Database initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to initialize database: {e}")
        return False

def main():
    print_header("AI-Driven Dynamic Pricing System")
    print("🤖 Welcome to the AI-Powered Pricing Engine!")
    print("📚 Based on research: 'AI-Driven Dynamic Pricing for E-commerce'")
    
    # Check Python version
    print_header("System Check")
    if not check_python_version():
        return
    
    # Install dependencies
    print_header("Installing Dependencies")
    response = input("Install required packages? (y/n): ")
    if response.lower() == 'y':
        if not install_dependencies():
            return
    
    # Initialize database
    print_header("Database Setup")
    if not initialize_database():
        print("\n⚠️  Database initialization failed, but you can try starting the server")
    
    # Instructions
    print_header("Setup Complete!")
    print("🎉 Setup completed successfully!\n")
    
    print("📋 Next Steps:")
    print("\n1️⃣  Start the Backend Server:")
    print("   cd backend")
    print("   python app.py")
    
    print("\n2️⃣  Open the Frontend:")
    print("   Open frontend/index.html in your browser")
    print("   OR run: cd frontend && python -m http.server 8000")
    
    print("\n3️⃣  Initialize Sample Data:")
    print("   - Open the Dashboard in your browser")
    print("   - Click 'Generate Sample Data' button")
    print("   - Explore the features!")
    
    print("\n" + "=" * 60)
    print("🌐 Backend API: http://localhost:5000")
    print("🎨 Frontend UI: http://localhost:8000 (if using HTTP server)")
    print("📖 Documentation: See README.md")
    print("=" * 60 + "\n")
    
    # Ask to start server
    response = input("Start the backend server now? (y/n): ")
    if response.lower() == 'y':
        print("\n🚀 Starting Flask server...\n")
        os.chdir('backend')
        subprocess.call([sys.executable, "app.py"])

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Setup cancelled. Run this script again when ready!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Please check the README.md for manual setup instructions")
