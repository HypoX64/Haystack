[TOC]
# Python
## base
### main
```python
def main():
    pass
if __name__ == '__main__':
    main()
```
### for
```python
for i,file in enumerate(files,0):
```
### sort
```python
'''
对列表进行排序并相应地更改另一个列表
我有两个列表：一个包含一组x点，另一个包含y点。Python以某种方式管理x点，或用户可以。我需要按照从最低到最高的顺序对它们进行排序，并且移动y点以跟随它们的x个对应点。
'''
>>> xs = [5, 2, 1, 4, 6, 3]
>>> ys = [1, 2, 3, 4, 5, 6]
>>> xs, ys = zip(*sorted(zip(xs, ys)))
>>> xs
(1, 2, 3, 4, 5, 6)
>>> ys
(3, 2, 6, 4, 1, 5)
```
### read and write txt
* read
```python
#method 1
for line in open(path):
    line=line.strip()
#method 2
def loadtxt(path):
    f = open(path, 'r')
    txt_data = f.read()
    f.close()
    return txt_data
'''
//r:读
//r+：可读可写，若文件不存在，报错, 进行了覆盖写；
//w+: 可读可写，若文件不存在，创建，进行了清空写；
//a+：可读可写但光标在最后面（然后读到最后面，所以读到空字符串），若文件不存在，创建，进行了追加写；
'''
```
* write txt
```python
#method 1
f = open(path,"w+")  
f.writelines(list)
#file.write(str)的参数是一个字符串，就是你要写入文件的内容.
#file.writelines(sequence)的参数是序列，比如列表，它会迭代帮你写入文件。
#method 2
def writetxt(path,txt):
    f = open(path,'a+')
    f.write(txt)
    f.close()
```
### csv
* write
```python
import csv
csvFile = open("csvData.csv", "w")            #创建csv文件
writer = csv.writer(csvFile)                  #创建写的对象
#先写入columns_name                             
writer.writerow(["index","a_name","b_name"])     #写入列的名称
#写入多行用writerows                                #写入多行
writer.writerows([[1,a,b],[2,c,d],[3,d,e]])
csvFile.close()
```
* read
```python
#load train csv
csv_data = []
reader = csv.reader(open('./datasets/train.csv'))
for line in reader:
    csv_data.append(line)
```
### random
* radom sort list
```python
import random
random.shuffle (list)
```
* random
```python
import random
print( random.randint(1,10) )        # 产生 1 到 10 的一个整数型随机数  
print( random.random() )             # 产生 0 到 1 之间的随机浮点数
print( random.uniform(1.1,5.4) )     # 产生  1.1 到 5.4 之间的随机浮点数，区间可以不是整数
print( random.choice('tomorrow') )   # 从序列中随机选取一个元素
print( random.randrange(1,100,2) )   # 生成从1到100的间隔为2的随机整数
a=[1,3,5,6,7]                # 将序列a中的元素顺序打乱
random.shuffle(a)

random.randint(1,50) # 随机整数：
random.randrange(0, 101, 2) # 随机选取0到100间的偶数：
random.choice('abcdefghijklmnopqrstuvwxyz!@#$%^&()') # 随机字符：
random.sample('zyxwvutsrqponmlkjihgfedcba',5)# 多个字符中生成指定数量的随机字符：
ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))# 从生成指定数量的随机字符：
''.join(random.sample(['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a'], 5))# 多个字符中选取指定数量的字符组成新字符串：
random.choice(['剪刀', '石头', '布'])# 随机选取字符串：
```

