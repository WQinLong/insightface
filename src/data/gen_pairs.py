import argparse
import sys
import os
import random
import numpy as np


class ImageClass():
    "Stores the paths to images for a given class"
    def __init__(self, class_name, image_paths,labels_flat):
        self.labels_flat = labels_flat
        self.class_name = class_name
        self.image_paths = image_paths

    def __str__(self):
        return self.class_name + ', ' + self.image_paths + self.labels_flat

    def __len__(self):
        return 1


def get_image_paths(facedir):
    image_paths = []
    if os.path.isdir(facedir):
        images = os.listdir(facedir)
        for img in images:
            if img.endswith('jpg'):
                image_paths.append(os.path.join(facedir,img))
    return image_paths


def get_all_image_data(paths, has_class_directories=True, start=0):
    image_datas = []
    for path in paths.split(':'):
        path_exp = os.path.expanduser(path)
        classes = os.listdir(path_exp)
        classes.sort()
        nrof_classes = len(classes)
        for i in range(nrof_classes):
            class_name = classes[i]
            labels_flat = i+ start
            facedir = os.path.join(path_exp, class_name)
            image_paths = get_image_paths(facedir)
            for image_path in image_paths:
                image_datas.append(ImageClass(class_name, image_path, labels_flat))

    return image_datas


parser = argparse.ArgumentParser(description='gen pairs own')
parser.add_argument('--input', default='', help='')
parser.add_argument('--output', default='', help='file to save.')

args = parser.parse_args()

data_dir = args.input
pairs_file = args.output

image_datas = get_all_image_data(data_dir)

num = len(image_datas)
num_same_0 =0
num_same_1 = 0

with open(pairs_file, 'w') as f:

    for i in range(num):
        for j in range(num):
            if i >= j:
                continue
            if image_datas[i].labels_flat==image_datas[j]:
                issame = 1
                num_same_1 = num_same_1+1
            else:
                issame = 0
                num_same_0 = num_same_0 + 1
            f.write('%s\t%s\t%d\n' % (image_datas[i].image_paths, image_datas[j].image_paths, issame))

    f.write('%d\t%d\n' % (num_same_0, num_same_1))







