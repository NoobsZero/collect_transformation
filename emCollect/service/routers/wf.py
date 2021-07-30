# encoding: utf-8
"""
@file: wf.py
@time: 2021/7/29 10:20
@author: Chen
@contact: Afakerchen@em-data.com.cn
@software: PyCharm
"""
import os
import shutil
import time

from starlette.responses import FileResponse
from fastapi import APIRouter, UploadFile, File

from emCollect.tool.mybaseUtil.getBaseUtil import BaseProgressBar

router = APIRouter(prefix="/wf",
                   tags=["违法"],
                   responses={404: {"description": "Not found"}})


@router.post('/rename/upload', summary='上传违法图片压缩包', description='将外来违法图片按格式改名并按类型分类')
async def file_upload(file: UploadFile = File(..., description="必填，压缩文件")):
    start = time.time()
    shutil.rmtree('./data')
    os.mkdir('./data')
    filename = file.filename
    with open('./data/%s' % filename, "wb") as f:
        f.write(await file.read())
    return {"message": "success", 'time': time.time() - start, 'filename': filename}
    # return FileResponse('./data/%s' % filename)
