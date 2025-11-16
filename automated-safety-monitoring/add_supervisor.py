#!/usr/bin/env python3
import sys
sys.path.append('.')
from app.database import DatabaseManager

def add_supervisor():
    """Add a new supervisor to the database"""
    db_manager = DatabaseManager()
    
    if not db_manager.connected:
        print("❌ Database not connected")
        return
    
    print("👨‍💼 Add New Supervisor")
    print("=" * 30)
    
    username = input("Username: ")
    password = input("Password: ")
    name = input("Full Name: ")
    email = input("Email (optional): ") or None
    department = input("Department (optional): ") or None
    
    supervisor = db_manager.add_supervisor(username, password, name, email, department)
    
    if supervisor:
        print(f"✅ Supervisor '{username}' added successfully!")
    else:
        print("❌ Failed to add supervisor")

def list_supervisors():
    """List all supervisors"""
    db_manager = DatabaseManager()
    
    if not db_manager.connected:
        print("❌ Database not connected")
        return
    
    supervisors = db_manager.get_supervisors()
    
    print("👨‍💼 Current Supervisors")
    print("=" * 30)
    
    for supervisor in supervisors:
        print(f"Username: {supervisor.username}")
        print(f"Name: {supervisor.name}")
        print(f"Email: {supervisor.email or 'N/A'}")
        print(f"Department: {supervisor.department or 'N/A'}")
        print(f"Last Login: {supervisor.last_login or 'Never'}")
        print("-" * 30)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "list":
        list_supervisors()
    else:
        add_supervisor()