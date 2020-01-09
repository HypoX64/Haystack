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

def find_save_resize_face(input_path):
    try:

        filename,extension = os.path.splitext(os.path.split(input_path)[1])
        # image = face_recognition.load_image_file(input_path)
        image = cv2.imread(input_path)
        h,w = image.shape[:2]
        #print(image.dtype)
        # Find all the faces in the image and print
        face_locations = face_recognition.face_locations(image)
        # print("found {} face(s) in this photograph.".format(len(face_locations)))
        
        origin_image = cv2.imread(input_path)
        mask = np.zeros(origin_image.shape[:2],dtype = "uint8")

        count=0
        for face_location in face_locations:
            # Print the location of each face in this image
            top, right, bottom, left = face_location
            #print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))
            # You can access the actual face itself like this:
            if IS_random_EXTEND:
                ex=int(((EXTEND-1+0.2*random.random())*(bottom-top))/2)
            else:
                ex=int(((EXTEND-1)*(bottom-top))/2)
            # ex_face=int((1*(bottom-top))/2)
            if ((bottom-top)>MINSIZE) and 0.95<abs((bottom-top)/(left-right))<1.05 and (top-ex)>0 and (bottom+ex)<h and (left-ex)>0 and (right+ex)<w:
                face = origin_image[top-ex:bottom+ex, left-ex:right+ex]
                face = cv2.resize(face, (512,512),interpolation=cv2.INTER_LANCZOS4)
                # cv2.imwrite(os.path.join(outdir_face,outname+filename+'_'+str(count)+'.jpg'),face)
                if lapulase(face)>Del_Blur_Score:
                    #print(os.path.join(outdir_face,random_str()+'.jpg'))
                    cv2.imwrite(os.path.join(outdir_face,random_str()+'.jpg'),face)
                    count = count+1
            #mask = cv2.rectangle(mask,(left-ex,top-ex),(right+ex,bottom+ex),255,-1)  
        #mask         
        # if count > 0:
        #     mask = resize(mask,256)
        #     origin_image = resize(origin_image,1024)
        #     cv2.imwrite(os.path.join(outdir_ori,outname+filename+'.jpg'),origin_image)
        #     cv2.imwrite(os.path.join(outdir_mask,outname+filename+'.png'),mask)
        # print(output_path)
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
Del_Blur_Score = 50
IS_random_EXTEND = False
# WORKERS = 4
# MINSIZE = 256

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
            percent = round(100*i/all_length,2)

            print('\r','','Ok:'+str(i),'Face:'+str(face_cnt)+' ',
                str(percent)+'%'+get_bar(percent,30),
                ' Used/All:'+str(int(used_time))+'s/'+str(int(used_time/i*all_length))+'s',end= " ")
            #starttime_show = datetime.datetime.now()

    print('\nFinished!','Finall find face:',face_cnt,' Cost time:',(datetime.datetime.now()-starttime).seconds,'s')