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

from camera_interface.camera import MachineVisionCamera
from controller.gui_operations import PyQTWidgetFunction
from controller.live_operations import LiveOperationFunction
from controller.debug_operations import DebugOperationFunction
from controller.gui_bindings import Controller

class MainWin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = PyQTWidgetFunction(self)
         
        ############### Loading existing pickle values for all the parameters of GUI ###############################
        pkl_file = glob.glob('Pickle/*')  
        if len(pkl_file)==0:
            with open('system_pickles/initial_param.pkl','rb') as f:
                brand_values = pickle.load(f) 
        else:
            for p in pkl_file:
                with open(p,"rb") as file:
                    brand_values = pickle.load(file)

        print("Brand",brand_values)
        ###### Setting the initial values in GUI Parameters
        if brand_values['ocr_method_enable'] == True:  ######## Set the ocr method radiobutton 
            self.ui.detection_recognition.setChecked(True)
        else:
            self.ui.detectionOnly.setChecked(True)
        
        self.ui.no_ofLine_comboBox.setCurrentText(str(brand_values['no_of_lines']))
        self.ui.line1Box.insert(brand_values['line1'])
        self.ui.line2Box.insert(brand_values['line2'])
        self.ui.line3Box.insert(brand_values['line3'])
        self.ui.line4Box.insert(brand_values['line4'])
        self.ui.minPercent_Entry.insert(str(brand_values['min_per_thresh']))
        self.ui.linearThresh_Entry.insert(str(brand_values['line_per_thresh']))
        self.ui.rejectCount_Entry.insert(str(brand_values['reject_count']))
        self.ui.cameraGain_Entry.insert(str(brand_values['camera_gain']))
        self.ui.exposureTime_Entry.insert(str(brand_values['exposure_time']))
        self.ui.triggerDelay_Entry.insert(str(brand_values['trigger_delay']))
        self.ui.roiEntry.insert(str(brand_values['roi']))
        
        ################ For Rejection Enable #############
        if brand_values['reject_enable'] == True:
            self.ui.rejectEnable_Yes.setChecked(True)
        else:
            self.ui.rejectEnable_No.setChecked(True)
 
        ################ For Save Image ##################
        if brand_values['save_img'] == True:
            self.ui.saveImage_Checkbox.setChecked(True)
        else:
            self.ui.saveImage_Checkbox.setChecked(False)

        ################ For Save Result #################
        if brand_values['save_result'] == True:
            self.ui.ui.setChecked(True)
        else:
            self.ui.ui.setChecked(False)
        
        ################# For Save NG Image #############
        if brand_values['save_ng'] == True:
            self.ui.saveNG_Checkbox.setChecked(True)
        else:
            self.ui.saveNG_Checkbox.setChecked(False)



import cv2 
def test_callback(numArray):
    # cv2.imshow('test', cv2.resize(numArray, (500,500)))
    # cv2.waitKey(100)
    numArray = cv2.putText(numArray, 'OpenCV', (50, 50), fontFace=cv2.FONT_HERSHEY_SIMPLEX ,  
                    fontScale=1, color = (255, 0, 0) , thickness = 2, lineType=cv2.LINE_AA) 
    
    numArray = cv2.resize(numArray, (3000, 3000))
    return numArray
    

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
    loadJsonStyle(ui, gui_operations)

    ui.closeEvent = camera.close_device
    ui.show()

    sys.exit(app.exec_())