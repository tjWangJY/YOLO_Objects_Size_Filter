import os
import argparse
import cv2


# make a concept for objects
# assume that the size of a certain object is axb
# if 'a' and 'b' are all smaller than the config of 'small' downside, the object is determined as 'small'
# if 'a' and 'b' are all larger than the config of 'large' downside, the object is determined as 'large'
small = 32
large = 96
# image type
image_type = 'jpg'
want_which_objects = 'small'  # choose from 'small', 'medium', and 'large'


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--images', type=str,
                        default='F:/Dataset/Helmet/Hardhat/Train/JPEGImage',
                        help='images path, must be applied to labels')
    parser.add_argument('--labels', type=str,
                        default='F:/Dataset/Helmet/Hardhat/Train/labels',
                        help='labels path, must be applied to images')
    parser.add_argument('--spath', type=str,
                        default='F:/wjy/small_ob',
                        help='save path of the filtered dataset')
    parser.add_argument('--sizecfg', type=list, default=[small, large], help='size filter config')
    args = parser.parse_args()
    return args


def source_check(args):
    images = []
    labels = []
    true_images = []
    for root,dirs,files in os.walk(args.images):
        for file in files:
            if file.split('.')[1] == image_type:
                images.append(file.split('.')[0])
    for root,dirs,files in os.walk(args.labels):
        for file in files:
            if file.split('.')[1] == 'txt':
                labels.append(file.split('.')[0])
    for name in images:
        if name in labels:
            true_images.append(name)
    print('找到%d个匹配的图片与label' % len(true_images))
    return true_images


def size_filter(args, names):
    small = args.sizecfg[0]
    large = args.sizecfg[1]
    smalls = []
    larges = []
    mediums = []
    for name in names:
        small_isExist = False
        large_isExist = False
        ima = cv2.imread(args.images + '/' + name + '.jpg')
        width = ima.shape[1]
        length = ima.shape[0]
        with open(args.labels + '/' + name + '.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                if float(line.split(' ')[3])*width <= small and float(line.split(' ')[4])*length <= small:
                    small_isExist = True
                if float(line.split(' ')[3])*width >= large and float(line.split(' ')[4])*length >= large:
                    large_isExist = True
                if small_isExist and large_isExist: break
        if small_isExist: smalls.append(name)
        if large_isExist: larges.append(name)
        if not small_isExist and not large_isExist: mediums.append(name)
        print('找到带有小目标的图片%d个，带有大目标的图片%d个，普通目标图片%d个' % (len(smalls), len(larges), len(mediums)))
    return [smalls, mediums, larges]


def generate_dataset(args, names):
    if not os.path.exists(args.spath+'/images'):
        os.makedirs('\\'.join(args.spath.split('/')) + '\\images')
    if not os.path.exists(args.spath + '/labels'):
        os.makedirs('\\'.join(args.spath.split('/')) + '\\labels')
    for name in names:
        os.system("xcopy %s %s" % ('\\'.join(args.images.split('/'))+'\\'+name+'.'+image_type,
                                   '\\'.join(args.spath.split('/')) + '\\images'))
        os.system("xcopy %s %s" % ('\\'.join(args.labels.split('/')) + '\\' + name + '.txt',
                                   '\\'.join(args.spath.split('/')) + '\\labels'))


def wanted_object():
    if want_which_objects == 'small': return 0
    if want_which_objects == 'medium': return 1
    if want_which_objects == 'large': return 2
    return 3


def main(args):
    names = source_check(args)
    if wanted_object() != 3:
        objects = size_filter(args, names)
        generate_dataset(args, objects[wanted_object()])
    else:
        print("want_which_objects输入不合法")


if __name__ == '__main__':
    args = parse_args()
    main(args)

