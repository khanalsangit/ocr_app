import os 
import sys

from PyQt5 import QtWidgets, QtCore, QtGui
from pyUIdesign import Ui_MainWindow

# from gui.pyUIdesign import Ui_MainWindow, 
from gui.PyUICBasicDemo import Ui_MainWindow 

from camera_interface.camera import MachineVisionCamera

class Albert(Ui_MainWindow):
    def __init__(self, main_window, camera: MachineVisionCamera) -> None:
        super().__init__()
        self.setupUi(main_window)
        self.camera = camera

    def set_camera_to_gui(self):
        self.camera.set_ui(self)
        self.bnEnum.clicked.connect(self.camera.enum_devices)
        self.bnOpen.clicked.connect(self.camera.open_device)
        self.bnClose.clicked.connect(self.camera.close_device)
        self.bnStart.clicked.connect(self.camera.start_grabbing)
        self.bnStop.clicked.connect(self.camera.stop_grabbing)

        self.bnSoftwareTrigger.clicked.connect(self.camera.trigger_once)
        self.radioTriggerMode.clicked.connect(self.camera.set_software_trigger_mode)
        self.radioContinueMode.clicked.connect(self.camera.set_continue_mode)

        self.bnGetParam.clicked.connect(self.camera.get_param)
        self.bnSetParam.clicked.connect(self.camera.set_param)

        self.bnSaveImage.clicked.connect(self.camera.save_bmp)
        

if __name__=="__main__":
    import sys
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    camera = MachineVisionCamera()

    albert = Albert(MainWindow, camera)
    albert.set_camera_to_gui()

    MainWindow.show()   
    sys.exit(app.exec_())