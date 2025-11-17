#!/usr/bin/env python3
"""
Create sample violation data for testing
"""
import json
import os
from datetime import datetime, timedelta
import random

def create_sample_violations():
    """Create sample violation data"""
    
    # Sample employee data
    employees = [
        {"id": "EMP001", "name": "Navjot Singh"},
        {"id": "EMP002", "name": "Raksha Patel"},
        {"id": "EMP003", "name": "Suneeth Kokala"},
        {"id": "EMP004", "name": "John Smith"},
        {"id": "EMP005", "name": "Sarah Johnson"}
    ]
    
    # Sample PPE violations
    ppe_types = ["helmet", "vest", "gloves", "boots", "goggles"]
    locations = ["Main Camera", "Entrance", "Workshop", "Loading Dock", "Assembly Line"]
    
    violations = []
    
    # Generate violations for the last 30 days
    for i in range(50):  # Create 50 sample violations
        # Random date in the last 30 days
        days_ago = random.randint(0, 30)
        hours_ago = random.randint(0, 23)
        minutes_ago = random.randint(0, 59)
        
        violation_time = datetime.now() - timedelta(days=days_ago, hours=hours_ago, minutes=minutes_ago)
        
        # Random employee
        employee = random.choice(employees)
        
        # Random missing PPE (1-3 items)
        num_missing = random.randint(1, 3)
        missing_ppe = random.sample(ppe_types, num_missing)
        
        # Random location
        location = random.choice(locations)
        
        # Random notification status
        notified = random.choice([True, False])
        notified_at = ""
        if notified:
            # Notification happened 1-60 minutes after violation
            notify_delay = random.randint(1, 60)
            notified_at = (violation_time + timedelta(minutes=notify_delay)).isoformat()
        
        violation = {
            "timestamp": violation_time.isoformat(),
            "employee_id": employee["id"],
            "employee_name": employee["name"],
            "missing_ppe": missing_ppe,
            "location": location,
            "notified": notified,
            "notified_at": notified_at
        }
        
        violations.append(violation)
    
    # Sort by timestamp (newest first)
    violations.sort(key=lambda x: x["timestamp"], reverse=True)
    
    # Create data directory if it doesn't exist
    os.makedirs("data/logs", exist_ok=True)
    
    # Write to log file
    log_file = "data/logs/ppe_violations.log"
    with open(log_file, "w") as f:
        for violation in violations:
            f.write(json.dumps(violation) + "\n")
    
    print(f"Created {len(violations)} sample violations in {log_file}")
    
    # Also create a JSON file for easy viewing
    json_file = "data/logs/sample_violations.json"
    with open(json_file, "w") as f:
        json.dump(violations, f, indent=2)
    
    print(f"Also saved as JSON in {json_file}")

if __name__ == "__main__":
    create_sample_violations()