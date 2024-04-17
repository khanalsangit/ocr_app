from gui.pyUIdesign import Ui_MainWindow
from gui.PyUICBasicDemo import Ui_MainWindow 
from camera_interface.camera import MachineVisionCamera
from .gui_operations import PyQTWidgetFunction
from .live_operations import LiveOperationFunction
from .debug_operations import DebugOperationFunction

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
        self.gui = gui
        self.live = live
        self.debug = debug
        self.connect_camera_and_ui()
        self.connect_methods_and_ui()
        self.live.system_param_load()
        self.live.reject_param_load()
        self.live.camera_param_load()
        self.live.save_param_load()
        self.debug.load_augment_param()
        
    def connect_camera_and_ui(self):
        ######################## camera function called ##############################
        self.gui.findCamera_Button.clicked.connect(lambda : self.camera.enum_devices(self.gui.comboBox))
        self.gui.onButton.clicked.connect(
            lambda : [
                self.camera.open_device(self.gui.comboBox), 
                self.camera.start_grabbing(self.gui.imageWidget_Debug if self.gui.get_current_mode() != "Live" else self.gui.imageWidget_Live) if self.camera.isOpen else None,
            ] 
        )
        self.gui.offButton.clicked.connect(self.camera.close_device)
        

    def connect_methods_and_ui(self):
        ####################### Live Mode function called ############################
        self.gui.stackWidget.setCurrentWidget(self.gui.liveMode_Page) ####### default switch mode 
        self.gui.editProject.setCurrentWidget(self.gui.createProject_Page) ####### default live mode page
        self.gui.switch_mode_flag = False  ##### switch mode flag
        self.gui.switchButton.clicked.connect(
            lambda : [
                self.camera.close_device(),
                self.camera.open_device(self.gui.comboBox) if self.camera.isOpen else None, 
                self.camera.start_grabbing(self.gui.imageWidget_Debug if self.gui.get_current_mode() == "Live" else self.gui.imageWidget_Live) if self.camera.isOpen else None, 
                self.gui.switch_mode(),
            ]
        )
        self.gui.stackWidget_cameraSetting.setCurrentWidget(self.gui.cameraSetting_Page) ######### default camera setting mode
        self.live.cameraSetting_Button.pressed.connect(self.live.camera_setting)
        self.live.openImage_Button.pressed.connect(
            lambda : self.live.open_image()
        )
        self.live.saveData_Button.pressed.connect(self.live.save_data)
        self.live.chooseDirectory_Button.pressed.connect(self.live.choose_directory_path)
        self.live.systemSetting_update_Button.pressed.connect(self.live.update_system_param)
        self.live.rejectSetting_updateButton.pressed.connect(self.live.update_reject_param)
        self.live.cameraSetting_update_Button.pressed.connect(self.live.update_camera_param)
        self.live.systemSetting_update_Button.pressed.connect(self.live.update_save_data_param)
        ####################### Debug Mode function called ######################
        self.gui.createProjectButton.clicked.connect(self.debug.create_project)
        self.gui.cameraButton.clicked.connect(self.debug.camera_debug)
        self.gui.preprocessingButton.clicked.connect(self.debug.preprocessing_step)
        self.gui.detectionButton.clicked.connect(self.debug.detection)
        self.gui.recognitionButton.clicked.connect(self.debug.recognition)
        self.gui.analysisButton.clicked.connect(self.debug.analysis)

     


        # self.gui.live.resetCounter_Button.clicked.connect(
        #     self.gui.live.reset_counter_values
        # )