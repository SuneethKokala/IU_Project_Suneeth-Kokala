import cv2
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from app.services.detection_service import DetectionService
from app.violation_logger import ViolationLogger

class CameraApp:
    def __init__(self):
        self.detection_service = DetectionService()
        self.violation_logger = ViolationLogger()
        self.employee_tracking = {}  # Track employee PPE status over time
        self.violation_threshold = 60  # 1 minute in seconds
        self.last_logged_violation = {}  # Prevent duplicate logging
    
    def check_violations(self, ppe_detections, face_detections):
        import time
        current_time = time.time()
        
        # Required PPE items
        required_ppe = ['helmet', 'vest']
        detected_ppe = [item['class'] for item in ppe_detections]
        
        for face in face_detections:
            employee_id = face['employee_id']
            employee_name = face['employee_name']
            
            # Find missing PPE
            missing_ppe = [item for item in required_ppe if item not in detected_ppe]
            
            # Initialize tracking for new employee
            if employee_id not in self.employee_tracking:
                self.employee_tracking[employee_id] = {
                    'name': employee_name,
                    'first_violation_time': None,
                    'missing_ppe': [],
                    'has_ppe': True
                }
            
            employee_data = self.employee_tracking[employee_id]
            
            if missing_ppe:
                # PPE violation detected
                if employee_data['first_violation_time'] is None:
                    # First time violation detected
                    employee_data['first_violation_time'] = current_time
                    employee_data['missing_ppe'] = missing_ppe
                    employee_data['has_ppe'] = False
                    print(f"⚠️ {employee_name}: PPE violation started - missing {', '.join(missing_ppe)}")
                
                # Check if 1 minute has passed
                elif current_time - employee_data['first_violation_time'] >= self.violation_threshold:
                    # Log violation only once after 1 minute
                    if employee_id not in self.last_logged_violation or \
                       current_time - self.last_logged_violation.get(employee_id, 0) > 3600:  # 1 hour cooldown
                        
                        self.violation_logger.log_violation(employee_id, employee_name, missing_ppe)
                        self.last_logged_violation[employee_id] = current_time
                        
                        # Reset tracking for this employee
                        employee_data['first_violation_time'] = current_time
            else:
                # PPE is present - reset violation tracking
                if not employee_data['has_ppe']:
                    print(f"✅ {employee_name}: PPE compliance restored")
                
                employee_data['first_violation_time'] = None
                employee_data['missing_ppe'] = []
                employee_data['has_ppe'] = True
    
    def run(self):
        # Try different camera indices
        cap = None
        for i in range(3):
            test_cap = cv2.VideoCapture(i)
            if test_cap.isOpened():
                ret, frame = test_cap.read()
                if ret:
                    print(f"✅ Using camera index {i}")
                    cap = test_cap
                    break
                else:
                    test_cap.release()
            else:
                test_cap.release()
        
        if cap is None:
            print("❌ Error: No working camera found")
            print("Please check camera permissions and availability")
            return
        
        print("✅ Camera opened successfully")
        frame_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print(f"❌ Error: Could not read frame (processed {frame_count} frames)")
                print("Camera may be in use by another application or permission denied")
                break
            
            frame_count += 1
            
            # Get detections
            result = self.detection_service.detect_all(frame)
            
            # Check for violations
            self.check_violations(result['ppe_detections'], result['face_detections'])
            
            # Draw PPE detections
            ppe_results = self.detection_service.ppe_model(frame, conf=0.1, iou=0.45)
            annotated_frame = ppe_results[0].plot()
            
            # Draw face boxes
            faces = self.detection_service.face_system.recognize_faces(frame)
            if faces:
                annotated_frame = self.detection_service.face_system.draw_face_boxes(annotated_frame, faces)
            
            # Add frame counter
            cv2.putText(annotated_frame, f"Frame: {frame_count}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            cv2.imshow('Safety Monitoring System', annotated_frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = CameraApp()
    app.run()