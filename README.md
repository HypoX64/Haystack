## Haystack
Gadgets and notes for learning and research
### System
* [monitor_linux.py](./System/monitor_linux.py)
A simple Deep Learning Server performance monitor. Written by python without any dependencies.
```bash
(base) hypo@lthpc:~$ python monitor_linux.py
Cpu   Temp: 48.0C | Freq: 2499.9MHz
Util: 85.6%  [###########################################-------]

Memory   Mem: 34354MB/64301MB | Swap: 0MB/62498MB
Mem: 53.0% [#############------------] Swap: 0.0% [-------------------------]

Gpu0: TITAN V   Temp: 45.0C | Power: 28w/250w | Mem: 950MB/12066MB | Fan: 31%
Util:0.0% [-------------------------]   Mem:7.9% [##-----------------------]

Gpu1: TITAN V   Temp: 46.0C | Power: 28w/250w | Mem: 950MB/12066MB | Fan: 31%
Util:0.0% [-------------------------]   Mem:7.9% [##-----------------------]

Network    ↑ all:10.2GB ↓ all:173.8GB     ↑ :147.6Kb/s ↓ :6000.5Kb/s

Filesystem           Mounted on           Used/Total           Used%
udev                 /dev                 0/32G                0%             
/dev/sda7            /                    9.9G/143G            8%             
tmpfs                /dev/shm             0/32G                0%             
tmpfs                /sys/fs/cgroup       0/32G                0%             
/dev/sdb1            /home                103G/2.7T            4%             
/dev/sdc1            /media/usb           3.6T/3.7T            99%    
```

### CV
* [find_face.py](./CV/find_face.py)
FInd face in images, then save them.
Depend on face_recognition, opencv-python.
```bash
(pytorch) hypo@hypo-7820:/media/hypo/OS/MyProject/Haystack/CV$ python find_face.py
filedir:'/media/hypo/OS/MyProject/BaiduImageSpider/download/Angelababy' 
outname:star
min_face_size(defult=256):256
cpu_workers(defult=4):4
Find picture: 504
Begining......
  Ok:500 Face:50  99.21%[##############################]  Used/All:143s/144s 
Finished! Finall find face: 50  Cost time: 145 s
```
### Notes
* [linux.md](./Notes/linux.md)
* [python.md](./Notes/python.md)
* [github.md](./Notes/github.md)
* [Sublime-settings.md](./Notes/Sublime-settings.md)