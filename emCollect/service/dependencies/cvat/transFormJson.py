# encoding: utf-8
"""
@file: transFormJson.py
@time: 2021/5/13 15:34
@author: Chen
@contact: Afakerchen@em-data.com.cn
@software: PyCharm
"""
import os

from PIL import Image, ImageDraw
import sys
import traceback
import json
import numpy as np
from .transFormFuntion import get_stamp13, images, categories, annotations


class ReadConfigure:
    def __init__(self):
        self.str = ""
        pass

    def read(self, filePath):
        try:
            fd = open(filePath, 'rb')
        except Exception as ex:
            print(ex)
            msg = traceback.format_exc()
            # print(msg)
            sys.exit(1)
        self.str = fd.read()
        # print "conf_content:", self.str
        return True

    def getReadData(self):
        return self.str


def parseInputParameter(filePath):
    rc = ReadConfigure()
    if not rc.read(filePath):
        sys.exit(1)
    return json.loads(rc.getReadData())


class JsonConfig:
    def __init__(self):
        self.objMap = {}

    @classmethod
    def loadConf(cls, filePath):
        self = cls.__new__(cls)
        self.objMap = parseInputParameter(filePath)
        return self

    def getKeys(self):
        return self.objMap.keys()

    def getValue(self, keyName):
        return self.objMap[keyName]


def mask2box(mask):
    """从mask反算出其边框
        mask：[h,w]  0、1组成的图片
    1对应对象，只需计算1对应的行列号（左上角行列号，右下角行列号，就可以算出其边框）
    """
    # np.where(mask==1)
    index = np.argwhere(mask == 1)
    rows = index[:, 0]
    clos = index[:, 1]
    # 解析左上角行列号
    left_top_r = np.min(rows)  # y
    left_top_c = np.min(clos)  # x
    # 解析右下角行列号
    right_bottom_r = np.max(rows)
    right_bottom_c = np.max(clos)
    # return [(left_top_r,left_top_c),(right_bottom_r,right_bottom_c)]
    # return [(left_top_c, left_top_r), (right_bottom_c, right_bottom_r)]
    # return [left_top_c, left_top_r, right_bottom_c, right_bottom_r]  # [x1,y1,x2,y2]
    return [left_top_c, left_top_r, right_bottom_c - left_top_c,
            right_bottom_r - left_top_r]  # [x1,y1,w,h] 对应COCO的bbox格式


def polygons_to_mask(img_shape, polygons):
    mask = np.zeros(img_shape, dtype=np.uint8)
    mask = Image.fromarray(mask)
    if len(polygons):
        xy = list(map(tuple, polygons))
        ImageDraw.Draw(mask).polygon(xy=xy, outline=1, fill=1)
    mask = np.array(mask, dtype=bool)
    return mask


labels = {}


def toPolygons(polygon):
    polygons = []
    if len(polygon):
        for po in polygon:
            polygons.append(po[0])
            polygons.append(po[1])
    return polygons


def dataToJson(json_path, img_path, coco_img_path):
    labelId = 1
    annotationsId = 1
    categoriesList, imagesList, annotationsList = [], [], []
    for src_dir, dirs, files in os.walk(json_path):
        for filename in files:
            try:
                oldjson = JsonConfig.loadConf(os.path.join(src_dir, filename))
                imagePath = os.path.join(img_path, str(filename).rstrip('.json'))
                im = Image.open(imagePath)
                imagesId = get_stamp13()
                imagesList.append(images(im, imagesId, os.path.join(coco_img_path, str(filename).rstrip('.json'))))
                for data in oldjson.getValue('objects'):
                    if not labels.get(data['label']):
                        labels[data['label']] = [labelId, data['label']]
                        labelId += 1
                    categoriesId = labels[data['label']][0]
                    if 'polygons' in data:
                        polygon = data['polygon']
                        annotationsList.append(
                            annotations(annotationsId=annotationsId, imagesIndex=imagesId, categoriesId=categoriesId,
                                        polygon=[toPolygons(polygon)],
                                        bbox=mask2box(polygons_to_mask([im.height, im.width], polygon))))
                    else:
                        annotationsList.append(
                            annotations(annotationsId=annotationsId, imagesIndex=imagesId, categoriesId=categoriesId))
                    annotationsId += 1
                # moveFileToDir(os.path.join(src_dir, filename), os.path.join(local_path, 'data'))
                # moveFileToDir(imagePath, os.path.join(local_path, 'img'))
            except FileNotFoundError as e:
                print(e)
                pass
    for key in labels:
        categoriesList.append(categories(key, labels))
    return [categoriesList, imagesList, annotationsList]
