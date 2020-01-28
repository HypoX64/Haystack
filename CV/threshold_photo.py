import numpy
import cv2
import os

img_dir = '/media/hypo/Hypo_U/桂林一调/理综'
out_dir = os.path.join(img_dir,'threshold')
THR = 12

img_names = os.listdir(img_dir)
if not os.path.isdir(out_dir):
    os.makedirs(out_dir)


for img_name in img_names:
    img = cv2.imread(os.path.join(img_dir,img_name), 0)
    img = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,21,THR)
    cv2.imwrite(os.path.join(out_dir,img_name), img)
