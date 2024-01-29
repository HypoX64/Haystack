import argparse
import hashlib
import json
import os
import subprocess
import sys
import time

# ffmpeg 3.4.6
from tqdm import tqdm

# ---------------------------------util-------------------------------

def makedirs(path):
    if os.path.isdir(path):
        pass
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
    if ext in ['.jpg','.png','.jpeg','.bmp','.heif','.webp','.tiff','.tif']:
        return True
    else:
        return False

def is_video(path):
    ext = os.path.splitext(path)[1]
    ext = ext.lower()
    if ext in ['.mp4','.flv','.avi','.mov','.mkv','.wmv','.rmvb','.mts','.3gp','.ts']:
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
        # print(cmd)
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

def get_md5_from_file(path,blocksize=1024*1024):
    try:
        f = open(path, "rb")
        f.seek(0)
        data = f.read(blocksize)
        md5_value = hashlib.md5(data).hexdigest()
    except:
        md5_value = '0'
    return md5_value

def write_json(json_path,dict_data):
    with open(json_path,'w') as f:
        json.dump(dict_data,f,indent=4,ensure_ascii=False)

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
parser.add_argument("--no_json", action='store_true', help='do not use json skip')
parser.add_argument("--cover_thr", type=float,default=0.7,help="cover when output_size/input_size < cover_thr")
parser.add_argument("--y", action='store_true', help='')
parser.add_argument("--q", action='store_true', help='')
parser.add_argument("--bin", type=str, default='',help='where is the ffmpeg /usr/local/bin/ /bin:/usr/bin:/usr/local/bin')
parser.add_argument("--max_rate_l1",type=float,default=0.002,help="max_bit_rate  0.0020 -> 1080P 4147kbps")
parser.add_argument("--max_rate_l2",type=float,default=0.005,help="max_bit_rate  0.0050 -> 1080P 10368kbps")

parser.add_argument("--max_size",type=int,default=9999,help="if video min(h,w) >max_size, resize it to 1/2")

parser.add_argument("--r",type=str,default='',help="")
parser.add_argument("--preset",type=str,default='veryfast',help="")
parser.add_argument("--crf",type=str,default='23',help="")
parser.add_argument("--vcodec",type=str,default='libx265',help="libx265 | libx264 | av1")
parser.add_argument("--acodec",type=str,default='aac',help="aac | copy")

parser.add_argument("--more",type=str,default='',help="more parser like: -s 1920x1080 -pix_fmt yuv420p")

'''
 -f mp4
 -c:v libx265 -preset veryfast -crf 25.0
 -c:a libfdk_aac
 -sn -tune:v none -b:a 192k
'''
opt = parser.parse_args()
if opt.dir == '':
    print('Please input parser. -h')
opt.dir = os.path.abspath(opt.dir)
script_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(script_dir,'video.json')
if not os.path.isfile(json_path):
    _data = {'easy_processed':{}}
    with open(json_path,'w') as f:
        json.dump(_data,f,indent=4)
with open(json_path,'r') as f:
    video_processed_infos = json.load(f)

l2_codec_type = ['h265','hevc','av1']
file_paths = Traversal(opt.dir)
video_paths = is_videos(file_paths)
befor_video_num = len(video_paths)
originalstorage = 0
finalstorage = 0

deal_list = {}
print('Reading video info...')
for path in tqdm(video_paths):
    if opt.no_json or path not in video_processed_infos['easy_processed']:
        md5_value = get_md5_from_file(path)
        if opt.no_json or md5_value not in video_processed_infos:
            try:
                fps,duration,height,width,bit_rate,codec_name = get_video_infos(path)
            except:
                print('failed to get infos:',path)
                continue
            isresize = False
            if min(height,width)>opt.max_size:
                isresize = True
            storage = round(os.path.getsize(path)/(1024*1024*1024),3)
            
            is_need_deal = False
            if (codec_name not in l2_codec_type) and (bit_rate>height*width*opt.max_rate_l1) and storage>0.01:
                deal_list[path] = {'fps':round(fps,2),'duration':round(duration,1),'size':str(width)+'x'+str(height),
                                'bit_rate':str(bit_rate)+'kbps','codec':codec_name,'need_resize':isresize,'storage':storage}
                is_need_deal = True
        
            if  codec_name in l2_codec_type and bit_rate>height*width*opt.max_rate_l2 and storage>0.01:
                deal_list[path] = {'fps':round(fps,2),'duration':round(duration,1),'size':str(width)+'x'+str(height),
                                'bit_rate':str(bit_rate)+'kbps','codec':codec_name,'need_resize':isresize,'storage':storage}
                is_need_deal = True
            
            if not is_need_deal:
                video_processed_infos[md5_value] = {
                    'name':os.path.basename(path),
                    'fps':round(fps,2),
                    'duration':round(duration,1),
                    'size':str(width)+'x'+str(height),
                    'bit_rate':str(bit_rate)+'kbps',
                    'codec_name':codec_name,
                    'storage':storage
                }
                video_processed_infos['easy_processed'][path]=1
