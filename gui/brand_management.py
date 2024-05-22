import sys 
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt
from pathlib import Path
import os
from typing import Callable
import yaml
import shutil
from Parameter_Value.param_tools import save_parameter
from Parameter_Value.live_param_value import *
from Parameter_Value.debug_param_value import *
import traceback
from gui.pyUIdesign import Ui_MainWindow
from typing import TYPE_CHECKING

class BrandFrame(QtWidgets.QFrame, Ui_MainWindow):
    def __init__(self, parent, brand_title):
        super(BrandFrame, self).__init__(parent)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMaximumSize(QtCore.QSize(250, 150))
        self.setMinimumSize(QtCore.QSize(0, 150))
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.brand_title = brand_title
        self.index = None 
        
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
        self.editButton.clicked.connect(self.rename_brand)
        self.loginButton.clicked.connect(self.login_brand)
            
    def delete_brand(self, path_to_brand = None):
        pwd = Path(BRAND_DIR / self.brand_title)
        shutil.rmtree(pwd)
        window.gridLayout.removeWidget(self)
        
    def rename_brand(self):
        rename_text, ok = QtWidgets.QInputDialog.getText(self, 'Rename Brand', 'Enter new brand name:')
        if ok:
            try:
                pwd = Path(BRAND_DIR / self.brand_title)
                config_file = Path(pwd / 'config.yaml')
                with open(config_file, 'r') as yaml_file:
                    data = yaml.safe_load(yaml_file)  
                data['BRAND']['brand_name'] = rename_text

                with open(config_file, 'w') as yaml_file:
                    yaml.dump(data, yaml_file)            
                        
                new_brand_dir = Path(BRAND_DIR / rename_text)
                pwd.rename(new_brand_dir)
                self.brand_title = rename_text
                QtWidgets.QMessageBox.information(self, 'Renamed', 'Brand renamed!')   
                window.update_layout()
            except:
                QtWidgets.QMessageBox.warning(self, 'Error', 'Empty field!')
    
    def login_brand(self):
        if hasattr(self, 'editWindow'):
            self.editWindow.activateWindow()
            self.editWindow.show()
        else:                                                        
            self.editWindow = editBrand(window, self.brand_title)
            self.editWindow.show()
            
class editBrand(QtWidgets.QMainWindow):
    def __init__(self, parent, brand):
        super(editBrand, self).__init__(parent)
        self.brand = brand
        self.widget = QtWidgets.QWidget(self)
        self.setGeometry(200, 100, 285, 244)
        self.setWindowTitle('Edit Brand')
        self.setMaximumSize(QtCore.QSize(285, 244))
        self.formLayout = QtWidgets.QFormLayout(self.widget)
        self.setCentralWidget(self.widget)
        self.setStyleSheet("QLabel{\n"
                                    "font-size:12px;\n"
                                    "font-family: Arial;\n"
                                    "}\n"
                            "QPushButton{\n"
                                        "color:white;\n"
                                        "background-color:#D9305C;\n"
                                    "}")
        self.addWidget()
        
    def addWidget(self):
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setText("Detection Model")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setText("Recognition Model")
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setText("Reference Image")
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setText("Detected Image")
        self.label_5 = QtWidgets.QLabel(self.widget)
        self.label_5.setText("Detection Labeled Image")
        self.label_6 = QtWidgets.QLabel(self.widget)
        self.label_6.setText("Recognition Labeled Image")
        self.label_7 = QtWidgets.QLabel(self.widget)
        self.label_7.setText("Detection Dataset ")
        self.label_8 = QtWidgets.QLabel(self.widget)
        self.label_8.setText("Recognition Dataset")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.label_8)
        
        for row in range(8):
            self.deleteButton = QtWidgets.QPushButton(self.widget)
            self.deleteButton.setText('Delete')
            self.formLayout.setWidget(row, QtWidgets.QFormLayout.FieldRole, self.deleteButton)
            self.deleteButton.clicked.connect(self.delete_func)
        
    def delete_func(self):
        # main = MainWindow()
        # brand_name = getattr(main, 'placeBrand')
        print(self.brand)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, main_ui:Ui_MainWindow, parent: QtWidgets.QMainWindow = None, brand_dir : Path = None, on_exit = None ):
        
        # self.brand_name = main_ui.projectName
        self.on_exit = None 
        if parent == None:
            super().__init__()
        else: 
            super().__init__(parent)
       
        self.brands = [] 
        self.brand_dir =  Path(brand_dir) if(type(brand_dir) !=  type(None)) else None 
        self.main_ui = main_ui
        self.setWindowTitle("Import Brand")
        self.mainWidget = QtWidgets.QWidget(self)
        self.mainWidget.setStyleSheet("#brand{\n"
                                         "border:1px solid;\n}")
        self.gridLayout = QtWidgets.QGridLayout(self.mainWidget)
        self.scrollWidget = QtWidgets.QScrollArea(self)
        self.scrollWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollWidget.setWidgetResizable(True)
        self.scrollWidget.setWidget(self.mainWidget)
        self.setCentralWidget(self.scrollWidget)
        self.setGeometry(200,100,900,700)
        self.placeBrand()
        if type(on_exit) != type(None):
            print('bboy')
            self.on_exit = on_exit


    def placeBrand(self):
        # self.gridLayout = self.widget.findChild(QtWidgets.QGridLayout)
        dir_list = os.listdir(BRAND_DIR) if type(self.brand_dir) == type(None) else os.listdir(self.brand_dir)

        rows = int((len(dir_list) / 3) + 1) if len(dir_list) % 3 else int((len(dir_list) / 3)) 
        for row in range(rows):
            for column in range(3):
                list_index = row * 3 + column
                num = 0
                if list_index < len(dir_list):
                    brand_title = dir_list[list_index]
                    brand = BrandFrame(self.mainWidget, brand_title)
                    # self.brands.append(BrandFrame(self.mainWidget, brand_title))
                    brand.setMaximumSize(QtCore.QSize(250, 150))
                    brand.setObjectName("brand")
                    brand.addBrand()
                    brand.index = list_index
                    brand.importButton.clicked.connect(self.change_brand(brand.brand_title, dir_list, brand.index))
                    num += 1
                    self.brands.append(brand)
                    self.gridLayout.addWidget(self.brands[-1], row, column)

    def change_brand(self, project_name, dir_list, index):
        def create_main_config():
            print(f'importing {project_name} from dir {dir_list[index]}, index {index} ')
            project_data = None 
            try:
                with open(Path(self.brand_dir / project_name / 'config.yaml')) as data_stream:
                    project_data = yaml.safe_load(data_stream)
            except Exception as e :
                print('error ', e )
                print(traceback.format_exc())
            try : 
                with open(Path(self.brand_dir.parent / 'main_config.yaml'), 'w') as yaml_file:
                    yaml.dump(project_data, yaml_file)
            except Exception as e :
                print('error writing to main_config.yaml')
                print(traceback.format_exc())
            # self.u.project_datai.setText(project_name)
            self._on_exit()
            self.close()
            
        return create_main_config
    

    def update_layout(self):
        for i in reversed(range(self.gridLayout.count())):
            widget = self.gridLayout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        self.placeBrand()
    
    def _on_exit(self):
        '''
        Assign a function that will update you gui based on the import logic 
        '''
        print('rhomes')
        self.on_exit()

        
