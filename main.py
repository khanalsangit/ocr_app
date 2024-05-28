import sys

from PyQt5.QtWidgets import QMainWindow
# from Custom_Widgets import *
from PyQt5 import QtCore, QtGui, QtWidgets 
from PyQt5.QtWidgets import QMainWindow, QApplication
from Custom_Widgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from camera_interface.camera import MachineVisionCamera
from controller.gui_operations import PyQTWidgetFunction
from controller.live_operations import LiveOperationFunction
from controller.debug_operations import DebugOperationFunction
from controller.gui_bindings import Controller
from ultralytics.models.yolo.model import YOLO
from ultralytics import YOLO
from algorithm.yolo import object_detection_yolo

###### Load YOLOV8model ####### 
model = YOLO("./best.pt")
    
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
    ##### Call the object detection function 
    return object_detection_yolo(model,numArray)



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
    camera.callback = lambda x: object_detection_yolo(model, x) # test_callback
    
    camera.ui_update_callback =  gui_operations.update_live_gui_with_based_on_result
    # loadJsonStyle(ui, gui_operations)
    ui.closeEvent = camera.close_device
    ui.update()
    QApplication.processEvents()
    ui.show()
    sys.exit(app.exec_())

    
   