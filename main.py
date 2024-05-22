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
    # from ultralytics.yolo.engine.results import Results
    # from ultralytics.yolo.utils.plotting import Annotator, colors

        ###### Load a model 
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

    
   