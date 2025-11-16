# export_model.py
from ultralytics import YOLO


MODEL = 'runs/detect/helmet_vest/weights/best.pt'


y = YOLO(MODEL)
# export to ONNX
y.export(format='onnx')
print('Exported to onnx')