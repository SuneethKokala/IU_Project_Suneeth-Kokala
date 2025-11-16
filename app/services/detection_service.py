import os
import numpy as np
from ultralytics import YOLO
from app.core.face_recognition_system import FaceRecognitionSystem

class DetectionService:
    def __init__(self):
        self.ppe_model = self._load_ppe_model()
        self.face_system = FaceRecognitionSystem()
    
    def _load_ppe_model(self):
        model_path = 'runs/detect/helmet_vest11/weights/best.pt'
        if os.path.exists(model_path):
            return YOLO(model_path)
        return YOLO('yolov8n.pt')
    
    def detect_ppe(self, image, conf=0.1, iou=0.45):
        results = self.ppe_model(image, conf=conf, iou=iou)
        detections = []
        
        for r in results:
            if r.boxes is not None:
                for box in r.boxes:
                    cls = int(box.cls[0])
                    confidence = float(box.conf[0])
                    coords = box.xyxy[0].tolist()
                    class_name = self.ppe_model.names.get(cls, f"class_{cls}")
                    
                    # Filter out belt detections
                    if class_name.lower() != 'belt':
                        detections.append({
                            "type": "ppe",
                            "class": class_name,
                            "confidence": confidence,
                            "bbox": coords
                        })
        
        return detections
    
    def detect_faces(self, image):
        faces = self.face_system.recognize_faces(image)
        detections = []
        
        for face in faces:
            detections.append({
                "type": "face",
                "employee_id": face['employee_id'],
                "employee_name": face['employee_name'],
                "confidence": face['confidence'],
                "bbox": list(face['face_location'])
            })
        
        return detections
    
    def detect_all(self, image):
        ppe_detections = self.detect_ppe(image)
        face_detections = self.detect_faces(image)
        
        return {
            "ppe_detections": ppe_detections,
            "face_detections": face_detections,
            "total_detections": len(ppe_detections) + len(face_detections)
        }