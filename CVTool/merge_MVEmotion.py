import os
import sys
import util
import datetime
from tqdm import tqdm
from multiprocessing import Pool

indir = '/dockerdata/hypolei/datasets/raw_data/MVEmotion'
outdir = '/dockerdata/hypolei/datasets/raw_data/MVEmotion_cvt'

util.makedirs(outdir)

subjects = os.listdir(indir)
subjects.sort()
# subjects = ['051_何婉媚']
# subjects = ['052']

datasets = ['DEAP','EMDB','FilmStim','IADS']
err_list = []
video_process_list = []

for subject in tqdm(subjects):
    util.makedirs(os.path.join(outdir,subject))
    for dataset in datasets:
        try:
            if os.listdir(os.path.join(indir,subject,dataset)) == []:
                continue
            util.makedirs(os.path.join(outdir,subject,'label',dataset))
            util.makedirs(os.path.join(outdir,subject,'data'))
    
            os.system('cp -r %s %s'%(os.path.join(indir,subject,dataset,'*.txt'),os.path.join(outdir,subject,'label',dataset)))
            
            times = os.listdir(os.path.join(indir,subject,dataset,'signal'))
            for time in times:
                os.system('cp -r %s %s'%(os.path.join(indir,subject,dataset,'signal',time,'data.txt'),os.path.join(outdir,subject,'data',time+'_'+dataset+'.txt')))
                videos = os.listdir(os.path.join(indir,subject,dataset,'signal',time))
                videos = util.is_videos(videos)
                videos.sort()
                if videos == []:
                    continue
                
                _bin = '/dockerdata/hypolei/project/3rdparty/ffmpeg-6.0-amd64-static'
                cmd = 'ffmpeg -y -loglevel quiet'
                # cmd = 'ffmpeg -y'
                cmd = 'PATH='+_bin+' && '+cmd
                cmd += ' -i '
                
                concat_str = 'concat:'
                for video in videos:
                    concat_str+=os.path.join(indir,subject,dataset,'signal',time,video)+'|'
                concat_str = concat_str[:-1]
                cmd = cmd + '"'+concat_str+'"'
                cmd += ' -vcodec libx265 -acodec an -crf 23 -preset medium '+os.path.join(outdir,subject,time+'_'+dataset+'.mp4')
                # os.system(cmd)
                video_process_list.append(cmd)
        except:
            print('Error:',subject,dataset)
            err_list.append(subject+'_'+dataset)
            continue
    # 7z a 002.7z 002 -bd -sdel
    os.system('7z a "{}.7z" "{}" -mmt=64 -bd -sdel'.format(os.path.join(outdir,subject,'data'),os.path.join(outdir,subject,'data')))
    os.system('7z a "{}.7z" "{}" -mmt=64 -bd -sdel'.format(os.path.join(outdir,subject,'label'),os.path.join(outdir,subject,'label')))

print('Error list:')
print(err_list)

print(len(video_process_list),'videos to process.')

# print('Do you want to ecodec?  Y/N')
# choose = input().strip()
# choose = str(choose.replace("'","")).lower()
# if choose in ['n','no','none']:
#     print('Exit.')
#     sys.exit(0)
# # print(video_process_list)

def process_one_scene(cmd):
    print(cmd)
    os.system(cmd)
    
def mycallback(arg):
    '''get the image data and update pbar'''
    pbar.update(1)
    return None

pbar = tqdm(total=len(video_process_list))

POOL_NUM = 16

pool = Pool(POOL_NUM)
for i,cmd in enumerate(video_process_list):
    pool.apply_async(process_one_scene, args=(cmd,),callback=mycallback)
pool.close()
pool.join()