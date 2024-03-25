from PyQt5 import QtWidgets, QtCore, QtGui
from main_gui import Ui_MainWindow


class MainWin(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWin,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # self.ui.create_project_button.pressed.connect(self.create_project)
        self.show()
    
    def save_data():
        pass

     ######################## Function to Create Project ###########################
         #####################################################################
             ##########################################################





#     ######################## Function to Create Project ###########################
#         #####################################################################
#             ##########################################################
#     def create_project(self):
#         self.parameters_function_widget = QtWidgets.QWidget(self.ui.centralwidget)
#         self.parameters_function_widget.setMinimumSize(QtCore.QSize(200, 400))
#         self.parameters_function_widget.setMaximumSize(QtCore.QSize(400, 16777215))
#         self.parameters_function_widget.setStyleSheet("background-color: rgb(255, 255, 255);")
#         self.parameters_function_widget.setObjectName("parameters_function_widget")
#         self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.parameters_function_widget)
#         self.horizontalLayout_3.setObjectName("horizontalLayout_3")
#         self.new_brand_frame = QtWidgets.QFrame(self.parameters_function_widget)
#         self.new_brand_frame.setMaximumSize(QtCore.QSize(16777215, 200))
#         self.new_brand_frame.setStyleSheet("")
#         self.new_brand_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
#         self.new_brand_frame.setFrameShadow(QtWidgets.QFrame.Raised)
#         self.new_brand_frame.setObjectName("new_brand_frame")
#         self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.new_brand_frame)
#         self.verticalLayout_7.setObjectName("verticalLayout_7")
#         self.create_project_label = QtWidgets.QLabel(self.new_brand_frame)
#         self.create_project_label.setText("Step 1. Create New Project")
#         self.create_project_label.setMinimumSize(QtCore.QSize(0, 50))
#         font = QtGui.QFont()
#         font.setFamily("Times New Roman")
#         font.setPointSize(16)
#         self.create_project_label.setFont(font)
#         self.create_project_label.setObjectName("create_project_label")
#         self.verticalLayout_7.addWidget(self.create_project_label, 0, QtCore.Qt.AlignHCenter)
#         self.line = QtWidgets.QFrame(self.new_brand_frame)
#         self.line.setFrameShape(QtWidgets.QFrame.HLine)
#         self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
#         self.line.setObjectName("line")
#         self.verticalLayout_7.addWidget(self.line)
#         self.create_project_buttons_frame = QtWidgets.QFrame(self.new_brand_frame)
#         self.create_project_buttons_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
#         self.create_project_buttons_frame.setFrameShadow(QtWidgets.QFrame.Raised)
#         self.create_project_buttons_frame.setObjectName("create_project_buttons_frame")
#         self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.create_project_buttons_frame)
#         self.horizontalLayout_2.setObjectName("horizontalLayout_2")
#         self.create_button = QtWidgets.QPushButton(self.create_project_buttons_frame)
#         self.create_button.pressed.connect(self.new_brand)
#         self.create_button.setText("Create")
#         self.create_button.setMinimumSize(QtCore.QSize(5, 30))
#         font = QtGui.QFont()
#         font.setFamily("Times New Roman")
#         font.setPointSize(12)
#         self.create_button.setFont(font)
#         self.create_button.setStyleSheet("QPushButton{\n"
# "     background: rgb(255, 255, 255);\n"
# "    border: 1px solid rgb(0, 0, 0);\n"
# "    border-radius:10px;\n"
# "\n"
# "}\n"
# "\n"
# "QPushButton:hover\n"
# "{\n"
# "   background-color: rgb(201, 202, 230);\n"
# "}\n"
# "    \n"
# " \n"
# "\n"
# "")
#         self.create_button.setObjectName("create_button")
#         self.horizontalLayout_2.addWidget(self.create_button)
#         self.import_button = QtWidgets.QPushButton(self.create_project_buttons_frame)
#         self.import_button.setText("Import")
#         self.import_button.setMinimumSize(QtCore.QSize(5, 30))
#         font = QtGui.QFont()
#         font.setFamily("Times New Roman")
#         font.setPointSize(12)
#         self.import_button.setFont(font)
#         self.import_button.setStyleSheet("QPushButton{\n"
# "     background: rgb(255, 255, 255);\n"
# "    border: 1px solid rgb(0, 0, 0);\n"
# "    border-radius:10px;\n"
# "\n"
# "}\n"
# "\n"
# "QPushButton:hover\n"
# "{\n"
# "   background-color: rgb(201, 202, 230);\n"
# "}\n"
# "    \n"
# " \n"
# "\n"
# "")
#         self.import_button.setObjectName("import_button")
#         self.horizontalLayout_2.addWidget(self.import_button)
#         self.verticalLayout_7.addWidget(self.create_project_buttons_frame)
#         self.horizontalLayout_3.addWidget(self.new_brand_frame)
#         self.ui.mainWindowGrid.addWidget(self.parameters_function_widget, 1, 1, 1, 1)

     

#     ###################### New Brand Frame #######################
#         ###################################################
#             ########################################
#     def new_brand(self):
#         print("I am here")
#         self.new_brand_grid = QtWidgets.QWidget(self.parameters_function_widget)
#         self.new_brand_grid.setMinimumSize(QtCore.QSize(100, 300))
#         self.new_brand_grid.setMaximumSize(QtCore.QSize(380, 16777215))
#         self.new_brand_grid.setStyleSheet("background-color: rgb(210, 205, 228);")
#         self.new_brand_grid.setObjectName("new_brand_grid")
#         self.new_brand_label = QtWidgets.QLabel(self.new_brand_grid)
#         self.new_brand_label.setMinimumSize(QtCore.QSize(0,0))
#         self.new_brand_label.setMaximumSize(QtCore.QSize(100,200))
#         self.new_brand_label.setText("New Brand Here")
#         self.new_brand_label.setGeometry(QtCore.QRect(100, 20, 150, 20))
#         font = QtGui.QFont()
#         font.setFamily("Times New Roman")
#         font.setPointSize(14)
#         self.new_brand_label.setFont(font)
#         self.new_brand_label.setObjectName("new_brand_label")
#         self.new_brand_entry = QtWidgets.QLineEdit(self.new_brand_grid)
#         self.new_brand_entry.setMinimumSize(QtCore.QSize(0,0))
#         self.new_brand_entry.setMaximumSize(QtCore.QSize(100,200))
#         self.new_brand_entry.setGeometry(QtCore.QRect(40, 50, 121, 31))
#         font = QtGui.QFont()
#         font.setFamily("Times New Roman")
#         font.setPointSize(12)
#         font.setBold(False)
#         font.setItalic(False)
#         font.setWeight(50)
#         self.new_brand_entry.setFont(font)
#         self.new_brand_entry.setStyleSheet("background-color: rgb(255, 255, 255);\n"
#         "font: 12pt \"Times New Roman\";")
#         self.new_brand_entry.setText("")
#         self.new_brand_entry.setObjectName("new_brand_entry")
#         self.new_brand_add_button = QtWidgets.QPushButton(self.new_brand_grid)
#         self.new_brand_add_button.setMinimumSize(QtCore.QSize(0,0))
#         self.new_brand_add_button.setMaximumSize(QtCore.QSize(100,200))
#         self.new_brand_add_button.setText("Add")
#         self.new_brand_add_button.setGeometry(QtCore.QRect(70, 90, 71, 31))
#         self.new_brand_add_button.setStyleSheet("background-color: rgb(85, 170, 255);\n"
#         "font: 14pt \"Times New Roman\";\n"
#         "color: rgb(231, 255, 255);")
#         self.new_brand_add_button.setObjectName("new_brand_add_button")        
#         self.ui.mainWindowGrid.addWidget(self.new_brand_grid, 2, 1, 1, 1)

if __name__=="__main__":
    import sys
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    app = QtWidgets.QApplication(sys.argv)
    obj = MainWin()
    sys.exit(app.exec_())




