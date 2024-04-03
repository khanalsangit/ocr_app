import pickle
import glob
class PyQTWidgetFunction():
    '''
    This class contains all the functions of GUI widgets
    '''
    pkl_dir = glob.glob('Pickle/*.pkl')
    for pkl in pkl_dir:
        print("Pickle",pkl)
            
    with open(pkl, 'rb') as brand:
        brand_values = pickle.load(brand) 

    def test_me(self):
        print("I am from gui operation")
        
    def set_ui(self, ui_object):
        self.ui = ui_object
    
    def switch_mode(self):
        '''
        Function that checks the switch mode and change its when button is clicked.
        '''
            
        if self.ui.switchButton.isChecked():
            self.ui.stackWidget.setCurrentWidget(self.ui.debugMode_Page)
            self.ui.switchButton.setText('Debug')
        else:
            self.ui.switchButton.setText('Live')
            self.ui.stackWidget.setCurrentWidget(self.ui.liveMode_Page)
    