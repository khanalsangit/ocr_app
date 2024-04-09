import sys 
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt
from pathlib import Path
import os
from typing import Callable
import yaml
import shutil

class BrandFrame(QtWidgets.QFrame):
    def __init__(self, parent, brand_title):
        super(BrandFrame, self).__init__(parent)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMaximumSize(QtCore.QSize(250, 150))
        self.setMinimumSize(QtCore.QSize(0, 150))
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.brand_title = brand_title
        
    def addBrand(self):
        self.frame1 = QtWidgets.QFrame(self)
        self.horizontalLayout1 = QtWidgets.QHBoxLayout(self.frame1)
        self.horizontalLayout1.setContentsMargins(0, 0, 0 ,0)
        self.imageLabel = QtWidgets.QLabel(self.frame1)
        self.imageLabel.setPixmap(QtGui.QPixmap("./LOGO/empty.png"))
        self.imageLabel.setScaledContents(True)
        self.imageLabel.setMaximumSize(QtCore.QSize(16777215, 100))

        self.frame2 = QtWidgets.QFrame(self)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame2.setStyleSheet("#iconFrame{\n"
                                  "border:1px solid #d4cdcd;\n}")
        self.verticalLayout.setSpacing(21)
        self.brandName = QtWidgets.QLabel(self.frame2)
        self.brandName.setMaximumSize(QtCore.QSize(16777215,16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.brandName.setFont(font)
        self.brandName.setAlignment(QtCore.Qt.AlignCenter)
        self.brandName.setText(self.brand_title)
        self.iconFrame = QtWidgets.QFrame(self.frame2)
        self.iconFrame.setMaximumSize(QtCore.QSize(16777215, 40))
        self.iconFrame.setObjectName('iconFrame')
        self.iconFrame.setStyleSheet("QPushButton{\n"
                                     "border:none;\n"
                                     "icon-size:25px 25px;\n}")
        self.horizontalLayout2 = QtWidgets.QHBoxLayout(self.iconFrame)
        self.horizontalLayout2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout2.setSpacing(0)
        self.loginButton = QtWidgets.QPushButton(self.iconFrame)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./LOGO/login.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.loginButton.setIcon(icon)
        self.binButton = QtWidgets.QPushButton(self.iconFrame)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("./LOGO/bin.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.binButton.setIcon(icon1)
        self.editButton = QtWidgets.QPushButton(self.iconFrame)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("./LOGO/edit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.editButton.setIcon(icon2)
        self.importButton = QtWidgets.QPushButton(self.frame2)
        self.importButton.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.importButton.setFont(font)
        self.importButton.setStyleSheet("color:white;\n"
                                        "background-color:#0dc177;\n"
                                        "border:none;\n"
                                        "border-radius:4px;")
        self.importButton.setText('Import')
        self.horizontalLayout.addWidget(self.frame1)
        self.horizontalLayout.addWidget(self.frame2)
        self.horizontalLayout1.addWidget(self.imageLabel)
        self.horizontalLayout2.addWidget(self.binButton)
        self.horizontalLayout2.addWidget(self.loginButton)
        self.horizontalLayout2.addWidget(self.editButton)
        self.verticalLayout.addWidget(self.brandName)
        self.verticalLayout.addWidget(self.iconFrame)
        self.verticalLayout.addWidget(self.importButton)
        self.binButton.clicked.connect(self.delete_brand)
        
    def delete_brand(self):
        pwd = Path(BRAND_DIR / self.brand_title)
        shutil.rmtree(pwd)
        window.gridLayout.removeWidget(self)
        
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("hello world!")
        self.mainWidget = QtWidgets.QWidget(self)
        self.mainWidget.setStyleSheet("#brand{\n"
                                         "border:1px solid;\n}")
        self.scrollWidget = QtWidgets.QScrollArea(self)
        self.scrollWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollWidget.setWidgetResizable(True)
        self.scrollWidget.setWidget(self.mainWidget)
        self.setCentralWidget(self.scrollWidget)
        self.setGeometry(200,100,900,700)
        self.gridLayout = QtWidgets.QGridLayout(self.mainWidget)
        self.placeBrand()
        
    def placeBrand(self):
        # self.gridLayout = self.widget.findChild(QtWidgets.QGridLayout)
        dir_list = os.listdir(BRAND_DIR)
        rows = int((len(dir_list) / 3) + 1) if len(dir_list) % 3 else int((len(dir_list) / 3)) 
        for row in range(rows):
            for column in range(3):
                list_index = row * 3 + column
                if list_index < len(dir_list):
                    self.brand_title = dir_list[list_index]
                    brand = BrandFrame(self.mainWidget, self.brand_title)
                    brand.setMaximumSize(QtCore.QSize(250, 150))
                    brand.setObjectName("brand")
                    brand.addBrand()
                    self.gridLayout.addWidget(brand, row, column)
        
class createWindow(QtWidgets.QMainWindow):
    brandNameEntered = QtCore.pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.widget = QtWidgets.QWidget(self)
        self.setWindowTitle('Create Brand')
        self.setGeometry(200,100,200,150)
        self.addWidget()
    
    def addWidget(self):
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setMaximumSize(QtCore.QSize(16777215, 10))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit.setFont(font)
        self.verticalLayout.addWidget(self.lineEdit)
        self.doneButton = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.doneButton.setFont(font)
        self.doneButton.setMaximumSize(QtCore.QSize(16777215, 25))
        self.doneButton.setStyleSheet("color:white;\n"
                                        "background-color:#0dc177;\n"
                                        "border:none;\n"
                                        "border-radius:4px;")
        self.verticalLayout.addWidget(self.doneButton)
        self.label.setText('Enter Brand Name')
        self.doneButton.setText('Done')
        self.setCentralWidget(self.widget)
        self.lineEdit.returnPressed.connect(self.emit_brand_name)

    def emit_brand_name(self):
        brand_name = self.lineEdit.text()
        self.brandNameEntered.emit(brand_name)
        self.close()
    # def __call__(self):
    #     value = self.lineEdit.text()
    #     return value
    
def create_brand(brand_name):
    brand_pwd = Path(BRAND_DIR / brand_name)
    print(brand_pwd)
    brand_config = Path(brand_pwd / 'config.yaml')

    try:
        brand_pwd.mkdir(parents=True , exist_ok=True)
        print(f'Directory creadted at {brand_pwd}')
        data = {
            'BRAND':{
                'brand_name': brand_name,
                'brand_path': str(BRAND_DIR),
                'brand_det_model':str,
                'brand_seg_model':str,
                'brand_pickle':str
            },
            'parameters_dir':str,
            'captured_image':str,
            'det_labeled_image':str,
            'reg_labeled_image':str,
            'det_augmented_image':str,
            'seg_augmented_image':str,
            'NG_image':str
        }
        with open(brand_config , 'w') as yaml_file:
            yaml.dump(data, yaml_file)
            
    except FileExistsError:
        print(f"Directory at {brand_pwd} already exists")
    except Exception as e:
        print(f"An error occurred: {e}")
        
# def brand_title():
#     dir_list = os.listdir(BRAND_DIR)
    # ...
    
if __name__ == '__main__':
    FILE = Path(__file__).parent
    BRAND_DIR = Path(FILE / 'Brands')
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    # window = createWindow()

    # window.gridLayout = QtWidgets.QGridLayout(window.widget)

    # for _ in range(12):
    #     window.placeBrand()
    
    # window.brandNameEntered.connect(create_brand)
    # window.brandNameEntered.connect(edit_brand)
    # window.lineEdit.returnPressed.connect(lambda: create_brand(window()))

    window.show()
    app.exec_()
    sys.exit()