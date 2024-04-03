import pickle
import os
import numpy as np
import tkinter
from tkinter import messagebox
########## Pickle file for brand name parameters
def new_brand_fun(brandname : str,
                ocr_method: str, 
                nooflines: int,
                line1: str,
                line2: str,
                line3: str,
                line4: str,
                minperthres: str, 
                lineperthres: str, 
                rej_count:int,
                rej_enable: int, 
                exp_time: str,
                trigger_delay: str,
                cam_gain: str,
                ROI:str,
                save_img: int,
                save_ng:int,
                save_result: int,
                img_dir: str
                ) -> None:
    brand_param = {'brand_name':brandname,
                   'ocr_method_enable':ocr_method,
                   'no_of_lines':nooflines,
                   'line1':line1,
                   'line2':line2,
                   'line3':line3,
                   'line4':line4,
                   'min_per_thresh':minperthres,
                   'line_per_thresh':lineperthres,
                   'reject_count':rej_count,
                   'reject_enable':rej_enable,
                   'exposure_time':exp_time,
                   'trigger_delay':trigger_delay,
                   'camera_gain':cam_gain,
                   'roi':ROI,
                   'save_img':save_img,
                   'save_ng':save_ng,
                   'save_result':save_result,
                   'img_dir':img_dir
                    }
   ####################### copy to the brands folder ################################
    dir_path = os.path.join(os.getcwd(),'Brands')
    new_pkl_dir = os.path.join(dir_path, '{}.pkl'.format(brandname))
    pickle.dump(brand_param,open(new_pkl_dir,'wb'))
    
    ####################### copy to the pickle folder ###############################
    pickle_path = os.path.join(os.getcwd(),'Pickle')
    new_pkl_path = os.path.join(pickle_path,'{}.pkl'.format(brandname))
    pickle.dump(brand_param,open(new_pkl_path,'wb'))

    ######################## copy to the system_pickles #############################
    system_pkl_path = os.path.join(os.getcwd(),'system_pickles')
    new_system_pkl_path = os.path.join(system_pkl_path,'initial_param.pkl')
    pickle.dump(brand_param,open(new_system_pkl_path,'wb'))

    tkinter.messagebox.showinfo("Info","Default Parameter Set Successfully")
new_brand_fun('Vaseline 200ML',True,3,'[^^^^^^^^^^^^^^]','[^^^^^^^^^^^^^^^]','[^^^^^^^^^^^^^^^]','None',30,30,10,False,300.0,0,21.0,'736:956,1332:1904',False,False,False,'C:/Users/Pc/Desktop/OCR_train/Vaseline 200 ML/Brands/Vaseline 200ML/images')
