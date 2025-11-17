#!/usr/bin/env python3
import os
import json
import requests
from datetime import datetime

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

def sync_to_supabase():
    # Load violations from log file
    log_path = 'data/logs/ppe_violations.log'
    if not os.path.exists(log_path):
        print("❌ No violations log file found")
        return
    
    violations = []
    with open(log_path, 'r') as f:
        for line in f:
            if line.strip():
                violations.append(json.loads(line.strip()))
    
    if not violations:
        print("❌ No violations to sync")
        return
    
    # Sync to Supabase using REST API
    headers = {
        'apikey': SUPABASE_SERVICE_KEY,
        'Authorization': f'Bearer {SUPABASE_SERVICE_KEY}',
        'Content-Type': 'application/json'
    }
    
    synced_count = 0
    
    for violation in violations:
        data = {
            'timestamp': violation['timestamp'],
            'employee_id': violation['employee_id'],
            'employee_name': violation['employee_name'],
            'missing_ppe': violation['missing_ppe'],
            'location': violation.get('location', 'Main Camera'),
            'notified': violation.get('notified', False)
        }
        
        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/ppe_violations",
            headers=headers,
            json=data
        )
        
        if response.status_code == 201:
            synced_count += 1
            print(f"✅ Synced: {violation['employee_name']}")
        else:
            print(f"❌ Failed to sync: {violation['employee_name']} - {response.text}")
    
    print(f"🎉 Synced {synced_count} violations to Supabase")

if __name__ == '__main__':
    sync_to_supabase()