from ultralytics import YOLO
if __name__ == '__main__':
    # Load a model
    model = YOLO('yolov8m-obb.pt')  # load a pretrained model (recommended for training)

    # Train the model
    results = model.train(data='data_config.yaml', epochs=50, imgsz=416, batch = 2)