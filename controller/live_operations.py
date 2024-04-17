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

    def __init__(self, parent: PyQTWidgetFunction):
        '''
        Initialize the variable associated with the live mode 

        Parameter
        -----------------------
        parent: PyQTWidgetFunction
            pass the object `PyQTWidgetFunction` that inherits the class `Ui_MainWindow` generated from `ui`
        '''
        ########### system parameters variables
        self.detection_recognition = parent.detection_recognition
        self.detectionOnly = parent.detectionOnly
        self.no_ofLine_comboBox = parent.no_ofLine_comboBox
        self.line1Box = parent.line1Box
        self.line2Box = parent.line2Box
        self.line3Box = parent.line3Box
        self.line4Box = parent.line4Box
        self.systemSetting_update_Button = parent.systemSetting_update_Button

        ########### rejection parameters variables
        self.minPercent_Entry = parent.minPercent_Entry
        self.lineThresh_Entry = parent.linearThresh_Entry
        self.rejectCount_Entry = parent.rejectCount_Entry
        self.rejectEnable_Yes = parent.rejectEnable_Yes
        self.rejectEnable_No = parent.rejectEnable_No
        self.rejectSetting_updateButton = parent.rejectSetting_updateButton 

         ########### camera parameters variables
        self.stackWidget_cameraSetting = parent.stackWidget_cameraSetting
        self.cameraSetting_Page = parent.cameraSetting_Page
        self.cameraSetting_Button = parent.cameraSetting_Button
        self.cameraSetting_update_Button = parent.cameraSetting_update_Button
        self.cameraGain_Entry = parent.cameraGain_Entry
        self.exposureTime_Entry = parent.exposureTime_Entry
        self.triggerDelay_Entry = parent.triggerDelay_Entry
        self.roiEntry1 = parent.roiEntry1
        self.roiEntry2 = parent.roiEntry2
        self.roiEntry3 = parent.roiEntry3
        self.roiEntry4 = parent.roiEntry4

         ########### save data parameters variables
        self.saveImage_Checkbox = parent.saveImage_Checkbox
        self.saveResult_Checkbox = parent.saveResult_Checkbox
        self.saveNG_Checkbox = parent.saveNG_Checkbox
        self.directoryName_Entry = parent.directoryName_Entry
        self.saveData_Page = parent.saveData_Page
        self.saveData_Button = parent.saveData_Button
        self.directoryName_Entry = parent.directoryName_Entry


        ############ last ng image 
        self.lastNG_Image = parent.lastNG_Image 

        ##### detection result 
        self.detectionResult = parent.detectionResult 
        self.detectionTime = parent.detectionTime 

        ####### good, not good, last not good counts 
        self.goodCount = parent.goodCount
        self.notGoodCount = parent.notGoodCount
        self.lastNG_Count = parent.lastNG_Count 
        self.lastNG_timeCount = parent.lastNG_timeCount 
        self.resetCounter_Button = parent.resetCounter_Button

    ###### Loading system widgets parameter
    def system_param_load(self)->None :
        '''
        Load the system parameter values from pickle
        '''
        with open(os.path.join(os.getcwd(),'Parameter_Value/system.pkl'),'rb') as f:
            system_param = pickle.load(f)   
        if system_param['ocr_method'] == True:  ######## Set the ocr method radiobutton 
            self.detection_recognition.setChecked(True)
        else:
            self.detectionOnly.setChecked(True)
        
        self.no_ofLine_comboBox.setCurrentText(str(system_param['nooflines']))
        self.line1Box.setText(system_param['line1'])
        self.line2Box.setText(system_param['line2'])
        self.line3Box.setText(system_param['line3'])
        self.line4Box.setText(system_param['line4'])

    ########## Loading rejection widgets parameters
    def reject_param_load(self)->None:
        '''
        Load the rejection parameter values from pickle
        '''
        with open(os.path.join(os.getcwd(),'Parameter_Value/rejection.pkl'),'rb') as f:
            reject_param = pickle.load(f)
        self.minPercent_Entry.setText(str(reject_param['min_per_thresh']))
        self.lineThresh_Entry.setText(str(reject_param['line_per_thresh']))
        self.rejectCount_Entry.setText(str(reject_param['reject_count']))
        if reject_param['reject_enable'] == True:
            self.rejectEnable_Yes.setChecked(True)
        else:
            self.rejectEnable_No.setChecked(True)

    ###### Loading camera widgets parameters
    def camera_param_load(self)->None:
        '''
        Load the camera parameter value from pickle
        '''
        with open(os.path.join(os.getcwd(),'Parameter_Value/camera.pkl'),'rb') as f:
            camera_param = pickle.load(f)
            first_point,second_point = camera_param['ROI'].split(',')
            first,second = first_point.split(':')
            third,forth = second_point.split(':')
        self.cameraGain_Entry.setText(str(camera_param['camera_gain']))
        self.exposureTime_Entry.setText(str(camera_param['exposure_time']))
        self.triggerDelay_Entry.setText(str(camera_param['trigger_delay']))
        self.roiEntry1.setText(str(first))
        self.roiEntry2.setText(str(second))
        self.roiEntry3.setText(str(third))
        self.roiEntry4.setText(str(forth))

    ###### Loading save param widgets parameter
    def save_param_load(self)->None:
        '''
        Load the save data parameter value from pickle
        '''
        with open(os.path.join(os.getcwd(),'Parameter_Value/save_data.pkl'),'rb') as f:
            save_data_param = pickle.load(f)
           
        ################ For Save Image ##################
        if save_data_param['save_img'] == True:
            self.saveImage_Checkbox.setChecked(True)
        else:
            self.saveImage_Checkbox.setChecked(False)

        ################ For Save Result #################
        if save_data_param['save_result'] == True:
            self.saveResult_Checkbox.setChecked(True)
        else:
            self.saveResult_Checkbox.setChecked(False)
        
        ################# For Save NG Image #############
        if save_data_param['save_ng'] == True:
            self.saveNG_Checkbox.setChecked(True)
        else:
            self.saveNG_Checkbox.setChecked(False)

        self.directoryName_Entry.setText(save_data_param['img_dir'])
        
    ########### Getting system parameters and save it
        
        system  = {
            'ocr_method':True if self.detection_recognition.isChecked() else False
            ,'no_of_lines':self.no_ofLine_comboBox.currentText()
            ,'line1':self.line1Box.text()
            ,'line2':self.line2Box.text()
            ,'line3':self.line3Box.text()
            ,'line4':self.line4Box.text()
        }
        


    def camera_setting(self)->None:
        '''
        Method that change the camera setting page in StackedWidget
        '''
        self.stackWidget_cameraSetting.setCurrentWidget(self.cameraSetting_Page)
        self.saveData_Button.setStyleSheet("QPushButton{\n"
        "    background-color: #eaeaea;\n"
        "    border:none;\n"
        "    border-top-left-radius:4px;\n"
        "    border-top-right-radius:4px;\n"
        "    border-bottom-right-radius:4px;\n"
        "\n"
        "\n"
        "}")
        self.cameraSetting_Button.setStyleSheet("QPushButton{\n"
        "    color:#D9305C;\n"
        "    border-top:1px solid#D9305C;\n"
        "    border-right:1px solid#D9305C;\n"
        "    border-top-left-radius:4px;\n"
        "    border-top-right-radius:4px;\n"
        "\n"
        "}\n"
        "\n"
        "\n"
        "\n"
        "")

    def save_data(self)->None:
        '''
        Method that change into save data page.
        '''
        self.stackWidget_cameraSetting.setCurrentWidget(self.saveData_Page)

        self.saveData_Button.setStyleSheet("QPushButton{\n"
        "    color:#D9305C;\n"
        "    border-top:1px solid#D9305C;\n"
        "    border-right:1px solid#D9305C;\n"
        "    border-top-left-radius:4px;\n"
        "    border-top-right-radius:4px;\n"
        "\n"
        "}\n"
        "\n"
        "\n"
        "\n"
        "")
        self.cameraSetting_Button.setStyleSheet(
            "QPushButton{\n"
        "    background-color: #eaeaea;\n"
        "    border:none;\n"
        "    border-top-left-radius:4px;\n"
        "    border-top-right-radius:4px;\n"
        "    border-bottom-right-radius:4px;\n"
        "\n"
        "\n"
        "}")

    def open_image(self, image = None)-> None:
        '''
        Method that opens the image to select the ROI to be used and display in the GUI
        '''
        file_path="current_img/1.jpg"
        started = 0
        if file_path:
            if type(image) == type(None):
                image = cv2.imread(file_path)
            r_image=cv2.resize(image,(int(0.75*image.shape[1]),int(0.75*image.shape[0])))
            ###### mouse click event########
            drawing = True
            ix,iy = -1,-1
            endy , endy = 0 ,0 
            def draw_rectangle(event, x, y, flags, param):
                try:
                    global ix,iy,drawing,roi, started, r_image,drawing
                    if event == cv2.EVENT_LBUTTONDOWN:
                        drawing = True
                        ix = x
                        iy = y
                        endx = x
                        endy = y
                    elif event == cv2.EVENT_MOUSEMOVE and drawing  == True:
                        endx = x
                        endy = y
                        r_image=cv2.resize(image,(int(0.75*image.shape[1]),int(0.75*image.shape[0])))
                        cv2.rectangle(r_image, (ix, iy),(endx, endy),(0, 255, 255),3)
                        cv2.imshow("ROI Selection", r_image)
                    elif event == cv2.EVENT_LBUTTONUP:
                        drawing = False
                        x1 = int(ix * image.shape[1] / r_image.shape[1])
                        y1 = int(iy * image.shape[0] / r_image.shape[0])
                        x2 = int((x) * image.shape[1] / r_image.shape[1])
                        y2 = int((y) * image.shape[0] / r_image.shape[0])
                        cv2.rectangle(r_image, (ix, iy),(x, y),(0, 255, 255),3)
                        cv2.imshow("ROI Selection", r_image)
                        cv2.waitKey(1500)
                        roi=str(int(y1))+':'+str(int(y2))+','+str(int(x1))+':'+str(int(x2))
                
                        cv2.destroyAllWindows()
                        started = 0
                except NameError as ne:
                    pass
            cv2.namedWindow("ROI Selection",cv2.WINDOW_AUTOSIZE)
            cv2.setMouseCallback("ROI Selection", draw_rectangle)
                # display the window
            while True:
                cv2.imshow("ROI Selection", r_image)
                cv2.waitKey(0) == ord('q')
                break
            cv2.destroyAllWindows()
            self.roiEntry.clear()  # clear any existing text in the entry box
            self.roiEntry.insert(roi)
            cv2.destroyAllWindows()
            

    def choose_directory_path(self):
        '''
        Method that sets the path to save the image.
        '''
        file_path = QFileDialog.getExistingDirectory(None,"Select Directory")
        file_path = QFileDialog.getExistingDirectory()
        if file_path:
            self.directoryName_Entry.insert(file_path)
        else:
            QMessageBox.warning(self,'Warning',"Please Select the Path")

        self.save_image_path = file_path

    def get_save_directory_path(self):
        """
        Method that returns the path to save the image
        """
        return self.save_image_path 
    

    def reset_counter_values(self):
        if int(self.goodCount.text()) == 0: 
            self.goodCount.setText('100')
        else:
            self.goodCount.setText('0')
    
    def update_camera_parameter(self, value):
        self.exposureTime_Entry.setText(str(value))