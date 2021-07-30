# encoding: utf-8
"""
@file: transFormJson.py
@time: 2021/5/13 15:34
@author: Chen
@contact: Afakerchen@em-data.com.cn
@software: PyCharm
"""
import os
import untangle
from PIL import Image
from .transFormFuntion import get_stamp13, annotations, images, categories

labels = {}


def dataToXml(xml_path, img_path, coco_img_path):
    annotationsId = 1
    labelId = 1
    categoriesList, imagesList, annotationsList = [], [], []
    for src_dir, dirs, files in os.walk(xml_path):
        for filename in files:
            try:
                imagePath = os.path.join(img_path, str(filename).replace('.xml', '.jpg'))
                im = Image.open(imagePath)
                imagesId = get_stamp13()
                imagesList.append(images(im, imagesId, os.path.join(coco_img_path, str(filename).rstrip('.json'))))
                for data in untangle.parse(os.path.join(src_dir, filename)).annotation.object:
                    if not labels.get(data['label']):
                        labels[data['label']] = [labelId, data['label']]
                        labelId += 1
                    name = data.name.__dict__['cdata']
                    categoriesId = labels[name][0]
                    xmin = int(data.bndbox.xmin.__dict__['cdata']) - 1
                    ymin = int(data.bndbox.ymin.__dict__['cdata']) - 1
                    xmax = int(data.bndbox.xmax.__dict__['cdata'])
                    ymax = int(data.bndbox.ymax.__dict__['cdata'])
                    assert (xmax > xmin)
                    assert (ymax > ymin)
                    o_width = abs(xmax - xmin)
                    o_height = abs(ymax - ymin)
                    bbox = [xmin, ymin, o_width, o_height]
                    annotationsList.append(annotations(annotationsId=annotationsId, imagesIndex=imagesId,
                                                       categoriesId=categoriesId, bbox=bbox))
                    annotationsId += 1
                # moveFileToDir(os.path.join(src_dir, filename), os.path.join(local_path, 'data'))
                # moveFileToDir(imagePath, os.path.join(local_path, 'img'))
            except FileNotFoundError as e:
                print(e)
                pass
    for key in labels:
        categoriesList.append(categories(key, labels))
    return [categoriesList, imagesList, annotationsList]
