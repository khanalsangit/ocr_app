import sys 
from PyQt5 import QtWidgets, QtGui, QtCore

class BrandFrame(QtWidgets.QFrame):
    def __init__(self, parent):
        super(BrandFrame, self).__init__(parent)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        
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
        self.verticalLayout.setSpacing(23)
        self.brandName = QtWidgets.QLabel(self.frame2)
        self.brandName.setMaximumSize(QtCore.QSize(16777215,12))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.brandName.setFont(font)
        self.brandName.setAlignment(QtCore.Qt.AlignCenter)
        self.brandName.setText('brand')
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
        
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("hello world!")
        self.widget = QtWidgets.QWidget(self)
        self.widget.setStyleSheet("#brand{\n"
                                         "border:1px solid;\n}")
        
        self.setCentralWidget(self.widget)
        
        self.setGeometry(200,100,900,700)
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        
    def placeBrand(self):
        brand = BrandFrame(self.widget)
        brand.setMaximumSize(QtCore.QSize(250, 150))
        brand.setObjectName("brand")
        # self.gridLayout = self.widget.findChild(QtWidgets.QGridLayout)

        self.gridLayout.addWidget(brand, len(self.gridLayout)//3, len(self.gridLayout)%3)
        brand.addBrand()

class createWindow(QtWidgets.QMainWindow):
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
    
def do_action():
    value = window.lineEdit.text()
    print('v',value)      
        
if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    # window = MainWindow()
    window = createWindow()
    # window.gridLayout = QtWidgets.QGridLayout(window.widget)
    # for row in range(4):
    #     for column in range(3):
    #         window.placeBrand(row, column)
    # for _ in range(12):
    #     window.placeBrand()
    
    window.lineEdit.returnPressed.connect(do_action)
    window.show()
    app.exec_()
    sys.exit()