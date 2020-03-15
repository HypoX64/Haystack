[TOC]
### 安装显卡驱动
```bash
#卸载旧的驱动
sudo apt-get purge nvidia*
sudo apt-get autoremove #这个命令有时候不用也可以
#
sudo add-apt-repository ppa:graphics-drivers/ppa
sudo apt update
ubuntu-drivers devices
sudo apt install nvidia-430
```
### 挂载U盘
```bash
root@lthpc:/home/hypo# fdisk -l
...
Device     Start        End    Sectors  Size Type
/dev/sdc1   2048 7813967871 7813965824  3.7T Microsoft basic data
root@lthpc:/home/hypo# cd /media  
root@lthpc:/media# mkdir usb
root@lthpc:/media# mount -t ntfs-3g /dev/sdc1 /media/usb 

#卸载挂载点
$ umount /dev/hda2
$ umount /usr
#参数可以是设备文件或安装点
```
### linux应用设置
* 百度盘
```bash
# 无法登录
rm -rf  ~/baidunetdisk #这个蛇皮的bug不知道啥时候才能修复
```
* goldendict
```bash
# 安装
sudo apt install goldendict
sudo apt install goldendict gawk
# 添加谷歌翻译
git clone https://github.com/soimort/translate-shell
cd translate-shell/
make
sudo make install
```
打开GoldenDict，【编辑】-【词典】-【词典来源】-【程序】，点击【添加】，勾上【已启用】，填写【类型】Html 和【名称】Google，在【命令行】中输入
```
trans -e google -s auto -t zh-CN -show-original y -show-original-phonetics n -show-translation y -no-ansi -show-translation-phonetics n -show-prompt-message n -show-languages y -show-original-dictionary n -show-dictionary n -show-alternatives n ''%GDWORD%''
```
### shell 中运行基本应用
```bash
nautilus #文件管理器
firefox #火狐浏览器
```
### 批量杀死应用
```bash
ps aux|grep python|grep -v grep|cut -c 9-15|xargs kill -15
# 管道符“|”用来隔开两个命令，管道符左边命令的输出会作为管道符右边命令的输入。下面说说用管道符联接起来的 
#几个命令： 
#“ps aux”是linux 里查看所有进程的命令。这时检索出的进程将作为下一条命令“grep python”的输入。 
#“grep python”的输出结果是，所有含有关键字“python”的进程，这是python程序
#“grep -v grep”是在列出的进程中去除含有关键字“grep”的进程。 
#“cut -c 9-15”是截取输入行的第9个字符到第15个字符，而这正好是进程号PID。 
#“xargs kill -15”中的xargs命令是用来把前面命令的输出结果（PID）作为“kill -15”命令的参数，并执行该令。 
#“kill -15”会正常退出指定进程，-9强行杀掉
```
### 常用系统命令
* 删除文件
```bash
rm -rf yourdir
#-r 就是向下递归，不管有多少级目录，一并删除
#-f 就是直接强行删除，不作任何提示的意思
```
* cp
```bash
cp [options] <source file or directory> <target file or directory>
# or
cp [options] source1 source2 source3 …. directory
#example
cp -rvf dir1 dir2 #复制文件夹dir1到dir2，显示进度
cp -rf dir1 dir #复制文件夹dir1到dir2，不显示进度
#-a 保留链接和文件属性，递归拷贝目录，相当于下面的d、p、r三个选项组合。
#-d 拷贝时保留链接。
#-f 删除已经存在目标文件而不提示。
#-i 覆盖目标文件前将给出确认提示，属交互式拷贝。
#-p 复制源文件内容后，还将把其修改时间和访问权限也复制到新文件中。
#-r 若源文件是一目录文件，此时cp将递归复制该目录下所有的子目录和文件。当然，目标文件必须为一个目录名。
#-l 不作拷贝，只是链接文件。
#-s 复制成符号连结文件 (symbolic link)，亦即『快捷方式』档案；
#-u 若 destination 比 source 旧才更新 destination。
```
* deb
```bash
sudo apt-get install -f #解决依赖关系
dpkg -i <package.deb> #安装一个 Debian 软件包，如你手动下载的文件。
dpkg -c <package.deb> #列出 <package.deb> 的内容。
dpkg -I <package.deb> #从 <package.deb> 中提取包裹信息。
dpkg -r <package> #移除一个已安装的包裹。
dpkg -P <package> #完全清除一个已安装的包裹。和 remove 不同的是，remove 只是删掉数据和可执行文件，purge 另外还删除所有的配制文件。
dpkg -L <package> #列出 <package> 安装的所有文件清单。同时请看 dpkg -c 来检查一个 .deb 文件的内容。
dpkg -s <package> #显示已安装包裹的信息。同时请看 apt-cache 显示 Debian 存档中的包裹信息，以及 dpkg -I 来显示从一个 .deb 文件中提取的包裹信息。
dpkg-reconfigure <package> #重新配制一个已经安装的包裹，如果它使用的是 debconf (debconf 为包裹安装提供了一个统一的配制界面)。
```
### 调整CPU性能模式
```bash
sudo apt-get install cpufrequtils
cpufreq-info
sudo cpufreq-set -g performance
##修改默认
sudo apt-get install sysfsutils
sudo gedit  /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
```
### 添加或禁用开机启动项
```bash
#禁用开机启动项
$ systemctl list-unit-files --type=service|grep enabled #查看开机启动的服务
$ sudo systemctl disable apache2.service #禁用掉该服务
#添加开机启动项
$ systemctl list-unit-files --type=service|grep team
teamviewerd.service                        enabled    
$ sudo systemctl enable teamviewerd.service
```
### 压缩解压
```bash
tar xvf filename.tar #.tar 解包 
tar cvf filename.tar dirname #.tar 打包 
gunzip filename.gz #.gz 解压1 
gzip -d filename.gz #.gz 解压2 
gzip filename #.gz 压缩 
tar zxvf filename.tar.gz #.tar.gz 和 .tgz 解压 
tar zcvf filename.tar.gz dirname #.tar.gz 和 .tgz 压缩 
unzip filename.zip #.zip 解压 
zip filename.zip dirname #.zip 压缩 
rar x filename.rar #.rar 解压 
rar a filename.rar dirname #.rar 压缩 

#.tar.gz 和 .tgz   多线程压缩解压
sudo apt install pigz
#压缩
tar cvf - test.txt | pigz > test.tar.gz
#解压
tar -I pigz -xvf /path/to/archive.tar.gz -C /where/to/unpack/it/
```
### ssh
* install
```bash
sudo apt-get install openssh-client 
sudo apt-get install openssh-server
```
* start
```bash
ps -e | grep ssh
sudo /etc/init.d/ssh start
```
* ip
```bash
ifconfig
```
* login
```bash
ssh hypo@192.168.0.1
ssh -X hypo@192.168.0.1  #GUI
```
* change port
```bash
ssh -p 1234 hypo@192.168.0.1
```
* exit
```bash
'Ctrl+D'
#or
exit
```
* ssh-keygen
```bash
ssh-keygen -t rsa
ssh-copy-id hypo@192.168.0.1
```
* run code
```bash
nohup python3 a.py &
```
* 远程启动火狐(需要在图形模式下)
```bash
firefox &
```
* transmit files
```bash
#压缩+解压流传输 把本地的文件复制到远程主机上
tar -c './dir' |pigz |ssh hypo@172.31.73.116 "gzip -d|tar -xC /home/hypo/MyProject"
tar -c './DeepMosaics' |pigz |ssh hypo@172.30.194.156 "gzip -d|tar -xC /media/hypo/Project/MyProject/DeepMosaics"

#把远程的文件复制到本地
scp root@www.test.com:/val/test/test.tar.gz /val/test/test.tar.gz
#把本地的文件复制到远程主机上
scp /val/test.tar.gz root@www.test.com:/val/test.tar.gz
#把远程的目录复制到本地
scp -r root@www.test.com:/val/test/ /val/test/

```
