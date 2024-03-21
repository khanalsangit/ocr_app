from PyQt5 import QtWidgets, QtCore, QtGui
from gui import Ui_MainWindow


class MainWin(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWin,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.create_project_button.pressed.connect(self.create_project)
        self.new_brand_add_button.pressed.connect(self.new_brand)
        self.show()

    ######################## Function to Create Project ###########################
        #####################################################################
            ##########################################################
    def create_project(self):
        self.create_project_grid = QtWidgets.QWidget(self.ui.centralwidget)
        self.create_project_grid.setMinimumSize(QtCore.QSize(300, 500))
        self.create_project_grid.setMaximumSize(QtCore.QSize(380, 16777215))
        self.create_project_grid.setStyleSheet("background-color: rgb(255, 255, 191);\n"
        "border-top-color: rgb(0, 0, 0);")
        self.create_project_grid.setObjectName("create_project_grid")
        self.create_project_label = QtWidgets.QLabel(self.create_project_grid)
        self.create_project_label.setText("Step 1: Create Project For New Brand")
        self.create_project_label.setGeometry(QtCore.QRect(35, 10, 260, 20))
        
        self.create_project_label.setStyleSheet("font: 13pt \"Times New Roman\";\n"
        "color: rgb(0, 170, 255);\n")
        # "font: 14pt \"MS Shell Dlg 2\";")
        self.create_project_label.setObjectName("create_project_label")
        self.line = QtWidgets.QFrame(self.create_project_grid)
        self.line.setGeometry(QtCore.QRect(35, 30, 260, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.create_button = QtWidgets.QPushButton(self.create_project_grid)
        self.create_button.setText("Create")
        self.create_button.setGeometry(QtCore.QRect(30, 70, 130, 50))
        self.create_button.setStyleSheet("font: 14pt \"Times New Roman\";\n"
        "color: rgb(255, 255, 255);\n"
        "background-color: rgb(0, 170, 255);\n")
        
        self.create_button.setObjectName("create_button")
        self.import_button = QtWidgets.QPushButton(self.create_project_grid)
        self.import_button.setText("Import")
        self.import_button.setGeometry(QtCore.QRect(180, 70, 130, 50))
        self.import_button.setStyleSheet("background-color: rgb(217, 217, 217);\n"
        "color: rgb(0, 0, 0);\n"
        "font: 14pt \"Times New Roman\";")
        self.import_button.setObjectName("import_button")
        self.ui.mainWindowGrid.addWidget(self.create_project_grid, 2, 1, 1, 1)

    ###################### New Brand Frame #######################
        ###################################################
            ########################################
    def new_brand(self):
        self.new_brand_frame = QtWidgets.QFrame(self.create_project_grid)
        self.new_brand_frame.setGeometry(QtCore.QRect(50, 90, 201, 151))
        self.new_brand_frame.setStyleSheet("background-color: rgb(210, 205, 228);")
        self.new_brand_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.new_brand_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.new_brand_frame.setObjectName("new_brand_frame")
        self.new_brand_label = QtWidgets.QLabel(self.new_brand_frame)
        self.new_brand_label.setText("New Brand Here")
        self.new_brand_label.setGeometry(QtCore.QRect(50, 20, 121, 20))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.new_brand_label.setFont(font)
        self.new_brand_label.setObjectName("new_brand_label")
        self.new_brand_entry = QtWidgets.QLineEdit(self.new_brand_frame)
        self.new_brand_entry.setGeometry(QtCore.QRect(40, 50, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.new_brand_entry.setFont(font)
        self.new_brand_entry.setStyleSheet("background-color: rgb(255, 255, 255);\n"
        "font: 12pt \"Times New Roman\";")
        self.new_brand_entry.setText("")
        self.new_brand_entry.setObjectName("new_brand_entry")
        self.new_brand_add_button = QtWidgets.QPushButton(self.new_brand_frame)
        self.new_brand_add_button.setText("Add")
        self.new_brand_add_button.setGeometry(QtCore.QRect(70, 90, 71, 31))
        self.new_brand_add_button.setStyleSheet("background-color: rgb(85, 170, 255);\n"
        "font: 14pt \"Times New Roman\";\n"
        "color: rgb(231, 255, 255);")
        self.new_brand_add_button.setObjectName("new_brand_add_button")

if __name__=="__main__":
    import sys
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    app = QtWidgets.QApplication(sys.argv)
    obj = MainWin()
    sys.exit(app.exec_())




