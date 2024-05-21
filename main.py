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

def test_callback(numArray):
    """_summary_

    Args:
        numArray (_type_): _description_

    Returns:
        _type_: _description_
    """
    from ultralytics import YOLO
    if __name__ == '__main__':
        ###### Load a model 
        model = YOLO("C:/Users/User/Desktop/PyQT5/Batch_Code_Inspection_System/Main/algorithm/Yolo/yolov8m-obb.pt")
        ##### Predict with the model
        results = model(numArray) ##### predict on the image
        img= results['orig_img']
        print("-------------------Image Info --------------------------------",type(results))
        
    # numArray = cv2.putText(numArray, 'OpenCV', (50, 50), fontFace=cv2.FONT_HERSHEY_SIMPLEX ,  
    #                 fontScale=1, color = (255, 0, 0) , thickness = 2, lineType=cv2.LINE_AA) 
    
    # numArray = cv2.resize(numArray, (3000, 3000))
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

    