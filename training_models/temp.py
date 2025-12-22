from ultralytics import YOLO

model = YOLO("yolov8n-pose.yaml")
results = model.train(data="court_keypoints/data.yaml", epochs=100, batch=24)
