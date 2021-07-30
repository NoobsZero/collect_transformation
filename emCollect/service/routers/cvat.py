# encoding: utf-8
"""
@file: cvat.py
@time: 2021/7/29 9:50
@author: Chen
@contact: Afakerchen@em-data.com.cn
@software: PyCharm
"""
import os
import time
import shutil
from typing import List
from fastapi import APIRouter, Query, File, UploadFile
from emCollect.common.baselog import logger
from ..dependencies.cvat.transFormMain import tfMain
from ..parseCommand import TransForm
from ... import Normal

cvatTem = Normal['cvatTem']

router = APIRouter(prefix="/cvat",
                   tags=["CVAT"],
                   responses={404: {"description": "Not found"}})


@router.get('/transform', summary='获取转换后的COCO数据（JSON）', description='将老工具json或xml转为CVAT中COCO格式')
async def getCocoJson(data_type: str = Query(..., description="必填，数据类型[json, xml]"),
                      img_path: str = Query(..., description="必填，图片路径"),
                      data_path: str = Query(None, description="可选，json或xml路径，默认为None需提前调用 upload 接口上传数据"),
                      coco_img_path: str = Query(None, description="可选，COCO文件中图片路径，默认为None使用 img_path 路径")):
    if coco_img_path is None:
        coco_img_path = img_path
    if data_path is None:
        # data_path = os.path.abspath('.') + '/data'
        data_path = cvatTem
    tf = TransForm.get_TransForm()
    tf.data_type = data_type
    tf.img_path = img_path
    tf.data_path = data_path
    tf.coco_img_path = coco_img_path
    return tfMain(tf, False)


@router.post("/transform/upload", summary='上传JSON或XML文件', description='将老工具json或xml转为CVAT中COCO格式')
async def file_upload(files: List[UploadFile] = File(..., description="必填，json或xml文件")):
    shutil.rmtree(cvatTem)
    os.mkdir(cvatTem)
    start = time.time()
    fileNames = []
    data = None
    try:
        for file in files:
            filename = file.filename
            with open(os.path.join(cvatTem, filename), "wb") as f:
                f.write(await file.read())
            fileNames.append(filename)
        data = {"message": "success", 'time': time.time() - start, 'filename': fileNames}
    except Exception as e:
        data = {"message": str(e), 'time': time.time() - start, 'filename': fileNames}
    finally:
        logger.info("info{}".format(data))
        return data
