# encoding: utf-8
"""
@file: transFormMain.py
@time: 2021/7/15 16:26
@author: Chen
@contact: Afakerchen@em-data.com.cn
@software: PyCharm
"""
import json

from .transFormFuntion import checkData, COCOoutPutFile, NpEncoder
from .transFormJson import dataToJson
from .transFormXml import dataToXml


def tfMain(commandParam, load=True):
    sut = checkData(commandParam.data_type, commandParam.img_path, commandParam.data_path)
    if sut is None:
        values = None
        if commandParam.data_type == 'json':
            values = dataToJson(commandParam.data_path, commandParam.img_path, commandParam.coco_img_path)
        elif commandParam.data_type == 'xml':
            values = dataToXml(commandParam.data_path, commandParam.img_path, commandParam.coco_img_path)
        keys = ['categories', 'images', 'annotations']
        dictionary = dict(zip(keys, values))
        j = json.dumps(dictionary, ensure_ascii=False, cls=NpEncoder, indent=4, sort_keys=True)
        if load:
            json_file_path = COCOoutPutFile(j, commandParam.local_path)
            return json_file_path
        else:
            return j
    else:
        return sut
