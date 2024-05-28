import os 
import yaml 
import datetime
import traceback

import cv2
from PyQt5.QtWidgets import QFileDialog
# from Augmentation.main import Augmentation_ProgressBar
from camera_interface.camera import MachineVisionCamera
from .gui_operations import PyQTWidgetFunction
from .live_operations import LiveOperationFunction
from .debug_operations import DebugOperationFunction
from Parameter_Value.debug_param_value import  camera_param, augmentation_param
from Parameter_Value.live_param_value import system_param, rejection_params, save_data_param
from Parameter_Value.param_tools import save_parameter, get_parameter
from PyQt5 import QtWidgets

class Controller():
    """
    Controller class that inherits the Ui_MainWindow from the autogenerated pyqt ui file
    
    Parameters
    ------------------
    camera: MachineVisionCamera
        instance of the MachineVisionCamera    
    gui: PyQTWidgetFunction
        instace of the current main window
    """
    def __init__(self, camera: MachineVisionCamera, live:LiveOperationFunction, debug:DebugOperationFunction, gui: PyQTWidgetFunction) -> None:
        """
        Initialize the controller, 
            - It connects the camera to ui components 
            - It connects methods to ui components 
        """
        self.camera = camera
        # self.augment = augment
        self.gui = gui
        self.current_brand_config = self.load_main_configs()
        self.live = live
        self.debug = debug

        self.connect_camera_and_ui()
        self.connect_methods_and_ui()

        # debug parameter
        self.load_saved_camera_parameter()
        self.load_current_augmentation_param()
        self.update_current_project()
        self.debug.brand_exit_call_back_method = lambda : [self.load_main_configs(), self.update_current_project()]

        #### Load the current brand pickle values
        self.load_current_system_param()
        self.load_current_rejection_param()
        self.load_live_camera_param()
        self.load_save_data_param()
        self.live.silence_line()
                
    def connect_camera_and_ui(self):
        ######################## camera function called ##############################
        self.gui.findCamera_Button.clicked.connect(lambda : self.camera.enum_devices(self.gui.comboBox))
        self.gui.onButton.clicked.connect(
            lambda : [
                self.camera.open_device(self.gui.comboBox), 
                self.camera.start_grabbing(self.gui.imageWidget_Debug if self.gui.get_current_mode() != "Live" else self.gui.imageWidget_Live) if self.camera.isOpen else None,
                self.gui.camera_on_status(),
            ] 
        )
        self.gui.offButton.clicked.connect(
            lambda:[
                self.camera.close_device(),
                self.gui.camera_off_status()
            ]
        )
       
        
    def connect_methods_and_ui(self):
        
        ####################### Live Mode function called ############################
        self.gui.stackWidget.setCurrentWidget(self.gui.liveMode_Page) ####### default switch mode 
        self.gui.editProject.setCurrentWidget(self.gui.createProject_Page) ####### default live mode page
        self.gui.switchButton.clicked.connect(
            lambda : [
                self.camera.close_device(),
                self.camera.open_device(self.gui.comboBox) if self.camera.isOpen else None, 
                self.camera.start_grabbing(self.gui.imageWidget_Debug if self.gui.get_current_mode() == "Live" else self.gui.imageWidget_Live) if self.camera.isOpen else None, 
                self.gui.switch_mode(),
            ]
        )
        self.gui.stackWidget_cameraSetting.camera_setting_page = True
        self.gui.stackWidget_cameraSetting.setCurrentWidget(self.gui.cameraSetting_Page) ######### default camera setting mode

        self.live.cameraSetting_update_Button.pressed.connect(
            lambda : [
                self.set_camera_live_parameter() if self.gui.stackWidget_cameraSetting.camera_setting_page else self.set_save_data_parameter()
            ]
        )


        self.live.cameraSetting_Button.pressed.connect(self.camera_setting)
        self.gui.openImage_Button.pressed.connect(
            lambda : self.live.open_image()
        )
        self.live.saveData_Button.pressed.connect(self.save_data)
        self.live.chooseDirectory_Button.pressed.connect(self.live.choose_directory_path)
        self.live.systemSetting_update_Button.pressed.connect(self.set_system_parameter)
        self.live.rejectSetting_updateButton.pressed.connect(self.set_reject_parameter)
        self.live.resetCounter_Button.pressed.connect(self.live.reset_counter_values)
        
 
        

  
        ####################### Debug Mode function called ######################

        # side panel buttons
        self.debug.createProjectButton.clicked.connect(self.debug.create_project)
        self.debug.cameraButton.clicked.connect(
            lambda : [
                self.debug.camera_debug(),          # switch to the gui
                self.update_captured_image_count()  # update the count in the image
            ]
        )
        self.debug.preprocessingButton.clicked.connect(self.debug.preprocessing_step)
        self.debug.detectionButton.clicked.connect(self.debug.detection)
        self.debug.recognitionButton.clicked.connect(self.debug.recognition)
        self.debug.analysisButton.clicked.connect(self.debug.analysis)

        # brand creation panel buttons connection
        self.debug.createButton.clicked.connect(self.debug.create_brand)
        self.debug.importButton.clicked.connect(self.debug.import_brand)

        # camera debug panel buttons connection
        self.debug.getParameter_Button.clicked.connect(self.get_mvs_camera_parameter)
        self.debug.setParameter_Button.clicked.connect(self.set_camera_parameter)
        self.debug.deleteImage_Button.clicked.connect(self.delete_captured_image)
        self.debug.captureButton.clicked.connect(self.capture_image)
        # augmentation panel buttons creation
        self.gui.augmentationButton.clicked.connect(self.set_augment_parameter)
        # self.gui.augmentationButton.clicked.connect(self.set_augment_parameter)


    

    def camera_setting(self)->None:
        '''
        Method that change the camera setting page in StackedWidget
        '''
        # self.live.cameraSetting_update_Button.pressed.connect(self.set_camera_live_parameter)
        self.gui.stackWidget_cameraSetting.camera_setting_page = True

        self.live.stackWidget_cameraSetting.setCurrentWidget(self.live.cameraSetting_Page)
        self.live.saveData_Button.setStyleSheet("")
        self.live.cameraSetting_Button.setStyleSheet("")

    def save_data(self)->None:
        '''
        Method that change into save data page.
        '''
        # self.live.cameraSetting_update_Button.pressed.connect(self.set_save_data_parameter)
        self.gui.stackWidget_cameraSetting.camera_setting_page = False
        self.live.stackWidget_cameraSetting.setCurrentWidget(self.live.saveData_Page)


        self.live.saveData_Button.setStyleSheet("#saveData_Button{\n"
                                                           "color:#D9305C;\n"
                                                            "background-color: white;\n"
                                                            "border-top:1px solid#D9305C;\n"
                                                            "border-right:1px solid#D9305C;\n"
                                                            "border-top-left-radius:4px;\n"
                                                            "border-top-right-radius:4px;\n"
                                                            "}")
        self.live.cameraSetting_Button.setStyleSheet("#cameraSetting_Button{\n"
                                                            "background-color: #eaeaea;\n"                                                              
                                                            "color:black;\n"                                                                
                                                            "border:none;\n"                                                                
                                                            "border-top-left-radius:4px;\n"                                                             
                                                            "border-top-right-radius:4px;\n"                                                                
                                                            "border-bottom-right-radius:4px;\n"                                                             
                                                            "}")


    def load_main_configs(self)->None:
        try:
            with open('./main_config.yaml', 'r') as file_stream:
                self.current_brand_config = yaml.safe_load(file_stream)
                return self.current_brand_config
            

        except Exception as e :
            print('error loading in main_config.yaml', e)
            print(traceback.format_exc())

    def update_current_project(self)->None:
        '''
        Sets the active project name in gui 
        '''
        try:
            config_file = self.load_main_configs()
            brand_name = config_file['brand_name']
            self.gui.projectName.setText(brand_name)

            ### Load all the pickle values for current active project
            self.load_current_system_param()
            self.load_current_rejection_param()
            self.load_live_camera_param()
            self.load_save_data_param()

        except Exception as e:
            print("Config file load failed")


    ### debug 

    def load_saved_camera_parameter(self)->None:
        '''
        loading saved parameters in current brand pickel values for camera
        '''
        try:
            temp_camera_param = get_parameter(self.current_brand_config['pickle_path'], 'camera_param', camera_param )

            exposure, gain, frame_rate = list(map(lambda a : temp_camera_param[a] , ['exposure', 'gain', 'frame_rate']))
            delay = 0  # TODO: decide what to do with delays 
            self.debug.set_camera_values_to_entry(exposure=exposure, gain=gain, frame_rate=frame_rate, delay=delay)
        except Exception as e:
            print('[-] Failed loading saved parameter ', e)
            print(traceback.format_exc())

    def load_current_augmentation_param(self):
        '''
        Loading the parameter of current augmentation parameter
        '''
        try:
            temp_augment_data_param = get_parameter(self.current_brand_config['pickle_path'], 'augment', augmentation_param)
            ntimes, rotate, flip, blur, contrast, elastic, rigid, recursion_rate = list(map(lambda a: temp_augment_data_param[a], ['ntimes','rotate','flip','blur','contrast','elastic','rigid','recursion_rate']))
            self.debug.load_augment_param(ntimes, rotate, flip, blur, contrast, elastic, rigid, recursion_rate)
        except Exception as e:
            print("[+] Augmentation Parameter load failed", e)
            print(traceback.format_exc())
    
    ### live
    def load_current_system_param(self):
        '''
        Loading the parameter of current system parameter
        '''
        try:
            temp_system_param = get_parameter(self.current_brand_config['pickle_path'], 'system', system_param )
            ocr_method, no_of_line, line1, line2, line3, line4 = list(map(lambda a : temp_system_param[a], ['ocr_method', 'nooflines', 'line1','line2','line3','line4']))
            self.live.system_param_load(ocr_method, no_of_line, line1, line2, line3, line4)
        except Exception as e:
            print('[-] Failed loading saved parameter ', e)
            print(traceback.format_exc())
    
    def load_current_rejection_param(self):
        '''
        Loading parameter of current rejection parameter
        '''
        try:
            temp_reject_param = get_parameter(self.current_brand_config['pickle_path'],'rejection',rejection_params)
            min_per_thresh, line_per_thresh, reject_count, reject_enable = list(map(lambda a: temp_reject_param[a], ['min_per_thresh', 'line_per_thresh', 'reject_count', 'reject_enable']))
            self.live.reject_param_load(min_per_thresh, line_per_thresh, reject_count, reject_enable)
        except Exception as e:
            print('-[] Failed loading saved parameter', e)
            print(traceback.format_exc())

    def load_live_camera_param(self):
        '''
        Loading parameter of current live camera parameter
        '''
        try:
            temp_live_camera_param = get_parameter(self.current_brand_config['pickle_path'],'camera_live', camera_param)
            exposure_time, camera_gain, trigger_delay,roi = list(map(lambda a: temp_live_camera_param[a],['exposure_time','camera_gain','trigger_delay','ROI']))
            self.live.camera_param_load(exposure_time, camera_gain, trigger_delay, roi)
        except Exception as e:
            print("Camera Parameter loading failed", e)
            print(traceback.format_exc())

    def load_save_data_param(self):
        '''
        Loading paramter of current save data parameter
        '''
        try:
            temp_save_data_param = get_parameter(self.current_brand_config['pickle_path'],'save_data',save_data_param)
            save_img, save_ng, save_result, img_dir = list(map(lambda a: temp_save_data_param[a],['save_img','save_ng','save_result','img_dir']))
            self.live.save_data_param_load(save_img, save_ng, save_result, img_dir)
        except Exception as e:
            print("[+] Save Data Parameter Load Failed", e)
            print(traceback.format_exc())
        
    def get_mvs_camera_parameter(self):
        '''
        Method to load camera parameters
        '''
        try:
            exposure, gain, frame_rate = self.camera.get_param()
            delay = 0  # TODO: decide what to do with delays 
            self.debug.set_camera_values_to_entry(exposure=exposure, gain=gain, frame_rate=frame_rate, delay=delay)
        except Exception as e:
            print('[-] Failed to get the mvs parameter')
            print(traceback.format_exc())
    def set_augment_parameter(self)->None:
        '''
        Update or saves the augmentation parameter in pickle
        '''
        try:
            file_path = self.current_brand_config['pickle_path']
            self.debug.update_augment_param(file_path)
            self.augment.augmentation()
        except Exception as e:
            print("Update augmentation parameters failed",e)
            print(traceback.format_exc())
    def set_system_parameter(self)->None:
        '''
        Update or saves the system parameter in pickle
        '''
        
        try:

            file_path = self.current_brand_config['pickle_path']
            self.live.update_system_param(file_path)
        except Exception as e:
            print('update system setting parameters failed ', e)
            print(traceback.format_exc())


    def set_reject_parameter(self)->None:
        '''
        Update or saves the rejection parameter in pickle
        '''
        try:
            file_path = self.current_brand_config['pickle_path']
            self.live.update_reject_param(file_path)
        except Exception as e:
            print('update reject setting parameters failed ', e)
            print(traceback.format_exc())

    def set_camera_parameter(self)->None:
        '''
        method to set the camera parameter
        '''
        try:
            exposure, gain, frame_rate, delay = self.debug.get_camera_values_to_entry()
            self.camera.set_param(exposure, gain, frame_rate)

            # save the parameter to pickel
            camera_param['exposure'] = exposure
            camera_param['gain'] = gain 
            camera_param['frame_rate'] = frame_rate

            save_parameter(self.current_brand_config['pickle_path'], 'camera_param', camera_param )
            self.live.msgbox_display("Camera Parameter Update Successfully")
        except Exception as e:
            print('error setting camera parameters ', e)
            print(traceback.format_exc())
        
    def set_camera_live_parameter(self)->None:
        '''
        Update the camera data parameter
        '''
        try:
            file_path = self.current_brand_config['pickle_path']
            self.live.update_camera_param(file_path)
           
        except Exception as e:
            print('update reject setting parameters failed ', e)
            print(traceback.format_exc())

    def set_save_data_parameter(self)->None:
        '''
        Update the save data parameter
        '''
        try:
            file_path = self.current_brand_config['pickle_path']
            self.live.update_save_data_param(file_path)
        except Exception as e:
            print('update reject setting parameters failed ', e)
            print(traceback.format_exc())

    
    def delete_captured_image(self):
        "method to delete the capture image" 
        fileName, filter = QFileDialog.getOpenFileName(None, 'Open file', 
            self.current_brand_config['images_path'], 'Image files (*.jpg)')
        if fileName:
            print('file Name')
        self.update_captured_image_count()
        ...

    def capture_image(self):
        '''
        method to capture the image
        '''

        try:
            self.camera.set_software_trigger_mode()
            self.camera.trigger_once()
            image = self.camera.get_current_image()
        except Exception as e: 
            print('[-] error capture', e)
            print(traceback.format_exc())
        
        try:
            # ret = self.camera.obj_cam_operation.Save_jpg( 
            #     os.path.join(self.current_brand_config['images_path'] , 
            #     datetime.datetime.now().strftime("%y-%m-%d-%I-%M-%S-%f %p.jpg"))
            # )

            cv2.imwrite(
                os.path.join(self.current_brand_config['images_path'] , 
                    datetime.datetime.now().strftime("%y-%m-%d-%I-%M-%S-%f %p.jpg")), 
                cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            )
        except Exception as e :
            print('exception ', e )
            print(traceback.format_exc())
        self.update_captured_image_count()

    def update_captured_image_count(self):
        '''
        method to update the image count in the gui by reading from the brand folder 
        '''

        image_count = len(os.listdir(self.current_brand_config['images_path']))
        self.debug.captured_image_count(image_count)
        ...
        
