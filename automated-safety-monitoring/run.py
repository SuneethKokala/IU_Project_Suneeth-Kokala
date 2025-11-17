#!/usr/bin/env python3
import argparse
import sys
import os

# Add app to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def run_api():
    """Start FastAPI server"""
    from app.api_app import app
    import uvicorn
    print(" Starting Safety Monitoring API...")
    print(" API Docs: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)

def run_camera():
    """Start camera detection"""
    from app.camera_app import CameraApp
    print(" Starting camera detection...")
    print(" Press 'q' to quit")
    app = CameraApp()
    app.run()

def run_dashboard():
    """Start web dashboard"""
    from app.web.dashboard import app
    print("Starting Safety Monitoring Dashboard...")
    print("Access: http://localhost:3001")
    print(" Login: supervisor / admin123")
    app.run(debug=True, host='0.0.0.0', port=3001)

def train_model():
    """Train YOLO model"""
    from models.yolo_trainer import train_model
    print(" Starting YOLO training...")
    train_model()

def train_faces():
    """Train face recognition"""
    import sys
    sys.path.append('app')
    from app.core.face_recognition_system import FaceRecognitionSystem
    
    print("👤 Training face recognition...")
    face_system = FaceRecognitionSystem()
    face_system.train_employee_faces('data/employee_photos')
    print("✅ Face training completed!")

def setup_database():
    """Setup PostgreSQL database"""
    from setup_database import create_database, setup_tables
    print("🗄️ Setting up PostgreSQL database...")
    if create_database():
        setup_tables()
    else:
        print("❌ Database setup failed")

def main():
    parser = argparse.ArgumentParser(description='Safety Monitoring System')
    parser.add_argument('command', choices=[
        'api', 'camera', 'dashboard', 'train-model', 'train-faces', 'setup-db'
    ], help='Command to run')
    
    args = parser.parse_args()
    
    print(" Safety Monitoring System v1.0.0")
    print("=" * 50)
    
    commands = {
        'api': run_api,
        'camera': run_camera,
        'dashboard': run_dashboard,
        'train-model': train_model,
        'train-faces': train_faces,
        'setup-db': setup_database
    }
    
    commands[args.command]()

if __name__ == '__main__':
    main()