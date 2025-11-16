# notification.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import json

# Configuration
SUPERVISOR_EMAIL = "supervisor@company.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_USER = "safety@company.com"
EMAIL_PASS = "your_app_password"

# Employee database (in production, this would be from a database)
EMPLOYEES = {
    "person_1": {"name": "John Doe", "id": "EMP001"},
    "person_2": {"name": "Jane Smith", "id": "EMP002"},
    "unknown": {"name": "Unknown Employee", "id": "UNKNOWN"}
}

def send_notification(employee_id, missing_ppe, location="Camera 1"):
    """Send email notification to supervisor"""
    try:
        employee = EMPLOYEES.get(employee_id, EMPLOYEES["unknown"])
        
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = SUPERVISOR_EMAIL
        msg['Subject'] = f"PPE Violation Alert - {employee['name']}"
        
        body = f"""
        PPE VIOLATION DETECTED
        
        Employee: {employee['name']} (ID: {employee['id']})
        Location: {location}
        Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        Missing PPE: {', '.join(missing_ppe)}
        
        Please take immediate action.
        
        Safety Monitoring System
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
        server.quit()
        
        print(f"Notification sent for {employee['name']}")
        return True
        
    except Exception as e:
        print(f"Failed to send notification: {e}")
        return False

def log_violation(employee_id, missing_ppe):
    """Log violation to file"""
    violation = {
        "timestamp": datetime.now().isoformat(),
        "employee_id": employee_id,
        "employee_name": EMPLOYEES.get(employee_id, EMPLOYEES["unknown"])["name"],
        "missing_ppe": missing_ppe
    }
    
    try:
        with open("ppe_violations.log", "a") as f:
            f.write(json.dumps(violation) + "\n")
    except Exception as e:
        print(f"Failed to log violation: {e}")