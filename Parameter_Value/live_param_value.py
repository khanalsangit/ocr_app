import pickle
import os
import sys

system_param = {
    'ocr_method':True,
    'nooflines': 3,
    'line1':'[^^^^^^^^^^^^^^]',
    'line2':'[^^^^^^^^^^^^^^^]',
    'line3':'[^^^^^^^^^^^^^^^]',
    'line4':'[^^^^^^^^^^^^^^^]'
}

rejection_params = {
    'min_per_thresh':30,
    'line_per_thresh':30,
    'reject_count':10,
    'reject_enable':True
}

camera_param = {
    'exposure_time':300,
    'trigger_delay':0,
    'camera_gain':21.0,
    'ROI':'736:956,1332:1904'
}

save_data_param = {
    'save_img':'False',
    'save_ng':'False',
    'save_result':'False',
    'img_dir':'None'
}

def save_parameter(param,pkl_name):
    pkl_path = os.path.join(os.getcwd(),'Parameter_Value')

    system_pkl_path = os.path.join(pkl_path,'{}.pkl'.format(pkl_name))
    pickle.dump(param,open(system_pkl_path,'wb'))

# save_parameter(system_param,'system')
# save_parameter(rejection_params,'rejection')
# save_parameter(camera_param,'camera')
# save_parameter(save_data_param,'save_data')