import cv2
import numpy as np
import time
import distance

def pHash(img):
    # step1：slace to 32x32
    img=cv2.resize(img,(32,32))
    img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img=img.astype(np.float32)

    # step2: DCT
    img=cv2.dct(img)
    img=img[0:8,0:8]
    # _sum=0.
    hash_str=''

    # step3:get avg 
    avg = np.sum(img[0:8,0:8] ) / 64.0
    # for i in range(8):
    #     for j in range(8):
    #         _sum+=img[i,j]
    # avg=_sum/64

    #step4:获得哈希
    for i in range(8):
        for j in range(8):
            if img[i,j]>avg:
                hash_str=hash_str+'1'
            else:
                hash_str=hash_str+'0'
    return hash_str

#计算汉明距离
def hmdistance(hash1,hash2):
    num=0
    assert len(hash1)==len(hash2)
    for i in range(len(hash1)):
        if hash1[i]!=hash2[i]:
            num+=1
    return num


if __name__ == '__main__':
    img=cv2.imread('data/3d_left.png')
    # img=cv2.imread('data/3d_left.png')
    t1 = time.time()
    for i in range(50000):
        hash=pHash(img)
    t2 = time.time()
    print('get pHash:',t2-t1)


    t1 = time.time()
    for i in range(1000000):
        # hmdistance(hash,hash)
        distance.hamming(hash,hash)
    t2 = time.time()
    print('hmdistance:',t2-t1)



