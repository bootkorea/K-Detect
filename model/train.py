from ultralytics import YOLO

# Load a model
model = YOLO('best.pt')  # load a pretrained model (recommended for training)

# Train the model
results = model.train(data='pm.yaml', epochs=50, imgsz=([1920, 1080]), batch=12, device=[1, 2, 3, 4, 5, 7])

