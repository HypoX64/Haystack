import os,json
import subprocess
import argparse
import sys
# ffmpeg 3.4.6
from tqdm import tqdm

# ---------------------------------util-------------------------------

def makedirs(path):
    if os.path.isdir(path):
        print(path,'existed')
    else:
        os.makedirs(path)
        print('makedir:',path)

def Traversal(filedir):
    file_list=[]
    for root,dirs,files in os.walk(filedir): 
        for file in files:
            file_list.append(os.path.join(root,file)) 
        for dir in dirs:
            Traversal(dir)
    return file_list

def is_img(path):
    ext = os.path.splitext(path)[1]
    ext = ext.lower()
    if ext in ['.jpg','.png','.jpeg','.bmp']:
        return True
    else:
        return False

def is_video(path):
    ext = os.path.splitext(path)[1]
    ext = ext.lower()
    if ext in ['.mp4','.flv','.avi','.mov','.mkv','.wmv','.rmvb','.mts']:
        return True
    else:
        return False

def is_imgs(paths):
    tmp = []
    for path in paths:
        if is_img(path):
            tmp.append(path)
    return tmp

def is_videos(paths):
    tmp = []
    for path in paths:
        if is_video(path):
            tmp.append(path)
    return tmp  


def args2cmd(args):
    cmd = ''
    for arg in args:
        cmd += (arg+' ')
    return cmd

def run(args,mode = 0):

    if mode == 0:
        cmd = args2cmd(args)
        print(cmd)
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


# ---------------------------------ffmpeg-------------------------------

def get_video_infos(videopath):
    args =  ['ffprobe -v quiet -print_format json -show_format -show_streams', '-i', '"'+videopath+'"']
    out_string = run(args,mode=1)
    infos = json.loads(out_string)
    try:
        fps = eval(infos['streams'][0]['avg_frame_rate'])
        width = int(infos['streams'][0]['width'])
        height = int(infos['streams'][0]['height'])
        codec_name = infos['streams'][0]['codec_name'] #  h264 hevc
    except Exception as e:
        fps = eval(infos['streams'][1]['r_frame_rate'])
        width = int(infos['streams'][1]['width'])
        height = int(infos['streams'][1]['height'])
        codec_name = infos['streams'][1]['codec_name']

    duration = float(infos['format']['duration'])
    bit_rate = int(infos['format']['bit_rate'])//1024

    return fps,duration,height,width,bit_rate,codec_name


parser=argparse.ArgumentParser()
parser.add_argument("--dir",type=str,default='',help="Dir to save 'data'")
parser.add_argument("--output",type=str,default='./tmp',help="")
parser.add_argument("--cover", action='store_true', help='!!!Overwrites the current file!!!')
parser.add_argument("--bin", action='store_true', help='use /usr/local/bin/ffmpeg')
parser.add_argument("--max_rate_l1",type=float,default=0.0012,help="max_bit_rate  0.0012 -> 1080P 2500kbps")
parser.add_argument("--max_rate_l2",type=int,default=0.0030,help="max_bit_rate  0.0012 -> 1080P 6800kbps")

parser.add_argument("--r",type=str,default='',help="")
parser.add_argument("--crf",type=str,default='23',help="")
parser.add_argument("--vcodec",type=str,default='libx265',help="libx265 | libx264 | av1")
parser.add_argument("--acodec",type=str,default='aac',help="aac | copy")

'''
 -f mp4
 -c:v libx265 -preset veryfast -crf 25.0
 -c:a libfdk_aac
 -sn -tune:v none -b:a 192k
'''
opt = parser.parse_args()
if opt.dir == '':
    print('Please input parser. -h')

l2_codec_type = ['h265','hevc','av1']
file_paths = Traversal(opt.dir)
video_paths = is_videos(file_paths)

deal_list = {}
for path in video_paths:
    fps,duration,height,width,bit_rate,codec_name = get_video_infos(path)
    if (codec_name not in l2_codec_type) and (bit_rate>height*width*opt.max_rate_l1):
        deal_list[path] = {'fps':round(fps,2),'duration':round(duration,1),'size':str(width)+'x'+str(height),
                           'bit_rate':str(bit_rate)+'kbps','codec':codec_name}
 
    if  codec_name in l2_codec_type and bit_rate>height*width*opt.max_rate_l2:
        deal_list[path] = {'fps':round(fps,2),'duration':round(duration,1),'size':str(width)+'x'+str(height),
                           'bit_rate':str(bit_rate)+'kbps','codec':codec_name}
 
print('Video need to ecodec:')
cnt = 1
for k in deal_list:
    print('%05d'%cnt,k,deal_list[k])
    cnt+=1


print('Do you want to ecodec?  Y/N')
choose = input().strip()
choose = str(choose.replace("'","")).lower()
if choose in ['n','no','none']:
    print('Exit.')
    sys.exit(0)

print('Begin ecodec...') 
# makedirs(opt.output)
for path in tqdm(deal_list):
    if path[0] in ['/','.']:
        save_path = os.path.join(opt.output,path[1:])
    elif path[0] in ['..']:
        save_path = os.path.join(opt.output,path[2:])
    else:
        save_path = os.path.join(opt.output,path)
    deal_list[path]['save_path'] = save_path
    makedirs(os.path.split(save_path)[0])
    ffmpeg = 'ffmpeg -y'
    if opt.bin:
        ffmpeg = 'PATH=/bin:/usr/bin:/usr/local/bin && '+ffmpeg
    args = [ffmpeg, '-i', '"'+path+'"',
            '-vcodec',opt.vcodec,
            '-crf',opt.crf,
            '-acodec',opt.acodec,
            ]
    if opt.vcodec in ['libx265','libx264']:
        args+=['-preset','veryfast']
    if opt.acodec != 'copy':
        args+=['-b:a','192k']
    if opt.r != '':
        args+=['-r',opt.r]
    args+=['"'+save_path+'"']
    print(args)
    run(args)

if opt.cover:
    print('Overwrite the origin video...')
    for path in deal_list:
        args = ['mv',deal_list[path]['save_path'],path]
        run(args)
    os.system('rm -r '+opt.output)
