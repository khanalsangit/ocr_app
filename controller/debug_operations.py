from __future__ import annotations
import pickle
import glob
import cv2
import os
import shutil
import traceback

from gui.pyUIdesign import Ui_MainWindow
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *
from Parameter_Value.param_tools import save_parameter, get_parameter


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .gui_operations import PyQTWidgetFunction

from gui import brand_management as bm 

class DebugOperationFunction(Ui_MainWindow):
    def __init__(self, parent: PyQTWidgetFunction):
        '''
        Initialize the variable associated with the debug mode 

        Parameter
        -------------------------
        parent: PyQTWidgetFunction
        pass the object `PyQTWidgetFunction` that inherits the class `Ui_MainWindow` generated from `ui`
        '''
        ###### debug buttons variables ######
        self.parent = parent
        self.editProject = parent.editProject
        self.createProject_Page = parent.createProject_Page
        self.createProjectButton = parent.createProjectButton
        self.cameraButton = parent.cameraButton
        self.preprocessingButton = parent.preprocessingButton
        self.detectionButton = parent.detectionButton
        self.recognitionButton = parent.recognitionButton
        self.analysisButton = parent.analysisButton

        ###### debug page variables ########
        self.camera_Page = parent.camera_Page
        self.dataProcessing_Page = parent.dataProcessing_Page
        self.detection_Page = parent.detection_Page
        self.recognition_Page = parent.recognition_Page
        self.analysis_Page = parent.analysis_Page

        # project create and import 
        self.createButton = parent.createButton
        self.importButton = parent.importButton

        # camera button
        self.getParameter_Button = parent.getParameter_Button 
        self.setParameter_Button = parent.setParameter_Button 
        self.deleteImage_Button = parent.deleteImage_Button
        self.captureButton = parent.captureButton 
        # camera entries 
        self.exposureEntry_Debug = parent.exposureEntry_Debug 
        self.gainEntry_Debug = parent.gainEntry_Debug 
        self.frameRateEntry_Debug = parent.frameRateEntry_Debug 
        self.delayEntry_Debug = parent.delayEntry_Debug
        self.totalImage_Count = parent.totalImage_Count 

        ##### augmentation widget variables
        self.nTimesEntry = parent.nTimesEntry
        self.rotateEntry = parent.rotateEntry
        self.blurEntry = parent.blurEntry
        self.contrastEntry = parent.contrastEntry
        self.recursionRateEntry = parent.recursionRateEntry
        self.flipEntry = parent.flipEntry
        self.rigidEntry = parent.rigidEntry
        self.elasticEntry = parent.elasticEntry

         
    def create_project(self)->None:
        '''
        Opens the create project section
        '''
        self.editProject.setCurrentWidget(self.createProject_Page)
        self.createProjectButton.setStyleSheet("QPushButton{\n"
        "    background-color:#0DC177;\n"
        "    border-radius:4px;\n"
        "}")
        self.cameraButton.setStyleSheet("")
        self.preprocessingButton.setStyleSheet("")
        self.detectionButton.setStyleSheet("")
        self.recognitionButton.setStyleSheet("")
        self.analysisButton.setStyleSheet("")

    def camera_debug(self)->None:
        '''
        Opens the camera section for debug mode
        '''
        self.editProject.setCurrentWidget(self.camera_Page)
        self.cameraButton.setStyleSheet("QPushButton{\n"
        "    background-color:#0DC177;\n"
        "    border-radius:4px;\n"
        "}")
        self.createProjectButton.setStyleSheet("")
        self.preprocessingButton.setStyleSheet("")
        self.detectionButton.setStyleSheet("")
        self.recognitionButton.setStyleSheet("")
        self.analysisButton.setStyleSheet("")
    
    def camera_image_button_bindings(self):
        self.getParameter_Button.clicked.connect(self.get_parameter_from_camera)
        ...

    def preprocessing_step(self)->None:
        '''
        Opens the preprocessing section
        '''
        self.editProject.setCurrentWidget(self.dataProcessing_Page)
        self.preprocessingButton.setStyleSheet("QPushButton{\n"
        "    background-color:#0DC177;\n"
        "    border-radius:4px;\n"
        "}")
        self.cameraButton.setStyleSheet("")
        self.createProjectButton.setStyleSheet("")
        self.detectionButton.setStyleSheet("")
        self.recognitionButton.setStyleSheet("")
        self.analysisButton.setStyleSheet("")
    
    def load_augment_param(self,ntimes:int, rotate:int, flip:int, blur:int, contrast:int, elastic:int, rigid:int, recursion_rate:float)-> None:
        '''
        Load the current augmentation parameters to the gui widgets
        '''
        self.nTimesEntry.setText(str(ntimes))
        self.rotateEntry.setText(str(rotate))
        self.blurEntry.setText(str(blur))
        self.contrastEntry.setText(str(contrast))
        self.recursionRateEntry.setText(str(elastic))
        self.flipEntry.setText(str(flip))
        self.rigidEntry.setText(str(rigid))
        self.elasticEntry.setText(str(recursion_rate))

    def detection(self)->None:
        '''
        Opens the detection section
        '''
        self.editProject.setCurrentWidget(self.detection_Page)
        self.detectionButton.setStyleSheet("QPushButton{\n"
        "    background-color:#0DC177;\n"
        "    border-radius:4px;\n"
        "}")
        self.createProjectButton.setStyleSheet("")
        self.cameraButton.setStyleSheet("")
        self.preprocessingButton.setStyleSheet("")
        self.recognitionButton.setStyleSheet("")
        self.analysisButton.setStyleSheet("")
    
    def recognition(self)->None:
        '''
        Opens the recognition section
        '''
        self.editProject.setCurrentWidget(self.recognition_Page)
        self.recognitionButton.setStyleSheet("QPushButton{\n"
        "    background-color:#0DC177;\n"
        "    border-radius:4px;\n"
        "}")
        self.detectionButton.setStyleSheet("")
        self.createProjectButton.setStyleSheet("")
        self.cameraButton.setStyleSheet("")
        self.preprocessingButton.setStyleSheet("")
        self.analysisButton.setStyleSheet("")
    
    def analysis(self)->None:
        '''
        Opens the analysis section
        '''
        self.editProject.setCurrentWidget(self.analysis_Page)
        self.analysisButton.setStyleSheet("QPushButton{\n"
        "    background-color:#0DC177;\n"
        "    border-radius:4px;\n"
        "}")
        self.detectionButton.setStyleSheet("")
        self.recognitionButton.setStyleSheet("")
        self.createProjectButton.setStyleSheet("")
        self.cameraButton.setStyleSheet("")
        self.preprocessingButton.setStyleSheet("")

    def create_brand(self):
        """
        Method to open brand creation window
        """
        # enabled = self.createButton.isEnabled()
        # self.createButton.setEnabled(not enabled)
        # if enabled:
        bm.createWindow(self.parent.main_window, brand_dir = './Brands/').show()
    
    def import_brand(self):
        """
        Method to open brand import windows
        """
        # enabled = self.importButton.isEnabled()
        # self.importButton.setEnabled(not enabled)
        # if enabled:
        import_window = bm.MainWindow(self.parent.main_window, brand_dir = './Brands/')
        import_window.on_exit = self.brand_exit_call_back_method
        import_window.show()
        

    def brand_exit_call_back_method(self):
        '''
        This method is triggered when there needs to be update in gui because of change in main_config.yaml file
        cases may be when importing yaml file, when updating parameters in the yaml

        Use this function as a place holder for you method, so that your method gets invoked when the brand management exits
        
        Usage
        ----------------
        brand_exit_call_back_method = your_methods
        
        '''
        # TODO: load new main_config.yaml 
        print('logic to update the project in the gui')
        ...

    def set_camera_values_to_entry(self, exposure: float | int, gain : float | int, frame_rate: float | int, delay: float | int ):
        self.exposureEntry_Debug.setText(str(exposure)) 
        self.gainEntry_Debug.setText(str(gain)) 
        self.frameRateEntry_Debug.setText(str(frame_rate)) 
        self.delayEntry_Debug.setText(str(delay))
        ...
    
    def get_camera_values_to_entry(self) -> list[float, float, float, float]:
        '''
        returns the values in the entry gui in camera parameters

        Returns
        ---------------------------------
        exposure : float
        gain: float
        frame_rate: float
        delay: float

        ---------------------------------
        Returns these vaule in a list in the following order.
        '''
        try:
            exposure = float(self.exposureEntry_Debug.text().strip(' ')) 
            gain = float(self.gainEntry_Debug.text().strip(' ')) 
            frame_rate = float(self.frameRateEntry_Debug.text().strip(' ')) 
            delay = float(self.delayEntry_Debug.text().strip(' '))
            return exposure, gain, frame_rate, delay
        except Exception as e:
            print('[-] failed to get camera parameter, ', e)
            print(traceback.format_exc()) 
    
    ########### Getting system parameters and save it
    def update_augment_param(self,file_path)->None:
        '''
        Saves the updated system parameter
        '''
        try:
            augment_param  = {
                'ntimes':self.nTimesEntry.text()
                ,'rotate':self.rotateEntry.text()
                ,'flip':self.flipEntry.text()
                ,'blur':self.blurEntry.text()
                ,'contrast':self.contrastEntry.text()
                ,'elastic':self.elasticEntry.text()
                ,'rigid':self.rigidEntry.text()
                ,'recursion_rate':self.recursionRateEntry.text()
            }
            save_parameter(file_path,'augment',augment_param)
            msgBox = QMessageBox()
            msgBox.setText("Augmentation Parameter Update Successfully")
            msgBox.setWindowTitle("Information")
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msgBox.exec()
        except Exception as e:
            print("Failed to get the system parameter")
            print(traceback.format_exc())
    def captured_image_count(self, image_count:int = 0):
        self.totalImage_Count.setText(str(image_count))