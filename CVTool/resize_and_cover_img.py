import os
import cv2
import shutil
import datetime
import threading
import platform
import numpy as np
import util

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

def resize(img,size,interpolation=cv2.INTER_LINEAR):
    '''
    cv2.INTER_NEAREST      最邻近插值点法
    cv2.INTER_LINEAR        双线性插值法
    cv2.INTER_AREA         邻域像素再取样插补
    cv2.INTER_CUBIC        双立方插补，4*4大小的补点
    cv2.INTER_LANCZOS4     8x8像素邻域的Lanczos插值
    '''
    h, w = img.shape[:2]
    if np.min((w,h)) ==size:
        return img
    if w >= h:
        res = cv2.resize(img,(int(size*w/h), size),interpolation=interpolation)
    else:
        res = cv2.resize(img,(size, int(size*h/w)),interpolation=interpolation)
    return res

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

def main():

    filedir =input("filedir:").strip()
    filedir=str(filedir.replace("'",""))
    maxsize=int(input("maxsize threshold value(min(h,w)):").strip())
    maxstorage = float(input("maxstorage threshold value(mb):").strip())
    #recommend:2500 2.0  / 2000 2.0

    file_list = util.Traversal(filedir)
    imgpath_list = picture_select(file_list)

    print("Find picture:"+" "+str(len(imgpath_list)))
    print('Begining......')
    starttime = datetime.datetime.now()
    starttime_show = datetime.datetime.now()
    cnt=0
    originalstorage=0.0
    finalstorage=0.0

    for i,path in enumerate(imgpath_list,1):
        # try:
        originalstorage += os.path.getsize(path)
        img = imread(path)
        h,w,ch = img.shape
        if (h>maxsize)&(w>maxsize):
            img = cv2.resize(img,(int(w/2),int(h/2)),cv2.INTER_CUBIC)
            t=threading.Thread(target=cv2.imwrite,args=(path, img,))  #t为新创建的线程
            t.start()
            cnt += 1
        elif (os.path.getsize(path)>1024*1024*maxstorage):
            t=threading.Thread(target=imwrite,args=(path, img,))  #t为新创建的线程
            t.start()
            cnt += 1
        # except:
        #     print(path,'Falled!')


        if i%100==0:
            endtime = datetime.datetime.now()
            print(i,'is finished','resize:',cnt,' Cost time:',(endtime-starttime_show).seconds,'s')
            starttime_show = datetime.datetime.now()
    
    for i,path in enumerate(imgpath_list,1):
        try:
            finalstorage += os.path.getsize(path)
        except:
            print(path,'Falled!')

    originalstorage = originalstorage/float(1024*1024)
    finalstorage = finalstorage/float(1024*1024)
    print("Finished!")
    print('resize:',cnt,' Cost time:',(datetime.datetime.now()-starttime).seconds,'s')
    print('Original Size:%.2fMB'%originalstorage,' Final Size:%.2fMB'%finalstorage,' Reduce Size:%.2fMB'%(originalstorage-finalstorage))
main()