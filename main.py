import os
import cv2
import pickle
import glob
import sys

from PyQt5.QtWidgets import QMainWindow
from Custom_Widgets import *
from PyQt5 import QtCore, QtGui, QtWidgets 
from camera_interface.camera import MachineVisionCamera
from controller.gui_operations import PyQTWidgetFunction
from controller.live_operations import LiveOperationFunction
from controller.debug_operations import DebugOperationFunction
from controller.gui_bindings import Controller
from ultralytics.models.yolo.model import YOLO
import yaml
from ultralytics import YOLO
import time

###### Load YOLOV8model ####### 
model = YOLO("C:/Users/User/Desktop/PyQT5/Batch_Code_Inspection_System/Main/runs/obb/train/weights/best.pt")
    
class MainWin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = PyQTWidgetFunction(self)

def test_callback(numArray):
    """_summary_

    Args:
        numArray (_type_): _description_

    Returns:
        _type_: _description_
    """
    
    with open("./main_config.yaml", 'r') as f: ##### Load configuration file #######
        current_brand_config = yaml.safe_load(f)
    pickle_path = os.path.join(current_brand_config['pickle_path'],'system.pkl')
    with open(pickle_path,'rb') as f:
        system_values = pickle.load(f)

####### if there is only detection #########
    if system_values['ocr_method'] == False:
        custom_labels = {
            0:'chhabi',
            1:'lal',
            2:'tamang',
            3:'sumit',
            4:'tamang'
        }

    start_time = time.time()
    results = model.predict(numArray,device = 'cuda') ##### predict on the image
    detection_time = time.time() - start_time

    # live.detectionTime.setText(detection_time)   ###### Add the detection time in GUI
    for result in results:
        all_info = result.obb
        No_of_box = len(all_info.xyxyxyxy)
        annotated_img = result.orig_img.copy()  # Copy the original image

        for box in all_info:
            # Extract the bounding box coordinates and convert them to integers
            x1, y1, x2, y2, x3, y3, x4, y4 = [int(coord) for coord in box.xyxyxyxy.flatten()]

            # Extract the class id
            class_id = int(box.cls)
            
            # Extract the default label and map it to the custom label
            default_label = result.names[class_id]
            custom_label = custom_labels.get(class_id, default_label)  

            # Draw the bounding box
            points = [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
            for j in range(4):
                cv2.line(annotated_img, points[j], points[(j + 1) % 4], (0, 255, 0), 2)

            # Put the custom label text near the bounding box
            cv2.putText(annotated_img, custom_label, (x1-50, y1 - 90), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # Ensure that the image is in BGR format for OpenCV
        if annotated_img.shape[2] == 3:  # if the image has 3 channels
            numArray = annotated_img
        else:
            raise ValueError("Unexpected number of channels in annotated image.")
        
    detection_time = time.time() - start_time

    if system_values['nooflines'] == str(No_of_box):  ##### Check if the no of lines matched with number of object
        rejected = False
        return numArray,rejected
    else:
        rejected = True
        return numArray,rejected

    
        

if __name__=="__main__":
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    app = QtWidgets.QApplication(sys.argv)
    ui = QMainWindow() # MainWin()
    gui_operations = PyQTWidgetFunction(ui)
    camera = MachineVisionCamera()
    # augment_mode = Augmentation_ProgressBar()
    live_mode = LiveOperationFunction(gui_operations)
    debug_mode = DebugOperationFunction(gui_operations)
    controller = Controller(camera, live_mode, debug_mode, gui_operations)
    camera.callback = test_callback
    
    camera.ui_update_callback =  gui_operations.update_live_gui_with_based_on_result
    loadJsonStyle(ui, gui_operations)
    ui.closeEvent = camera.close_device
    ui.show()

    sys.exit(app.exec_())

    
   