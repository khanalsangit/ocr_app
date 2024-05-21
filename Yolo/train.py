from ultralytics import YOLO
if __name__ == '__main__':
    # Load a model
    # model = YOLO('yolov8n-obb.yaml')  # build a new model from YAML
    model = YOLO('yolov8m-obb.pt')  # load a pretrained model (recommended for training)
    # model = YOLO('yolov8n-obb.yaml').load('yolov8n.pt')  # build from YAML and transfer weights

    # Train the model
    results = model.train(data='data_config.yaml', epochs=50, imgsz=416, batch = 2)