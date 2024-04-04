import sys 
import ctypes

from PyQt5.QtWidgets import QMessageBox, QMainWindow

from .MvImport.MvCameraControl_class import * 
from .MvImport.MvErrorDefine_const import * 
from .MvImport.CameraParams_header import *

from .CamOperation_class import CameraOperation 

from .tools import TxtWrapBy, ToHexStr

class MachineVisionCamera:
    def __init__(self) -> None:
        self.deviceList = MV_CC_DEVICE_INFO_LIST()
        self.cam = MvCamera()
        self.nSelCamIndex = 0
        self.obj_cam_operation: CameraOperation = 0
        self.isOpen = False
        self.isGrabbing = False
        self.isCalibMode = True # Whether it is calibration mode (get the original image)

        self.trigger_mode = None

    def set_ui(self, ui):
        self.ui = ui 

    # Bind the drop-down list to the device information index
    def xFunc(self, event):
        self.nSelCamIndex = TxtWrapBy("[", "]", self.ui.ComboDevices.get())

    def set_device_information_index(self, camera_name): # same as xFunc
        # camera_name : self.ui.ComboDevices.get()
        self.nSelCamIndex = TxtWrapBy("[", "]", camera_name)

    # decoding characters
    def decoding_char(self, c_ubyte_value):
        c_char_p_value = ctypes.cast(c_ubyte_value, ctypes.c_char_p)
        try:
            decode_str = c_char_p_value.value.decode('gbk')  # Chinese characters
        except UnicodeDecodeError:
            decode_str = str(c_char_p_value.value)
        return decode_str

    # ch:枚举相机 | en:enum devices
    def enum_devices(self):
        self.deviceList = MV_CC_DEVICE_INFO_LIST()
        ret = MvCamera.MV_CC_EnumDevices(MV_GIGE_DEVICE | MV_USB_DEVICE, self.deviceList)
        if ret != 0:
            strError = "Enum devices fail! ret = :" + ToHexStr(ret)
            self.message_box( "Error", strError)
            return ret

        if self.deviceList.nDeviceNum == 0:
            self.message_box( "Info", "Find no device",QMessageBox.Ok)
            return ret
        print("Find %d devices!" % self.deviceList.nDeviceNum)

        devList = []
        for i in range(0, self.deviceList.nDeviceNum):
            mvcc_dev_info = cast(self.deviceList.pDeviceInfo[i], POINTER(MV_CC_DEVICE_INFO)).contents
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

        self.ui.ComboDevices.clear()
        self.ui.ComboDevices.addItems(devList)
        self.ui.ComboDevices.setCurrentIndex(0)

    # ch:打开相机 | en:open device
    def open_device(self):
        if self.isOpen:
            self.message_box( "Error", 'Camera is Running!')
            return MV_E_CALLORDER

        self.nSelCamIndex = self.ui.ComboDevices.currentIndex()
        if self.nSelCamIndex < 0:
            self.message_box( "Error", 'Please select a camera!')
            return MV_E_CALLORDER

        self.obj_cam_operation = CameraOperation(self.cam, self.deviceList, self.nSelCamIndex)
        ret = self.obj_cam_operation.Open_device()
        if 0 != ret:
            strError = "Open device failed ret:" + ToHexStr(ret)
            self.message_box( "Error", strError)
            self.isOpen = False
        else:
            self.set_continue_mode()

            self.get_param()

            self.isOpen = True
            self.enable_controls()
        
        from ctypes import c_int
        stEnumInt = c_int()
        print(self.obj_cam_operation.obj_cam.MV_CC_GetEnumValue("TriggerMode", stEnumInt))

    
    # ch:开始取流 | en:Start grab image
    def start_grabbing(self):
        ret = self.obj_cam_operation.Start_grabbing(self.ui.widgetDisplay.winId())
        if ret != 0:
            strError = "Start grabbing failed ret:" + ToHexStr(ret)
            self.message_box( "Error", strError)
        else:
            self.isGrabbing = True
            self.enable_controls()
    
    # ch:停止取流 | en:Stop grab image
    def stop_grabbing(self):
        ret = self.obj_cam_operation.Stop_grabbing()
        if ret != 0:
            strError = "Stop grabbing failed ret:" + ToHexStr(ret)
            self.message_box( "Error", strError)
        else:
            self.isGrabbing = False
            self.enable_controls()
    
    # ch:关闭设备 | Close device
    def close_device(self):
        if self.isOpen:
            self.obj_cam_operation.Close_device()
            self.isOpen = False

        self.isGrabbing = False

        self.enable_controls()    

    # ch:设置触发模式 | en:set trigger mode
    def set_continue_mode(self):
        strError = None

        ret = self.obj_cam_operation.Set_trigger_mode(False)
        if ret != 0:
            strError = "Set continue mode failed ret:" + ToHexStr(ret) + " mode is " + str(is_trigger_mode)
            self.message_box( "Error", strError)
        else:
            self.ui.radioContinueMode.setChecked(True)
            self.ui.radioTriggerMode.setChecked(False)
            self.ui.bnSoftwareTrigger.setEnabled(False)
    
    # ch:设置软触发模式 | en:set software trigger mode
    def set_software_trigger_mode(self):

        ret = self.obj_cam_operation.Set_trigger_mode(True)
        if ret != 0:
            strError = "Set trigger mode failed ret:" + ToHexStr(ret)
            self.message_box( "Error", strError)
        else:
            self.ui.radioContinueMode.setChecked(False)
            self.ui.radioTriggerMode.setChecked(True)
            self.ui.bnSoftwareTrigger.setEnabled(self.isGrabbing)
    
    # ch:设置触发命令 | en:set trigger software
    def trigger_once(self):
        ret = self.obj_cam_operation.Trigger_once()
        if ret != 0:
            strError = "TriggerSoftware failed ret:" + ToHexStr(ret)
            self.message_box( "Error", strError)

    # ch:存图 | en:save image
    def save_bmp(self):
        ret = self.obj_cam_operation.Save_Bmp()
        if ret != MV_OK:
            strError = "Save BMP failed ret:" + ToHexStr(ret)
            self.message_box( "Error", strError)
        else:
            print("Save image success")

    def is_float(self, str):
        try:
            float(str)
            return True
        except ValueError:
            return False
    
    # ch: 获取参数 | en:get param
    def get_param(self):
        ret = self.obj_cam_operation.Get_parameter()
        if ret != MV_OK:
            strError = "Get param failed ret:" + ToHexStr(ret)
            self.message_box( "Error", strError)
        else:
            self.ui.edtExposureTime.setText("{0:.2f}".format(self.obj_cam_operation.exposure_time))
            self.ui.edtGain.setText("{0:.2f}".format(self.obj_cam_operation.gain))
            self.ui.edtFrameRate.setText("{0:.2f}".format(self.obj_cam_operation.frame_rate))

    # ch: 设置参数 | en:set param
    def set_param(self):
        frame_rate = self.ui.edtFrameRate.text()
        exposure = self.ui.edtExposureTime.text()
        gain = self.ui.edtGain.text()

        if self.is_float(frame_rate)!=True or self.is_float(exposure)!=True or self.is_float(gain)!=True:
            strError = "Set param failed ret:" + ToHexStr(MV_E_PARAMETER)
            self.message_box( "Error", strError)
            return MV_E_PARAMETER
        
        ret = self.obj_cam_operation.Set_parameter(frame_rate, exposure, gain)
        if ret != MV_OK:
            strError = "Set param failed ret:" + ToHexStr(ret)
            self.message_box("Error", strError)
        return MV_OK

    # ch: 设置控件状态 | en:set enable status
    def enable_controls(self):
        # Set the status of the group first, and then set the status of each control individually.
        self.ui.groupGrab.setEnabled(self.isOpen)
        self.ui.groupParam.setEnabled(self.isOpen)

        self.ui.bnOpen.setEnabled(not self.isOpen)
        self.ui.bnClose.setEnabled(self.isOpen)

        self.ui.bnStart.setEnabled(self.isOpen and (not self.isGrabbing))
        self.ui.bnStop.setEnabled(self.isOpen and self.isGrabbing)
        self.ui.bnSoftwareTrigger.setEnabled(self.isGrabbing and self.ui.radioTriggerMode.isChecked())
  
        self.ui.bnSaveImage.setEnabled(self.isOpen and self.isGrabbing)

    def message_box(self, title: str, text: str, value = None):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle(title)
        msgBox.setText(text)
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            print('OK clicked')
            return True 
        else:
            print('Cancel clicked')
            return False 