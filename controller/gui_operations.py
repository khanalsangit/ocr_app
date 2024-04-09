import pickle
import glob
import cv2
import os
import shutil
from gui.pyUIdesign import Ui_MainWindow
#from gui.PyUICBasicDemo import Ui_MainWindow 
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *

class PyQTWidgetFunction(Ui_MainWindow):
    def __init__(self, main_window) -> None:
        super().__init__()
        self.setupUi(main_window)

    ################################################################ Live Mode Functions ###############################################################
            ################################################################################################################################
                    ################################################################################################################
                            ###########################################################################################
    def switch_mode(self):
        '''
        This function switch the live or debug mode
        '''
        if self.switchButton.isChecked():
            self.stackWidget.setCurrentWidget(self.debugMode_Page)
            self.switchButton.setText('Debug')
        else:
            self.switchButton.setText('Live')
            self.stackWidget.setCurrentWidget(self.liveMode_Page)

    def camera_setting(self):
        '''
        Function that change the camera setting page in StackedWidget
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

    def save_data(self):
        '''
        Function that change into save data page.
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
            self.roiEntry.clear()  # clear any existing text in the entry box
            self.roiEntry.insert(roi)
            cv2.destroyAllWindows()

    def choose_directory_path(self):
        '''
        Function that sets the path to save the image.
        '''
        file_path = QFileDialog.getExistingDirectory(self,"Select Directory")
        if file_path:
            self.directoryName_Entry.insert(file_path)
        else:
            QMessageBox.warning(self,'Warning',"Please Select the Path")

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
        brand_param_dict = {'brand_name':self.projectName.text()
                    ,'ocr_method_enable': True if self.detection_recognition.isChecked() else False
                    ,'no_of_lines':self.no_ofLine_comboBox.currentText()
                    ,'line1':self.line1Box.text()
                    ,'line2':self.line2Box.text()
                    ,'line3':self.line3Box.text()
                    ,'line4':self.line4Box.text()
                    ,'min_per_thresh':self.minPercent_Entry.text()
                    ,'line_per_thresh':self.linearThresh_Entry.text()
                    ,'reject_count':self.rejectCount_Entry.text()
                    ,'reject_enable':True if self.rejectEnable_Yes.isChecked() else False 
                    ,'exposure_time':self.exposureTime_Entry.text()
                    ,'trigger_delay':self.triggerDelay_Entry.text()
                    ,'camera_gain':self.cameraGain_Entry.text()
                    ,'roi':self.roiEntry.text()
                    ,'save_img':True if self.saveImage_Checkbox.isChecked() else False
                    ,'save_ng':True if self.saveNG_Checkbox.isChecked() else False
                    ,'save_result':True if self.saveResult_Checkbox.isChecked() else False
                    ,'img_dir':self.directoryName_Entry.text()
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

        ##################################################### DEBUG METHOD ####################################################
            ##############################################################################################################
                ######################################################################################################
                    ##########################################################################################
    
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

