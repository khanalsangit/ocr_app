# from gui.pyUIdesign import Ui_MainWindow
from gui.PyUICBasicDemo import Ui_MainWindow 
from camera_interface.camera import MachineVisionCamera

def test():
    """
    your document here
    : param kind: optional
    : type kind: list 
    : raise 
    : return: The value of test
    : rtype: list[str]
    """
    ...

class Controller(Ui_MainWindow):
    
    def __init__(self, main_window, camera: MachineVisionCamera) -> None:
        super().__init__()
        self.setupUi(main_window)
        self.camera = camera

    def set_camera_to_gui(self):
        self.camera.set_ui(self)

        self.bnEnum.clicked.connect(self.camera.enum_devices)
        self.bnOpen.clicked.connect(self.camera.open_device)
        self.bnClose.clicked.connect(self.camera.close_device)
        self.bnStart.clicked.connect(self.camera.start_grabbing)
        self.bnStop.clicked.connect(self.camera.stop_grabbing)

        self.bnSoftwareTrigger.clicked.connect(self.camera.trigger_once)
        self.radioTriggerMode.clicked.connect(self.camera.set_software_trigger_mode)
        self.radioContinueMode.clicked.connect(self.camera.set_continue_mode)

        self.bnGetParam.clicked.connect(self.camera.get_param)
        self.bnSetParam.clicked.connect(self.camera.set_param)

        self.bnSaveImage.clicked.connect(self.camera.save_bmp)
        #'''
        
    def basic_demo_test(self):

        self.camera.set_ui(self)
        
        self.bnEnum.clicked.connect(self.camera.enum_devices)
        self.bnOpen.clicked.connect(self.camera.open_device)
        self.bnClose.clicked.connect(self.camera.close_device)
        self.bnStart.clicked.connect(self.camera.start_grabbing)
        self.bnStop.clicked.connect(self.camera.stop_grabbing)

        self.bnSoftwareTrigger.clicked.connect(self.camera.trigger_once)
        self.radioTriggerMode.clicked.connect(self.camera.set_software_trigger_mode)
        self.radioContinueMode.clicked.connect(self.camera.set_continue_mode)

        self.bnGetParam.clicked.connect(self.camera.get_param)
        self.bnSetParam.clicked.connect(self.camera.set_param)

        self.bnSaveImage.clicked.connect(self.camera.save_bmp)
        #'''