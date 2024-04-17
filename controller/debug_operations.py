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
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .gui_operations import PyQTWidgetFunction

import brand_management as bm

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

    def load_augment_param(self)->None:
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
        bm.createWindow(self.parent.main_window).show()
    
    def import_brand(self):
        bm.MainWindow(self.parent.main_window, brand_dir = './Brands/').show()
        ...
