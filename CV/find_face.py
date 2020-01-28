import face_recognition
import os
import shutil
import datetime
import concurrent.futures
import cv2
import numpy as np
import random
import string

all_img_cnt = 0

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

def resize(img,size,interpolation=cv2.INTER_LINEAR):
    h, w = img.shape[:2]
    if np.min((w,h)) ==size:
        return img
    if w >= h:
        res = cv2.resize(img,(int(size*w/h), size),interpolation=interpolation)
    else:
        res = cv2.resize(img,(size, int(size*h/w)),interpolation=interpolation)
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

def find_save_resize_face(input_path):
    try:

        filename,extension = os.path.splitext(os.path.split(input_path)[1])
        
        origin_image = cv2.imread(input_path)
        h,w = origin_image.shape[:2]
        mask = np.zeros(origin_image.shape[:2],dtype = "uint8")
        rat = min(origin_image.shape[:2])/LOADSIZE
        image = resize(origin_image, LOADSIZE,interpolation = cv2.INTER_AREA)

        face_locations = face_recognition.face_locations(image,number_of_times_to_upsample=1,model=MODEL)
               
        count=0
        mask_count = 0
        for face_location in face_locations:
            
            top, right, bottom, left = face_location
            top, right, bottom, left = int(top*rat), int(right*rat), int(bottom*rat), int(left*rat)
            # EX
            if IS_random_EXTEND:
                ex=int(((EXTEND-1+0.2*random.random())*(bottom-top))/2)
            else:
                ex=int(((EXTEND-1)*(bottom-top))/2)

            if ((bottom-top)>MINSIZE) and 0.95<abs((bottom-top)/(left-right))<1.05 and (top-ex)>0 and (bottom+ex)<h and (left-ex)>0 and (right+ex)<w:
                face = origin_image[top-ex:bottom+ex, left-ex:right+ex]
                face = cv2.resize(face, (512,512),interpolation=cv2.INTER_LANCZOS4)
                if lapulase(face)>Del_Blur_Score:
                    cv2.imwrite(os.path.join(outdir_face,random_str()+'.jpg'),face)
                    count = count+1
            if SAVE_MASK:
                try:
                    if MASK_TYPE=='contour':
                        _ex = int((bottom - top)*0.5)
                        face_get_landmark = origin_image[top-_ex:bottom+_ex, left-_ex:right+_ex]
                        face_landmark = face_recognition.face_landmarks(face_get_landmark)[0]
                        face_point = []
                        face_point = face_point+face_landmark['left_eyebrow']+face_landmark['right_eyebrow']+face_landmark['chin'][::-1]
                        face_point = np.array(face_point) + np.array([left-_ex,top-_ex])
                        face_point[:10] = face_point[:10] - np.array([0,int((bottom-top)*HIGH_MASK)])
                        mask = cv2.fillPoly(mask,[face_point],(255))
                    elif MASK_TYPE=='rect':
                        _ex = int((bottom - top)*0.05)
                        mask = cv2.rectangle(mask,(int(left-_ex*0.5),top-_ex),(int(right+_ex*0.5),bottom+_ex),(255),-1)
                    mask_count += 1
                except Exception as e:
                    pass
        if SAVE_MASK:     
            if count == mask_count and count > 0:
                mask = resize(mask,512,interpolation = cv2.INTER_AREA)
                origin_image = resize(origin_image,512,interpolation = cv2.INTER_AREA)
                cv2.imwrite(os.path.join(outdir_ori,outname+filename+'.jpg'),origin_image)
                cv2.imwrite(os.path.join(outdir_mask,outname+filename+'.png'),mask)
        return count

    except Exception as e:
        #print(input_path,e)
        return 0


filedir = (input("filedir:").strip()).replace("'","")
outname = (input("outname:").strip()).replace("'","") #outname = 'star'
MINSIZE = int((input("min_face_size(defult=256):").strip()).replace("'",""))
WORKERS = int((input("cpu_workers(defult=4):").strip()).replace("'",""))

# EXTEND=1.4
EXTEND = 1.6
Del_Blur_Score = 20  # normal-> 20 | clear -> recommed 50
IS_random_EXTEND = False
MODEL = 'cnn' # 'hog' | 'cnn'
SAVE_MASK = True
MASK_TYPE = 'rect' # rect | contour
HIGH_MASK = 0.2 # more vertical mask
LOADSIZE = 512 # load to this size and process

outdir='./output/'+outname

outdir_ori = os.path.join(outdir,'origin_image')
outdir_face = os.path.join(outdir,'face')
outdir_mask = os.path.join(outdir,'mask')
if not os.path.isdir(outdir):
    os.makedirs(outdir)
    os.makedirs(outdir_ori)
    os.makedirs(outdir_face)
    os.makedirs(outdir_mask)

file_list = Traversal(filedir)
imgpath_list = picture_select(file_list)
random.shuffle(imgpath_list)
all_length = len(imgpath_list)

print("Find picture:"+" "+str(all_length))
print('Begining......')
print('Finished/Find Face  % Bar  Usedtime/Totaltime')

starttime = datetime.datetime.now()
face_cnt=0
with concurrent.futures.ProcessPoolExecutor(max_workers=WORKERS) as executor:
    for i,imgpath,count in zip(range(1,len(imgpath_list)+1),
                               imgpath_list,
                               executor.map(find_save_resize_face,imgpath_list)):
        # print(imgpath)
        face_cnt+=count
        if i%100==0:
            endtime = datetime.datetime.now()
            used_time = (endtime-starttime).seconds
            percent = round(100*i/all_length,1)

            print('\r','',str(i)+'/'+str(face_cnt)+' ',
                str(percent)+'%'+get_bar(percent,30),
                ' '+str(int(used_time))+'s/'+str(int(used_time/i*all_length))+'s',end= " ")
            #starttime_show = datetime.datetime.now()

    print('\nFinished!','Finall find face:',face_cnt,' Cost time:',(datetime.datetime.now()-starttime).seconds,'s')