
from __future__ import annotations
import pickle
import glob
import cv2
import os
import traceback
from gui.pyUIdesign import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import *
from Parameter_Value.param_tools import save_parameter, get_parameter
from typing import TYPE_CHECKING
import time
from copy import deepcopy
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
        self.chooseDirectory_Button = parent.chooseDirectory_Button
       
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
        self.circleWidget = parent.circleWidget

    ########## Live Mode Result Parameter ########
    live_mode_param = {
        'detection_time':0,
        'last_ten_result':[],
        'good':0,
        'not_good':0,
        'last_not_good_count':0,
        'last_not_good_time':0
    }
        
    def silence_line(self)->None:
        '''
        Silence the lines based on the number of line
        '''
        combo_box = int(self.no_ofLine_comboBox.currentText())

        if combo_box == 0:
            self.line1Box.setDisabled(True)
            self.line2Box.setDisabled(True)
            self.line3Box.setDisabled(True)
            self.line4Box.setDisabled(True)
        elif combo_box == 1:
            self.line1Box.setDisabled(False)
            self.line2Box.setDisabled(True)
            self.line3Box.setDisabled(True)
            self.line4Box.setDisabled(True)
        elif combo_box == 2:
            self.line1Box.setDisabled(False)
            self.line2Box.setDisabled(False)
            self.line3Box.setDisabled(True)
            self.line4Box.setDisabled(True)
        
        elif combo_box == 3:
            self.line1Box.setDisabled(False)
            self.line2Box.setDisabled(False)
            self.line3Box.setDisabled(False)
            self.line4Box.setDisabled(True)
        elif combo_box == 4:
            self.line1Box.setDisabled(False)
            self.line2Box.setDisabled(False)
            self.line3Box.setDisabled(False)
            self.line4Box.setDisabled(False)

    def msgbox_display(self,msg,type)-> None:
        '''
        Displays the messagebox 
        Parameters:
        msg: Message to be display
        type: Type of Message like Information and warning
        '''
        msgBox = QMessageBox()
        msgBox.setText("{}".format(msg))
        msgBox.setWindowTitle("{}".format(type))
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msgBox.exec()
        

    def system_param_load(self, ocr_method:str, no_of_line:int, line1box:str, line2box:str, line3box:str, line4box:str)->None :
        '''
        Set the current system parameter values into gui widgets.
        '''
        if ocr_method == True:  ######## Set the ocr method radiobutton 
            self.detection_recognition.setChecked(True)
        else:
            self.detectionOnly.setChecked(True)
        
        self.no_ofLine_comboBox.setCurrentText(str(no_of_line))
        self.line1Box.setText(line1box) # system_param['line1'])
        self.line2Box.setText(line2box)
        self.line3Box.setText(line3box)
        self.line4Box.setText(line4box)

    ########## Loading rejection widgets parameters
    def reject_param_load(self,min_per_thresh:str,line_per_thresh:str, reject_count:str, reject_enable:bool)->None:
        '''
        Set the current rejection parameter values into gui widgets
        '''
        self.minPercent_Entry.setText(str(min_per_thresh))
        self.lineThresh_Entry.setText(str(line_per_thresh))
        self.rejectCount_Entry.setText(str(reject_count))
        if reject_enable == True:
            self.rejectEnable_Yes.setChecked(True)
        else:
            self.rejectEnable_No.setChecked(True)

    ###### Loading camera widgets parameters
    def camera_param_load(self,exposure_time, cam_gain:str, trigger_delay:int, roi:str)->None:
        '''
        Set the current live camera parameter values into gui widgets
        '''
        first_point,second_point = roi.split(',')
        first,second = first_point.split(':')
        third,forth = second_point.split(':')
        self.cameraGain_Entry.setText(str(cam_gain))
        self.exposureTime_Entry.setText(str(exposure_time))
        self.triggerDelay_Entry.setText(str(trigger_delay))
        self.roiEntry1.setText(str(first))
        self.roiEntry2.setText(str(second))
        self.roiEntry3.setText(str(third))
        self.roiEntry4.setText(str(forth))

    ###### Loading save data param widgets parameter
    def save_data_param_load(self,save_img:bool, save_result:bool, save_ng:bool, img_dir: os.path)->None:
        '''
        Set the current save data parameter in gui widgets
        '''
        ################ For Save Image ##################
        if save_img == True:
            self.saveImage_Checkbox.setChecked(True)
        else:
            self.saveImage_Checkbox.setChecked(False)

        ################ For Save Result #################
        if save_result == True:
            self.saveResult_Checkbox.setChecked(True)
        else:
            self.saveResult_Checkbox.setChecked(False)
        
        ################# For Save NG Image #############
        if save_ng == True:
            self.saveNG_Checkbox.setChecked(True)
        else:
            self.saveNG_Checkbox.setChecked(False)

        self.directoryName_Entry.setText(img_dir)
        
    ########### Getting system parameters and save it
    def update_system_param(self,file_path)->None:
        '''
        Saves the updated system parameter
        '''
        try:
            system  = {
                'ocr_method':True if self.detection_recognition.isChecked() else False
                ,'nooflines':self.no_ofLine_comboBox.currentText()
                ,'line1':self.line1Box.text()
                ,'line2':self.line2Box.text()
                ,'line3':self.line3Box.text()
                ,'line4':self.line4Box.text()
            }
            save_parameter(file_path,'system',system)
            self.silence_line()
            self.msgbox_display("System Parameter Save Successfully",'Success')
        except Exception as e:
            print("Failed to get the system parameter")
            print(traceback.format_exc())
        
    def update_reject_param(self,file_path)->None:
        '''
        Saves the updated rejection parameter
        '''
        try:
            reject = {
                'min_per_thresh':self.minPercent_Entry.text()
                ,'line_per_thresh':self.lineThresh_Entry.text()
                ,'reject_count':self.rejectCount_Entry.text()
                ,'reject_enable':True if self.rejectEnable_Yes.isChecked() else False 
            }
            save_parameter(file_path,'rejection',reject)
            self.msgbox_display("Rejection Parameter Save Successfully","Success")
        except Exception as e:
            print("Failed to get the rejection parameter",e)
            print(traceback.format_exc())

    def update_camera_param(self,file_path)->None:
        '''
        Saves the updated camera parameter
        '''
        try:
            roi1 = self.roiEntry1.text()
            roi2 = self.roiEntry2.text()
            roi3 = self.roiEntry3.text()
            roi4 = self.roiEntry4.text()
            camera = {
            'exposure_time':self.exposureTime_Entry.text()
            ,'trigger_delay':self.triggerDelay_Entry.text()
            ,'camera_gain':self.cameraGain_Entry.text()
            ,'ROI':'{}:{},{}:{}'.format(roi1,roi2,roi3,roi4)
            }
           
            save_parameter(file_path,'camera_live', camera)
            self.msgbox_display("Camera Parameter Update Successfully","Information")
        except Exception as e:
            print("Failed to get the camera parameter",e)
            print(traceback.format_exc())

    def update_save_data_param(self,file_path)->None:
        '''
        Saves the save data parameter
        '''
        try:
            save_data = {
            'save_img':True if self.saveImage_Checkbox.isChecked() else False
            ,'save_ng':True if self.saveNG_Checkbox.isChecked() else False
            ,'save_result':True if self.saveResult_Checkbox.isChecked() else False
            ,'img_dir':self.directoryName_Entry.text()
            }
            save_parameter(file_path,'save_data',save_data)
            self.msgbox_display("Save Data Update Successfully","Information")
        except Exception as e:
            print("Failed to get the save data parameter")
            print(traceback.format_exc())
     

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
            self.roiEntry1.clear()  # clear any existing text in the entry box
            self.roiEntry2.clear()
            self.roiEntry3.clear()
            self.roiEntry4.clear()
            first_point,second_point = roi.split(',')
            first,second = first_point.split(':')
            third,forth = second_point.split(':')
            self.roiEntry1.insert(first)
            self.roiEntry2.insert(second)
            self.roiEntry3.insert(third)
            self.roiEntry4.insert(forth)
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

    def display_last_ten(self)->None:
        """ Display last ten images
        Args:
            image : input image from camera
            event (event): display image event
        """ 
        # senders = self.sender()  # Get the button that was clicked
        # index = buttons.index(senders)  # Get the index of the clicked button
        print("Button clicked")

    def display_last_NG(self,image)->None:
        '''
        Display last Not Good Image
        '''
        if not (image is  None):
            new_h = self.lastNG_Image.height() 
            new_w = self.lastNG_Image.width()
            image = cv2.resize(image, (new_w, new_h))
            image = QImage(image.data, new_w, new_h, QImage.Format.Format_BGR888)
            self.lastNG_Image.setPixmap(QtGui.QPixmap.fromImage(image))

    def last_ng_time(self,start_time,last_time)->None:
        '''
            Display Last Not Good time
        Args:

        '''
        start_time = time.time()
        if last_time==0:
            current_time = 0
        else:
            current_time = int(time.time() - start_time) 
        self.lastNG_timeCount.setText(str(current_time) + ' sec')

    def red_blinking(self) -> None:
        '''
        Display or Blink the red color rectangle when the detection result if Not Good.
        '''
        self.detectionResult.setText("Not Good")
        self.detectionResult.setStyleSheet("QLabel{\n"
        "    color:white;\n"
        "    background-color:#D9305C;\n"
        "    border-radius:2px;\n"
        "    font: 16pt Arial;"
        "}")
        self.detectionResult.setAlignment(QtCore.Qt.AlignCenter)
    
    def blue_blinking(self) -> None:
        '''
        Display or Blink the blue color rectangle when the detection result is Good.
        '''
        self.detectionResult.setText("Good")
        self.detectionResult.setStyleSheet("QLabel{\n"
        "    color:white;\n"
        "    background-color:#349beb;\n"
        "    border-radius:2px;\n"
        "    font: 16pt Arial;"
        "}")
        self.detectionResult.setAlignment(QtCore.Qt.AlignCenter)

    


        


            
       