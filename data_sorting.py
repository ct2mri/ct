import os
from os import walk
import numpy as np
import matplotlib.pyplot as plt
from pydicom import dcmread
import cv2
from PIL import Image as im
import shutil
import colors
# from position_search import position_linear_search

TILT_ANGLE = 10

path = './24040215/57030000/'
folders = set()
#################################################################
## Sorting Data as per Convolution Kernel
for (dirpath, _, filenames) in walk(path):
    pass
for fname in filenames:
    try:
        file_path = dirpath+fname
        conv_ker = dcmread(file_path).ConvolutionKernel[0]
        if conv_ker in folders:
            shutil.copy(file_path,'./'+conv_ker)
        else:
            folders.add(conv_ker)
            os.makedirs('./'+conv_ker)
            shutil.copy(file_path,'./'+conv_ker)
    except:
        # print(dir(dcmread(file_path)))
        print(colors.CRED + 'Error' + colors.CEND, file_path)

#################################################################

