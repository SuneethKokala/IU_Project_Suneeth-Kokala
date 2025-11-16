#!/usr/bin/env python3
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sys
import os

# Add app to path
sys.path.append('.')
from config.settings import DATABASE_HOST, DATABASE_PORT, DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD

def create_database():
    """Create PostgreSQL database and user"""
    try:
        # Connect to PostgreSQL server
        conn = psycopg2.connect(
            host=DATABASE_HOST,
            port=DATABASE_PORT,
            user='postgres',  # Default admin user
            password=input("Enter PostgreSQL admin password: ")
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Create user
        try:
            cursor.execute(f"CREATE USER {DATABASE_USER} WITH PASSWORD '{DATABASE_PASSWORD}';")
            print(f"✅ User '{DATABASE_USER}' created")
        except psycopg2.errors.DuplicateObject:
            print(f"ℹ️ User '{DATABASE_USER}' already exists")
        
        # Create database
        try:
            cursor.execute(f"CREATE DATABASE {DATABASE_NAME} OWNER {DATABASE_USER};")
            print(f"✅ Database '{DATABASE_NAME}' created")
        except psycopg2.errors.DuplicateDatabase:
            print(f"ℹ️ Database '{DATABASE_NAME}' already exists")
        
        # Grant privileges
        cursor.execute(f"GRANT ALL PRIVILEGES ON DATABASE {DATABASE_NAME} TO {DATABASE_USER};")
        print(f"✅ Privileges granted to '{DATABASE_USER}'")
        
        cursor.close()
        conn.close()
        
        # Test connection with new user
        test_conn = psycopg2.connect(
            host=DATABASE_HOST,
            port=DATABASE_PORT,
            database=DATABASE_NAME,
            user=DATABASE_USER,
            password=DATABASE_PASSWORD
        )
        test_conn.close()
        print("✅ Database setup completed successfully!")
        
        return True
        
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        return False

def setup_tables():
    """Create database tables"""
    try:
        from app.database import DatabaseManager
        from config.settings import SUPERVISOR_USERNAME, SUPERVISOR_PASSWORD
        
        db_manager = DatabaseManager()
        if db_manager.connected:
            print("✅ Database tables created successfully!")
            
            # Add default supervisor
            db_manager.add_supervisor(
                username=SUPERVISOR_USERNAME,
                password=SUPERVISOR_PASSWORD,
                name="Default Supervisor",
                email="supervisor@company.com",
                department="Safety"
            )
            
            return True
        else:
            print("❌ Failed to connect to database")
            return False
    except Exception as e:
        print(f"❌ Table creation failed: {e}")
        return False

if __name__ == "__main__":
    print("🗄️ PostgreSQL Database Setup")
    print("=" * 40)
    
    print("1. Creating database and user...")
    if create_database():
        print("\n2. Creating tables...")
        setup_tables()
        
        print("\n✅ Setup complete! You can now run:")
        print("python3 run.py camera")
        print("python3 run.py dashboard")
    else:
        print("\n❌ Setup failed. Check PostgreSQL installation and credentials.")