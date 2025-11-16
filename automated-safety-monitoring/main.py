# main.py - Main application entry point
import sys
import os
import argparse

# Add app to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def run_dashboard():
    """Start the web dashboard"""
    from app.web.dashboard import app
    print("🌐 Starting Safety Monitoring Dashboard...")
    print("📊 Access dashboard at: http://localhost:3001")
    print("👤 Login: supervisor / admin123")
    app.run(debug=True, host='0.0.0.0', port=3001)

def run_detection():
    """Start real-time PPE detection"""
    from app.camera_app import CameraApp
    print("📹 Starting real-time PPE detection...")
    print("❌ Press 'q' to quit")
    app = CameraApp()
    app.run()

def train_model():
    """Train YOLO model"""
    from models.yolo_trainer import train_model
    print("🤖 Starting YOLO model training...")
    train_model()

def train_faces():
    """Train face recognition"""
    from app.core.face_recognition_system import FaceRecognitionSystem
    print("👤 Starting face recognition training...")
    face_system = FaceRecognitionSystem()
    face_system.train_employee_faces('data/employee_photos')
    print("✅ Face training completed!")

def main():
    parser = argparse.ArgumentParser(description='Safety Monitoring System')
    parser.add_argument('command', choices=['dashboard', 'detect', 'train-model', 'train-faces'], 
                       help='Command to run')
    
    args = parser.parse_args()
    
    print("🛡️ Safety Monitoring System v1.0.0")
    print("=" * 50)
    
    if args.command == 'dashboard':
        run_dashboard()
    elif args.command == 'detect':
        run_detection()
    elif args.command == 'train-model':
        train_model()
    elif args.command == 'train-faces':
        train_faces()

if __name__ == '__main__':
    main()