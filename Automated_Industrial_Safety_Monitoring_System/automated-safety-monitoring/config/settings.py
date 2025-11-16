# Configuration settings for Safety Monitoring System

# Database settings
LOG_FILE = 'data/logs/ppe_violations.log'
FACE_ENCODINGS_FILE = 'data/face_encodings.pkl'
EMPLOYEE_PHOTOS_DIR = 'data/employee_photos'

# Model settings
PPE_MODEL_PATH = 'runs/detect/helmet_vest11/weights/best.pt'
REQUIRED_PPE = ['helmet', 'vest']

# Detection settings
VIOLATION_THRESHOLD = 300  # 5 minutes in seconds
CONFIDENCE_THRESHOLD = 0.1
IOU_THRESHOLD = 0.45

# Dashboard settings
SUPERVISOR_USERNAME = "supervisor"
SUPERVISOR_PASSWORD = "admin123"
DASHBOARD_PORT = 3001

# Camera settings
CAMERA_INDEX = 0