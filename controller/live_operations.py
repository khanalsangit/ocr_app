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

class LiveOperationFunction(Ui_MainWindow):
    def __init__(self, parent: PyQTWidgetFunction = None):
        '''
        Initialize the variable associated with the live mode 

        Parameter
        -----------------------
        parent: PyQTWidgetFunction
            pass the object `PyQTWidgetFunction` that inherits the class `Ui_MainWindow` generated from `ui`
        '''
        # system setting 
        self.detectionOnly = parent.detectionOnly 
        self.detection_recognition = parent.detection_recognition
        self.no_ofLine_comboBox = parent.no_ofLine_comboBox
        self.line1Box = parent.line1Box
        self.line2Box = parent.line2Box 
        self.line3Box = parent.line3Box 
        self.line4Box = parent.line4Box
        self.systemSetting_update_Button = parent.systemSetting_update_Button
        
        # Rejection Setting 
        self.minPercent_Entry = parent.minPercent_Entry
        self.linearThresh_Entry = parent.linearThresh_Entry 
        self.rejectCount_Entry = parent.rejectCount_Entry
        self.rejectEnable_Yes = parent.rejectEnable_Yes 
        self.rejectEnable_No = parent.rejectEnable_No
        self.rejectSetting_updateButton = parent.rejectSetting_updateButton 

        # camera setting
        self.exposureTime_Entry = parent.exposureTime_Entry 
        self.triggerDelay_Entry = parent.triggerDelay_Entry 
        self.cameraGain_Entry = parent.cameraGain_Entry 
        # TODO: set x1, x2, y1, y2 position of the ROI
        self.cameraSetting_update_Button = parent.cameraSetting_update_Button
        
        # save data
        # TODO: button for the directory
        self.directoryName_Entry = parent.directoryName_Entry

        # detection result 
        self.detectionResult = parent.detectionResult 
        self.detectionTime = parent.detectionTime 

        # good, not good, last not good counts 
        self.goodCount = parent.goodCount
        self.notGoodCount = parent.notGoodCount
        self.lastNG_Count = parent.lastNG_Count 
        self.lastNG_timeCount = parent.lastNG_timeCount 
        self.resetCounter_Button = parent.resetCounter_Button

        # last ng image 
        self.lastNG_Image = parent.lastNG_Image 

    def reset_counter_values(self):
        if int(self.goodCount.text()) == 0: 
            self.goodCount.setText('100')
        else:
            self.goodCount.setText('0')
    
    def update_camera_parameter(self, value):
        self.exposureTime_Entry.setText(str(value))