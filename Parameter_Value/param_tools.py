import sys
import os
import pickle
import traceback
from pathlib import Path 

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
    if os.path.exists(os.path.join(pickle_parameter_path, '{}.pkl'.format(pkl_name))):
        print('[+] Loading from the pickle file', )
        return pickle.load(open(os.path.join(pickle_parameter_path, '{}.pkl'.format(pkl_name)), 'rb'))
    elif param:
        save_parameter(pickle_parameter_path, 'camera_param', param)
        return param    
    else:
        try:
            raise FileNotFoundError 
        except Exception as e :
            print('Pickle folder error ', e)
            print(traceback.format_exc())
