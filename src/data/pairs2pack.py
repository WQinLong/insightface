import mxnet as mx
from mxnet import ndarray as nd
import argparse
import pickle
import sys
import os


def read_pairs(pairs_filename):
    pairs = []
    with open(pairs_filename, 'r') as f:
        for line in f.readlines()[1:]:
            pair = line.strip().split()
            pairs.append(pair)
    return np.array(pairs)


def get_paths(pairs_filename):
    pairs = []
    with open(pairs_filename, 'r') as f:
        for line in f.readlines()[1:]:
            pair = line.strip().split()
            pairs.append(pair)

    nrof_skipped_pairs = 0
    path_list = []
    issame_list = []
    for pair in pairs:
        if len(pair) == 3:
            path0 = pair[0]
            path1 = pair[1]
            if pair[2] == '1':
                issame = True
            if pair[2] == '1':
                issame = False
        if os.path.exists(path0) and os.path.exists(path1):
            path_list += (path0, path1)
            issame_list.append(issame)
        else:
            print('not exists', path0, path1)
            nrof_skipped_pairs += 1
    if nrof_skipped_pairs>0:
        print('Skipped %d image pairs' % nrof_skipped_pairs)
    return path_list, issame_list


parser = argparse.ArgumentParser(description='Package LFW images')
# general
parser.add_argument('--pairs_filename', default='', help='')

parser.add_argument('--output', default='', help='path to save.')
args = parser.parse_args()
pairs_filename = args.pairs_filename

lfw_paths, issame_list = get_paths(pairs_filename)
lfw_bins = []
#lfw_data = nd.empty((len(lfw_paths), 3, image_size[0], image_size[1]))
i = 0
for path in lfw_paths:
  with open(path, 'rb') as fin:
    _bin = fin.read()
    lfw_bins.append(_bin)
    #img = mx.image.imdecode(_bin)
    #img = nd.transpose(img, axes=(2, 0, 1))
    #lfw_data[i][:] = img
    i+=1
    if i%1000==0:
      print('loading pairs data', i)

with open(args.output, 'wb') as f:
  pickle.dump((lfw_bins, issame_list), f, protocol=pickle.HIGHEST_PROTOCOL)