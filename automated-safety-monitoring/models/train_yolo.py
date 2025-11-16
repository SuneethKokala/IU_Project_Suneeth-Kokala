# train_yolo.py
import os
os.environ['TORCH_WEIGHTS_ONLY'] = 'False'
from ultralytics import YOLO


# Edit these paths as needed
DATA_YAML = 'datasets/Helmet-Vest-Belt.v1i.yolov8/data.yaml'
MODEL_SAVE = 'runs/detect/helmet_vest'


if __name__ == '__main__':
# Train from scratch without pre-trained weights
    model = YOLO('yolov8n.yaml')  # Use architecture config instead of weights


# Train: epochs, batch, imgsz adjustable
    model.train(data=DATA_YAML, epochs=20, batch=8, imgsz=640, project='runs/detect', name='helmet_vest', pretrained=False, patience=30)


# After training, the best model will be at runs/detect/helmet_vest/weights/best.pt
    print('Training finished. Best weights in runs/detect/helmet_vest/weights/best.pt')