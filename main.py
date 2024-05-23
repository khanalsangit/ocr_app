import os
import cv2
import pickle
import glob
import sys
import shutil

from PyQt5.QtWidgets import QMainWindow
from Custom_Widgets import *
from PyQt5 import QtCore, QtGui, QtWidgets 
from camera_interface.camera import MachineVisionCamera
from controller.gui_operations import PyQTWidgetFunction
from controller.live_operations import LiveOperationFunction
from controller.debug_operations import DebugOperationFunction
# from Augmentation.main import Augmentation_ProgressBar

from controller.gui_bindings import Controller

class MainWin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = PyQTWidgetFunction(self)
        # self.live = LiveOperationFunction(self)

import yaml
from ultralytics import YOLO
import time
import torch

def test_callback(numArray):
    """_summary_

    Args:
        numArray (_type_): _description_

    Returns:
        _type_: _description_
    """
    ####### if there is only detection #########

    # live = LiveOperationFunction()

    with open("./main_config.yaml", 'r') as f: ##### Load configuration file #######
        current_brand_config = yaml.safe_load(f)
    pickle_path = os.path.join(current_brand_config['pickle_path'],'system.pkl')
    with open(pickle_path,'rb') as f:
        system_values = pickle.load(f)
  
    if system_values['ocr_method'] == False:
        ###### Load a model ####### 
        model = YOLO("best.pt")
        start_time = time.time()
        results = model.predict(numArray,device = 0) ##### predict on the image
        detection_time = time.time() - start_time
        print("Detection time",detection_time)
        # live.detectionTime.setText(detection_time)   ###### Add the detection time in GUI
        for result in results:
            all_info = result.obb
            No_of_box = len(all_info.xyxyxyxy)
            annotated_img = result.plot()  ##### Images with bounding box
            # Ensure that the image is in BGR format for OpenCV
            if annotated_img.shape[2] == 3:  # if the image has 3 channels
                numArray = annotated_img
            else:
                raise ValueError("Unexpected number of channels in annotated image.")

        if system_values['nooflines'] == str(No_of_box):  ##### Check if the no of lines matched with number of object
            rejected = False
            return numArray,rejected
        else:
            rejected = True
            return numArray,rejected
    # from ultralytics.utils import ASSETS
    # from ultralytics.models.yolo.obb import OBBPredictor

    # args = dict(model='best.pt', source=numArray)
    # predictor = OBBPredictor(overrides=args)
    # result = predictor.predict_cli()
    # print("Predictor",predictor)
    # rejected = True
    # return numArray, rejected
        
        

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

    
   