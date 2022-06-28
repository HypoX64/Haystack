import os
import sys
import json
import time
import argparse
from tqdm import tqdm

def args2cmd(args):
    cmd = ''
    for arg in args:
        cmd += (arg+' ')
    return cmd


parser=argparse.ArgumentParser()
parser.add_argument("--dir",type=str,default='/mnt/c/Users/hypo/Videos/bilibili',help="Dir to save 'data'")
parser.add_argument("--output",type=str,default='bilibili_convert',help="")
parser.add_argument("--up_fold", action='store_true', help='')
parser.add_argument("--bin", type=str, default='',help='where is the ffmpeg /usr/local/bin/ /bin:/usr/bin:/usr/local/bin')

opt = parser.parse_args()
if opt.dir == '':
    print('Please input parser. -h')


convert_infos = {}
bads = []

opt.output = os.path.join(os.path.split(opt.dir)[0],opt.output)
if not os.path.isdir(opt.output):
    os.makedirs(opt.output)
# print(opt.output)
# if opt.up_fold:
up_names = os.listdir(opt.dir)


# check all videos and gei infos
for up in up_names:
    up_path = os.path.join(opt.dir,up)
    if not os.path.isdir(os.path.join(opt.output,up)):
        os.makedirs(os.path.join(opt.output,up))
    video_ids = os.listdir(up_path)
    for video in video_ids:
        cover_path = os.path.join(opt.dir,up,video,'cover.jpg')
        info_path = os.path.join(opt.dir,up,video,'info.json')
        if not (os.path.isfile(cover_path) and os.path.isfile(info_path)):
            bads.append(os.path.join(opt.dir,up,video))
            continue

        f = open(info_path, 'r')
        txt = f.read()
        f.close()
        try:
            title = json.loads(txt)['Title']
        except:
            bads.append(os.path.join(opt.dir,up,video))
            continue

        video_dir = os.path.join(opt.dir,up,video)
        convert_infos[video_dir] = {}
        convert_infos[video_dir]['up'] = up
        convert_infos[video_dir]['cover'] = cover_path
        convert_infos[video_dir]['title'] = title
        convert_infos[video_dir]['id'] = video
        convert_infos[video_dir]['p'] = []

        # 分P
        ps = os.listdir(video_dir)
        for p in ps:
            p_dir = os.path.join(video_dir,p)
            if os.path.isdir(p_dir):
                if not os.path.join(p_dir,'info.json'):
                    bads.append(os.path.join(opt.dir,up,video))
                    break
                f = open(os.path.join(p_dir,'info.json'), 'r')
                txt = f.read()
                f.close()
                p_name = json.loads(txt)['EpisodeTitle']
                if os.path.getsize(os.path.join(p_dir,'video.m4s'))<1024 or os.path.getsize(os.path.join(p_dir,'audio.m4s'))<1024 :
                    bads.append(os.path.join(opt.dir,up,video))
                    break
                convert_infos[video_dir]['p'].append({'video':os.path.join(p_dir,'video.m4s'),
                                           'audio':os.path.join(p_dir,'audio.m4s'),
                                           'p_name':p_name}) 


# print bad video
print('--------------------download error--------------------')
for bad in bads:print(bad)

outs = os.listdir(opt.output)
# convert
print('--------------------convert--------------------')
for video in tqdm(convert_infos):
    # print(video,convert_infos[video])
    # break
    for cnt,p in enumerate(convert_infos[video]['p']):
        tmp_path = os.path.join(opt.output,convert_infos[video]['up'],'tmp.mp4')
        out_path = os.path.join(opt.output,convert_infos[video]['up'],convert_infos[video]['up']+'_'+convert_infos[video]['id']+'_'+\
            convert_infos[video]['title'].replace(' ','').replace(' ','').replace('【','[').replace('】',']')\
            .replace(':','').replace('|','').replace('*','').replace('?','').replace('"','').replace('/','')\
            .replace('<','').replace('>','').replace('｜','').replace('！','').replace('？','')+\
            '_'+'p'+str(cnt)+'.mp4')

        args1 = ['ffmpeg -y -loglevel quiet',
                '-i',p['video'],
                '-i',p['audio'],
                '-vsync 0',
                '-c:v copy',
                '-c:a copy',
                '"'+tmp_path+'"'
        ]

        args2 = ['ffmpeg -y -loglevel quiet',
                '-i','"'+tmp_path+'"',
                '-i',convert_infos[video]['cover'],
                '-map 0 -map 1',
                '-c copy -c:v:1 png -disposition:v:1 attached_pic',
                '"'+out_path+'"'
        ]

        cmd1 = args2cmd(args1)
        cmd2 = args2cmd(args2)
        if os.path.split(out_path)[1] not in outs:
            # print(cmd1)
            # print(cmd2)
            os.system(cmd1)
            os.system(cmd2)
            if os.path.isfile(tmp_path):
                os.remove(tmp_path)
        #     os.system(cmd)
            