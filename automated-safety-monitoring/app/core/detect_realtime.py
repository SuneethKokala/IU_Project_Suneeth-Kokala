# detect_realtime.py
import cv2
from ultralytics import YOLO
from utils import draw_boxes, check_ppe_for_workers
from face_recognition_system import FaceRecognitionSystem
import time


# Path to your trained model. Change if needed.
MODEL_PATH = 'runs/detect/helmet_vest11/weights/best.pt' # after training
CONF = 0.25  # Lower threshold to detect more objects




def main(source=0):  # Use camera index 0
# source: 0 for webcam, or RTSP/HTTP video stream
    model = YOLO(MODEL_PATH)
    face_system = FaceRecognitionSystem()


    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        print('Failed to open source:', source)
        return


    fps_time = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            print('Frame not received, breaking')
            break


# Run inference (results is a list of ultralytics Results)
        results = model(frame, imgsz=640) # get results
        frame, detections = draw_boxes(frame, results, conf_thres=CONF)
        
        # Recognize faces
        recognized_employees = face_system.recognize_faces(frame)
        frame = face_system.draw_face_boxes(frame, recognized_employees)
        
        # Get current employee info for PPE checking
        current_employee = recognized_employees[0] if recognized_employees else None
        alerts = check_ppe_for_workers(detections, current_employee)
        for i, a in enumerate(alerts):
            cv2.putText(frame, a, (10, 30 + i*24), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)


# FPS
        fps = 1.0 / (time.time() - fps_time) if fps_time else 0.0
        fps_time = time.time()
        cv2.putText(frame, f'FPS: {fps:.1f}', (10, frame.shape[0]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1)


        cv2.imshow('PPE Monitoring', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    cap.release()
    cv2.destroyAllWindows()




if __name__ == '__main__':
# Use camera index 0
    main(0)