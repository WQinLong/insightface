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
        return self.class_name + ', ' + str(len(self.image_paths)) + ' images'

    def __len__(self):
        return len(self.image_paths)


def get_image_paths(facedir):
    image_paths = []
    if os.path.isdir(facedir):
        images = os.listdir(facedir)
        for img in images:
            if img.endswith('jpg'):
                image_paths.append(img)
        #image_paths = [os.path.join(facedir,img) for img in images]
    return image_paths


def get_dataset(paths, has_class_directories=True,start=0):
    dataset = []
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
            dataset.append(ImageClass(class_name, image_paths, labels_flat))

    return dataset


parser = argparse.ArgumentParser(description='gen pairs own')
parser.add_argument('--input', default='', help='')
parser.add_argument('--output', default='', help='file to save.')
parser.add_argument('--a', type=int, default=10, help='file to save.')
parser.add_argument('--b', type=int, default=300, help='file to save.')
args = parser.parse_args()

data_dir = args.input
pairs_file = args.output

dataset = get_dataset(data_dir)

num = len(dataset)

flag = np.zeros((1000, 1000, 1000))
flag1 = np.zeros((700, 200, 700, 200))
with open(pairs_file, 'w') as f:
    f.write('%d\t%d\n' %(args.a, args.b))
    for i in range(args.a):
        for j1 in range(args.b):
            n = random.randint(0, num-1)
            image_paths = dataset[n].image_paths
            m = len(image_paths)

            r1 = 0
            r2 = 0
            t = 0
            while(1):
                t = t+1
                if t > 100 or m==0:
                    n = random.randint(0, num - 1)
                    image_paths = dataset[n].image_paths
                    m = len(image_paths)
                    t = 0
                    continue
                r1 = random.randint(0, m-1)
                r2 = random.randint(0, m-1)
                if r1 == r2:
                    continue
                if flag[n, r1, r2] == 1:
                    continue
                if flag[n, r2, r1] == 1:
                    continue
                flag[n, r1, r2] = 1

                f.write('%s\t%s\t%s\n' %(dataset[n].class_name, image_paths[r1].split('.jpg')[0],
                                       image_paths[r2].split('.jpg')[0]))
                break

        for j1 in range(args.b):
            n1 = 0
            n2 = 0
            while n1 == n2:
                n1 = random.randint(0, num-1)
                image_paths1 = dataset[n1].image_paths
                m1 = len(image_paths1)

                n2 = random.randint(0, num - 1)
                image_paths2 = dataset[n2].image_paths
                m2 = len(image_paths2)

            r1 = 0
            r2 = 0
            t = 0
            while 1:
                t = t+1
                if t > 100 or m1==0 or m2==0:
                    n1 = 0
                    n2 = 0
                    while n1 == n2:
                        n1 = random.randint(0, num - 1)
                        image_paths1 = dataset[n1].image_paths
                        m1 = len(image_paths1)

                        n2 = random.randint(0, num - 1)
                        image_paths2 = dataset[n2].image_paths
                        m2 = len(image_paths2)
                    t = 0
                    continue
                r1 = random.randint(0, m1-1)
                r2 = random.randint(0, m2-1)

                if flag1[n1, r1, n2, r2] == 1:
                    continue
                if flag1[n2, r2, n1, r1] == 1:
                    continue
                flag1[n1, r1, n2, r2] = 1

                f.write('%s\t%s\t%s\t%s\n' %(dataset[n1].class_name, image_paths1[r1].split('.jpg')[0],
                                           dataset[n2].class_name, image_paths2[r2].split('.jpg')[0]))
                break



