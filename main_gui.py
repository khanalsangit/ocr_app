import sys
from PyQt5.QtWidgets import *
from pyUIdesign import  Ui_MainWindow
from Custom_Widgets import*
from CamOperation_class import CameraOperation
sys.path.append("./MvImport")

from MvImport.MvCameraControl_class import *
from MvImport.MvErrorDefine_const import *
from MvImport.CameraParams_header import *
import ctypes

# class MainWindow(QMainWindow):
#     def __init__(self, parent=None):
#         # QMainWindow.__init__(self)
#         super(MainWindow,self).__init__()
#         self.ui = Ui_MainWindow()
#         self.ui.setupUi(self)
#         loadJsonStyle(self, self.ui)
#         self.show()

# 将返回的错误码转换为十六进制显示
def ToHexStr(num):
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
    
    # Decoding Characters
    def decoding_char(c_ubyte_value):
        c_char_p_value = ctypes.cast(c_ubyte_value, ctypes.c_char_p)
        try:
            decode_str = c_char_p_value.value.decode('gbk')  # Chinese characters
        except UnicodeDecodeError:
            decode_str = str(c_char_p_value.value)
        return decode_str

    # ch:枚举相机 | en:enum devices
    def enum_devices():
        global deviceList
        global obj_cam_operation

        deviceList = MV_CC_DEVICE_INFO_LIST()
        ret = MvCamera.MV_CC_EnumDevices(MV_GIGE_DEVICE | MV_USB_DEVICE, deviceList)
        if ret != 0:
            strError = "Enum devices fail! ret = :" + ToHexStr(ret)
            QMessageBox.warning(mainWindow, "Error", strError, QMessageBox.Ok)
            return ret

        if deviceList.nDeviceNum == 0:
            QMessageBox.warning(mainWindow, "Info", "Find no device", QMessageBox.Ok)
            return ret
        print("Find %d devices!" % deviceList.nDeviceNum)

        devList = []
        for i in range(0, deviceList.nDeviceNum):
            mvcc_dev_info = cast(deviceList.pDeviceInfo[i], POINTER(MV_CC_DEVICE_INFO)).contents
            if mvcc_dev_info.nTLayerType == MV_GIGE_DEVICE:
                print("\ngige device: [%d]" % i)
                user_defined_name = decoding_char(mvcc_dev_info.SpecialInfo.stGigEInfo.chUserDefinedName)
                model_name = decoding_char(mvcc_dev_info.SpecialInfo.stGigEInfo.chModelName)
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
                user_defined_name = decoding_char(mvcc_dev_info.SpecialInfo.stUsb3VInfo.chUserDefinedName)
                model_name = decoding_char(mvcc_dev_info.SpecialInfo.stUsb3VInfo.chModelName)
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

        ui.comboBox.clear()
        ui.comboBox.addItems(devList)
        ui.comboBox.setCurrentIndex(0)
        open_device()
        start_grabbing()

    # ch:打开相机 | en:open device
    def open_device():
        global deviceList
        global nSelCamIndex
        global obj_cam_operation
        global isOpen
        if isOpen:
            QMessageBox.warning(mainWindow, "Error", 'Camera is Running!', QMessageBox.Ok)
            return MV_E_CALLORDER

        nSelCamIndex = ui.comboBox.currentIndex()
        if nSelCamIndex < 0:
            QMessageBox.warning(mainWindow, "Error", 'Please select a camera!', QMessageBox.Ok)
            return MV_E_CALLORDER

        obj_cam_operation = CameraOperation(cam, deviceList, nSelCamIndex)
        ret = obj_cam_operation.Open_device()
        if 0 != ret:
            strError = "Open device failed ret:" + ToHexStr(ret)
            QMessageBox.warning(mainWindow, "Error", strError, QMessageBox.Ok)
            isOpen = False
        else:
            strError = None
            ret = obj_cam_operation.Set_trigger_mode(False)

            isOpen = True

    # ch:开始取流 | en:Start grab image
    def start_grabbing():
        global obj_cam_operation
        global isGrabbing

        ret = obj_cam_operation.Start_grabbing(ui.imageWidget_Debug.winId())
        if ret != 0:
            strError = "Start grabbing failed ret:" + ToHexStr(ret)
            QMessageBox.warning(mainWindow, "Error", strError, QMessageBox.Ok)
        else:
            isGrabbing = True

    # ch:停止取流 | en:Stop grab image
    def stop_grabbing():
        global obj_cam_operation
        global isGrabbing
        ret = obj_cam_operation.Stop_grabbing()
        if ret != 0:
            strError = "Stop grabbing failed ret:" + ToHexStr(ret)
            QMessageBox.warning(mainWindow, "Error", strError, QMessageBox.Ok)
        else:
            isGrabbing = False

    # ch:关闭设备 | Close device
    def close_device():
        global isOpen
        global isGrabbing
        global obj_cam_operation

        if isOpen:
            obj_cam_operation.Close_device()
            isOpen = False

        isGrabbing = False
        
    
    def toogle_mode():
        if ui.switchButton.isChecked():
           ui.stackWidget.setCurrentWidget(ui.liveMode_Page)
           ui.switchButton.setText('Live')
        
        else:
            ui.switchButton.setText('Debug')
            ui.stackWidget.setCurrentWidget(ui.debugMode_Page)

    # Init app, bind ui 
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(mainWindow)
    loadJsonStyle(mainWindow,ui)
    
    ui.findCamera_Button.clicked.connect(enum_devices)
    ui.switchButton.clicked.connect(toogle_mode)
    mainWindow.show()
    app.exec_()
    close_device()
    sys.exit()