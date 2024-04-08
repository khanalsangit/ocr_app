import os 
import sys

from PyQt5 import QtWidgets, QtCore, QtGui


# from gui.pyUIdesign import Ui_MainWindow, 
from gui.PyUICBasicDemo import Ui_MainWindow 
from gui_camera_bindings.controller import Controller
from camera_interface.camera import MachineVisionCamera

import cv2 
def test_callback(numArray):
    print('image size ', numArray.shape)
    cv2.imshow('test', cv2.resize(numArray, (500,500)))
    cv2.waitKey(1)
    

if __name__=="__main__":
    import sys
    from multiprocessing import process
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    camera = MachineVisionCamera()
    controller = Controller(MainWindow, camera=camera)
    controller.set_camera_to_gui()
    camera.callback = test_callback

    MainWindow.show()   
    sys.exit(app.exec_())