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

class CircleFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.frameLayout = QtWidgets.QGridLayout(self)
        self.frameLayout.setContentsMargins(0, 0, 0, 0)
        self.frameLayout.setSpacing(12) 
        # for _ in range(10):
        #    self.addCircle()
        # self.custom_signal = pyqtSignal(str)

    def addCircle(self):

        # self.buttons_name = []
        # self.buttons = []
        # for i in range(10):
            self.circle = QtWidgets.QPushButton()#f"{i}")
            # self.circle.setObjectName(f'circle{i}')
            self.circle.setMaximumHeight(120)
            self.circle.setMaximumWidth(180)
            self.circle.setStyleSheet("background-color: white;" "color: red;" "border: 1px solid red;" "border-radius:10px;" "height:35px;" "width:35px;")
            self.frameLayout.addWidget(self.circle, len(self.frameLayout) // 5, len(self.frameLayout) % 5)
            # self.circle.clicked.connect(partial(self.do_something, self.circle))
            # self.circle.clicked.connect(self.do_something)
            # self.buttons_name.append(f'circle{i}')
            # self.buttons.append(self.circle)
            return self.circle
        
    def do_something(self):
        # self.custom_signal.emit('hello world!')
        sender = self.sender()
        index = self.buttons.index(sender)
        print(index)



class PyQTWidgetFunction(Ui_MainWindow):
    def __init__(self, main_window) -> None:
        super().__init__()
        self.last_ten_circle = CircleFrame()
        self.main_window = main_window
        self.setupUi(main_window)
        self.additional_setup() 
        self.save_image_path = None 
        self.live = LiveOperationFunction(self)
        self.debug = DebugOperationFunction(self)

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
            self.circle_buttons.append(self.circle_name)
            self.circle_name.setObjectName(f'{_}')
            self.circle_name.clicked.connect(partial(self.display_index, self.circle_name))
    def display_index(self, circle_name):
        print(str(circle_name.objectName()))

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
        '''
            Update live gui after trigger or image is received
        Args:
            image: image received from camera
            rejection: status while rejection
        '''
        # print("Length of ciecle",self.circle_buttons)
        # print("Circle buttons",self.circle_buttons[0])
        if rejection == True:
            status = 'not_good'
            self.live.live_mode_param['not_good'] += 1
            self.live.live_mode_param['last_not_good_count'] = 0
            self.live.display_last_NG(image)
            self.notGoodCount.setText(str(self.live.live_mode_param['not_good']))
            self.live.last_ng_time(0,'0')
            self.live.red_blinking()


                
        else:
            status = 'good'
            self.live.live_mode_param['good'] += 1
            self.live.live_mode_param['last_not_good_count'] += 1
            self.goodCount.setText(str(self.live.live_mode_param['good']))
            self.lastNG_Count.setText(str(self.live.live_mode_param['last_not_good_count']))
            self.live.blue_blinking()
        
        current_image_info = {'image': deepcopy(image), 'status': status}
        self.live.live_mode_param['last_ten_result'] = [current_image_info] +  self.live.live_mode_param['last_ten_result']
        if len(self.live.live_mode_param['last_ten_result']) >= 10: # removing the previous results if there are more than ten circles
            self.live.live_mode_param['last_ten_result'].pop(-1)
        name = 'circle0'
      
        # for i, point in enumerate(self.live.live_mode_param['last_ten_result']):
        #     if self.live.live_mode_param['last_ten_result'][i]['status'] == "good":
        #         self.circle_name.setStyleSheet("background: green;" "border: 1px solid green;" "border-radius:10px;" "height:35px;" "width:35px;")
        #     else:
        #         self.circle_name.setStyleSheet("background: red;" "border: 1px solid green;" "border-radius:10px;" "height:35px;" "width:35px;")

        for idx in range(len(self.circle_buttons)): ##### Displaying the color of last ten circles green if status is good else red
            if self.live.live_mode_param['last_ten_result'][i]['status'] == "good":
                self.circle_buttons[idx].setStyleSheet("background: green;" "border: 1px solid green;" "border-radius:10px;" "height:35px;" "width:35px;")
            else:
                self.circle_buttons[idx].setStyleSheet("background: red;" "border: 1px solid green;" "border-radius:10px;" "height:35px;" "width:35px;")


 
        

