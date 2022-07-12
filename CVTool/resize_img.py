from pickletools import optimize
from tkinter.tix import Tree
import cv2
import numpy as np
import os,json
import subprocess
import argparse
from tqdm import tqdm
from PIL import Image
from skimage import io,transform
import warnings
warnings.filterwarnings("ignore")

# ---------------------------------util-------------------------------

def makedirs(path):
    if os.path.isdir(path):
        print(path,'existed')
    else:
        os.makedirs(path)
        print('makedir:',path)

def Traversal(filedir):
    file_list=[]
    for root,dirs,files in os.walk(filedir): 
        for file in files:
            file_list.append(os.path.join(root,file)) 
        for dir in dirs:
            Traversal(dir)
    return file_list

def is_img(path):
    ext = os.path.splitext(path)[1]
    ext = ext.lower()
    if ext in ['.jpg','.png','.jpeg','.bmp']:
        return True
    else:
        return False

def is_video(path):
    ext = os.path.splitext(path)[1]
    ext = ext.lower()
    if ext in ['.mp4','.flv','.avi','.mov','.mkv','.wmv','.rmvb','.mts']:
        return True
    else:
        return False

def is_imgs(paths):
    tmp = []
    for path in paths:
        if is_img(path):
            tmp.append(path)
    return tmp

def is_videos(paths):
    tmp = []
    for path in paths:
        if is_video(path):
            tmp.append(path)
    return tmp  


def args2cmd(args):
    cmd = ''
    for arg in args:
        cmd += (arg+' ')
    return cmd

def run(args,mode = 0):

    if mode == 0:
        cmd = args2cmd(args)
        print(cmd)
        os.system(cmd)

    elif mode == 1:
        '''
        out_string = os.popen(cmd_str).read()
        For chinese path in Windows
        https://blog.csdn.net/weixin_43903378/article/details/91979025
        '''
        cmd = args2cmd(args)
        stream = os.popen(cmd)._stream
        sout = stream.buffer.read().decode(encoding='utf-8')
        return sout

    elif mode == 2:
        cmd = args2cmd(args)
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        sout = p.stdout.readlines()
        return sout

def get_size(h,w,max_size):
    if w >= h:
        return max_size,int(max_size*w/h)
    else:
        return int(max_size*h/w),max_size


parser=argparse.ArgumentParser()
parser.add_argument("--dir",type=str,default='',help="Dir to save 'data'")
parser.add_argument("--output",type=str,default='./tmp',help="")
parser.add_argument("--max_size",type=int,default=512, help="if img min size >max_size, resize it")


opt = parser.parse_args()
if opt.dir == '':
    print('Please input parser. -h')
makedirs(opt.output)

paths = Traversal(opt.dir)
img_paths = is_imgs(paths)

for path in tqdm(img_paths):
    # # opencv
    # img = cv2.imread(path)
    # new_h,new_w = get_size(img.shape[0],img.shape[1],opt.max_size)
    # img = cv2.resize(img,(new_w,new_h),interpolation=cv2.INTER_LANCZOS4)
    # # print(os.path.join(opt.output,os.path.split(path)[1].replace('jpg','png')))
    # cv2.imwrite(os.path.join(opt.output,os.path.split(path)[1].replace('jpg','png')),img)

    # # PIL
    # img = Image.open(path)
    # w,h = img.size
    # new_h,new_w = get_size(h,w,opt.max_size)
    # img = img.resize((new_w,new_h),Image.ANTIALIAS)
    # img.save(os.path.join(opt.output,os.path.split(path)[1].replace('jpg','png')),optimize=True)

    # skimage
    img = io.imread(path)
    new_h,new_w = get_size(img.shape[0],img.shape[1],opt.max_size)
    img = transform.resize(img,(new_h,new_w))
    io.imsave(os.path.join(opt.output,os.path.split(path)[1].replace('jpg','png')),(img*255.0).astype('uint8'))
    # print(img.shape) 