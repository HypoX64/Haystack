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
[https://blog.csdn.net/brucewong0516/article/details/85776194](【python】详解multiprocessing多进程-process模块（一）)
* run（）
       表示进程运行的方法。可以在子类中重写此方法。标准run() 方法调用传递给对象构造函数的可调用对象作为目标参数（如果有），分别使用args和kwargs参数中的顺序和关键字参数。
* start（）
       进程准备就绪，等待CPU调度。
* join（[ 超时] ）
       如果可选参数timeout是None，则该方法将阻塞，直到join()调用其方法的进程终止。如果timeout是一个正数，它最多会阻塞超时秒。请注意，None如果方法的进程终止或方法超时，则返回该方法。检查进程exitcode以确定它是否终止。
* name
       进程的名称。该名称是一个字符串，仅用于识别目的。
* is_alive（）
       返回进程是否存活。从start() 方法返回到子进程终止的那一刻，进程对象仍处于活动状态。
* daemon
       进程的守护进程标志，一个布尔值。必须在start()调用之前设置，当进程退出时，它会尝试终止其所有守护进程子进程。
* pid
       返回进程ID。在产生该过程之前，这将是 None。
* exitcode
       子进程的退出代码。None如果流程尚未终止，这将是。负值-N表示孩子被信号N终止。

```python
from multiprocessing import Process, Queue
def preload(pool):
    .......
    pool.put(data)

def main():
    pool = Queue(opt.image_pool)
    for i in range(opt.load_process):
        p = Process(target=preload,args=(pool,))
        p.daemon = True
        p.start()
    data = pool.get()

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
[参考手册](https://docs.scipy.org/doc/numpy-1.17.0/reference/)
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
## scipy
[参考手册](https://docs.scipy.org/doc/scipy-1.4.1/reference/)

## pyinstaller

```bash
pyinstaller test.py -F

```
| -h，--help                  | 查看该模块的帮助信息                                         |
| --------------------------- | ------------------------------------------------------------ |
| -F，-onefile                | 产生单个的可执行文件                                         |
| -D，--onedir                | 产生一个目录（包含多个文件）作为可执行程序                   |
| -a，--ascii                 | 不包含 Unicode 字符集支持                                    |
| -d，--debug                 | 产生 debug 版本的可执行文件                                  |
| -w，--windowed，--noconsolc | 指定程序运行时不显示命令行窗口（仅对 Windows 有效）          |
| -c，--nowindowed，--console | 指定使用命令行窗口运行程序（仅对 Windows 有效）              |
| -o DIR，--out=DIR           | 指定 spec 文件的生成目录。如果没有指定，则默认使用当前目录来生成 spec 文件 |
| -p DIR，--path=DIR          | 设置 Python 导入模块的路径（和设置 PYTHONPATH 环境变量的作用相似）。也可使用路径分隔符（Windows 使用分号，Linux 使用冒号）来分隔多个路径 |
| -n NAME，--name=NAME        | 指定项目（产生的 spec）名字。如果省略该选项，那么第一个脚本的主文件名将作为 spec 的名字 |

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
### fill
* cv2.rectangle
```python
cv2.rectangle(image, (x,y), (x+w,y+h), (0,255,0), 2)
#参数：pt1,对角坐标１, pt2:对角坐标２
# 注意这里根据两个点pt1,pt2,确定了对角线的位置，进而确定了矩形的位置
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
[实例库](https://matplotlib.org/gallery/index.html)
### colors  markers
```python
colors= ['blue','orange','green','red','purple','brown','pink','gray','olive','cyan']
markers = ['.',',','o','v','^','<','>','1','2','3','4','s','p','*','h','H','+','x','D','d','|','_']
```
### 3d+scatter
```python
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
arr  = np.zeros((300,3))
arr[0:100]  = np.random.uniform(0, 1, (100,3))
arr[100:200]  = np.random.uniform(1, 2, (100,3))
arr[200:300]  = np.random.uniform(2, 3, (100,3))
for i in range(3):
    ax.scatter(arr[i*100:(i+1)*100,0], arr[i*100:(i+1)*100,1], arr[i*100:(i+1)*100,2])

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
plt.show()

```

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
### def network
[关于Pytorch几种定义网络的方法](https://zhuanlan.zhihu.com/p/80308275)
* 直接申明
```python
import torch
import torch.nn as nn
from torch.autograd import Variable
from collections import OrderedDict
class Net():
    def __init__(self):
        super(nn.Module, NN).__init__()
        self.fc1 = nn.Linear(10,10)
        self.relu1 = nn.ReLU(inplace=True)
        self.fc2 = nn.Linear(10,2)
    def forward(self,x):
        x = self.fc1(x)
        x = self.relu1(x)
        x = self.fc2(x)
        return x
```
* nn.ModuleList()
```python
class Net():
    def __init__(self):
        super(nn.Module, NN).__init__()
        self.base = nn.ModuleList([nn.Linear(10,10), nn.ReLU(), nn.Linear(10,2)])
    def forward(self,x):
        x = self.base(x)
        return x
#nn.ModuleList()接收的参数为一个List，这样就可以很方便的定义一个网络，比如 
```

* nn.Sequential()
```python
# nn.Sequential()里面自带了forward函数，可以直接操作输入，而nn.ModuleList()需要定义一个forward函数
class Net():
    def __init__(self):
        super(nn.Module, NN).__init__()
        self.base = nn.Sequential(nn.Linear(10,10), nn.ReLU(), nn.Linear(10,2))
    def forward(self,x):
        x = self.base(x)
        return x
 
# OrderedDict
class MultiLayerNN5(nn.Module):
    def __init__(self):
        super(MultiLayerNN5, self).__init__()
        self.base = nn.Sequential(OrderedDict([
            ('0', BasicConv(1, 16, 5, 1, 2)),
            ('1', BasicConv(16, 32, 5, 1, 2)),
        ]))
        self.fc1 = nn.Linear(32 * 7 * 7, 10)

    def forward(self, x):
        x = self.base(x)
        x = x.view(x.size(0), -1)
        x = self.fc1(x)
        return x
```
* add_module
```python
class MultiLayerNN4(nn.Module):
    def __init__(self):
        super(MultiLayerNN4, self).__init__()
        self.base = nn.Sequential()
        self.base.add_module('0', BasicConv(1, 16, 5, 1, 2))
        self.base.add_module('1', BasicConv(16, 32, 5, 1, 2))
        self.fc1 = nn.Linear(32 * 7 * 7, 10)

    def forward(self, x):
        x = self.base(x)
        x = x.view(x.size(0),-1)
        x = self.fc1(x)
```
* 骚操作 用for定义多路
```python
class lstm(nn.Module):
    def __init__(self,input_size,time_step,input_nc,num_classes,Hidden_size=128,Num_layers=2):
        super(lstm, self).__init__()
        self.input_size=input_size
        self.time_step=time_step
        self.input_nc=input_nc
        self.point = input_size*time_step
        for i in range(input_nc):
            exec('self.lstm'+str(i) + '=lstm_block(input_size, time_step)')
        self.fc = nn.Linear(Hidden_size*input_nc, num_classes)

    def forward(self, x):
        y = []
        x = x.view(-1,self.input_nc,self.time_step,self.input_size)
        for i in range(self.input_nc):
            y.append(eval('self.lstm'+str(i)+'(x[:,i,:])'))
        x = torch.cat(tuple(y), 1)
        x = self.fc(x)
        return x
```
* 骚操作 用for定义多层
```python
class encoder_2d(nn.Module):
    def __init__(self, input_nc, output_nc, ngf=64, n_downsampling=3, n_blocks=9, norm_layer=nn.BatchNorm2d, 
                 padding_type='reflect'):
        assert(n_blocks >= 0)
        super(encoder_2d, self).__init__()        
        activation = nn.ReLU(True)        
        model = [nn.ReflectionPad2d(3), nn.Conv2d(input_nc, ngf, kernel_size=7, padding=0), norm_layer(ngf), activation]
        ### downsample
        for i in range(n_downsampling):
            mult = 2**i
            model += [nn.ReflectionPad2d(1),nn.Conv2d(ngf * mult, ngf * mult * 2, kernel_size=3, stride=2, padding=0),
                      norm_layer(ngf * mult * 2), activation]
        self.model = nn.Sequential(*model)
    def forward(self, input):
        return self.model(input)  

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
