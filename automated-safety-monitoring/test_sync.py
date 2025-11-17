#!/usr/bin/env python3
import os
import sys
import json
from datetime import datetime
sys.path.append('app')

from app.database import DatabaseManager, Violation

def test_sync():
    db_manager = DatabaseManager()
    
    if not db_manager.connected:
        print("❌ Database not connected")
        return
    
    # Test data
    test_violation = {
        'timestamp': '2024-01-15T10:30:00Z',
        'employee_id': 'EMP001',
        'employee_name': 'John Doe',
        'missing_ppe': ['helmet', 'vest'],
        'location': 'Main Camera',
        'notified': False
    }
    
    session = db_manager.get_session()
    
    try:
        timestamp = datetime.fromisoformat(test_violation['timestamp'].replace('Z', '+00:00'))
        
        db_violation = Violation(
            timestamp=timestamp,
            employee_id=test_violation['employee_id'],
            employee_name=test_violation['employee_name'],
            missing_ppe=json.dumps(test_violation['missing_ppe']),
            location=test_violation.get('location', 'Main Camera'),
            notified=test_violation.get('notified', False)
        )
        
        session.add(db_violation)
        session.commit()
        print("✅ Test violation added successfully")
        
    except Exception as e:
        session.rollback()
        print(f"❌ Error: {e}")
    finally:
        session.close()

if __name__ == '__main__':
    test_sync()