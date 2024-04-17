from __future__ import annotations
import pickle
import glob
import cv2
import os
import shutil

from gui.pyUIdesign import Ui_MainWindow
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *
from Parameter_Value import *
from PyQt5.QtCore import pyqtSlot


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

        # bindings of the buttons 
        self.create_project_button_bindings()

        ##### augmentation widget variables
        self.nTimesEntry = parent.nTimesEntry
        self.rotateEntry = parent.rotateEntry
        self.blurEntry = parent.blurEntry
        self.contrastEntry = parent.contrastEntry
        self.recursionRateEntry = parent.recursionRateEntry
        self.flipEntry = parent.flipEntry
        self.rigidEntry = parent.rigidEntry
        self.elasticEntry = parent.elasticEntry

    def load_augment_param(self)-> None:
        '''
        Load the augmentation parameters from pickle values
        '''
        with open(os.path.join(os.getcwd(),'Parameter_Value/augment.pkl'),'rb') as f:
            augmentation = pickle.load(f)
        self.nTimesEntry.setText(str(augmentation['ntimes']))
        self.rotateEntry.setText(str(augmentation['rotate']))
        self.blurEntry.setText(str(augmentation['blur']))
        self.contrastEntry.setText(str(augmentation['contrast']))
        self.recursionRateEntry.setText(str(augmentation['recursion_rate']))
        self.flipEntry.setText(str(augmentation['flip']))
        self.rigidEntry.setText(str(augmentation['rigid']))
        self.elasticEntry.setText(str(augmentation['elastic']))
    
         
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


    def create_project_button_bindings(self)->None:
        '''
        Opens the create and import button sections
        '''
        self.createButton.clicked.connect(self.create_brand)
        self.importButton.clicked.connect(self.import_brand)

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
        enabled = self.createButton.isEnabled()
        self.createButton.setEnabled(not enabled)
        if enabled:
            bm.createWindow(self.parent.main_window, brand_dir = './Brands/').show()
    
    def import_brand(self):
        enabled = self.importButton.isEnabled()
        self.importButton.setEnabled(not enabled)
        if enabled:
            import_window = bm.MainWindow(self.parent.main_window, brand_dir = './Brands/')
            import_window.on_exit = self.load_project_from_yaml
            import_window.show()
            print('end')
        
    
    def load_project_from_yaml(self):
        '''
        This method is triggered when there needs to be update in gui because of change in main_config.yaml file
        cases may be when importing yaml file, when updating parameters in the yaml 
        '''
        print('logic to update the project in the gui')
        ...

    def set_camera_values_to_entry(self):
        self.exposureEntry_Debug.setText() 
        self.gainEntry_Debug.setText() 
        self.frameRateEntry_Debug.setText() 
        self.delayEntry_Debug.setText()
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
            
            Returns these vaule in a list in the following order.
        '''
        exposure = float(self.exposureEntry_Debug.text().strip(' ')) 
        gain = float(self.gainEntry_Debug.text().strip(' ')) 
        frame_rate = float(self.frameRateEntry_Debug.text().strip(' ')) 
        delay = float(self.delayEntry_Debug.text().strip(' '))
        return exposure, gain, frame_rate, delay 