import os
import cv2
import pickle
import glob
import sys
import shutil

from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtWidgets, QtCore, QtGui
from gui.pyUIdesign import Ui_MainWindow
from Custom_Widgets import *
from Custom_Widgets import *

from camera_interface.camera import MachineVisionCamera
from controller.gui_operations import PyQTWidgetFunction
from controller.live_operations import LiveOperationFunction
from controller.debug_operations import DebugOperationFunction
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
    # cv2.imshow('test', cv2.resize(numArray, (500,500)))
    # cv2.waitKey(100)
    numArray = cv2.putText(numArray, 'OpenCV', (50, 50), fontFace=cv2.FONT_HERSHEY_SIMPLEX ,  
                    fontScale=1, color = (255, 0, 0) , thickness = 2, lineType=cv2.LINE_AA) 
    
    numArray = cv2.resize(numArray, (3000, 3000))
    rejected = True
    return numArray, rejected 
    

if __name__=="__main__":
    import sys
    from multiprocessing import process
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    app = QtWidgets.QApplication(sys.argv)
    ui = QMainWindow() # MainWin()

    camera = MachineVisionCamera()
    gui_operations = PyQTWidgetFunction(ui)
    live_mode = LiveOperationFunction(gui_operations)
    debug_mode = DebugOperationFunction(gui_operations)
    controller = Controller(camera, live_mode, debug_mode, gui_operations)
    camera.callback = test_callback
    camera.ui_update_callback =  gui_operations.update_live_gui_with_based_on_result
    loadJsonStyle(ui, gui_operations)
    ui.closeEvent = camera.close_device
    ui.show()

    sys.exit(app.exec_())