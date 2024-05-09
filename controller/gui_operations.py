import os
import cv2
import sys
import glob
import shutil
import pickle
import cv2.data
import yaml
import traceback

from gui.pyUIdesign import Ui_MainWindow
#from gui.PyUICBasicDemo import Ui_MainWindow 
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *

from .live_operations import LiveOperationFunction
from .debug_operations import DebugOperationFunction 

class PyQTWidgetFunction(Ui_MainWindow):
    def __init__(self, main_window) -> None:
        super().__init__()

        self.main_window = main_window
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
        print("Switch Mode Here")
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


    def camera_on_status(self):
        self.onButton.setStyleSheet("QPushButton{\n"
            "    background-color: #EF1B79;\n"
            "    color:white;\n"
            "    border:none;\n"
            "}\n"
            "QPushButton:pressed{\n"
            "    border-top:2px solid black;\n"
            "    border-left: 2px solid black;\n"
            "}\n"
            ""
        )     
        self.offButton.setStyleSheet("QPushButton{\n"
            "    background: white;\n"
            "    color:black;\n"
            "    border:none;\n"
            "}\n"
            "QPushButton:pressed{\n"
            "    border-left:2px solid black;\n"
            "    border-top:2px solid black;\n"
            "}\n"
            "    \n"
            ""
        )

    def camera_off_status(self):
        self.onButton.setStyleSheet("QPushButton{\n"
            "    background-color: white;\n"
            "    color:black;\n"
            "    border:none;\n"
            "}\n"
            "QPushButton:pressed{\n"
            "    border-top:2px solid black;\n"
            "    border-left: 2px solid black;\n"
            "}\n"
            ""
        )     
        self.offButton.setStyleSheet("QPushButton{\n"
            "    background: #EF1B79;\n"
            "    color:white;\n"
            "    border:none;\n"
            "}\n"
            "QPushButton:pressed{\n"
            "    border-left:2px solid black;\n"
            "    border-top:2px solid black;\n"
            "}\n"
            "    \n"
            ""
        )
    
    def update_live_gui_with_based_on_result(self, image: cv2 = None, rejection=None):
        from PyQt5.QtGui import QPixmap, QImage
        import numpy as np 
        import time
        if not (image is  None):
            new_h = self.lastNG_Image.height() 
            new_w = self.lastNG_Image.width()
            image = cv2.resize(image, (new_w, new_h))
            image = QImage(image.data, new_w, new_h, QImage.Format.Format_BGR888)
            self.lastNG_Image.setPixmap(QtGui.QPixmap.fromImage(image))
          


      


 
        