### path&file
* get the subfile path
```python
filenames = os.listdir(path)
```
* Get filepath,filename and extension
```python
(filepath,tempfilename) = os.path.split(output_path)
(filename,extension) = os.path.splitext(tempfilename)
```
* Traversal
```python
def Traversal(filedir):
    file_list=[]
    for root,dirs,files in os.walk(filedir): 
        for file in files:
            file_list.append(os.path.join(root,file)) 
        for dir in dirs:
            Traversal(dir)
    return file_list
```
* [python 获取文件大小，创建时间和访问时间](https://www.cnblogs.com/shaosks/p/5614630.html)

### time
```python
#ns
import time
t1 = time.time()
......
t2 = time.time()
print(t2-t1)
#s
import datetime
starttime = datetime.datetime.now()
endtime = datetime.datetime.now()
print('Cost time:',(endtime-starttime).seconds,'s')
```

### MulticoreOptimization(concurrent.futures)
```python
map(func, *iterables, timeout=None) 
#func：为需要异步执行的函数 
#iterables：可以是一个能迭代的对象，例如列表等。每一次func执行，会从iterables中取参数。 
#timeout：设置每次异步操作的超时时间,如果timeout参数不指定的话，则不设置超时间。 
```
* example 1:
```python
import concurrent.futures
def cut_save_process(person_name):
    return True
    
with concurrent.futures.ProcessPoolExecutor(max_workers=Process_Worker) as executor:
    for flag in executor.map(cut_save_process,person_names):
        pass
```
* example 2:
```python
def pool_factorizer_go(nums, nprocs):
   nprocs=xxx
    with ProcessPoolExecutor(max_workers=nprocs) as executor:
        return {num:factors for num, factors in
                                zip(nums,
                                    executor.map(factorize_naive, nums))}
```
* example 3:
```python
import concurrent.futures
with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
	for imgpath,count in zip(imgpath_list,executor.map(find_save_resize_face,imgpath_list,outpath_list)):
		print(imgpath)
		print(count)
```
### re
[web](http://www.runoob.com/python/python-reg-expressions.html)
* example1:(find picture)
```python
re.search(r'png$|jpg$|jpeg$|bmp$', filename, re.I)
```
* example2:
```python
re.search(r'(.*) are (.*?) .*', filename, re.I)
'''
 (.*) 第一个匹配分组，.* 代表匹配除换行符之外的所有字符。
 (.*?) 第二个匹配分组，.*? 后面多个问号，代表非贪婪模式，也就是说只匹配符合条件的最少字符
后面的一个 .* 没有括号包围，所以不是分组，匹配效果和第一个一样，但是不计入匹配结果中。
'''
```
* sort str by number
```python
import re
s = ['1.dat','10.dat','5.dat']
new = sorted(s,key = lambda i:int(re.match(r'(\d+)',i).group()))
```
### multiprocessing 
```python
import multiprocessing
import time

def func(msg):
    return multiprocessing.current_process().name + '-' + msg

if __name__ == "__main__":
    pool = multiprocessing.Pool(processes=4) # 创建4个进程
    results = []
    for i in range(10):
        msg = "hello %d" %(i)
        results.append(pool.apply_async(func, (msg, )))
    pool.close() # 关闭进程池，表示不能再往进程池中添加进程，需要在join之前调用
    pool.join() # 等待进程池中的所有进程执行完毕
    print ("Sub-process(es) done.")
    
    for res in results:
        print (res.get())
```
### print
* 数字格式化输出
```python
print('%.2f' % (end-start))
ptint('%05d' % i)
```
* format
```python
print(('Cpu   Temp: {0:.1f}C | Freq: {1:.1f}MHz').format(cpu_temp,cpu_freq))
```
### threading
```python
import threading
t=threading.Thread(target=tcplink,args=(clientsock,))  #t为新创建的线程
t.start()
```
### argparse
```python
import argparse
import sys
parse=argparse.ArgumentParser()
parse.add_argument("--savedir",type=str,default='./',help="Dir to save 'data'")
args , _ = parse.parse_known_args(sys.argv[1:])
SAVEDIR = args.savedir
```
## numpy
* zeros/ones
```python
np.zeros(shape, dtype=float, order='C')
'''
u,无符号整数，u8(64位）
f,浮点数，f8（64位）
c,浮点负数，
o,对象，
s,a，字符串，s24
u,unicode,u24
'''
```
* np.array to list
```python
a.tolist()
```
* .dtype  .shape  .astype  .reshape
```python
a.dtype  #查看数据类型
a.shape  #查看形状
a.astype  #修改数据类型
a.reshape  #修改形状
```
*  根据某一列进行排序
```python
#按照数组的第一列进行排序
data = data[np.argsort(data[:,0])]
```

## pyinstaller

```bash
pyinstaller test.py-F
```
## opencv-python
[Document](https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_setup/py_table_of_contents_setup/py_table_of_contents_setup.html)
### imread
```python
import numpy as np
import cv2
img = cv2.imread('messi5.jpg',0)
'''
第二个参数是一个标志，指定应该读取图像的方式。
cv2.IMREAD_COLOR：加载彩色图像。任何图像的透明度都将被忽略。这是默认标志。
cv2.IMREAD_GRAYSCALE：以灰度模式加载图像
cv2.IMREAD_UNCHANGED：加载图像，包括alpha通道
您可以简单地分别传递整数1,0或-1，而不是这三个标志。
'''
```
### resize
```python
#CV2.INTER_NEAREST      最邻近插值点法
#CV2.NTER_LINEAR         双线性插值法
#CV2.INTER_AREA             邻域像素再取样插补
#CV2.INTER_CUBIC           双立方插补，4*4大小的补点
#CV2.INTER_LANCZOS4         8x8像素邻域的Lanczos插值
#當我們縮小影像時，使用CV_INTER_AREA會有比較好的效果，當我們放大影像，CV_INTER_CUBIC會有最好的效果，但是計算花費時間較多，CV_INTER_LINEAR能在影像品質和花費時間上取得不錯的平衡。 CV_INTER_LANCZOS4    Lanczos插补，8*8大小的补点

```





### imshow

```python
cv2.imshow('image',img)
'''
注意：即使图像路径错误，它也不会抛出任何错误，但会给你print   img None
注意：第一个参数是一个窗口名称，它是一个字符串。第二个论点是我们的图像。您可以根据需要创建任意数量的窗口，但具有不同的窗口名称。
注意：有一种特殊情况，您可以在以后创建窗口并将图像加载到该窗口。在这种情况下，您可以指定窗口是否可调整大小。它使用函数cv2.namedWindow()完成。默认情况下，标志为cv2.WINDOW_AUTOSIZE。但是如果指定flag cv2.WINDOW_NORMAL，则可以调整窗口大小。当图像尺寸过大并向窗口添加轨迹栏时，它会很有用。
'''
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
#以下代码用于按's'并退出则保存图像，或者按ESC键直接退出而不保存。
k = cv2.waitKey(0)
if k == 27:         # wait for ESC key to exit
    cv2.destroyAllWindows()
elif k == ord('s'): # wait for 's' key to save and exit
    cv2.imwrite('messigray.png',img)
    cv2.destroyAllWindows()
```
### imwrite
```python
cv2.imwrite(filename,img)
```
### split&merge
* 通道拆分
```python
(B, G, R) = cv2.split(image)
```
* 通道合并
```python
zeros = np.zeros(image.shape[:2], dtype = "uint8")#生成一个值为0的单通道数组
#分别扩展B、G、R成为三通道。另外两个通道用上面的值为0的数组填充
cv2.imshow("Blue", cv2.merge([B, zeros, zeros]))
cv2.imshow("Green", cv2.merge([zeros, G, zeros]))
cv2.imshow("Red", cv2.merge([zeros, zeros, R]))
```
## matplotlib

## pytorch
[org](https://pytorch.org/)
[Document_Chinese](https://pytorch-cn.readthedocs.io/zh/latest/)
### hello
```
import torch
torch.cuda.is_available()
print(torch.rand(3,3).cuda())
```
### save and load
```python
torch.save(net.cpu().state_dict(), model_name)
net = UNet(n_channels=3, n_classes=1)
net.load_state_dict(torch.load(model_name))
```


# Anaconda
## install
1.download 'Anaconda3-2019.07-Linux-x86_64.sh'
2.sh 'Anaconda3-2019.07-Linux-x86_64.sh'
3.if failed:
```bash
vim ~/.bashrc
export PATH=$PATH:/home/hypo/anaconda3/bin
source ~/.bashrc
```
### basic commands
```bash
conda --version                   #查看conda版本
conda update conda                #更新conda
conda create --help               #查看conda环境管理命令帮助信息
conda create --name envname       #新建虚拟环境
conda remove --name envname --all #删除虚拟环境
conda list                        #查看当前环境安装的包
conda info --envs                 #查看conda环境信息
conda activate envname            #激活环境
conda deactivate                  #退出当前环境
```
### solution
* conda安装环境出现safetyerror
```bash
conda remove -n <env name> --all #删除该环境所有包
conda clean -a #清空anaconda pkg缓存
```
### 换源
```bash
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge 
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/msys2/
#设置搜索时显示通道地址
conda config --set show_channel_urls yes
# or linux下将以上配置文件写在~/.condarc中
vim ~/.condarc
channels:
  - https://mirrors.ustc.edu.cn/anaconda/pkgs/main/
  - https://mirrors.ustc.edu.cn/anaconda/cloud/conda-forge/
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
  - defaults
show_channel_urls: true
```
