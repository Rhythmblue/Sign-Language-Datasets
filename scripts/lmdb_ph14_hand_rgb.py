# ------------------------------------------------------------------------------
# Copyright (c) USTC, China
# Licensed under the MIT License.
# Written by Hao Zhou (zhouh156@mail.ustc.edu.cn)
# ------------------------------------------------------------------------------


import argparse
import glob
import os
import pickle

import numpy as np
from PIL import Image
from torch.utils.data import DataLoader, Dataset

import lmdb


class Video3D(object):
    def __init__(self, info_dict, tag='rgb'):
        '''
            keys of info_dict: name, path, length
            tag: 'rgb'(default) or 'flow'
            notes: if indexs of your img is 0,1,2,3, your frame num should be 4.
        '''
        self.name = info_dict['name']
        self.path = info_dict['path']
        self.length = info_dict['length']
        self.tag = tag

        self.tmp_path = info_dict['tmp_path']
        if self.tmp_path != '':
            folder = os.path.join(self.tmp_path, self.name)
            if not os.path.exists(folder):
                os.makedirs(folder)

    def load_img(self, path, idx):
        tmp = Image.open(path).convert('RGB')
        if self.tmp_path == '':
            tmp_name = os.path.join('./tmp_proc', '{:s}_{:d}.jpg'.format(self.name, idx))
        else:
            tmp_name = os.path.join(self.tmp_path, self.name, '{:06d}.jpg'.format(idx))
        tmp = tmp.resize((112, 112), Image.BICUBIC)
        tmp.save(tmp_name)
        rt = [open(tmp_name, 'rb').read()]
        if self.tmp_path == '':
            os.remove(tmp_name)
        return rt

    def get_cover_frames(self):
        '''
            return:
                num_frames * height * width * channel (rgb:3 , flow:2) 
        '''
        frame_list = sorted(glob.glob(self.path))
        frames = []
        for idx, path in enumerate(frame_list):
            frames.extend(self.load_img(path, idx))
        return frames


class FullVideoDateset(Dataset):

    def __init__(self, video_info, tag='rgb'):
        self.tag = tag
        self.videos = [Video3D(x, tag=tag) for x in video_info]

    def __len__(self):
        return len(self.videos)

    def __getitem__(self, index):
        clip = self.videos[index].get_cover_frames()     
        name = self.videos[index].name
        length = self.videos[index].length
        return clip, name, length


def collate_fn_fullvideo(batch):
    clip, name, length = zip(*batch)
    return clip[0], name[0], length[0]


def load_info(data_path, tmp_path):
    infos = []
    for task in ['train', 'dev', 'test']:
        data = pickle.load(open('data/phoenix2014/{:s}.pkl'.format(task), 'rb'))
        task_info = []
        for _, row in enumerate(data):
            video_info = {
                'name': row[0],
                'path': os.path.join(data_path, task, row[0], '1', '*.png'),
                'length': row[1],
                'tmp_path': tmp_path,
            }
            task_info.append(video_info)
        infos.append(task_info)
        print('Count-{:s}: {:d}'.format(task, len(task_info)))
    return infos


def main(opts):
    infos = load_info(opts.source_path, opts.target_tmp_path)

    dataset = [
        FullVideoDateset(infos[0], tag='rgb'),
        FullVideoDateset(infos[1], tag='rgb'),
        FullVideoDateset(infos[2], tag='rgb'),
    ]

    loader = [
        DataLoader(dataset[0], 1, shuffle=False, num_workers=opts.num_workers, collate_fn=collate_fn_fullvideo),
        DataLoader(dataset[1], 1, shuffle=False, num_workers=opts.num_workers, collate_fn=collate_fn_fullvideo),
        DataLoader(dataset[2], 1, shuffle=False, num_workers=opts.num_workers, collate_fn=collate_fn_fullvideo)
    ]

    if not os.path.exists(opts.target_path):
        os.makedirs(opts.target_path)
        print('makedirs: {:s}'.format(opts.target_path))
    env = lmdb.open(opts.target_path, map_size=1099511627776)
    txn = env.begin(write=True)

    for k, task in enumerate(['train', 'dev', 'test']):
        print(task)
        for i, (clip, name, length) in enumerate(loader[k]):
            assert len(clip) == length
            for j in range(length):
                key = task+'/'+name+'/'+'{:06d}'.format(j)
                txn.put(key=key.encode(), value=clip[j])
            print('{:d}/{:d}, {:d}, {:s}'.format(i+1, len(infos[k]), length, key))
    txn.commit()
    env.close()


def parse_args():
    p = argparse.ArgumentParser(description='slr')
    p.add_argument('source_path', type=str, default='', help='source path of original data [fullFrame-210x260px]')
    p.add_argument('target_path', type=str, default='', help='target path of lmdb') 
    p.add_argument('-nw', '--num_workers', type=int, default=4, help='num_workers of dataloader')
    p.add_argument('-tt', '--target_tmp_path', type=str, default='', help='target path of resized images') 
    parameter = p.parse_args()    
    return  parameter


if __name__ == '__main__':
    opts = parse_args()
    main(opts)
