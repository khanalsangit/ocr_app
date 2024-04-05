import os 
import sys

from PyQt5 import QtWidgets, QtCore, QtGui


# from gui.pyUIdesign import Ui_MainWindow, 
from gui.PyUICBasicDemo import Ui_MainWindow 
from gui_camera_bindings.controller import Controller
from camera_interface.camera import MachineVisionCamera

        

if __name__=="__main__":
    import sys
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    camera = MachineVisionCamera()
    controller = Controller(MainWindow, camera=camera)
    controller.set_camera_to_gui()

    MainWindow.show()   
    sys.exit(app.exec_())