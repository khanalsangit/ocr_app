import sys
import os
import pickle
import traceback
from pathlib import Path 

camera_param = {
    'exposure': 1000,
    'gain': 15, 
    'frame_rate': 10,
    'delay': 10,
}

augmentation_param = {
    'ntimes':5,
    'rotate':10,
    'flip':True,
    'blur':5,
    'contrast':10,
    'elastic':10,
    'rigid':10,
    'recursion_rate':0.4
}

def save_parameter(pickle_parameter_path: Path, pkl_name: str, param: dict):
    if not os.path.exists(pickle_parameter_path):
        try:
            raise FileNotFoundError 
        except Exception as e :
            print('Pickle folder error ', e)
            print(traceback.format_exc())

    system_pkl_path = os.path.join(pickle_parameter_path,'{}.pkl'.format(pkl_name))
    pickle.dump(param,open(system_pkl_path,'wb'))

def get_parameter(pickle_parameter_path: Path, pkl_name: str, param: dict = None):
    if os.path.exists(os.path.join(pickle_parameter_path, pkl_name)):
        return pickle.load(open(os.path.join(pickle_parameter_path, pkl_name), 'rb'))
    elif param:
        save_parameter(pickle_parameter_path, param)    
    else:
        try:
            raise FileNotFoundError 
        except Exception as e :
            print('Pickle folder error ', e)
            print(traceback.format_exc())
# save_parameter(augmentation_param,'augment')
