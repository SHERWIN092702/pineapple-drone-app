from ultralytics import YOLO

# Load a YOLOv8n PyTorch model
model = YOLO('/home/rpi5/Desktop/yolo_object/best.pt')

# Export the model to NCNN format
model.export(format="ncnn", imgsz=2160)  # creates 'yolov8n_ncnn_model'