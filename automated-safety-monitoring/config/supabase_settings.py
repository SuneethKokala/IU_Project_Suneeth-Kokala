# Supabase Configuration
# Replace these with your actual Supabase credentials

# Get these from Supabase Dashboard > Settings > Database
SUPABASE_URL = "https://your-project-ref.supabase.co"
SUPABASE_ANON_KEY = "your-anon-key"
SUPABASE_SERVICE_KEY = "your-service-role-key"

# Database connection details
DATABASE_HOST = "db.your-project-ref.supabase.co"
DATABASE_PORT = 5432
DATABASE_NAME = "postgres"
DATABASE_USER = "postgres"
DATABASE_PASSWORD = "your-database-password"
DATABASE_URL = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

# Other settings (keep existing)
LOG_FILE = 'data/logs/ppe_violations.log'
FACE_ENCODINGS_FILE = 'data/face_encodings.pkl'
EMPLOYEE_PHOTOS_DIR = 'data/employee_photos'
PPE_MODEL_PATH = 'runs/detect/helmet_vest11/weights/best.pt'
REQUIRED_PPE = ['helmet', 'vest']
VIOLATION_THRESHOLD = 300
CONFIDENCE_THRESHOLD = 0.1
IOU_THRESHOLD = 0.45
SUPERVISOR_USERNAME = "supervisor"
SUPERVISOR_PASSWORD = "admin123"
DASHBOARD_PORT = 3001
CAMERA_INDEX = 0