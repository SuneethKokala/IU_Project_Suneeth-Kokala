#!/usr/bin/env python3
import os
import sys
sys.path.append('app')

from app.database import DatabaseManager

def check_table():
    db_manager = DatabaseManager()
    
    if db_manager.connected:
        violations = db_manager.get_violations()
        print(f"✅ Found {len(violations)} violations in database")
        
        for v in violations[:5]:  # Show first 5
            print(f"- {v.employee_name} ({v.employee_id}) missing {v.missing_ppe} at {v.timestamp}")
    else:
        print("❌ Database not connected")

if __name__ == '__main__':
    check_table()