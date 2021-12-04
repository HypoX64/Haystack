[toc]

## 1 环境配置
### 1.1  base
https://blog.csdn.net/chy555chy/article/details/113338885

### 1.2 VScode
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
#### 1.2.2 使用vscode配置cmake 以及gdb调试
* launch.json
```json
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "debug",
            "type": "cppdbg",
            "request": "launch",
            "stopAtEntry": false,
            "program": "${workspaceRoot}/build/example/tensorrtTest",
            "args": [
                "-advdd",
                "dsasd0",
            ],
            "miDebuggerPath": "/usr/bin/gdb",
            "sourceFileMap": {
                "/build/glibc-S9d2JN": "/usr/src/glibc"
            }
        }
    ]
}
```
* tasks.json
```json
    "tasks": [
        {
            "label": "build",
            "type": "shell",
            "command": "cd build && cmake .. && make"
        }
```

### 1.3 windows
[gcc](http://mingw-w64.yaxm.org/doku.php)  [cmake](https://cmake.org/)
### 1.4 VS studio

## 2 gcc
```
  -v                       Display the programs invoked by the compiler.
  -###                     Like -v but options quoted and commands not executed.
  -E                       Preprocess only; do not compile, assemble or link.
  -S                       Compile only; do not assemble or link.
  -c                       Compile and assemble, but do not link.
  -o <file>                Place the output into <file>.
  -L

```
### 2.1 多版本gcc切换
```bash
################
#根据多次踩坑的经验，最好不要用下面的方法，最好老老实实手动给/usr/bin/gcc /usr/bin/g++ /usr/bin/c++ /usr/bin/cc 进行软链接，注意gcc和c++的区别，c++可以是g++的软链接
################

# 下载安装欲新增版本的gcc工具
apt-get install gcc-4.8 g++-4.8
# 查看系统中已安装的gcc版本
ls /usr/bin/gcc*
# 将各个版本gcc加入gcc候选中，设置优先级
update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-4.8 3
# 选择要使用的gcc版本
update-alternatives --config gcc


```
### 2.2 gcc g++的区别
编译阶段，g++会调用gcc，对于c++代码，两者是等价的，但是gcc命令不能自动和C＋＋程序使用的库lstdc++联接。

### 2.3 Flag
```bash
-Wno-deprecated    #屏蔽警告
-g                 #debug 模式
-std=c++11         #指定c++标准
-fPIC              #产生与位置无关代码。全部使用相对地址，故而代码可以被加载器加载到内存的任意位置，都可以正确的执行。这正是共享库所要求的

```

### 2.4 pkg-config
如何知道库的存放路径和头文件路径？
```bash
# 在使用前请设置PKG_CONFIG_PATH的路径
export PKG_CONFIG_PATH=/your/path:$PKG_CONFIG_PATH
# 某个库在安装完成后，会在其安装目录下的 lib/ 下生成 .pc 文件。把这个文件复制到 PKG_CONFIG_PATH 下。然后用 pkg-config --libs libxxx , 查看是否生效。
# --list-all : 列出所有已经安装的共享库
# --cflags : 列出指定库的预处理和编译 flag
# --libs : 列出指定库的链接 flag
```

### 2.5 ldd
```bash
# list, dynamic, dependencies
# 列出动态库依赖关系
ldd util.so
```

## 3 cmake
[cmake-examples](https://github.com/ttroy50/cmake-examples)
[最简单的例子](https://blog.csdn.net/u011341856/article/details/102408063)
[语句使用方法](https://zhuanlan.zhihu.com/p/92928820)

### 3.1 install 
```bash
sudo apt-get install openssl libssl-dev
wget ... #下载源码
tar zxvf cmake-3.20.6.tar.gz
cd cmake-3.20.6
./bootstrap
make -j8
make install
```
### 3.2 基本语法
```cmake
${PROJECT_NAME} # Name of the project given to the project command.
${CMAKE_BINARY_DIR} # The path to the top level of the build tree.
${PROJECT_SOURCE_DIR} # Top level source directory for the current project.
${ORIGIN} # 运行程序所在目录
cmake_minimum_required(VERSION 3.5) #最低版本限制
project (hello) # 指定项目名

aux_source_directory(/dir/to/your/src DIR_LIB_SRCS) # 查找在某个路径下的所有源文件 
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)#设置输出二进制文件路径
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)#设置输出so的位置

add_executable(<name> source1 [source2 ...]) #Add an executable to the project using the specified source files.


include_directories("/include") #配置头文件目录
link_directories("lib") #配置库文件目录 : 设置 lib 库文件查找目录 

# 很多设置可以在输入cmake命令的同时输入，比如
-DCMAKE_CXX_COMPILER=/usr/bin/c++ #指定编译器
-DCMAKE_BUILD_TYPE=Release #指定为发行版
-DCMAKE_INSTALL_PREFIX=/usr/local #指定安装目录


```
### 3.3 基本实例
```cmake 

cmake_minimum_required(VERSION 3.5)

# Set the project name
project (hello)

# Add an executable
add_executable(hello_cmake main.cpp)

```

### 3.4 使用动态库
```cmake
cmake_minimum_required (VERSION 3.8)
project (demo)

#配置头文件目录
include_directories("/include")
#配置库文件目录 : 设置 lib 库文件查找目录 
link_directories("lib")
#注意lib中的文件应拷贝到usr/lib
 
# 将源代码添加到此项目的可执行文件。
add_executable (${PROJECT_NAME} "main.cpp" )

#设置编译链接的库
target_link_libraries(
	${PROJECT_NAME}	#本项目的解决方案名称
	avcodec		#动态库名字
	
# 最后设置一下运行时动态库的路径，记得把so拷贝设置好的路径下
SET(CMAKE_BUILD_WITH_INSTALL_RPATH TRUE) 
SET(CMAKE_INSTALL_RPATH ${ORIGIN}/lib)
)

也可以单独链接某个so
# 或者单独按照路径链接某个so
# SHARED表示添加的是动态库 IMPORTED表示是引入已经存在的动态库
add_library( avcodec SHARED IMPORTED )
set_target_properties( avcodec PROPERTIES IMPORTED_LOCATION ${ffmpeg_libs_DIR}/libavcodec.so )

```

### 3.5 other
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


### 3.6 pkg-config
在使用 CMake 作为项目构建工具时，有一些库并没有提供 cmake 文件，往往提供的是 pkg-config 的 .pc 文件, 下面演示使用PkgConfig将ffmpeg引入项目
```cmake
find_package(PkgConfig REQUIRED)

pkg_check_modules(ffmpeg REQUIRED IMPORTED_TARGET libavcodec libavformat libavutil)

target_link_libraries(${PROJECT_NAME} PRIVATE PkgConfig::ffmpeg)

```

## 4 c++
### 4.1 基本使用
https://zhuanlan.zhihu.com/p/343271809
#### 4.1.1 基本类型
| 类型 | 最小尺寸 |
| :--- | :--- |
| bool | 未定义 |
| char | 8位 |
| w_char_t | 16位 |
| char16_t | 16位 |
| char32_t | 32位 |
| short | 16位 |
| int | 16位 |
| long | 32位 |
| long long | 64位 |
| float | 6位有效数字 |
| double | 10位有效数字 |
| long double | 10位有效数字 |

#### 4.1.2 作用域
作用域：C++中大多数作用域都用花括号分隔。
作用域中一旦声明了某个名字，它所嵌套的所有作用域都能访问该名字。
在作用域声明的变量或被智能指针包裹的，离开作用域时会自动回收
#### 4.1.3 命名空间



#### 4.1.4 函数
##### 4.1.4.1 三种传值方式
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
##### 4.1.4.1 重载

#### 4.1.5 类
https://www.runoob.com/cplusplus/cpp-constructor-destructor.html
#### 4.1.5.1 构造函数
```c++
class Line
{
   public:
      void setLength( double len );
      double getLength( void );
      Line();  // 这是构造函数
 
   private:
      double length;
};
//成员初始化的顺序与它们在类定义中出现 的顺序一致
//使用它所述类的其他构造函数执行它自己的初始化过程。

// 成员函数定义，包括构造函数
Line::Line(void)
{
    cout << "Object is being created" << endl;
}
...
```
#### 4.1.5.2 带参数的构造函数
```c++
//但如果需要，构造函数也可以带有参数。这样在创建对象时就会给对象赋初始值
class Line
{
   public:
      void setLength( double len );
      double getLength( void );
      Line(double len);  // 这是构造函数
 
   private:
      double length;
};
// 成员函数定义，包括构造函数
Line::Line(void)
{
    cout << "Object is being created" << endl;
}
...


int main( )
{
   Line line(10.0);
   return 0;
}
```

#### 4.1.5.3 析构函数
类的析构函数是类的一种特殊的成员函数，**它会在每次删除所创建的对象时执行。**
析构函数的名称与类的名称是完全相同的，只是在前面加了个波浪号（~）作为前缀，它不会返回任何值，也不能带有任何参数。析构函数有助于在跳出程序（比如关闭文件、释放内存等）前释放资源。
```c++
class Line
{
   public:
      void setLength( double len );
      double getLength( void );
      Line();   // 构造函数声明
      ~Line();  // 析构函数声明
 
   private:
      double length;
};

Line::Line(void)
{
    cout << "Object is being created" << endl;
}
Line::~Line(void)
{
    cout << "Object is being deleted" << endl;
}
```
#### 4.1.5.4 不同的初始化方法
```c++
A a;  // a存在栈上,不需要手动释放，该类析构函数会自动执行
A* a = new a();  // a存在堆中,需要手动delete
/****************************
1 前者在栈中分配内存，后者在堆中分配内存
2 动态内存分配会使对象的可控性增强
3 大程序用new，小程序不加new，直接申请
4 new必须delete删除，不用new系统会自动回收内存
*****************************/
// new创建类对象例子：
CTest* pTest = new CTest();
delete pTest;
// (std::nothrow)
Book *book = new (std::nothrow) Book();
if (book == NULL) {
	//do some when fail
}
```


### 4.3 字符串
#### 4.3.1 格式化输出

#### 4.3.2  获取当前路径并拼接
```c++
#include <stdio.h>
#include <unistd.h>
char *buffer;
buffer = getcwd(NULL, 0);
const char *model_path = strcat(buffer,"/models");
```

### 4.4 vector
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

//c++ 11以上可直接{}初始化
vector<int> a = {1,2,3.0,4,5,6,7};

// 二维
int N=5, M=6; 
vector<vector<int>> obj(N); //定义二维动态数组大小5行
vector<vector<int> > obj(N, vector<int>(M)); //定义二维动态数组5行6列 

```
* 作用域

声明形如vector<> vec;
如果vec不是new出来而是作为普通变量的那么不需要delete, 在变量超出作用域时会自动回收如果是用*vec = new vector<>()这种方式动态创建的vector那么需要delete vec
vec里存放的元素如果不是指针那么不用delete, 这些元素在vec被释放时会被一起释放
vec里存放的元素是指针并且这些指针都是指向自己new的对象的话, 那么需要自己一个个delete

* 操作
```c++
//插入
std::vector<float> a(100,0);
std::vector<float> padding(100,0);
melspect.insert(a.begin(),padding.begin(),padding.end());


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

### 4.5 list
https://blog.csdn.net/abc882715/article/details/78783792
```c++
#include <list>
#include <string>
#include <iostream>
std::list<std::string> strings {"the","cat","sat","on","the","mat"};
//Lists将元素按顺序储存在链表中. 与 向量(vectors)相比, 它允许快速
/*
assign() 给list赋值 
back() 返回最后一个元素 
begin() 返回指向第一个元素的迭代器 
clear() 删除所有元素 
empty() 如果list是空的则返回true 
end() 返回末尾的迭代器 
erase() 删除一个元素 
front() 返回第一个元素 
get_allocator() 返回list的配置器 
insert() 插入一个元素到list中 
max_size() 返回list能容纳的最大元素数量 
merge() 合并两个list 
pop_back() 删除最后一个元素 
pop_front() 删除第一个元素 
push_back() 在list的末尾添加一个元素 
push_front() 在list的头部添加一个元素 
rbegin() 返回指向第一个元素的逆向迭代器 
remove() 从list删除元素 
remove_if() 按指定条件删除元素 
rend() 指向list末尾的逆向迭代器 
resize() 改变list的大小 
reverse() 把list的元素倒转 
size() 返回list中的元素个数 
sort() 给list排序 
splice() 合并两个list 
swap() 交换两个list 
unique() 删除list中重复的元素
*/
```

### 4.6 map
https://blog.csdn.net/shuzfan/article/details/53115922
```c++
#include <iostream>
#include <map>
int main(int argc, char** argv) {
    std::map<std::string, std::string> opt;
    for (int i = 0; i < (argc - 1) / 2; i++) {
        std::string key = argv[1 + i * 2];
        key = key.substr(1, key.length());
        opt.insert(std::pair<std::string, std::string>(key, argv[(i + 1) * 2]));
    }
    std::map<std::string, std::string>::iterator iter;
    for (iter = opt.begin(); iter != opt.end(); iter++) {
        std::cout << iter->first << " : " << iter->second << std::endl;
    }
}

// c++11 以上可以直接{}进行初始化

// 变态级别初始化演示
std::map<int,std::map<std::string,std::vector<int>>> params;
params = {
    {   0,{   {"a",{2,3,4,5}},  {"b",{100,100,75,75}}   }   },
    {   1,{   {"a",{0,1,4,5}},  {"b",{75,75,75,75}}     }   },
};
```

### 4.7 内存泄漏及垃圾回收
当你在写```XXX_Class * pObj = new XXX_Class();```这一行的时候，脑子里面还在默念记得要释放pObj ，记得要释放pObj

#### 4.7.1  什么时候要做垃圾回收？
* 使用new或malloc进行动态分配内存
```c++
//使用new和delete运算符在程序运行期间动态分配与释放内存空间
//new运算符会根据所要求的内存大小在内存中分配足够的空间，并返回所分配内存的指针值，也就是内存地址。
//  数据类型 *指针变量 = new 数据类型(初值);
...
//  数据类型 *指针数组变量 = new 数据类型[元素个数];
double* pvalue = unllptr;
pvalue = new double[20];
delete [] pvalue;


// malloc

// new和malloc的区别 https://blog.csdn.net/qq_34170700/article/details/104999328
```
* new class
```c++


```

#### 4.7.2 如何检测代码中的内存泄漏
* 如果在做重复的操作过程中一直保持稳定增长，那么一定有内存泄露
```bash
ps -aux | grep [your process name]
# 每隔一秒检测一次
n=0;while(true);do pmap -d pid | grep mapped;n=$((n + 1));sleep 1;done
```
* valgrind

#### 4.7.3 智能指针


### 4.8 c++11 特性
#### 4.8.1 std::nothrow
直接new如果失败要抛出异常的，结果就是为了健壮性代码里到处都是try。而c++本身catch得很慢
所以一般健壮的分配方式都用new (nothrow) xxx的(当然也有用malloc等的)，之后判断NULL就ok了。
```c++
book = new (std::nothrow) Book();
if (book == NULL) {
	//do some when fail
}
```
#### 4.8.2 智能指针shared_ptr

## 5 [opencv](https://docs.opencv.org/master/de/d7a/tutorial_table_of_content_core.html)
### 5.1 install
参考:<br>
https://docs.opencv.org/master/d7/d9f/tutorial_linux_install.html<br>
https://blog.csdn.net/weixin_43953829/article/details/96473891<br>
https://zhuanlan.zhihu.com/p/118222087<br>

```bash
# 安装依赖
sudo apt-get install build-essential cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev python-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev liblapacke-dev libxvidcore-dev libx264-dev libatlas-base-dev gfortran ffmpeg

# 整合筛选
sudo apt-get install build-essential cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libdc1394-22-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev liblapacke-dev
libxvidcore-dev libx264-dev libatlas-base-dev gfortran ffmpeg

# 最小化
libjpeg-dev libpng-dev libtiff-dev
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


# 错误解决
# /usr/bin/ld: ../../lib/libopencv_imgcodecs.so.4.4.0: undefined reference to `opj_stream_default_create' 请下载openjpg，源码安装
wget https://codeload.github.com/uclouvain/openjpeg/zip/refs/tags/v2.4.0
unzip v2.4.0
cd openjpeg-2.4.0
mkdir build
cd build
cmake ..
make
sudo make install
# /usr/bin/ld: ../../lib/libopencv_imgcodecs.so.4.4.0: undefined reference to `TIFFReadDirectory@LIBTIFF_4.0' 不要在conda环境下编译

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

#### 5.1.1 常见问题
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
### 5.2 API
#### 5.2.1 pixel
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

#### 5.2.2 Mat
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
##### 5.2.2.1 快速访问并修改Mat中的像素的多种方法
https://blog.csdn.net/xiaowei_cqu/article/details/19839019

#### 5.2.3 打开图片,获取长宽，色彩空间转换，显示，保存
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

#### 5.2.4 resize
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
#### 5.2.5 矩阵运算
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
#### 5.2.6 通道的拆分与合并
```c++
//通道合并：merge()函数,与split()函数是一对相反的操作
// void split(const Mat& src, vector<Mat>& dst);
// void cv::merge(const Mat* mv, size_t count, OutputArray dst);
#include <opencv2/opencv.hpp>
using namespace cv;
 
int main(int argc, char** crgv) {
	//定义一些Mat对象
	Mat imageBlueChannel;
	Mat imageGreenChannel;
	Mat imageRedChannel;
	Mat mergeImage;
	Mat srcImage = imread("1.jpg", 1);
 
	//先通道分离
	std::vector<Mat> channels;
	split(srcImage, channels);//拆分
	imageBlueChannel = channels.at(0);//蓝通道
	imageGreenChannel = channels.at(1);//绿通道
	imageRedChannel = channels.at(2);//红通道
	imshow("蓝通道", imageBlueChannel);
	imshow("绿通道", imageGreenChannel);
	imshow("红通道", imageRedChannel);
	//对拆分的数据进行合并
	merge(channels, mergeImage);//合并
	imshow("合并后的图像", mergeImage);
 
	waitKey(0);
	return 0;
}
```
#### 5.2.7 骚操作
* extract 2D Mat from a 4D Mat
```c++
// from the ssd_mobilenet_object_detection sample   
Mat detectionMat(prob.size[2], prob.size[3], CV_32F, prob.ptr<float>());
```

## 6 [TensorRT](https://developer.nvidia.com/zh-cn/tensorrt)
### 6.1 install
#### 6.1.1 drive and cuda and cudnn
[见linux.md](./linux.md)

#### 6.1.2 TensorRT
* 下载符合要求的https://developer.nvidia.com/nvidia-tensorrt-download
* 安装教程https://docs.nvidia.com/deeplearning/tensorrt/install-guide/index.html#installing-tar
* 解压
```bash
tar -zxvf
```
* 配置环境变量
```bash
vim ~/.bashrc
export LD_LIBRARY_PATH=/path/to/TensorRT-7.2.3.4/lib:$LD_LIBRARY_PATH
export LIBRARY_PATH=/path/to/TensorRT-7.2.3.4/lib::$LIBRARY_PATH
```
* 测试
```bash
cd samples
make -j
cd ../bin
./sample_mnist
```
### 6.2 use

## 7 [libtorch](https://pytorch.org/tutorials/advanced/cpp_frontend.html)

## 8 [openvino](https://github.com/openvinotoolkit/openvino/wiki/BuildingForLinux)
### 8.1 install 
```bash
# 按照官方教程安装

# cmake可选项
cmake -DCMAKE_BUILD_TYPE=Release -DENABLE_MKL_DNN=ON -DENABLE_CLDNN=OFF -DNGRAPH_ONNX_IMPORT_ENABLE=ON -DNGRAPH_DEBUG_ENABLE=ON -DENABLE_PYTHON=ON -DPYTHON_EXECUTABLE=`which python3.7` -DPYTHON_LIBRARY=/home/hypo/anaconda3/envs/openvino/lib/libpython3.7m.so -DPYTHON_INCLUDE_DIR=/home/hypo/anaconda3/envs/openvino/include/python3.7m ..
# 编译
make -j8
# 安装
sudo cmake --install . --prefix /usr/local/openvino
# 安装测试-优化工具
git clone https://github.com/openvinotoolkit/open_model_zoo.git
sudo cmake -E copy_directory ./open_model_zoo/ /usr/local/openvino/deployment_tools/open_model_zoo/

cd /usr/local/openvino/deployment_tools/open_model_zoo/demos

# 转译优化模型 将ONNX模型转换为IR
cd ~/openvino/model-optimizer
conda activate openvino
python3 ~/openvino/model-optimizer/mo.py --input_model <INPUT_MODEL>.onnx

# 下载测试模型
cd open_model_zoo/tools/downloader
./downloader.py --print_all
./downloader.py --name resnet-50-pytorch
./

# 在项目中使用cmake 引入
find_package(InferenceEngine REQUIRED)
target_link_libraries(${PROJECT_NAME} PRIVATE ${InferenceEngine_LIBRARIES})
cmake -DInferenceEngine_DIR=/path/to/openvino/build/ .


```

### 8.2 搭建自己的推理易用库
要求
* 1.一个新的类，使用onnx path初始化
* 2.infer函数
* 3.输出输出既可以的cv::mat 也可以是vector

## 9 c++工程常见问题
### 9.1 gdb调试

### 9.2 bug
### 9.2.1 file format not recognized; treating as linker script
问题说明:软链接失效，进入相应目录查看```ls -l```是否存在相应的软链接
解决办法:重新链接

### 9.2.2 undefined reference to `std::
* undefined reference to 'std::cout'
**问题分析：**
使用gcc 编译c++ 代码时需要链接-lstdc++  ```gcc main.cpp -lstdc++ -o main.o```
**解决办法：**
```bash
# 1.直接连接
gcc main.cpp -lstdc++ -o main.o  # makefile
link_libraries(stdc++)           # cmake
# 2.替换为g++编译
```

### 9.2.3 undefined reference to `Json::Reader::parse或类似的无法调用
* undefined reference to `Json::Value::toStyledString[abi:cxx11]() const'
**问题分析：**
编译库使用了不同版本的gcc或者环境有所改变
**解决办法：**
重新编译该库

### 9.2.4 GLIBCXX_3.4.20' not found
* /lib64/libstdc++.so.6: version `GLIBCXX_3.4.20' not found (required by 
**问题分析：**
手动升级到了gcc版本后新的动态库没有替换旧版本的动态库。
**解决办法：**
```bash
# 检查一下动态库
strings /usr/lib/libstdc++.so.6 | grep GLIBC  # 发现没有符合要求的
# 用新的gcc的libstdc++替换旧的
find /usr -name libstdc++.so*

```

