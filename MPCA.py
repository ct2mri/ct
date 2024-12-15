import os
from os import walk
import matplotlib.pyplot as plt
import numpy as np
import cv2
from pydicom import dcmread

#step1: edge detection using Sobel operator and binarization edge image is obtained 
def edge_detection_binarization(img_gray, type='sobel'):
    # Convert to graycsale
    # img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Blur the image for better edge detection
    img_blur = cv2.GaussianBlur(img_gray, (3,3), 0)
    edges = None 
    if type == 'sobel':        
        # Sobel Edge Detection
        edges = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5)
    else:
        # Canny edge detection
        edges = cv2.Canny(image=img_blur, threshold1=100, threshold2=200)
    ret,th1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
    return th1

#Step2: Identify bounding boxes
def bounding_boxes(img):
    return cv2.selectROI(img)

if __name__ == '__main__':
    path = '/home/sip/Documents/Project_CT2MRI/old_data/ct/T/67428521'
    file = dcmread(path)
    img = file.pixel_array
    # print(img.shape, type(img))
    plt.imshow(img,cmap='gray')
    # new_img = edge_detection_binarization(img, 'sobel')
    # plt.imshow(new_img)
    # new_img = bounding_boxes(new_img)
    # plt.imshow(new_img)    new_img = edge_detection_binarization(img, 'sobel')
    # plt.show(new_img)
    # new_img = bounding_boxes(new_img)
    # plt.imshow(new_img)
    plt.show()
