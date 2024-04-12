import pickle
import glob
import cv2
import os
import shutil
import sys
from gui.pyUIdesign import Ui_MainWindow
#from gui.PyUICBasicDemo import Ui_MainWindow 
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *

from .live_operations import LiveOperationFunction
from .debug_operations import DebugOperationFunction 

class PyQTWidgetFunction(Ui_MainWindow):
    def __init__(self, main_window) -> None:
        super().__init__()
        self.setupUi(main_window)
        self.save_image_path = None 

        self.live = LiveOperationFunction(self)
        self.debug = DebugOperationFunction(self)
    ################################################################ Live Mode Functions ###############################################################
            ################################################################################################################################
                    ################################################################################################################
                            ###########################################################################################
    def switch_mode(self):
        '''
        This method switch the live or debug mode
        '''
        if self.switchButton.isChecked():
            self.stackWidget.setCurrentWidget(self.debugMode_Page)
            self.switchButton.setText('Debug')
        else:
            self.switchButton.setText('Live')
            self.stackWidget.setCurrentWidget(self.liveMode_Page)
    
    def get_current_mode(self) -> str:
        """
        returns the current mode of the gui: Live or Debug

        Returns
        --------------
        mode: str
            returns string either Debug or Live

        """
        return self.switchButton.text()

        ######################### Method to save all the parameters ########################
        ###########################################################################
            ##################################################################
       
    def get_live_gui_values(self)-> None:
        '''
        Function that takes all the user inputs values from GUI and saved in pickle file
        '''
        brand_param_dict = {
            'brand_name':self.projectName.text()
            ,'ocr_method_enable': True if self.detection_recognition.isChecked() else False
            ,'no_of_lines':self.no_ofLine_comboBox.currentText()
            ,'line1':self.line1Box.text()
            ,'line2':self.line2Box.text()
            ,'line3':self.line3Box.text()
            ,'line4':self.line4Box.text()
            ,'min_per_thresh':self.minPercent_Entry.text()
            ,'line_per_thresh':self.linearThresh_Entry.text()
            ,'reject_count':self.rejectCount_Entry.text()
            ,'reject_enable':True if self.rejectEnable_Yes.isChecked() else False 
            ,'exposure_time':self.exposureTime_Entry.text()
            ,'trigger_delay':self.triggerDelay_Entry.text()
            ,'camera_gain':self.cameraGain_Entry.text()
            ,'roi':self.roiEntry.text()
            ,'save_img':True if self.saveImage_Checkbox.isChecked() else False
            ,'save_ng':True if self.saveNG_Checkbox.isChecked() else False
            ,'save_result':True if self.saveResult_Checkbox.isChecked() else False
            ,'img_dir':self.directoryName_Entry.text()
        }


        pkl_dir = glob.glob('Pickle/*.pkl')
        for pkl in pkl_dir:
            print("Pickle",pkl)
            
        with open(pkl, 'rb') as brand:
            brand_values = pickle.load(brand)
        

        
        with open(pkl,'wb') as new_brand:
            pickle.dump(brand_param_dict, new_brand) #writing pickle files for brand parameters
        srcs = pkl
        pik_lst = pkl.split('.')
        pik_str = str(pik_lst[0])
        pik_str = pik_str.split('\\')
        dests = os.getcwd() + '/Pickle/' + pik_str[1]
        shutil.copy(srcs, dests)
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Parameter Save Successfully")
        msgBox.setWindowTitle("Parameter")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msgBox.exec()

       

