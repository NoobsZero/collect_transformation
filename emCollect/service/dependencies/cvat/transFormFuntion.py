# encoding: utf-8
"""
@file: transFormFuntion.py
@time: 2021/7/16 9:36
@author: Chen
@contact: Afakerchen@em-data.com.cn
@software: PyCharm
"""
import json
import os
import shutil

import numpy as np
from datetime import datetime
import time


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)


def get_stamp13(datetime_obj=None):
    if datetime_obj is None:
        t = time.time()
        return int(round(t * 1000))
    # 生成13时间戳   eg:1557842280000
    datetime_obj = datetime.strptime(datetime_obj, '%Y-%m-%d %H:%M:%S.%f')
    # datetime_str = datetime.datetime.strftime(datetime_obj, '%Y-%m-%d %H:%M:%S.%f')
    # # 10位，时间点相当于从1.1开始的当年时间编号
    date_stamp = str(int(time.mktime(datetime_obj.timetuple())))
    # # 3位，微秒
    data_microsecond = str("%06d" % datetime_obj.microsecond)[0:3]
    date_stamp = date_stamp + data_microsecond
    return int(date_stamp)


imagesKeys = ['id', 'width', 'height', 'file_name', 'license', 'flickr_url', 'coco_url', 'date_captured']
categoriesKeys = ['id', 'name', 'supercategory']


def annotations(annotationsId, imagesIndex, categoriesId, polygon=None, area='', bbox=None, iscrowd=0):
    if bbox is None:
        bbox = []
    if polygon is None:
        polygon = []
    annotationsValues = [annotationsId, imagesIndex, categoriesId, polygon, area, bbox, iscrowd]
    return dict(zip(['id', 'image_id', 'category_id', 'segmentation', 'area', 'bbox', 'iscrowd'], annotationsValues))


def categories(label, labels):
    categoriesValues = [labels[label][0], labels[label][1], '']
    return dict(zip(categoriesKeys, categoriesValues))


def images(im, imagesIdex, addr):
    imagesValues = [imagesIdex, im.width, im.height, addr, '0', '', '', '0']
    return dict(zip(imagesKeys, imagesValues))


def moveFileToDir(root_src_file, root_dst_dir):
    """
        移动文件到目录
    :param root_src_file: 源文件
    :param root_dst_dir: 指定目录
    """
    if os.path.isfile(root_src_file):
        if not os.path.exists(root_dst_dir):
            os.makedirs(root_dst_dir)
        root_dst_file = os.path.join(root_dst_dir, os.path.split(root_src_file)[-1])
        shutil.move(root_src_file, root_dst_file)


def checkData(data_type, img_path, data_path):
    img_paths = [os.path.join(src_dir, filename) for src_dir, dirs, files in os.walk(img_path) for filename in files]
    data_paths = []
    for src_dir, dirs, files in os.walk(data_path):
        for filename in files:
            imagePath = None
            if data_type == 'json':
                imagePath = os.path.join(img_path, str(filename).rstrip('.json'))
            elif data_type == 'xml':
                imagePath = os.path.join(img_path, str(filename).replace('.xml', '.jpg'))
            if imagePath in img_paths:
                img_paths.remove(imagePath)
            else:
                data_paths.append(os.path.join(src_dir, filename))
    if len(img_paths) > 0 or len(data_paths) > 0:
        return {'img_paths': img_paths, 'data_paths': data_paths}
    else:
        return None


def COCOoutPutFile(j, local_path):
    json_file_path = os.path.join(local_path, 'coco_' + str(get_stamp13()) + '.json')
    with open(json_file_path, 'a', encoding='utf-8',
              errors="ignore") as fo:
        fo.write(j)
        fo.flush()
    return json_file_path
