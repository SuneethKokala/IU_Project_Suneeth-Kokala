import json
import os
from datetime import datetime
from config.database import get_supabase_client, VIOLATIONS_TABLE

class DatabaseService:
    def __init__(self):
        self.supabase = get_supabase_client()
    
    def save_violation_to_db(self, violation_data):
        """Save violation to Supabase database"""
        try:
            result = self.supabase.table(VIOLATIONS_TABLE).insert(violation_data).execute()
            return True, result
        except Exception as e:
            print(f"Database error: {e}")
            return False, str(e)
    
    def sync_log_to_database(self):
        """Sync all violations from log file to database"""
        log_file = 'data/logs/ppe_violations.log'
        if not os.path.exists(log_file):
            return False, "No log file found"
        
        try:
            with open(log_file, 'r') as f:
                violations = [json.loads(line.strip()) for line in f if line.strip()]
            
            # Prepare data for database
            db_violations = []
            for v in violations:
                db_violation = {
                    'timestamp': v['timestamp'],
                    'employee_id': v['employee_id'],
                    'employee_name': v['employee_name'],
                    'missing_ppe': json.dumps(v['missing_ppe']),
                    'location': v.get('location', 'Main Camera'),
                    'notified': v.get('notified', False),
                    'notified_at': v.get('notified_at', None)
                }
                db_violations.append(db_violation)
            
            # Insert all violations
            result = self.supabase.table(VIOLATIONS_TABLE).insert(db_violations).execute()
            return True, f"Synced {len(db_violations)} violations to database"
            
        except Exception as e:
            return False, f"Sync error: {str(e)}"
    
    def get_violations_from_db(self):
        """Get all violations from database"""
        try:
            result = self.supabase.table(VIOLATIONS_TABLE).select("*").order('timestamp', desc=True).execute()
            return result.data
        except Exception as e:
            print(f"Database fetch error: {e}")
            return []