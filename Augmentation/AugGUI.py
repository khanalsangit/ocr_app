import os
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget,
    QProgressDialog, QMessageBox
)
from PyQt5.QtCore import Qt, QTimer
import yaml
from Augmentation.main_aug import main_file, count,aug_num  # Import count from main_aug



class MainWindow(QMainWindow):
    def __init__(self,parent):
        super().__init__(parent=parent)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Image Augmentation')

        # Button to start the augmentation process
        self.augment_button = QPushButton('Start Augmentation', self)
        self.augment_button.clicked.connect(self.start_augmentation)

        # Set layout
        layout = QVBoxLayout()
        layout.addWidget(self.augment_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def start_augmentation(self):
        with open("./main_config.yaml", 'r') as f:
            current_brand_config = yaml.safe_load(f)

        dir = current_brand_config['images_path']
        self.file_count = sum(len(files) for _, _, files in os.walk(dir))

        self.progress_dialog = QProgressDialog("Augmenting image...", "Cancel", 0, 200, self)
        self.progress_dialog.setWindowModality(Qt.WindowModal)
        self.progress_dialog.setAutoClose(False)
        self.progress_dialog.setAutoReset(False)
        self.progress_dialog.canceled.connect(self.handle_cancel)
        self.progress_dialog.show()

        # Start the augmentation process in a separate thread
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(100)  # Check the progress every 100 milliseconds

        QTimer.singleShot(0, main_file)  # Start main_file function immediately

    def handle_cancel(self):
        self.timer.stop()
        self.progress_dialog.close()

    def update_progress(self):
        global count  # Ensure we are accessing the global count variable
        x=count
        progress_value = (x/((self.file_count/2)*aug_num))*100 
        self.progress_dialog.setValue(progress_value)
        if  progress_value== 100:  # Assuming the process completes when count reaches 6
            self.progress_dialog.close()
            self.show_completion_message()

    def show_completion_message(self):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText("Augmentation completed!")
        msg_box.setWindowTitle("Completion")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.buttonClicked.connect(self.close_all_windows)
        msg_box.exec_()

    def close_all_windows(self):
        self.close()  # Close the main window

    

# Entry point of the application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
