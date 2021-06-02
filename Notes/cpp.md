[toc]

## 环境配置
### base
1.linux自带g++
2.安装gdb用于调试
3.vscode走起
git同步？？？
https://blog.csdn.net/chy555chy/article/details/113338885

### Vscode
* Ctrl+Shift+P
* 输入edit或者configuration，选择”C/Cpp:Edit Configurations”
* 在c_cpp_properties.json中“includePath”的属性中添加你的库文件的地址就行了
tasks.json
```json
            "args": [
                "-g",
                "${file}",
                "-o",
                "${fileDirname}/${fileBasenameNoExtension}",
                "`pkg-config", "--cflags", "--libs", "opencv4`"
            ],
```
c_cpp_properties.json
```json
            "includePath": [
                "${workspaceFolder}/**",
                "/usr/include",
                "/usr/local/include/**",
                "/usr/local/include/opencv4",
                "/usr/local/include/opencv4/opencv2"
            ],
```
settings.json(自动格式化代码)
```json
    "editor.formatOnSave": true,
    "C_Cpp.clang_format_style": "{ BasedOnStyle: Chromium, IndentWidth: 4}"
```

## gcc
```
  -v                       Display the programs invoked by the compiler.
  -###                     Like -v but options quoted and commands not executed.
  -E                       Preprocess only; do not compile, assemble or link.
  -S                       Compile only; do not assemble or link.
  -c                       Compile and assemble, but do not link.
  -o <file>                Place the output into <file>.
  -L

```


