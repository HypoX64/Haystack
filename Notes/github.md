[TOC]

# Git
## Base
```shell
 git pull origin master                  # 将远程仓库里面的项目拉下来
git rm -r --cached target              # 删除target文件夹
git add *  ###如有新添加的文件执行此行，添加所有的文件
git commit -m "输入你本次提交的文字"
git push -u origin master
```
## 合并仓库
大致思路是伪造远程的repo1仓库为repo2的一个分支，然后合并进来；
若是文件有冲突、或要建立子目录，建议在repo1中先解决，再进行如上操作。
example:
目前开发是2个仓库，线上仓库online_a（对应的branch分支为online）,测试环境online_b（对应的branch分支为demo），测试环境需要时刻保持onine_a上的最新稳定稳定代码同步过来。

```shell
#1：在测试仓库onine_b 上执行：测试仓库添加远程生产仓库(切换到自己的测试仓库下执行以下命令，比如我的当期测试online_b.git)
git remote add online_a git@github.com:fantasy/online_a.git#将online_a作为远程仓库，添加到online_b中，设置别名为online_a(自定义，这里我是为了方便区分仓库名)

#2从远程仓库下载，这时我们弄个新的
git fetch online_a #从online_a仓库中抓取数据到本仓库,注意这里是上面设置的别名

#3.将online_a仓库抓去的online分支作为新分支checkout到本地，新分支名设定为online_repo1
git checkout -b online_repo1 online-a/online  //注意这里也是别名online_a

#4.切换回本地测试的online_b的demo分支
git checkout demo

#5.将online_repo1合并入demo分支
git merge online_repo1
```

# Markdown
## 表格
|      |      |      |
| ---- | ---- | ---- |
|      |      |      |
|      |      |      |
|      |      |      |

## 标题
```markdown
大标题
====
中标题
-------
# 一级标题
## 二级标题
### 三级标题
#### 四级标题
##### 五级标题
###### 六级标题
```
## 列表
插入圆点符号：编辑的时候使用的是星号 *，星号后面要有一个空格，否则为普通星号
* 列表一
* 列表二
* 列表三
二级圆点、三级圆点：多加一个Tab，即第二行一个Tab，第三行两个Tab

* 列表一
    * 列表二
        *列表三

## 缩进
>缩进一
>>缩进二
>>>缩进三
>>>>缩进四
>>>>
>>>>>缩进五


## 插入链接图片
[百度](http://baidu.com)
* 插入网络图片：![](网络图片链接地址)，即叹号!+方括号[]+括号()，如果不加叹号!就会变成普通文本，方括号里可以加入一些 标识性的信息
![baidu](http://www.baidu.com/img/bdlogo.gif "百度logo")  
<img src=http://www.baidu.com/img/bdlogo.gif  style="zoom:50%">

* 插入GITHub仓库里的图片：![](图片链接地址)，即叹号!+方括号[]+括号()，URL写法：http://github.com/自己的用户名/项目名/raw/分支名/存放图片的文件夹/文件夹里的图片名字

* 给图片加上超链接：即点击一个图片进入指定网页，方括号里写自己起的标识名称，上下两行标识要一致。
[![baidu]](http://baidu.com)  
[baidu]:http://www.baidu.com/img/bdlogo.gif "百度Logo"<br>
* 图片居中
<div align="center">    
<img src="http://www.baidu.com/img/bdlogo.gif " alt="image" style="zoom:50%;" />
</div>
## 插入代码片段
插入代码片段：在代码上下行用```标记，注意`符号是tab键上面那个，要实现语法高亮，则在```后面加上编程语言的名称

复制代码
```Java
public static void main(String[] args){}
```

```javascript
document.getElementById("ts").innerHTML="Hello"
```

## 其他
复制代码
换行：使用标签<br>

单行文本：前面使用两个Tab

多行文本:每行行首加两个Tab

部分文字高亮：使用``包围，这个符号不是单引号，而是Tab上方，数字1左边那个按键的符号

文字超链接格式：[要显示的文字](链接的地址"鼠标悬停显示")，在URL之后用双引号括起来一个字符串，即鼠标悬停显示的文本，可不写
