# yolo_trainer.py - YOLO model training
import os
os.environ['TORCH_WEIGHTS_ONLY'] = 'False'
from ultralytics import YOLO

# Configuration
DATA_YAML = 'datasets/Helmet-Vest-Belt.v1i.yolov8/data.yaml'
MODEL_SAVE = 'runs/detect/helmet_vest'

def train_model(epochs=200, batch_size=8, img_size=640):
    """Train YOLO model for PPE detection"""
    print("🚀 Starting YOLO training for PPE detection...")
    
    # Train from scratch without pre-trained weights
    model = YOLO('yolov8n.yaml')
    
    # Train with specified parameters
    model.train(
        data=DATA_YAML, 
        epochs=epochs, 
        batch=batch_size, 
        imgsz=img_size, 
        project='runs/detect', 
        name='helmet_vest', 
        pretrained=False, 
        patience=30
    )
    
    print('✅ Training finished. Best weights in runs/detect/helmet_vest/weights/best.pt')
    return model

if __name__ == '__main__':
    train_model()