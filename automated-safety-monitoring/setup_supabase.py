#!/usr/bin/env python3
import sys
sys.path.append('.')

def setup_supabase():
    print("🚀 Supabase Setup for Safety Monitoring System")
    print("=" * 50)
    
    print("\n1. Go to https://supabase.com")
    print("2. Create account and new project")
    print("3. Get your connection details from Settings > Database")
    print("\n4. Update config/supabase_settings.py with your details:")
    
    # Get user input
    host = input("\nEnter DATABASE_HOST (db.xxx.supabase.co): ")
    password = input("Enter DATABASE_PASSWORD: ")
    
    # Update the config file
    config_content = f'''# Supabase Configuration
# Your actual Supabase credentials

DATABASE_HOST = "{host}"
DATABASE_PORT = 5432
DATABASE_NAME = "postgres"
DATABASE_USER = "postgres"
DATABASE_PASSWORD = "{password}"
DATABASE_URL = f"postgresql://{{DATABASE_USER}}:{{DATABASE_PASSWORD}}@{{DATABASE_HOST}}:{{DATABASE_PORT}}/{{DATABASE_NAME}}"

# Other settings
LOG_FILE = 'data/logs/ppe_violations.log'
FACE_ENCODINGS_FILE = 'data/face_encodings.pkl'
EMPLOYEE_PHOTOS_DIR = 'data/employee_photos'
PPE_MODEL_PATH = 'runs/detect/helmet_vest11/weights/best.pt'
REQUIRED_PPE = ['helmet', 'vest']
VIOLATION_THRESHOLD = 300
CONFIDENCE_THRESHOLD = 0.1
IOU_THRESHOLD = 0.45
SUPERVISOR_USERNAME = "supervisor"
SUPERVISOR_PASSWORD = "admin123"
DASHBOARD_PORT = 3001
CAMERA_INDEX = 0'''
    
    with open('config/supabase_settings.py', 'w') as f:
        f.write(config_content)
    
    print("✅ Configuration updated!")
    
    # Test connection
    print("\n5. Testing connection...")
    try:
        from app.database import DatabaseManager
        db = DatabaseManager()
        if db.connected:
            print("✅ Connected to Supabase!")
            
            # Create default supervisor
            db.add_supervisor("supervisor", "admin123", "Default Supervisor", "admin@company.com", "Safety")
            print("✅ Default supervisor created!")
            
        else:
            print("❌ Connection failed. Check your credentials.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    setup_supabase()