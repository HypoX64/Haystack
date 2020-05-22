import face_recognition
import os
import shutil
import datetime
import concurrent.futures
import cv2
import numpy as np
import random
import string

def random_str(length=12):
    """
    Generate secret key from alpha and digit.
    :param length: length of secret key.
    :return: [length] long secret key.
    """
    key = ''
    while length:
        key += random.choice(string.ascii_letters + string.digits)
        length -= 1
    return key

def get_bar(percent,num = 25):
    # graphs = ' ▏▎▍▋▊▉'
    percent = round(percent)
    bar = '['
    for i in range(num):
        if i < round(percent/int((100/num))):
            bar += '#'
        else:
            bar += '-'
    bar += ']'
    return bar

def lapulase(resImg):
    img2gray = cv2.cvtColor(resImg, cv2.COLOR_BGR2GRAY)  # 将图片压缩为单通道的灰度图
    res = cv2.Laplacian(img2gray, cv2.CV_64F)
    score = res.var()
    return score

def resize(img,size):
    h, w = img.shape[:2]
    if min(h, w) ==size:
        return img
    if w >= h:
        res = cv2.resize(img,(int(size*w/h), size),interpolation=cv2.INTER_LANCZOS4)
    else:
        res = cv2.resize(img,(size, int(size*h/w)),interpolation=cv2.INTER_LANCZOS4)
    return res

def Traversal(filedir):
    file_list=[]
    for root,dirs,files in os.walk(filedir): 
        for file in files:
            file_list.append(os.path.join(root,file)) 
        for dir in dirs:
            Traversal(dir)
    return file_list

def is_img(ext):
    ext = ext.lower()
    if ext in ['.jpg','.png','.jpeg','.bmp']:
        return True
    else:
        return False

def picture_select(file_list):
    imgpath_list=[]
    for pic in file_list:
        if is_img(os.path.splitext(pic)[1]):
            imgpath_list.append(pic)
    return imgpath_list

def del_noface_image(input_path):
    try:
        image = cv2.imread(input_path)
        h,w = image.shape[:2]
        face_locations = face_recognition.face_locations(image)
        if len(face_locations)>0 and lapulase(image)>Del_Blur_Score:       
            return 0
        else:
            try:
                os.remove(input_path)
                return 1
            except Exception as e:
                return 0
    except Exception as e:
        try:
            os.remove(input_path)
            return 1
        except Exception as e:
            return 0


filedir = (input("filedir:").strip()).replace("'","")
WORKERS = int((input("cpu_workers(defult=4):").strip()).replace("'",""))

Del_Blur_Score = 50


file_list = Traversal(filedir)
imgpath_list = picture_select(file_list)
random.shuffle(imgpath_list)
all_length = len(imgpath_list)

print("Find picture:"+" "+str(all_length))
print('Begining......')
print('Finished/del images  % Bar  Usedtime/Totaltime')

starttime = datetime.datetime.now()
del_cnt=0
with concurrent.futures.ProcessPoolExecutor(max_workers=WORKERS) as executor:
    for i,imgpath,count in zip(range(1,len(imgpath_list)+1),
                               imgpath_list,
                               executor.map(del_noface_image,imgpath_list)):

        del_cnt+=count
        if i%100==0:
            endtime = datetime.datetime.now()
            used_time = (endtime-starttime).seconds
            percent = round(100*i/all_length,1)

            print('\r','',str(i)+'/'+str(del_cnt)+' ',
                str(percent)+'%'+get_bar(percent,30),
                ' '+str(int(used_time))+'s/'+str(int(used_time/i*all_length))+'s',end= " ")

    print('\nFinished!','Finall del image:',del_cnt,' Cost time:',(datetime.datetime.now()-starttime).seconds,'s')