from PyQt5 import QtWidgets, QtCore, QtGui
from pyUIdesign import Ui_MainWindow
import os
from PyQt5.QtWidgets import *
import cv2
from main_gui import *
import pickle
import glob
import sys
import shutil

class MainWin(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWin,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.ui.stackWidget.setCurrentWidget(self.ui.liveMode_Page) ####### default switch mode 
        self.switch_mode_flag = False  ##### switch mode flag
        self.ui.switchButton.clicked.connect(self.switch_mode)
        self.ui.stackWidget_cameraSetting.setCurrentWidget(self.ui.cameraSetting_Page) ######### default camera setting mode
        self.ui.cameraSetting_Button.pressed.connect(self.camera_setting)
        self.ui.openImage_Button.pressed.connect(self.open_image)
        self.ui.saveData_Button.pressed.connect(self.save_data)
        self.ui.click_Button.pressed.connect(self.choose_directory_path)
        self.ui.systemSetting_update_Button.pressed.connect(self.save_gui_values)
        self.ui.rejectSetting_updateButton.pressed.connect(self.save_gui_values)
        self.ui.cameraSetting_update_Button.pressed.connect(self.save_gui_values)
        self.show()

        ##################################################### LIVE METHOD ####################################################
            ##############################################################################################################
                ######################################################################################################
                    ##########################################################################################
        
        ############### Loading existing pickle values for all the parameters of GUI ###############################
        pkl_file = glob.glob('Pickle/*')  
        if len(pkl_file)==0:
            with open('system_pickles/initial_param.pkl','rb') as f:
                brand_values = pickle.load(f) 
        else:
            for p in pkl_file:
                with open(p,"rb") as file:
                    brand_values = pickle.load(file)

        print("Minimum Percent",self.ui.minPercent_Entry.text())
        ###### Setting the initial values in GUI Parameters
        if brand_values['ocr_method_enable'] == True:  ######## Set the ocr method radiobutton 
            self.ui.detection_recognition.setChecked(True)
        else:
            self.ui.detectionOnly.setChecked(True)
        
        self.ui.no_ofLine_comboBox.setCurrentText(str(brand_values['no_of_lines']))
        self.ui.line1Box.insert(brand_values['line1'])
        self.ui.line2Box.insert(brand_values['line2'])
        self.ui.line3Box.insert(brand_values['line3'])
        self.ui.line4Box.insert(brand_values['line4'])
        self.ui.minPercent_Entry.insert(str(brand_values['min_per_thresh']))
        self.ui.linearThresh_Entry.insert(str(brand_values['line_per_thresh']))
        self.ui.rejectCount_Entry.insert(str(brand_values['reject_count']))
        self.ui.cameraGain_Entry.insert(str(brand_values['camera_gain']))
        self.ui.exposureTime_Entry.insert(str(brand_values['exposure_time']))
        self.ui.triggerDelay_Entry.insert(str(brand_values['trigger_delay']))
        self.ui.roiEntry.insert(str(brand_values['roi']))
        
        ################ For Rejection Enable #############
        if brand_values['reject_enable'] == True:
            self.ui.rejectEnable_Yes.setChecked(True)
        else:
            self.ui.rejectEnable_No.setChecked(True)
 
        ################ For Save Image ##################
        if brand_values['save_img'] == True:
            self.ui.saveImage_Checkbox.setChecked(True)
        else:
            self.ui.saveImage_Checkbox.setChecked(False)

        ################ For Save Result #################
        if brand_values['save_result'] == True:
            self.ui.saveResult_Checkbox.setChecked(True)
        else:
            self.ui.saveResult_Checkbox.setChecked(False)
        
        ################# For Save NG Image #############
        if brand_values['save_ng'] == True:
            self.ui.saveNG_Checkbox.setChecked(True)
        else:
            self.ui.saveNG_Checkbox.setChecked(False)


    def switch_mode(self):
        '''
        Function that checks the switch mode and change its when button is clicked.
        '''
            
        if self.ui.switchButton.isChecked():
            self.ui.stackWidget.setCurrentWidget(self.ui.debugMode_Page)
            self.ui.switchButton.setText('Debug')
        else:
            self.ui.switchButton.setText('Live')
            self.ui.stackWidget.setCurrentWidget(self.ui.liveMode_Page)

    ######################### Function to save all the parameters ########################
        ###########################################################################
            ##################################################################
       
    def save_gui_values(self)-> None:
        '''
        Function that takes all the user inputs values from GUI and saved in pickle file
        '''
        global param_values
        global save_image_sel_val
        global save_ocr_sel_val
        global rej_enable_status
        global line1_enable_status
        global line2_enable_status
        global save_img_status
        global save_ng_status 
        global save_det_status
        global save_result_status
        global crop_save
        global brand_values

        pkl_dir = glob.glob('Pickle/*.pkl')
        for pkl in pkl_dir:
            print("Pickle",pkl)
            
        with open(pkl, 'rb') as brand:
            brand_values = pickle.load(brand)
        brand_param_dict = {'brand_name':self.ui.projectName.text()
                    ,'ocr_method_enable': True if self.ui.detection_recognition.isChecked() else False
                    ,'no_of_lines':self.ui.no_ofLine_comboBox.currentText()
                    ,'line1':self.ui.line1Box.text()
                    ,'line2':self.ui.line2Box.text()
                    ,'line3':self.ui.line3Box.text()
                    ,'line4':self.ui.line4Box.text()
                    ,'min_per_thresh':self.ui.minPercent_Entry.text()
                    ,'line_per_thresh':self.ui.linearThresh_Entry.text()
                    ,'reject_count':self.ui.rejectCount_Entry.text()
                    ,'reject_enable':True if self.ui.rejectEnable_Yes.isChecked() else False 
                    ,'exposure_time':self.ui.exposureTime_Entry.text()
                    ,'trigger_delay':self.ui.triggerDelay_Entry.text()
                    ,'camera_gain':self.ui.cameraGain_Entry.text()
                    ,'roi':self.ui.roiEntry.text()
                    ,'save_img':True if self.ui.saveImage_Checkbox.isChecked() else False
                    ,'save_ng':True if self.ui.saveNG_Checkbox.isChecked() else False
                    ,'save_result':True if self.ui.saveResult_Checkbox.isChecked() else False
                    ,'img_dir':self.ui.directoryName_Entry.text()
                }

        
        with open(pkl,'wb') as new_brand:
            pickle.dump(brand_param_dict, new_brand) #writing pickle files for brand parameters
        srcs = pkl
        pik_lst = pkl.split('.')
        pik_str = str(pik_lst[0])
        pik_str = pik_str.split('\\')
        dests = os.getcwd() + '/Pickle/' + pik_str[1]
        shutil.copy(srcs, dests)
        QMessageBox.information(self,'Success',"Parameter Saved Successfully")



    def camera_setting(self):
        '''
        Function that change the camera setting page.
        '''
        self.ui.stackWidget_cameraSetting.setCurrentWidget(self.ui.cameraSetting_Page)
        self.ui.saveData_Button.setStyleSheet("QPushButton{\n"
"    background-color: #eaeaea;\n"
"    border:none;\n"
"    border-top-left-radius:4px;\n"
"    border-top-right-radius:4px;\n"
"    border-bottom-right-radius:4px;\n"
"\n"
"\n"
"}")
        self.ui.cameraSetting_Button.setStyleSheet("QPushButton{\n"
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
   
    def open_image(self)-> None:
        '''
        Function that opens the image to select the ROI to be used and display in the GUI
        '''
        file_path="current_img/1.jpg"
        started = 0
        if file_path:
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
            self.ui.roiEntry.clear()  # clear any existing text in the entry box
            self.ui.roiEntry.insert(roi)
            cv2.destroyAllWindows()

    def save_data(self):
        '''
        Function that change into save data page.
        '''
        self.ui.stackWidget_cameraSetting.setCurrentWidget(self.ui.saveData_Page)

        self.ui.saveData_Button.setStyleSheet("QPushButton{\n"
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
        self.ui.cameraSetting_Button.setStyleSheet(
        "QPushButton{\n"
    "    background-color: #eaeaea;\n"
    "    border:none;\n"
    "    border-top-left-radius:4px;\n"
    "    border-top-right-radius:4px;\n"
    "    border-bottom-right-radius:4px;\n"
    "\n"
    "\n"
    "}")
    

    def choose_directory_path(self):
        '''
        Function that sets the path to save the image.
        '''
        file_path = QFileDialog.getExistingDirectory(self,"Select Directory")
        if file_path:
            self.ui.directoryName_Entry.insert(file_path)
        else:
            QMessageBox.warning(self,'Warning',"Please Select the Path")

    

if __name__=="__main__":
    import sys
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    app = QtWidgets.QApplication(sys.argv)
    obj = MainWin()
    sys.exit(app.exec_())