## cmake
[cmake-examples](https://github.com/ttroy50/cmake-examples)
[最简单的例子](https://blog.csdn.net/u011341856/article/details/102408063)
[语句使用方法](https://zhuanlan.zhihu.com/p/92928820)

```cmake 
# 版本限制-必须
cmake_minimum_required(VERSION 3.5)
# 项目名-必须
project (hello)
# 查找在某个路径下的所有源文件
aux_source_directory(< dir > < variable >)
# executable
add_executable(hello_cmake main.cpp)


add_library(<name> [STATIC | SHARED | MODULE]
            [EXCLUDE_FROM_ALL]
            source1 [source2 ...])
#<name> ：库的名字，直接写名字即可，不要写lib，会自动加上前缀的哈。
#[STATIC | SHARED | MODULE] ：类型有三种。
#SHARED,动态库
#STATIC,静态库
#MODULE,在使用 dyld 的系统有效,如果不支持 dyld,则被当作 SHARED 对待。


```
* 简单的工程目录
src           文件夹：存放.cpp文件
include   文件夹：存放.h头文件
example 文件夹：存放例子代码
lib            文件夹：存放编译时产生的链接库
* fatal error: xxx.h: No such file or directory
编译器不知道去哪里找.h
```bash
└── utils
    ├── CMakeLists.txt
    ├── include
    │   └── util.hpp
    └── src
        └── util.cpp
```
```cmake
project (utils)
aux_source_directory(./src DIR_LIB_SRCS)
add_library(${PROJECT_NAME} SHARED ${DIR_LIB_SRCS})
target_include_directories( ${PROJECT_NAME}
    PUBLIC ${PROJECT_SOURCE_DIR}/include
)
```

## c++
### 三种传值方式
```c++
// 以vector为例
function1(std::vector<std::vector<int> > vec)//传值
function2(std::vector<std::vector<int> >& vec)//传引用
function3(std::vector<std::vector<int> >* vec)//传指针
// 调用
function1(vec)//传入值,会发生拷贝构造
function2(vec)//传入引用,不会发生拷贝构造  建议
function3(&vec)//传入地址,不会发生拷贝构造

```
### 格式化输出
### 字符串
#### 获取当前路径并拼接
```c++
#include <stdio.h>
#include <unistd.h>
char *buffer;
buffer = getcwd(NULL, 0);
const char *model_path = strcat(buffer,"/models");
```
### vector
* 初始化
```c++
// 调用的包
#include <vector>
using namespace std;
// 初始化
vector<int> a ;                                //声明一个int型向量a
vector<int> a(10) ;                            //声明一个初始大小为10的向量
vector<int> a(10, 1) ;                         //声明一个初始大小为10且初始值都为1的向量
vector<int> b(a) ;                             //声明并用向量a初始化向量b
vector<int> b(a.begin(), a.begin()+3) ;        //将a向量中从第0个到第2个(共3个)作为向量b的初始值

int n[] = {1, 2, 3, 4, 5} ;
vector<int> a(n, n+5) ;              //将数组n的前5个元素作为向量a的初值
vector<int> a(&n[1], &n[4]) ;        //将n[1] - n[4]范围内的元素作为向量a的初值

// 二维
int N=5, M=6; 
vector<vector<int>> obj(N); //定义二维动态数组大小5行
vector<vector<int> > obj(N, vector<int>(M)); //定义二维动态数组5行6列 
```
* 操作
```c++
push_back()         //在数组的最后添加一个数据
pop_back()          //去掉数组的最后一个数据
at()                //得到编号位置的数据
begin()             //得到数组头的指针
end()               //得到数组的最后一个单元+1的指针
front()             //得到数组头的引用
back()              //得到数组的最后一个单元的引用
max_size()          //得到vector最大可以是多大
capacity()          //当前vector分配的大小
size()              //当前使用数据的大小
resize()            //改变当前使用数据的大小，如果它比当前使用的大，者填充默认值
reserve()           //改变当前vecotr所分配空间的大小
erase()             //删除指针指向的数据项
clear()             //清空当前的vector
rbegin()            //将vector反转后的开始指针返回(其实就是原来的end-1)
rend()              //将vector反转构的结束指针返回(其实就是原来的begin-1)
empty()             //判断vector是否为空
swap()              //与另一个vector交换数据
```
* 遍历打印
```c++
// c++ 11 新方法
for(auto i:myvector){
    cout<<i<<' ';
}
// 传统方法
for (int i = 0; i < myvector.size(); i++) 
    cout << myvector[i] << ' ';
```
* list2vector
```c++
list<string> authors = { "jie","rice","pig" };
vector<string>articles = { "a","an","the" };
articles.assign(authors.begin(), authors.end());

for (auto c : articles)
{
    cout << c << endl;
}

```

### list
https://blog.csdn.net/abc882715/article/details/78783792
```c++
#include <list>
#include <string>
#include <iostream>
std::list<std::string> strings {"the","cat","sat","on","the","mat"};

```


## [opencv](https://docs.opencv.org/master/de/d7a/tutorial_table_of_content_core.html)
### install
参考:<br>
https://docs.opencv.org/master/d7/d9f/tutorial_linux_install.html<br>
https://blog.csdn.net/weixin_43953829/article/details/96473891<br>
https://zhuanlan.zhihu.com/p/118222087<br>

```bash
# 安装依赖
sudo apt-get install build-essential
sudo apt-get install cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev
sudo apt-get install python-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev
sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev liblapacke-dev
sudo apt-get install libxvidcore-dev libx264-dev
sudo apt-get install libatlas-base-dev gfortran
sudo apt-get install ffmpeg
# 下载
wget https://codeload.github.com/opencv/opencv/zip/4.4.0
unzip 4.4.0
cd opencv-4.4.0
mkdir build
cd build
# 编译
cmake -D CMAKE_BUILD_TYPE=Release -D CMAKE_INSTALL_PREFIX=/usr/local ..
make -j8
# 安装，注意加sudo因为会安装在/usr/local/lib
sudo make install

```
测试:<br>
```bash
mkdir demo
vim demo.cpp
vim CMakeList.txt
```
```c++
#include <opencv2/opencv.hpp>
using namespace cv;
using namespace std;
int main(int argc, char const *argv[])
{
    Mat Src;
    Src = imread("../imgs/test.jpg");
    cout<<"test ok!"<<endl;
    return 0;
}
```
```cmake
cmake_minimum_required(VERSION 2.8)
project( demo )
find_package( OpenCV REQUIRED )
include_directories( ${OpenCV_INCLUDE_DIRS} )
add_executable( demo demo.cpp )
target_link_libraries( demo ${OpenCV_LIBS} )
```
```bash
cmake .
make
./demo
```

#### 常见问题
```bash
# 若使用cmake,后面的步骤其实不用操作？
pkg-config --modversion opencv4
# 解决报错缺失了opencv.pc这个配置信息文件
cd /usr/local/lib/pkgconfig
sudo vim opencv4.pc
# 注意版本以及lib是否匹配
'
prefix=/usr/local
exec_prefix=${prefix}
includedir=${prefix}/include
libdir=${exec_prefix}/lib

Name: opencv
Description: The opencv library
Version:4.4.0
Cflags: -I${includedir}/opencv4
Libs: -L${libdir} -lopencv_stitching -lopencv_objdetect -lopencv_calib3d -lopencv_features2d -lopencv_highgui -lopencv_videoio -lopencv_imgcodecs -lopencv_video -lopencv_photo -lopencv_ml -lopencv_imgproc -lopencv_flann  -lopencv_core
'
pkg-config --modversion opencv4
# 解决共享路径问题
# cannot open shared object file: No such file or directory
sudo vim /etc/ld.so.conf.d/opencv.conf
'
include /etc/ld.so.conf.d/*.conf
/usr/local/lib
'
sudo ldconfig
```
### API
#### pixel
```c++
Vec3b color;            //用color变量描述一种RGB颜色
color[0] = 255;         //B分量
color[1] = 0;           //G分量
color[2] = 0;           //R分量

//灰度像素
uchar value = img.at<uchar>(i,j);       //读出第i行第j列像素值
img.at<uchar>(i,j) = 128;               //将第i行第j列像素值设置为128

//彩色像素
Vec3b pixel  = colorImage.at<Vec3b>(i, j)； //读出第i行第j列像素值
//将第i行第j列像素值设置为
Vec3b pixel;      //定义三通道像素值变量
pixel[0] = 0;     //Blue
pixel[1] = 0;     //Green
pixel[2] = 255;   //Red
colorImage.at<Vec3b>(i, j) = pixel
```
#### Mat
```c++
#include <opencv2/opencv.hpp>
using namespace cv;
using namespace std;
int main(int argc, char const *argv[])
{
    Mat grayImage(400, 600, CV_8UC1);       //创建一个大小为600x800的单通道灰度图
    Mat colorImage(400, 600, CV_8UC3);      //创建一个大小为600x800的三通道彩色图
    Mat M(2,2, CV_8UC3, Scalar(0,0,255));   //用Scalar(0,0,255)创建大小为2x2的三通道彩色图
    //直接打印
    cout << "M = " << endl << " " << M << endl << endl;
    /*M = 
    [  0,   0, 255,   0,   0, 255;
    0,   0, 255,   0,   0, 255]*/
    //遍历
    for(int i = 0; i < colorImage.rows; ++i)         //遍历行
        for(int j = 0; j < colorImage.cols; ++j)     //遍历列
        {
            Vec3b pixel = {0,0,255};
            // Vec3b pixel;            //定义三通道像素值变量
            // pixel[0] = i % 255;     //Blue
            // pixel[1] = j % 255;     //Green
            // pixel[2] = 0;           //Red
            colorImage.at<Vec3b>(i, j) = pixel;
        }
    return 0;
}

```
#### 打开图片,获取长宽，色彩空间转换，显示，保存
```c++
int main(int argc, char const *argv[])
{
    Mat Img;
    Img = imread("../imgs/test.jpg");

    int channels = Img.channels();   //通道数
    int nRows = Img.rows;            //行数
    int nCols = Img.cols; //列数
    
    cout<<channels<<" "<<nRows<<" "<<nCols<<endl;

    Mat Gray;
    cvtColor(Img, Gray, COLOR_BGR2GRAY); //cvtColor(src, dst, COLOR_BGR2GRAY)

    namedWindow("colorImage", WINDOW_AUTOSIZE);
    imshow("colorImage", Gray);
    waitKey(0);

    imwrite("./test.png", Gray);

    return 0;
}
```

#### resize
```c++
#include <opencv2/opencv.hpp>
using namespace cv;
using namespace std;
int main(int argc, char const *argv[])
{
    Mat Img;
    Img = imread("../imgs/test.jpg");

    Mat ImgResize;
    Size dsize = Size(nCols*2,nRows*2);
    //1 INTER_LINEAR
    //2 INTER_CUBIC
    //3 INTER_AREA 
    //4 INTER_LANCZOS4
    resize(Img,ImgResize,dsize,1);
    imwrite("./test.png", ImgResize);

    return 0;
}
```
#### 矩阵运算
很强，可以当numpy来使。
https://blog.csdn.net/hookie1990/article/details/79213722
```c++
#include <opencv2/opencv.hpp>
// 矩阵除数
cv::Mat a = cv::Mat::ones(cv::Size(3, 2), CV_32F);
std::cout << a / 2.0 << std::endl;
// 矩阵相加
I=I1+I2;
// 点乘
I=I.mul(I);
// 乘
I=alpha*I;
// 类型转化
I.convertTo(I1,CV_32F);
I.convertTo(I1,CV_8UC3);
```
## [libtorch](https://pytorch.org/tutorials/advanced/cpp_frontend.html)