# face_recognition_system.py
import cv2
import face_recognition
import numpy as np
import os
import pickle

class FaceRecognitionSystem:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []
        self.employees_db = {}
        self.load_employee_faces()
    
    def load_employee_faces(self):
        """Load trained face encodings from file"""
        try:
            with open('data/face_encodings.pkl', 'rb') as f:
                data = pickle.load(f)
                self.known_face_encodings = data['encodings']
                self.known_face_names = data['names']
                self.employees_db = data['employees']
            print(f"Loaded {len(self.known_face_names)} employee faces")
        except FileNotFoundError:
            print("No face encodings found. Please train employee faces first.")
    
    def train_employee_faces(self, employee_photos_dir):
        """Train face recognition with employee photos"""
        self.known_face_encodings = []
        self.known_face_names = []
        self.employees_db = {}
        
        if not os.path.exists(employee_photos_dir):
            print(f"Directory {employee_photos_dir} not found")
            return
        
        for filename in os.listdir(employee_photos_dir):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                # Extract employee info from filename: "EMP001_John_Doe.jpg"
                name_parts = filename.split('.')[0].split('_')
                if len(name_parts) >= 3:
                    emp_id = name_parts[0]
                    emp_name = ' '.join(name_parts[1:])
                else:
                    emp_id = filename.split('.')[0]
                    emp_name = emp_id
                
                image_path = os.path.join(employee_photos_dir, filename)
                image = face_recognition.load_image_file(image_path)
                
                # Get face encodings
                face_encodings = face_recognition.face_encodings(image)
                
                if face_encodings:
                    self.known_face_encodings.append(face_encodings[0])
                    self.known_face_names.append(emp_id)
                    self.employees_db[emp_id] = {
                        'name': emp_name,
                        'id': emp_id
                    }
                    print(f"Trained face for {emp_name} ({emp_id})")
                else:
                    print(f"No face found in {filename}")
        
        # Save encodings
        self.save_face_encodings()
    
    def save_face_encodings(self):
        """Save face encodings to file"""
        os.makedirs('data', exist_ok=True)
        data = {
            'encodings': self.known_face_encodings,
            'names': self.known_face_names,
            'employees': self.employees_db
        }
        with open('data/face_encodings.pkl', 'wb') as f:
            pickle.dump(data, f)
        print("Face encodings saved successfully")
    
    def recognize_faces(self, frame):
        """Recognize faces in frame and return employee info"""
        try:
            # Use larger frame for better detection
            small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
            
            # Find faces with different model
            face_locations = face_recognition.face_locations(rgb_small_frame, model="hog")
            if not face_locations:
                return []
                
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        except Exception as e:
            print(f"Face recognition error: {e}")
            return []
        
        recognized_employees = []
        
        for face_encoding, face_location in zip(face_encodings, face_locations):
            # Compare with known faces
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            
            best_match_index = np.argmin(face_distances)
            
            if matches[best_match_index] and face_distances[best_match_index] < 0.5:
                emp_id = self.known_face_names[best_match_index]
                employee_info = self.employees_db.get(emp_id, {'name': 'Unknown', 'id': emp_id})
                
                # Scale back face location
                top, right, bottom, left = face_location
                top *= 2
                right *= 2
                bottom *= 2
                left *= 2
                
                recognized_employees.append({
                    'employee_id': emp_id,
                    'employee_name': employee_info['name'],
                    'face_location': (top, right, bottom, left),
                    'confidence': 1 - face_distances[best_match_index]
                })
        
        return recognized_employees
    
    def draw_face_boxes(self, frame, recognized_employees):
        """Draw boxes around recognized faces"""
        for employee in recognized_employees:
            top, right, bottom, left = employee['face_location']
            
            # Draw rectangle
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            
            # Draw label
            label = f"{employee['employee_name']} ({employee['employee_id']})"
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
            cv2.putText(frame, label, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)
        
        return frame