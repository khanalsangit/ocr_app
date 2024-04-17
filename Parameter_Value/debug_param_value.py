import pickle
import os
import sys

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

def save_parameter(param,pkl_name):
    pkl_path = os.path.join(os.getcwd(),'Parameter_Value')

    system_pkl_path = os.path.join(pkl_path,'{}.pkl'.format(pkl_name))
    pickle.dump(param,open(system_pkl_path,'wb'))

save_parameter(augmentation_param,'augment')
