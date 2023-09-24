import argparse
import datetime
import os
import platform
import shutil
import threading
import time

import cv2
import numpy as np
import util
from skimage import io,transform
from tqdm import tqdm

system_type = 'Linux'
if 'Windows' in platform.platform():
    system_type = 'Windows'

def imread(file_path,mod = 'normal',loadsize = 0, rgb=False):
    '''
    mod:  'normal' | 'gray' | 'all'
    loadsize: 0->original
    '''
    if system_type == 'Linux':
        if mod == 'normal':
            img = cv2.imread(file_path,1)
        elif mod == 'gray':
            img = cv2.imread(file_path,0)
        elif mod == 'all':
            img = cv2.imread(file_path,-1)
    
    #In windows, for chinese path, use cv2.imdecode insteaded.
    #It will loss EXIF, I can't fix it
    else: 
        if mod == 'normal':
            img = cv2.imdecode(np.fromfile(file_path,dtype=np.uint8),1)
        elif mod == 'gray':
            img = cv2.imdecode(np.fromfile(file_path,dtype=np.uint8),0)
        elif mod == 'all':
            img = cv2.imdecode(np.fromfile(file_path,dtype=np.uint8),-1)
            
    if loadsize != 0:
        img = resize(img, loadsize, interpolation=cv2.INTER_CUBIC)

    if rgb and img.ndim==3:
        img = img[:,:,::-1]

    return img

def resize(img,size,interpolation=cv2.INTER_CUBIC,mode=0):
    if mode == 0:
        img = cv2.resize(img,size,interpolation=interpolation)
    elif mode == 1:
        img = transform.resize(img,(size[1],size[0]))
        img = (img*255).astype(np.uint8)
    return img
    


def imwrite(file_path,img,use_thread=False):
    '''
    in other to save chinese path images in windows,
    this fun just for save final output images
    '''
    def subfun(file_path,img):
        if system_type == 'Linux':
            cv2.imwrite(file_path, img)
        else:
            cv2.imencode('.jpg', img)[1].tofile(file_path)
    if use_thread:
        t = threading.Thread(target=subfun,args=(file_path, img,))
        t.daemon()
        t.start
    else:
        subfun(file_path,img)


def picture_select(file_list):
    imgpath_list=[]
    for pic in file_list:
        if util.is_img(pic):
            imgpath_list.append(pic)
    return imgpath_list

def cover_img(file_path,img):
    os.remove(file_path)
    cv2.imwrite(file_path.replace('.png','.jpg'),img)


parser=argparse.ArgumentParser()
parser.add_argument("--dir",type=str,default='./',help="Dir to save 'data'")
parser.add_argument("--maxsize",type=int,default=2500,help="")
parser.add_argument("--maxstorage",type=float,default=2.0,help="")
parser.add_argument("--resizemode",type=int,default=0,help="0:opencv 1:skimage")

opt = parser.parse_args()


def main():

    filedir = opt.dir
    maxsize = opt.maxsize
    maxstorage = opt.maxstorage
    #recommend:2500 2.0  / 2000 2.0
    print('Find image...')
    file_list = util.Traversal(filedir)
    imgpath_list = picture_select(file_list)

    print("Found:"+" "+str(len(imgpath_list)))
    print('Start...')
    starttime = datetime.datetime.now()
    starttime_show = datetime.datetime.now()
    cnt=0
    originalstorage=0.0
    finalstorage=0.0

    for path in tqdm(imgpath_list):
        try:
            originalstorage += os.path.getsize(path)
            img = imread(path)
            h,w,ch = img.shape
            if (h>maxsize)&(w>maxsize):
                img = resize(img,(int(w/2),int(h/2)),cv2.INTER_CUBIC,mode=opt.resizemode)
                t=threading.Thread(target=cover_img,args=(path, img,))  #t为新创建的线程
                t.start()
                cnt += 1
            elif (os.path.getsize(path)>1024*1024*maxstorage):
                img = resize(img,(int(w/2),int(h/2)),cv2.INTER_CUBIC,mode=opt.resizemode)
                t=threading.Thread(target=cover_img,args=(path, img,))  #t为新创建的线程
                t.start()
                cnt += 1
        except:
            print(path,'Process falled!')


        # if i%100==0:
        #     endtime = datetime.datetime.now()
        #     print(i,'is finished','resize:',cnt,' Cost time:',(endtime-starttime_show).seconds,'s')
        #     starttime_show = datetime.datetime.now()
    
    time.sleep(1)
    print("Calculate size...")
    for i,path in enumerate(imgpath_list,1):
        try:
            finalstorage += os.path.getsize(path.replace('.png','.jpg'))
        except:
            print(path,'Calculate size falled!')

    originalstorage = originalstorage/float(1024*1024)
    finalstorage = finalstorage/float(1024*1024)
    print("Finished!")
    print('resize:',cnt,' Cost time:',(datetime.datetime.now()-starttime).seconds,'s')
    print('Original Size:%.2fMB'%originalstorage,' Final Size:%.2fMB'%finalstorage,' Reduce Size:%.2fMB'%(originalstorage-finalstorage))
main()