import os
import cv2
import cv2.data
from copy import deepcopy 
from gui.pyUIdesign import Ui_MainWindow
#from gui.PyUICBasicDemo import Ui_MainWindow 
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
from functools import partial

from .live_operations import LiveOperationFunction
from .debug_operations import DebugOperationFunction 

from PyQt5.QtCore import QObject, QEvent, QCoreApplication, QTimer, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QFrame
from Parameter_Value.debug_param_value import  camera_param
from Parameter_Value.param_tools import save_parameter, get_parameter
from algorithm.yolo import object_detection_yolo
class CircleFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.frameLayout = QtWidgets.QGridLayout(self)
        self.frameLayout.setContentsMargins(0, 0, 0, 0)
        self.frameLayout.setSpacing(12) 

    def addCircle(self):
            self.circle = QtWidgets.QPushButton()#f"{i}")
            # self.circle.setObjectName(f'circle{i}')
            self.circle.setMaximumHeight(120)
            self.circle.setMaximumWidth(180)
            # self.circle.setStyleSheet("background-color: white;" "color: red;" "border: 1px solid red;" "border-radius:10px;" "height:35px;" "width:35px;")
            self.frameLayout.addWidget(self.circle, len(self.frameLayout) // 5, len(self.frameLayout) % 5)
            return self.circle
    
class PyQTWidgetFunction(Ui_MainWindow):
    def __init__(self, main_window) -> None:
        super().__init__()
        self.detectionTime = None
        self.goodCount = None
        self.notGoodCount = None
        self.lastNG_Count = None
        self.last_ten_circle = CircleFrame()
        self.main_window = main_window
        self.setupUi(main_window)
        self.save_image_path = None 

        # Initialize live and debug operations
        self.live = LiveOperationFunction(self)
        self.debug = DebugOperationFunction(self)

        self.additional_setup() 

    ################################################################ Live Mode Functions ###############################################################
            ################################################################################################################################
                    ################################################################################################################
                            ###########################################################################################

    def additional_setup(self)->None:
        '''
        Functions to generate the last 10 circle for good or bad detection
        '''
         # circle
        self.circleWidget = CircleFrame(self.lastTenResult_Frame)
        self.circleWidget.setMaximumSize(QtCore.QSize(16777215, 64))
        self.circleWidget.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.circleWidget.setFrameShadow(QtWidgets.QFrame.Raised)
        self.circleWidget.setObjectName("circleWidget")
        self.verticalLayout_12.addWidget(self.circleWidget)
  
        self.circle_buttons = []
        for _ in range(10):
            self.circle_name = self.circleWidget.addCircle()
            self.circle_name.setObjectName(f'{_}')
            self.circle_name.clicked.connect(partial(self.live.display_last_ten, self.circle_name))
            self.circle_buttons.append(self.circle_name)

    def switch_mode(self)->None:
        '''
        This method switch the live or debug mode
        '''
      
        if self.switchButton.isChecked():
            self.stackWidget.setCurrentWidget(self.debugMode_Page)
            self.switchButton.setText('Debug')
        else:
            self.switchButton.setText('Live')
            self.stackWidget.setCurrentWidget(self.liveMode_Page)
    
    def get_current_mode(self)-> str:
        """
        returns the current mode of the gui: Live or Debug

        Returns
        --------------
        mode: str
            returns string either Debug or Live

        """
        return self.switchButton.text()

    def camera_on_status(self):

        self.onButton.setStyleSheet("#onButton{\n"
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
        self.offButton.setStyleSheet("#offButton{\n"
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
        self.onButton.setStyleSheet(" ")     
        self.offButton.setStyleSheet(" ")
    

    def update_live_gui_with_based_on_result(self, image: cv2 = None, rejection : dict = None):
        '''
            Update live gui after trigger or image is received
        Args:
            image: image received from camera
            rejection: status while rejection
        '''
        ng_image_checkbox = True if self.saveNG_Checkbox.isChecked() else False
        img_checkbox = True if self.saveImage_Checkbox.isChecked() else False
        detect_info = rejection
        reject_status = detect_info['reject_status']
        orig_img = detect_info['orig_img']
        
        ###### Display detection time #######
        self.detectionTime.setText(str(round((detect_info['detect_time']),2)))
 
        if reject_status == True:
            status = 'not_good'
            self.live.live_mode_param['not_good'] += 1
            self.live.live_mode_param['last_not_good_count'] = 0
            self.live.display_last_NG(image)
            self.notGoodCount.setText(str(self.live.live_mode_param['not_good']))
            self.live.red_blinking()
            if ng_image_checkbox == True:  ##### save not good image
                self.live.save_ng_image(orig_img)
            
        else:
            status = 'good'
            self.live.live_mode_param['good'] += 1
            self.live.live_mode_param['last_not_good_count'] += 1
            self.goodCount.setText(str(self.live.live_mode_param['good']))
            self.lastNG_Count.setText(str(self.live.live_mode_param['last_not_good_count']))
            self.live.blue_blinking()
            if img_checkbox == True: #### save image
                self.live.save_image(orig_img)

        current_image_info = {'image': deepcopy(image), 'status': status}
        self.live.live_mode_param['last_ten_result'] = [current_image_info] +  self.live.live_mode_param['last_ten_result']
        if len(self.live.live_mode_param['last_ten_result']) > 10: # removing the previous results if there are more than ten circles
            self.live.live_mode_param['last_ten_result'].pop(-1)
        
        for idx in range(len(self.live.live_mode_param['last_ten_result'])): ##### Displaying the color of last ten circles green if status is good else red
            style_green = '''#circleWidget QPushButton{
                background : green;
                border : 1px solid green;
                border-radius:10px;
                height : 35px;
                width : 35px;
                }
            '''
            style_red = '''#circleWidget QPushButton{
                background : red;
                border : 1px solid green;
                border-radius:10px;
                height : 35px;
                width : 35px;
                }
            '''
            if self.live.live_mode_param['last_ten_result'][idx]['status'] == "good":
                pass
                self.circle_buttons[idx].setStyleSheet(style_green)
            else:
                self.circle_buttons[idx].setStyleSheet(style_red)


          
 
        



