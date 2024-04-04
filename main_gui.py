from PyQt5 import QtWidgets, QtCore, QtGui
from pyUIdesign import Ui_MainWindow
import os
from PyQt5.QtWidgets import *
import cv2
import pickle
import glob
import sys
import shutil
######### camera libraries #######
from CamOperation_class import CameraOperation
sys.path.append("./MvImport")

from MvImport.MvCameraControl_class import *
from MvImport.MvErrorDefine_const import *
from MvImport.CameraParams_header import *
import ctypes
from gui_operations import PyQTWidgetFunction
class MainWin(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # self.ui = Ui_MainWindow()
        # self.ui.setupUi(self)
        # self.widget_func = PyQTWidgetFunction(self.ui)
        self.ui = PyQTWidgetFunction(self)
        
        ######################## camera function called ##############################
        self.ui.findCamera_Button.clicked.connect(self.enum_devices)
        self.ui.onButton.clicked.connect(self.open_device)
        self.ui.offButton.clicked.connect(self.close_device)

        self.ui.stackWidget.setCurrentWidget(self.ui.liveMode_Page) ####### default switch mode 
        self.ui.editProject.setCurrentWidget(self.ui.createProject_Page) ####### default live mode page
        self.switch_mode_flag = False  ##### switch mode flag
        self.ui.switchButton.clicked.connect(self.ui.switch_mode)
        self.ui.stackWidget_cameraSetting.setCurrentWidget(self.ui.cameraSetting_Page) ######### default camera setting mode
        self.ui.cameraSetting_Button.pressed.connect(self.ui.camera_setting)
        self.ui.openImage_Button.pressed.connect(self.ui.open_image)
        self.ui.saveData_Button.pressed.connect(self.ui.save_data)
        self.ui.click_Button.pressed.connect(self.ui.choose_directory_path)
        self.ui.systemSetting_update_Button.pressed.connect(self.ui.save_gui_values)
        self.ui.rejectSetting_updateButton.pressed.connect(self.ui.save_gui_values)
        self.ui.cameraSetting_update_Button.pressed.connect(self.ui.save_gui_values)
    
        ####################### debug ######################
        self.ui.createProjectButton.clicked.connect(self.ui.create_project)
        self.ui.cameraButton.clicked.connect(self.ui.camera_debug)
        self.ui.preprocessingButton.clicked.connect(self.ui.preprocessing_step)
        self.ui.detectionButton.clicked.connect(self.ui.detection)
        self.ui.recognitionButton.clicked.connect(self.ui.recognition)
        self.ui.analysisButton.clicked.connect(self.ui.analysis)

        self.show()

        
        ############### Loading existing pickle values for all the parameters of GUI ###############################
        pkl_file = glob.glob('Pickle/*')  
        if len(pkl_file)==0:
            with open('system_pickles/initial_param.pkl','rb') as f:
                brand_values = pickle.load(f) 
        else:
            for p in pkl_file:
                with open(p,"rb") as file:
                    brand_values = pickle.load(file)

        
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



        ##################################################### CAMERA FUNCTIONS ####################################################
            ##############################################################################################################
                ######################################################################################################
                    ##########################################################################################

        # 将返回的错误码转换为十六进制显示
    def ToHexStr(self,num):
        chaDic = {10: 'a', 11: 'b', 12: 'c', 13: 'd', 14: 'e', 15: 'f'}
        hexStr = ""
        if num < 0:
            num = num + 2 ** 32
        while num >= 16:
            digit = num % 16
            hexStr = chaDic.get(digit, str(digit)) + hexStr
            num //= 16
        hexStr = chaDic.get(num, str(num)) + hexStr
        return hexStr
    if __name__ == '__main__':
        ########### import functions of gui_operations.py
        global deviceList
        deviceList = MV_CC_DEVICE_INFO_LIST()
        global cam
        cam = MvCamera()
        global nSelCamIndex
        nSelCamIndex = 0
        global obj_cam_operation
        obj_cam_operation = 0
        global isOpen
        isOpen = False
        global isGrabbing
        isGrabbing = False
        global isCalibMode  # 是否是标定模式（获取原始图像）
        isCalibMode = True
        
       
        
        # widget_object.set_ui()
        # Decoding Characters
        def decoding_char(self,c_ubyte_value):
            c_char_p_value = ctypes.cast(c_ubyte_value, ctypes.c_char_p)
            try:
                decode_str = c_char_p_value.value.decode('gbk')  # Chinese characters
            except UnicodeDecodeError:
                decode_str = str(c_char_p_value.value)
            return decode_str
        
        # ch:枚举相机 | en:enum devices
        def enum_devices(self):
            global deviceList
            global obj_cam_operation

            deviceList = MV_CC_DEVICE_INFO_LIST()
            ret = MvCamera.MV_CC_EnumDevices(MV_GIGE_DEVICE | MV_USB_DEVICE, deviceList)
            if ret != 0:
                strError = "Enum devices fail! ret = :" + self.ToHexStr(ret)
                QMessageBox.warning(self, "Error", strError, QMessageBox.Ok)
                return ret

            if deviceList.nDeviceNum == 0:
                QMessageBox.warning(self, "Info", "Find no device", QMessageBox.Ok)
                return ret
            print("Find %d devices!" % deviceList.nDeviceNum)

            devList = []
            for i in range(0, deviceList.nDeviceNum):
                mvcc_dev_info = cast(deviceList.pDeviceInfo[i], POINTER(MV_CC_DEVICE_INFO)).contents
                if mvcc_dev_info.nTLayerType == MV_GIGE_DEVICE:
                    print("\ngige device: [%d]" % i)
                    user_defined_name = self.decoding_char(mvcc_dev_info.SpecialInfo.stGigEInfo.chUserDefinedName)
                    model_name = self.decoding_char(mvcc_dev_info.SpecialInfo.stGigEInfo.chModelName)
                    print("device user define name: " + user_defined_name)
                    print("device model name: " + model_name)

                    nip1 = ((mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0xff000000) >> 24)
                    nip2 = ((mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0x00ff0000) >> 16)
                    nip3 = ((mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0x0000ff00) >> 8)
                    nip4 = (mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0x000000ff)
                    print("current ip: %d.%d.%d.%d " % (nip1, nip2, nip3, nip4))
                    devList.append(
                        "[" + str(i) + "]GigE: " + user_defined_name + " " + model_name + "(" + str(nip1) + "." + str(
                            nip2) + "." + str(nip3) + "." + str(nip4) + ")")
                elif mvcc_dev_info.nTLayerType == MV_USB_DEVICE:
                    print("\nu3v device: [%d]" % i)
                    user_defined_name = self.decoding_char(mvcc_dev_info.SpecialInfo.stUsb3VInfo.chUserDefinedName)
                    model_name = self.decoding_char(mvcc_dev_info.SpecialInfo.stUsb3VInfo.chModelName)
                    print("device user define name: " + user_defined_name)
                    print("device model name: " + model_name)

                    strSerialNumber = ""
                    for per in mvcc_dev_info.SpecialInfo.stUsb3VInfo.chSerialNumber:
                        if per == 0:
                            break
                        strSerialNumber = strSerialNumber + chr(per)
                    print("user serial number: " + strSerialNumber)
                    devList.append("[" + str(i) + "]USB: " + user_defined_name + " " + model_name
                                + "(" + str(strSerialNumber) + ")")

            self.ui.comboBox.clear()
            self.ui.comboBox.addItems(devList)
            self.ui.comboBox.setCurrentIndex(0)
            self.open_device()
            self.start_grabbing()

        # ch:打开相机 | en:open device
        def open_device(self):
            global deviceList
            global nSelCamIndex
            global obj_cam_operation
            global isOpen
            if isOpen:
                QMessageBox.warning(self, "Error", 'Camera is Running!', QMessageBox.Ok)
                return MV_E_CALLORDER

            nSelCamIndex = self.ui.comboBox.currentIndex()
            if nSelCamIndex < 0:
                QMessageBox.warning(self, "Error", 'Please select a camera!', QMessageBox.Ok)
                return MV_E_CALLORDER

            obj_cam_operation = CameraOperation(cam, deviceList, nSelCamIndex)
            ret = obj_cam_operation.Open_device()
            print("RET", ret)
            if 0 != ret:
                strError = "Open device failed ret:" + self.ToHexStr(ret)
                QMessageBox.warning(self, "Error", strError, QMessageBox.Ok)
                isOpen = False
            else:
                strError = None
                ret = obj_cam_operation.Set_trigger_mode(False)

                isOpen = True

        # ch:开始取流 | en:Start grab image
        def start_grabbing(self):
            global obj_cam_operation
            global isGrabbing

            ret = obj_cam_operation.Start_grabbing(self.ui.imageWidget_Live.winId())
            if ret != 0:
                strError = "Start grabbing failed ret:" + self.ToHexStr(ret)
                QMessageBox.warning(self, "Error", strError, QMessageBox.Ok)
            else:
                isGrabbing = True

        # ch:停止取流 | en:Stop grab image
        def stop_grabbing(self):
            global obj_cam_operation
            global isGrabbing
            ret = obj_cam_operation.Stop_grabbing()
            if ret != 0:
                strError = "Stop grabbing failed ret:" + self.ToHexStr(ret)
                QMessageBox.warning(self, "Error", strError, QMessageBox.Ok)
            else:
                isGrabbing = False

        # ch:关闭设备 | Close device
        def close_device(self):
            global isOpen
            global isGrabbing
            global obj_cam_operation

            if isOpen:
                obj_cam_operation.Close_device()
                isOpen = False

            isGrabbing = False


if __name__=="__main__":
    import sys
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWin()
    ui.show()
    sys.exit(app.exec_())




