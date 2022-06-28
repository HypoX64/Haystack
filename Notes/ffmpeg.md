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

vim ~/.bashrc
export LD_LIBRARY_PATH=/usr/local/lib/:$LD_LIBRARY_PATH
source ~/.bashrc


```

### Base
```bash
-vf crop=600:600:600:0 # 剪裁, 输出w,h，开始裁剪的w，h
-s 360x360             # 改变分辨率
-vf scale=iw/2:ih/2    # 分辨率缩小一倍
-filter_complex hstack # 水平拼接两个视频
-filter:a "volume=1.5" # 音量
-ar 48000              # 音频采样率
-vcodec libx264 -crf 18 -pix_fmt yuv420p

-loglevel quiet #有时候需要隐蔽的执行ffmpeg不希望输出任何日志，提示。
PATH=/bin:/usr/bin:/usr/local/bin #指定路径
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
```python
def args2cmd(args):
    cmd = ''
    for arg in args:
        cmd += (arg+' ')
    return cmd

def run(args,mode = 0):

    if mode == 0:
        cmd = args2cmd(args)
        os.system(cmd)

    elif mode == 1:
        '''
        out_string = os.popen(cmd_str).read()
        For chinese path in Windows
        https://blog.csdn.net/weixin_43903378/article/details/91979025
        '''
        cmd = args2cmd(args)
        stream = os.popen(cmd)._stream
        sout = stream.buffer.read().decode(encoding='utf-8')
        return sout

    elif mode == 2:
        cmd = args2cmd(args)
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        sout = p.stdout.readlines()
        return sout

def splice_video(video_paths,video_shape,splice_shape,output_path,fps):
    h,w = video_shape
    o_h_num,o_w_num = splice_shape

    for path in video_paths[:o_h_num*o_w_num]:
        args.append('-i '+path)

    args.append('-filter_complex')
    args.append('"nullsrc=size='+str(w*o_w_num)+'x'+str(h*o_h_num)+' [tmp0];')

    for i in range(o_h_num*o_w_num):
        args.append('[{0:s}:v] setpts=PTS-STARTPTS,scale={1:s}x{2:s} [p{3:s}];'.format(str(i),str(w),str(h),str(i)))

    for x in range(o_h_num):
        for y in range(o_w_num):
            if x == o_h_num-1 and y == o_w_num -1:
                args.append('[tmp{0:d}][p{1:d}] overlay=shortest=1:x={2:d}:y={3:d}"'.format(
                    x*o_h_num+y,x*o_h_num+y,x*w,y*h))
            else:
                args.append('[tmp{0:d}][p{1:d}] overlay=shortest=1:x={2:d}:y={3:d}[tmp{4:d}];'.format(
                    x*o_h_num+y,x*o_h_num+y,x*w,y*h,x*o_h_num+y+1))

    args += [
            '-pix_fmt','yuv420p',
            '-vcodec','libx264',
            '-crf','18',
            output_path,
    ]

    print(args2cmd(args))
    sout = run(args,mode=0)
```