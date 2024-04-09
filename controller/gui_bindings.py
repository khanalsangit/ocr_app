from gui.pyUIdesign import Ui_MainWindow
from gui.PyUICBasicDemo import Ui_MainWindow 
from camera_interface.camera import MachineVisionCamera
from controller.gui_operations import PyQTWidgetFunction

class Controller():
    def __init__(self, camera: MachineVisionCamera, gui_operate: PyQTWidgetFunction) -> None:
        # super().__init__()
        # self.setupUi(main_window)
        self.camera = camera
        self.gui_operate = gui_operate


    def set_gui_func_to_gui(self):
         ######################## camera function called ##############################
        self.gui_operate.findCamera_Button.clicked.connect(self.camera.enum_devices)
        self.gui_operate.onButton.clicked.connect(self.camera.open_device)
        self.gui_operate.offButton.clicked.connect(self.camera.close_device)

        ####################### Live Mode function called ############################
        self.gui_operate.stackWidget.setCurrentWidget(self.gui_operate.liveMode_Page) ####### default switch mode 
        self.gui_operate.editProject.setCurrentWidget(self.gui_operate.createProject_Page) ####### default live mode page
        self.gui_operate.switchButton.clicked.connect(self.gui_operate.switch_mode)
        self.gui_operate.stackWidget_cameraSetting.setCurrentWidget(self.gui_operate.cameraSetting_Page) ######### default camera setting mode
        self.gui_operate.cameraSetting_Button.pressed.connect(self.gui_operate.camera_setting)
        self.gui_operate.openImage_Button.pressed.connect(self.gui_operate.open_image)
        self.gui_operate.saveData_Button.pressed.connect(self.gui_operate.save_data)
        self.gui_operate.click_Button.pressed.connect(self.gui_operate.choose_directory_path)
        self.gui_operate.systemSetting_update_Button.pressed.connect(self.gui_operate.save_gui_values)
        self.gui_operate.rejectSetting_updateButton.pressed.connect(self.gui_operate.save_gui_values)
        self.gui_operate.cameraSetting_update_Button.pressed.connect(self.gui_operate.save_gui_values)
    
        ####################### Debug Mode function called ######################
        self.gui_operate.createProjectButton.clicked.connect(self.gui_operate.create_project)
        self.gui_operate.cameraButton.clicked.connect(self.gui_operate.camera_debug)
        self.gui_operate.preprocessingButton.clicked.connect(self.gui_operate.preprocessing_step)
        self.gui_operate.detectionButton.clicked.connect(self.gui_operate.detection)
        self.gui_operate.recognitionButton.clicked.connect(self.gui_operate.recognition)
        self.gui_operate.analysisButton.clicked.connect(self.gui_operate.analysis)


