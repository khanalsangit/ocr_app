
# Batch-Code-Inspection system

This is a repository that contains the latest OCR technique that detects and recognizes batch labels used for industrial purposes, which helps to increase the efficiency and production of industry.


## Badges

![openSource License](https://img.shields.io/badge/License-Commercial-blue)

![openSource License](https://img.shields.io/badge/build-passing-green)

![](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

## Table of contents 

* [Features](#features)
* [Documentation](#documentation)
* [Run Locally](#run)
* [Tech Stack](#tecchstack)
* [License](#license)
* [Contributors](#contributors)* 
* [Questions](#questions)

<a name="features"></a>
## Features

- High Speed Batch code inspection
- In-built feature for easy one step training
- In-built feature for data annotation and data augmentation.
- Cross platform

<a name="documentation"></a>
## Documentation

### This project has two stages:

- Text Detection
- Text Recognition

### Overall system is completed in following steps:
- Data Collection and Preprocessing
At first, data, i.e., the product's batch label, is collected from industries by using the Hikrobot camera, sensor, and bar light. The raw data that has been collected must be processed to fit into the OCR model. Here, image cropping ,image alignment and Image partition techniques are used to preprocess the image. For Detection whole image is considered but for recognition the we need to find the roi of each batch lines and used image alignment technique to align them. And then each line is partitioned into two parts so that model can also train and learn both full and half images. link for data preprocessing files is 'https://github.com/lalchhabi/Batch_Encoding_Error_Detector/tree/master/data_preparation_script'

- Data Training
Now the data is ready to train, for detection, Differentiable Binarization(DB) net algorithm and MobileNetV3 architecture is used to train the model for more than 200 epochs depending upon accuracy you get while training. Similarly for Recognition Scene Text Recognition with a Single Visual Model(SVTR) algorithm and MobileNetV1Enhance architecture is used. To train the model we have -:

If CPU version installed, please set the parameter use_gpu to false in the configuration.(det_mv3_db.yml) python3 tools/train.py -c configs/det/det_mv3_db.yml
-o Global.pretrained_model=./pretrain_models/MobileNetV3_large_x0_5_pretrained

<a name="run"></a>
## Run Locally

Clone the project

```bash
  git clone https://link-to-project
```

Go to the project directory

```bash
  cd my-project
```

Install dependencies

```bash
  pip install -r requirements
```
```bash
  pipwin install cairocffi
```

Start the project

```bash
  python main_gui.py
```
OR convert '.ui' file 
```bash
  pyuic5 -x mainGUI.ui -o pyUIdesign.py
  
  # Run GUI
  python pyUIdesign.py
```

<a name="techstack"></a>
## Tech Stack

**Client:** python, PyQT

**Server:** paddlepaddle, 

