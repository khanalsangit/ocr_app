from ultralytics import YOLO
    # from ultralytics.yolo.engine.results import Results
    # from ultralytics.yolo.utils.plotting import Annotator, colors

        ###### Load a model ####### 
model = YOLO("C:/Users/User/Desktop/PyQT5/Batch_Code_Inspection_System/Main/best.pt")
##### Predict with the model
results = model(numArray) ##### predict on the image
for result in results:
    names = result.names
    annotated_img = result.plot()  ##### Images with bounding box
    boxes = result.obb.xyxyxyxy.cpu().numpy()
    classes = result.names
    # Ensure that the image is in BGR format for OpenCV
    if annotated_img.shape[2] == 3:  # if the image has 3 channels
        numArray = annotated_img
    #     cv2.imshow("Image", annotated_img)
    else:
        raise ValueError("Unexpected number of channels in annotated image.")
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
rejected = True
return numArray, rejected