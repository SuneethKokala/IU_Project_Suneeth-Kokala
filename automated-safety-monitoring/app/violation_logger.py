import json
import os
from datetime import datetime
from app.database import DatabaseManager

class ViolationLogger:
    def __init__(self, log_file='data/logs/ppe_violations.log'):
        self.log_file = log_file
        self.db_manager = DatabaseManager()
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    def log_violation(self, employee_id, employee_name, missing_ppe, location="Main Camera"):
        # Try database first
        db_violation = self.db_manager.log_violation(employee_id, employee_name, missing_ppe, location)
        
        # Fallback to file logging
        violation = {
            "timestamp": datetime.now().isoformat(),
            "employee_id": employee_id,
            "employee_name": employee_name,
            "missing_ppe": missing_ppe,
            "location": location,
            "notified": False
        }
        
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(violation) + '\n')
        
        if not db_violation:
            print(f"🚨 VIOLATION LOGGED TO FILE: {employee_name} missing {', '.join(missing_ppe)}")
        
        return violation