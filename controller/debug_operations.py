from __future__ import annotations
import pickle
import glob
import cv2
import os
import shutil

from gui.pyUIdesign import Ui_MainWindow
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *

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

        self.create_project_button_bindings()
    

    def create_project(self):
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
        

    def create_project_button_bindings(self):
        self.createButton.clicked.connect(self.create_brand)
        self.importButton.clicked.connect(self.import_brand)

    def camera_debug(self):
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
    
    def preprocessing_step(self):
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
    
    def detection(self):
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
    
    def recognition(self):
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
    
    def analysis(self):
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

