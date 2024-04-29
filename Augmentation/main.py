import Augmentation.aug
import os
import argparse
import random
import shutil
from PIL import Image
import yaml
import pickle
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
import sys
import time
def augmentation():
    ###### Load configuration file
    def load_config_file():
        with open('./main_config.yaml', 'r') as file_stream:
                        current_brand_config = yaml.safe_load(file_stream)
                        return current_brand_config
                        
    yaml_file = load_config_file()
    pickle_path = os.path.join(yaml_file['pickle_path'],'augment.pkl')

    with open(pickle_path,'rb') as f:
            augment_values = pickle.load(f)
    print("Augment values",augment_values)
    dir = yaml_file['images_path']
    rotate_val = int(augment_values['rotate'])
    blur = int(augment_values['blur'])
    contrast = int(augment_values['contrast'])
    elastic = int(augment_values['elastic'])
    rigid = int(augment_values['rigid'])
    rr = augment_values['recursion_rate']
    n = augment_values['ntimes']
    rotate_list = [-rotate_val, rotate_val]
    blvalue_list = [-blur, blur]
    cvalue_list = [-contrast, contrast]
    evalue_list = [-elastic, elastic]
    rvalue_list = [-rigid, rigid]

    # type = 'paddle'
    dir_name = dir+'Detection_Dataset'
    if not os.path.isdir(dir_name):
        os.mkdir(dir_name,)
        print('Detection_Dataset Folder Created')
    else:
        pass
    outdir=dir_name+'/'
    count=0


    print("Augmentation Started")

    aug_weight = 0
    current_file_name = ''
    weights = [0.1, 0.2, 0.1,0.2,0.2,0.1,0.1]   ####### probability values of each augmentation methods

    def random_augment():
        '''
        A function that chooses the augmentation method randomly and return the 
        probability values, image_path, bounding_box_path, augmentation method name
        '''
        (aug_method, weights_1), = random.choices(list(zip(aug_methods,weights)))

        aug_methods.pop(aug_methods.index(aug_method))
        aug_method_name, func, args = aug_method
        new_file = os.path.join(outdir,args[0])
        args = (new_file,*args[1:])
        if not isinstance(args, list):
            args = [*args]
        # print("Function Info",func(*args))
        image, bounding_box = func(*args)
        return weights_1, image, bounding_box, aug_method_name

    def recursive_augment(img, bounding_box, outdir, rr):
        '''
        Implement an augmentation method recursively by adding its associated probability until the sum of probabilities is greater than the recursion rate.

        Parameters:
        - img (str): Path of the image returned by the augmentation method.
        - bounding_box (str): Path of the bounding box returned by the augmentation method.
        - rr (float): Recursion rate indicating the threshold for stopping the recursion.
        '''

        global aug_weight, current_file_name
        prob_val, img, bbox, aug_method_name = random_augment()
        # print("[*] Augmenting Image ", img)
        # print("     [*] Choosing methods ", aug_method_name)
        aug_weight += prob_val
        if aug_weight >= rr:
            # print("Condition found")
            aug_weight = 0
            
            augmented_image_path = os.path.join(outdir, f"{current_file_name}_aug_{count}.jpg")
            shutil.copy(img, augmented_image_path)
            
            augmented_text_path = os.path.join(outdir,f"{current_file_name}_aug_{count}.txt")
            shutil.copy(bounding_box, augmented_text_path)
            
            # print('[+] save file ', os.path.join(outdir, augmented_image_path))
            return
        else:
            # print("[*] added weight value",aug_weight)
            current_file_name = current_file_name + '_' + aug_method_name  #### For file name
            recursive_augment(img, bbox, outdir, rr)
        
    # Copy all the files in the output directory
    for filename in os.listdir(dir):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            for i in range(0,n):
                i = str(i)
                shutil.copy(os.path.join(dir, filename), os.path.join(outdir, filename.replace('.jpg', f'_{i}.jpg')))
                shutil.copy(os.path.join(dir, filename.replace(".jpg",'.txt')), os.path.join(outdir, filename.replace(".jpg",'.txt').replace('.txt', f'_{i}.txt')))


    # Apply Augmentation
    list_of_files = os.listdir(outdir)
    for filename in list_of_files:
        if filename.endswith('.jpg') or filename.endswith('.png'):
            # print('---------------------------------------------')
            bounding_box = filename.replace(".jpg",'.txt')
            i = ''
            angle = float(random.randrange(float(rotate_list[0]), float(rotate_list[1])))
            blur = int(random.randrange(float(blvalue_list[0]), float(blvalue_list[1])))
            contrast = float(random.randrange(float(cvalue_list[0]), float(cvalue_list[1])))
            elastic = int(random.randrange(float(evalue_list[0]), float(evalue_list[1])))
            rigid = int(random.randrange(float(rvalue_list[0]), float(rvalue_list[1])))
            aug_methods = [                                               ###### Augmentation methods
                ('ori', aug.original, (filename,outdir,i)),
                ('ro', aug.rotate, (filename,angle,outdir,i)),
                ('fl', aug.img_flip, (filename,outdir,i)),
                ('bl', aug.blur, (filename,blur,outdir,i)),
                ('co', aug.contrast, (filename,contrast,outdir,i)),
                ('el', aug.elastic_transform, (filename,elastic,outdir,i)),
                ('ri', aug.rigid, (filename,rigid,outdir,i))
            ]
            current_file_name = filename.replace('.jpg', '')
            recursive_augment(filename, bounding_box, outdir, rr)  ###### calling recursive function

            # unaugmented image remove
            os.remove(os.path.join(outdir, filename)) ##### remove existing image
            os.remove(os.path.join(outdir, filename.replace('.jpg', '.txt')))   ##### remove existing files
            # print('[-] removed file ', os.path.join(outdir, filename))

            # print('--------------------------------------')
            count += 1
            if count % 100 == 0:
                print("Number of data created: ", count)

    print("Total number of data created: ", count)

    print("Augmentation Completed")



