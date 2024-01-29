import argparse
import hashlib
import json
import os
import subprocess
import sys
import time

from PIL import Image
from tqdm import tqdm
from threading import Thread
from multiprocessing import Process,Pool
import multiprocessing as mp

'''
sudo apt update
sudo apt install imagemagick
'''

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

def get_filename_without_extension(file_path):
    file_name_with_ext = os.path.basename(file_path)
    file_name_without_ext = os.path.splitext(file_name_with_ext)[0]
    return file_name_without_ext

def getsize_as_mb(file_path):
    return round(os.path.getsize(file_path)/1024/1024,4)

# ---------------------------------this-------------------------------
def get_image_metadata(file_path):
    with Image.open(file_path) as img:
        info = {
            "path": file_path,
            "format": img.format,
            "mode": img.mode,
            "size": img.size,
            "storage": round(os.path.getsize(file_path)/1024/1024,4), #mb
        }
        info['bpp'] = round(get_bpp(info['size'],info['storage']),4)
        return info

def get_bpp(size, storage):
    # size: (w,h) storage: MB
    return storage*1024*1024*8/size[0]/size[1]

# ---------------------------------begin-------------------------------

parser=argparse.ArgumentParser()
parser.add_argument("--dir",type=str,default='',help="Dir to save 'data'")
parser.add_argument("--y", action='store_true', help='')
parser.add_argument("--no_json", action='store_true', help='do not use json skip')
parser.add_argument("--cover_thr", type=float,default=0.7,help="cover when output_size/input_size < cover_thr")
parser.add_argument("--quality",type=int,default=90, help="")
parser.add_argument("--max_bpp",type=float,default=1.74, help="1.74 -> 6000x4000 -> 5MB")
parser.add_argument("--max_size",type=int,default=3000,help="if image min(h,w) >max_size, resize it to 1/2")
parser.add_argument("--thr_storage",type=int,default=0.2,help="if image storage < thr_storage(mb), skip it")
parser.add_argument("--pool",type=int,default=8, help="")
parser.add_argument("--more",type=str,default='',help="more parser like: -s 1920x1080 -pix_fmt yuv420p")

opt = parser.parse_args()
if opt.dir == '':
    print('Please input parser. -h')
opt.dir = os.path.abspath(opt.dir)
script_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(script_dir,'image.json')
if not os.path.isfile(json_path):
    _data = {'easy_processed':{}}
    with open(json_path,'w') as f:
        json.dump(_data,f,indent=4)
with open(json_path,'r') as f:
    image_processed_infos = json.load(f)


file_paths = Traversal(opt.dir)
img_paths = is_imgs(file_paths)
befor_img_num = len(img_paths)

deal_list = {}
print('Reading image info...')
for path in tqdm(img_paths):
    try:
        md5 = get_md5_from_file(path)
        if md5 in image_processed_infos and not opt.no_json:
            continue
        metadata = get_image_metadata(path)
        if metadata['storage'] < opt.thr_storage:
            image_processed_infos[md5] = metadata
            continue
        if metadata['bpp'] < opt.max_bpp and min(metadata['size']) < opt.max_size:
            image_processed_infos[md5] = metadata
            continue
        deal_list[path] = {
            'size' : '{}x{}'.format(metadata['size'][0],metadata['size'][1]),
            'storage': metadata['storage'],
            'bpp': metadata['bpp'],
            'cmd':['-quality',str(opt.quality)]
        }
        if min(metadata['size']) > opt.max_size:
            deal_list[path]['cmd']+= ['-resize','{}x{}'.format(metadata['size'][0]//2,metadata['size'][1]//2)]
    except:
        print('cannot get image infos from: {}'.format(path) )

write_json(json_path,image_processed_infos)

print('Image need to ecodec:')
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


def process_one(path,deal_infos):
    # convert DSC00533.JPG -resize 6000x4000 -quality 90 output.heic
    # basename = get_filename_without_extension(path)
    tmp_path = os.path.join(os.path.dirname(path),get_filename_without_extension(path)+'_tmpfh349s.heif')
    save_path = tmp_path.replace('_tmpfh349s.heif','.heif')
    args = ['convert','"{}"'.format(path)] + deal_infos['cmd']+ ['"'+tmp_path+'"']
    run(args)
    after_size = getsize_as_mb(tmp_path)
    
    if after_size < deal_infos['storage']*opt.cover_thr:
        os.system('rm "{}"'.format(path))
        os.system('mv "{}" "{}"'.format(tmp_path,save_path))
        data_queue.put(
            {
                'before':deal_infos['storage'],
                'after':after_size,
                'json':{
                    'md5':get_md5_from_file(save_path),
                    'metadata': get_image_metadata(save_path)
                }
            }
        )
    else:
        os.system('rm "{}"'.format(tmp_path))
        data_queue.put(
            {
                'before':deal_infos['storage'],
                'after':deal_infos['storage'],
                'json':{
                    'md5':get_md5_from_file(path),
                    'metadata': get_image_metadata(path)
                }
            }
        )
    

def mycallback(arg):
    '''get the image data and update pbar'''
    pbar.update(1)
    return None

pbar = tqdm(total=len(deal_list))
data_queue = mp.Queue(len(deal_list))

if len(deal_list) > 0:
    pool = Pool(opt.pool)
    for path in deal_list:
        pool.apply_async(process_one, args=(path,deal_list[path],),callback=mycallback)
    pool.close()
    pool.join()

    originalstorage = 0
    finalstorage = 0
    while not data_queue.empty():
        data = data_queue.get()
        image_processed_infos[data['json']['md5']] = data['json']['metadata']
        originalstorage += data['before']
        finalstorage += data['after']

    originalstorage /= 1024.0
    finalstorage /= 1024.0
    write_json(json_path,image_processed_infos)
    print('Original Size:%.3fGB'%originalstorage,
        ' Final Size:%.3fGB'%finalstorage,
        ' Reduce:%.3f'%((originalstorage-finalstorage)/originalstorage*100)+'%')

    after_img_num = len(is_imgs(Traversal(opt.dir)))
    if after_img_num != befor_img_num:
        print('after_img_num != befor_img_num, please check')
        print('befor_img_num:',befor_img_num)
        print('after_img_num:',after_img_num)
