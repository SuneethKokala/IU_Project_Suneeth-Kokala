# detect_general.py - Use general pre-trained YOLO
import cv2
from ultralytics import YOLO
import time

def main(source=0):
    # Use general pre-trained model
    model = YOLO('yolov8n.pt')  # Downloads automatically
    
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
        
        # Run inference
        results = model(frame, imgsz=640)
        
        # Draw results
        annotated_frame = results[0].plot()
        
        # FPS
        fps = 1.0 / (time.time() - fps_time) if fps_time else 0.0
        fps_time = time.time()
        cv2.putText(annotated_frame, f'FPS: {fps:.1f}', (10, annotated_frame.shape[0]-10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1)
        
        cv2.imshow('General YOLO Detection', annotated_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(0)