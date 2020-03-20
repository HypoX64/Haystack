import os
import cv2
import shutil
import datetime
import threading
import util


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
        try:
            originalstorage += os.path.getsize(path)
            img = cv2.imread(path)
            h,w,ch = img.shape
            if (h>maxsize)&(w>maxsize):
                img = cv2.resize(img,(int(w/2),int(h/2)),cv2.INTER_AREA)
                t=threading.Thread(target=cv2.imwrite,args=(path, img,))  #t为新创建的线程
                t.start()
                cnt += 1
            elif (os.path.getsize(path)>1024*1024*maxstorage):
                t=threading.Thread(target=cv2.imwrite,args=(path, img,))  #t为新创建的线程
                t.start()
                cnt += 1
        except:
            print(path,'Falled!')


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