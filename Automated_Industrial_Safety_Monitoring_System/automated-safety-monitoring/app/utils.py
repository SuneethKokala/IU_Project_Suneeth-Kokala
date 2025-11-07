# utils.py
import cv2
import numpy as np


CLASS_NAMES = ['belt', 'helmet', 'vest']


def draw_boxes(frame, results, conf_thres=0.35):
    """Draw boxes from ultralytics results object onto frame and return detections list.
Detections list format: [{'class': 'helmet', 'conf':0.9, 'box':[x1,y1,x2,y2]}, ...]
"""
    detections = []
    for r in results: # results from model(frame)
        boxes = r.boxes
        for b in boxes:
            conf = float(b.conf[0]) if hasattr(b.conf, '__len__') else float(b.conf)
            if conf < conf_thres:
                continue
            cls = int(b.cls[0]) if hasattr(b.cls, '__len__') else int(b.cls)
            xyxy = b.xyxy[0].cpu().numpy() if hasattr(b.xyxy, 'cpu') else np.array(b.xyxy[0])
            x1,y1,x2,y2 = xyxy.astype(int).tolist()
            label = CLASS_NAMES[cls]
            detections.append({'class': label, 'conf': conf, 'box': [x1,y1,x2,y2]})
            # Draw
            cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 2)
            text = f"{label} {conf:.2f}"
            (tw, th), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
            cv2.rectangle(frame, (x1, y1 - th - 6), (x1 + tw, y1), (0,255,0), -1)
            cv2.putText(frame, text, (x1, y1 - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,0), 1, cv2.LINE_AA)
    return frame, detections




def check_ppe_for_workers(detections, current_employee=None):
    """Check PPE compliance and send violations to dashboard."""
    import time
    import json
    from datetime import datetime
    
    # Track last notification time to avoid spam
    if not hasattr(check_ppe_for_workers, 'last_notification'):
        check_ppe_for_workers.last_notification = 0
    
    classes = {d['class'] for d in detections}
    alerts = []
    missing_ppe = []
    
    # Check for missing PPE
    if 'helmet' not in classes:
        alerts.append('No helmet detected in frame')
        missing_ppe.append('helmet')
    if 'vest' not in classes:
        alerts.append('No vest detected in frame')
        missing_ppe.append('vest')
    if 'belt' not in classes:
        alerts.append('No safety belt detected in frame')
        missing_ppe.append('belt')
    
    # Send to dashboard if PPE is missing (limit to once every 30 seconds)
    current_time = time.time()
    if missing_ppe and (current_time - check_ppe_for_workers.last_notification) > 30:
        if current_employee:
            employee_id = current_employee['employee_id']
            employee_name = current_employee['employee_name']
        else:
            employee_id = "UNKNOWN"
            employee_name = "Unknown Employee"
        
        # Log violation to file for dashboard
        violation = {
            "timestamp": datetime.now().isoformat(),
            "employee_id": employee_id,
            "employee_name": employee_name,
            "missing_ppe": missing_ppe
        }
        
        try:
            with open("ppe_violations.log", "a") as f:
                f.write(json.dumps(violation) + "\n")
        except Exception as e:
            print(f"Failed to log violation: {e}")
        
        check_ppe_for_workers.last_notification = current_time
        alerts.append(f"ALERT SENT TO DASHBOARD!")
    
    return alerts