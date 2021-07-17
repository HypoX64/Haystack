### base
```bash
-vf crop=600:600:600:0 # 剪裁, 输出h,w，开始裁剪的h，w
-s 360x360             # 改变分辨率
-filter_complex hstack # 水平拼接两个视频
-filter:a "volume=1.5" 

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