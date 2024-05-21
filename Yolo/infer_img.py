import cv2
import numpy as np
import matplotlib.pyplot as plt
from ultralytics import YOLO
import torch

def predict_image():
    # Load the YOLOv8 model
    model = YOLO("C:/Users/User/Desktop/PyQT5/Batch_Code_Inspection_System/Main/algorithm/Yolo/yolov8m-obb.pt")

    # Load the image
    image = cv2.imread('C:/Users/User/Desktop/PyQT5/Batch_Code_Inspection_System/Main/test/bus.jpg')
    if image is None:
        raise ValueError(f"Image not found at its location")
    
    # Convert the image to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Perform inference
    results = model(image_rgb)
    
    # Extract information from the results
    predictions = []
    for result in results:
        if isinstance(result, torch.Tensor):
            result = result.cpu().numpy()
        for pred in result:
            # Extract bounding box coordinates
            bbox = pred[:4]
            # Extract confidence score
            conf = pred[4]
            # Extract class label
            cls = pred[5]

            # Append the prediction details to the list
            predictions.append({
                'bbox': bbox.tolist(),
                'confidence': conf,
                'class': int(cls)
            })
            
            # Draw bounding box on the image
            x1, y1, x2, y2 = map(int, bbox)
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            label = f"{model.names[int(cls)]}: {conf:.2f}"
            cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the image
    cv2.imshow("Detected Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return predictions
    
predict_image()


