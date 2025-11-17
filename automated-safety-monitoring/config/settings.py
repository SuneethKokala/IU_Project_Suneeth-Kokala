# Configuration settings for Safety Monitoring System

# Import Supabase settings
try:
    from config.supabase_settings import *
except ImportError:
    # Fallback to local PostgreSQL
    DATABASE_HOST = "localhost"
    DATABASE_PORT = 5432
    DATABASE_NAME = "safety_monitoring"
    DATABASE_USER = "safety_user"
    DATABASE_PASSWORD = "safety_password"
    DATABASE_URL = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

# Fallback file settings
LOG_FILE = 'data/logs/ppe_violations.log'
FACE_ENCODINGS_FILE = 'data/face_encodings.pkl'
EMPLOYEE_PHOTOS_DIR = 'data/employee_photos'

# Model settings
PPE_MODEL_PATH = 'runs/detect/helmet_vest11/weights/best.pt'
REQUIRED_PPE = ['helmet', 'vest']

# Detection settings
VIOLATION_THRESHOLD = 60  # 1 minute in seconds
CONFIDENCE_THRESHOLD = 0.1
IOU_THRESHOLD = 0.45

# Dashboard settings
SUPERVISOR_USERNAME = "supervisor"
SUPERVISOR_PASSWORD = "admin123"
DASHBOARD_PORT = 3001

# Camera settings
CAMERA_INDEX = 0