write_json(json_path,video_processed_infos)

print('Video need to ecodec:')
cnt = 1
for k in deal_list:
    print('%05d'%cnt,k,deal_list[k])
    cnt+=1

if not opt.y:
    print('Do you want to ecodec?  Y/N')
    choose = input().strip()
    choose = str(choose.replace("'","")).lower()
    if choose in ['n','no','none']:
        print('Exit.')
        sys.exit(0)

print('Begin ecodec...') 
# makedirs(opt.output)

for path in tqdm(deal_list):
    originalstorage += (os.path.getsize(path)/(1024*1024*1024))
    if path[0] in ['/','.']:
        save_path = os.path.join(opt.output,path[1:])
    elif path[0] in ['..']:
        save_path = os.path.join(opt.output,path[2:])
    else:
        save_path = os.path.join(opt.output,path)

    filepath,tempfilename = os.path.split(save_path)
    filename,extension = os.path.splitext(tempfilename)

    save_path = os.path.join(filepath,filename+'.mp4')  

    deal_list[path]['save_path'] = save_path
    makedirs(os.path.split(save_path)[0])
    ffmpeg = 'ffmpeg -y -vsync 0'
    if opt.q:
        ffmpeg += ' -loglevel quiet'
    
    if opt.bin != '':
        ffmpeg = 'PATH='+opt.bin+' && '+ffmpeg
    args = [ffmpeg, '-i', '"'+path+'"',
            '-vcodec',opt.vcodec,
            '-crf',opt.crf,
            '-acodec',opt.acodec,
            ]
    if opt.vcodec in ['libx265','libx264']:
        args+=['-preset',opt.preset]
    args+=['-vsync','2']
    if opt.more != '':
        args+=[opt.more]
    if (deal_list[path]['need_resize']):
        args+=['-vf','scale=iw/2:ih/2']
    if opt.acodec != 'copy':
        args+=['-b:a','192k']
    if opt.r != '':
        args+=['-r',opt.r]
    args+=['"'+save_path+'"']
    if not opt.q:
        print(args)
    run_flag = True
    if os.path.exists(save_path):
        try:
            fps,duration,height,width,bit_rate,codec_name = get_video_infos(path)
        except:
            duration = 0
            print('failed to get infos:',path)
            continue
        if abs(deal_list[path]['duration']-duration)<1 :
            print('The video has been processed, skip...')
            run_flag = False
    if run_flag:    
        run(args)
    storage = round(os.path.getsize(save_path)/(1024*1024*1024),3)
    deal_list[path]['out_storage'] = storage
    finalstorage += storage
    time.sleep(1)
    
    # mv
    if opt.cover:
        new_path = deal_list[path]['save_path']
        try:
            if deal_list[path]['out_storage']/deal_list[path]['storage']<opt.cover_thr:
                # update json
                md5_value = get_md5_from_file(new_path)
                try:
                    fps,duration,height,width,bit_rate,codec_name = get_video_infos(new_path)
                except:
                    print('failed to get infos:',new_path)
                video_processed_infos[md5_value] = {
                    'name':os.path.basename(new_path),
                    'fps':round(fps,2),
                    'duration':round(duration,1),
                    'size':str(width)+'x'+str(height),
                    'bit_rate':str(bit_rate)+'kbps',
                    'codec_name':codec_name,
                    'storage':storage
                }
                video_processed_infos['easy_processed'][os.path.join(os.path.split(path)[0],os.path.basename(new_path))]=1
                
                # move and del
                args = ['rm -r ','"'+path+'"']
                run(args)
                args = ['mv','"'+new_path+'"','"'+os.path.split(path)[0]+'"']
                run(args)
            else:
                args = ['rm -r ','"'+new_path+'"']
                run(args)
        except:
            pass

write_json(json_path,video_processed_infos)

after_video_num = len(is_videos(Traversal(opt.dir)))
if after_video_num != befor_video_num:
    print('after_video_num != befor_video_num, please check')
    print('befor_video_num:',befor_video_num)
    print('after_video_num:',after_video_num)

print('Original Size:%.2fGB'%originalstorage,
      ' Final Size:%.2fGB'%finalstorage,
      ' Reduce:%.2f'%((originalstorage-finalstorage)/originalstorage*100)+'%')
