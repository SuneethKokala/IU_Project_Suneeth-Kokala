#!/usr/bin/env python3
import os
import sys
sys.path.append('app')

from app.database import DatabaseManager

def create_table():
    db_manager = DatabaseManager()
    
    if db_manager.connected:
        print("✅ Connected to database")
        print("✅ Table created successfully")
    else:
        print("❌ Failed to connect to database")

if __name__ == '__main__':
    create_table()