class createWindow(QtWidgets.QMainWindow):
    # brandNameEntered = QtCore.pyqtSignal(str)
    def __init__(self,parent = None, brand_dir: Path = None):
        if parent != None:
            super(createWindow, self).__init__(parent)
        else:
            super().__init__()
        print('typeee', type(brand_dir))
        self.brand_dir = brand_dir if(type(brand_dir) ==  type(str)) else Path(brand_dir)
        
        
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
        self.lineEdit.returnPressed.connect(self.create_brand)

    def create_brand(self, path_to_brand = None):
        brand_name = self.lineEdit.text()
        if type(path_to_brand) == type(None) and type(self.brand_dir) == type(None) :
            brand_pwd = Path(BRAND_DIR / brand_name)
        elif type(path_to_brand) != type(None): 
            if not os.path.exists(path_to_brand):
                print('error path to brand given: ', path_to_brand)
                return 
            brand_pwd = Path(path_to_brand / brand_name)
        elif type(self.brand_dir) != type(None):
            if not os.path.exists(self.brand_dir):
                print('error path to brand given: ', path_to_brand)
                return 
            brand_pwd = Path(Path(self.brand_dir) / brand_name)
        else :
            print('configure path')
        
        brand_config = Path(brand_pwd / 'config.yaml')
        try:
            brand_pwd.mkdir(parents=True , exist_ok=True)
            print(f'Directory creadted at {brand_pwd}')
            data = {
                'brand_name': brand_name,
                
                'main_path': './Brands',
                'brand_path': os.path.join('./Brands', brand_name, ''),
                
                'images_path': os.path.join('./Brands', brand_name, 'images', ''), # saves the captured image in this folder -- the image to train on 

                'detection_path': os.path.join('./Brands', brand_name, 'detection', ''),
                'detection_model_path': os.path.join('./Brands', brand_name, 'detection', 'model', ''),
                'detection_result_path': os.path.join('./Brands', brand_name, 'detection', 'result', ''),
                'detection_dataset_path': os.path.join('./Brands', brand_name, 'detection', 'dataset', ''),

                'recognition_path': os.path.join('./Brands', brand_name, 'recognition', ''),
                'recognition_model_path': os.path.join('./Brands', brand_name, 'recognition', 'model', ''),
                'recognition_result_path': os.path.join('./Brands', brand_name, 'recognition', 'result', ''),
                'recognition_dataset_path': os.path.join('./Brands', brand_name, 'recognition', 'dataset', ''),

                'pickle_path': os.path.join('./Brands', brand_name, 'pickle_values'),

                'good_image_path': os.path.join('./Brands', brand_name, 'good_images'),
                'not_good_image_path': os.path.join('./Brands', brand_name, 'not_good_images'),
            }
            with open(brand_config , 'w') as yaml_file:
                yaml.dump(data, yaml_file)

            for key, value in data.items():
                if '_path' in key:
                    os.makedirs(Path(brand_pwd.parent.parent / value), exist_ok=True)
                
            #### Create a Pickle file for brand
            save_parameter(os.path.join(brand_pwd,'pickle_values'),'system',system_param)
            save_parameter(os.path.join(brand_pwd,'pickle_values'),'rejection',rejection_params)
            save_parameter(os.path.join(brand_pwd, 'pickle_values'), 'camera_param',camera_param)
            save_parameter(os.path.join(brand_pwd,'pickle_values'),'save_data',save_data_param)
            save_parameter(os.path.join(brand_pwd, 'pickle_values'), 'augment',augmentation_param)
            save_parameter(os.path.join(brand_pwd, 'pickle_values'),'camera_live',camera_live)
        except FileExistsError:
            print(f"Directory at {brand_pwd} already exists")
            print(traceback.format_exc())
        except Exception as e:
            print(f"An error occurred: {e}")
            print(traceback.format_exc())
        self.close()
    
if __name__ == '__main__':
    FILE = Path(__file__).parent
    BRAND_DIR = Path(FILE / 'Brands')
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    
    window.show()
    app.exec_()
    sys.exit()