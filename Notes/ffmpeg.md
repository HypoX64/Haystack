[toc]
### 编译
```bash
yum install nasm
git clone https://code.videolan.org/videolan/x264.git
git clone https://bitbucket.org/multicoreware/x265_git.git

cd x264
./configure --enable-static --enable-shared
make
make install

cd x265_git
cd build/linux
sh make-Makefiles.bash
make
make install

vim ~/.bashrc
export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:/usr/local/lib/pkgconfig
source ~/.bashrc

wget https://ffmpeg.org/releases/ffmpeg-4.4.1.tar.gz
tar zxvf ffmpeg-4.4.1.tar.gz
cd ffmpeg-4.4.1

./configure --enable-shared --enable-gpl --enable-libx264 --enable-libx265 --prefix=/usr/local

make -j8
make install 
# ffmpeg和ffprobe安装在/usr/local/bin，最好去掉连接到full的预编译版本


# 这里.so没有帮忙拷贝 很坑(搞错了，不好意，嘿嘿，不用理)
# mkdir lib
# scp -r */*.so* ./lib
# ls lib


```

### Base
```bash
-vf crop=600:600:600:0 # 剪裁, 输出w,h，开始裁剪的w，h
-s 360x360             # 改变分辨率
-filter_complex hstack # 水平拼接两个视频
-filter:a "volume=1.5" # 音量
-ar 48000              # 音频采样率
-vcodec libx264 -crf 18 -pix_fmt yuv420p


```

### 统计总帧数
```bash
ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames -of default=nokey=1:noprint_wrappers=1 input.mp4
```

### 图片转视频
```
ffmpeg -y -r 60 -i %05d.png -crf 18 -pix_fmt yuv420p out.mp4
```

### 通过pipe推流到python
```bash

```

### wav与pcm的转换
```bash
# wav 2 pcm
ffmpeg -i mix_new_silent.wav -f s16le -ar 16000 -ac 1 -acodec pcm_s16le output.pcm
# pcm 2 wav
ffmpeg -ac 1 -ar 16000 -f s16le -i .\output.pcm test.wav
```


### 多宫格效果
```bash
ffmpeg -i 1.mp4 -i 2.mp4 -i 3.mp4 -i 4.mp4 
-filter_complex "nullsrc=size=1440x360 [base];
[0:v] setpts=PTS-STARTPTS,scale=360x360 [p0];
[1:v] setpts=PTS-STARTPTS, scale=360x360 [p1];
[2:v] setpts=PTS-STARTPTS, scale=360x360 [p2];
[3:v] setpts=PTS-STARTPTS, scale=360x360 [p3];
[base][p0] overlay=shortest=1[tmp1];
[tmp1][p1] overlay=shortest=1:x=360 [tmp2];
[tmp2][p2] overlay=shortest=1:x=720 [tmp3];
[tmp3][p3] overlay=shortest=1:x=1080;"
 -c:v libx264 out.mp4
```

```bash
ffmpeg -re -i 1.mp4 -re -i 2.mp4 -re -i 3.mp4 -re -i 4.mp4 -filter_complex "nullsrc=size=1440x360 [base]; [0:v] setpts=PTS-STARTPTS,scale=360x360 [p0];[1:v] setpts=PTS-STARTPTS, scale=360x360 [p1];[2:v] setpts=PTS-STARTPTS, scale=360x360 [p2];[3:v] setpts=PTS-STARTPTS, scale=360x360 [p3];[base][p0] overlay=shortest=1[tmp1];[tmp1][p1] overlay=shortest=1:x=360 [tmp2];[tmp2][p2] overlay=shortest=1:x=720 [tmp3];[tmp3][p3] overlay=shortest=1:x=1080" -c:v libx264 out.mp4
```