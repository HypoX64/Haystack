import cv2
import argparse
from tqdm import tqdm
import os
import util
import numpy as np

from skimage.metrics import peak_signal_noise_ratio
from skimage.metrics import structural_similarity


parser=argparse.ArgumentParser()
parser.add_argument("--dir",type=str,default='',help="Dir to save 'data'")
parser.add_argument("--step",type=int,default=30*60,help="")
parser.add_argument("--max_frame",type=int,default=10,help="")
opt = parser.parse_args()
if opt.dir == '':
    print('Please input parser. -h')

'''
ref.mp4 is the reference video
'''

video_paths = util.Traversal(opt.dir)
video_output_infos = {}
print('read video...')
for video_path in tqdm(video_paths):
    if not os.path.isfile(video_path):
        continue
    video = cv2.VideoCapture(video_path)
    video_name = os.path.basename(video_path)
    if not video.isOpened():
        print('Failed to open video:',video_name)
        continue
    video_output_infos[video_name] = {}
    video_output_infos[video_name]['frames'] = []

    frame_count = 0
    while True:
        ret, frame = video.read()
        if not ret or len(video_output_infos[video_name]['frames'])>opt.max_frame:
            break
        if frame_count%opt.step == 0:
            video_output_infos[video_name]['frames'].append(frame)
            # print(frame.shape)
        frame_count+=1
    video.release()

print('compare video...')
for video_name in tqdm(video_output_infos):
    if video_name != 'ref.mp4':
        psnrs = []
        ssims = []
        for i in range(len(video_output_infos[video_name]['frames'])):
            psnrs.append(peak_signal_noise_ratio(video_output_infos['ref.mp4']['frames'][i],
                video_output_infos[video_name]['frames'][i],data_range=255))
            ssims.append(structural_similarity(video_output_infos['ref.mp4']['frames'][i],
                video_output_infos[video_name]['frames'][i],multichannel=True,data_range=255))
        video_output_infos[video_name]['psnr'] = np.mean(psnrs)
        video_output_infos[video_name]['ssim'] = np.mean(ssims)

for video_name in video_output_infos:
    if video_name != 'ref.mp4':
        print(video_name,round(video_output_infos[video_name]['psnr'],3),round(video_output_infos[video_name]['ssim'],3))