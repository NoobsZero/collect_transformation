# encoding: utf-8
"""
@file: cj.py
@time: 2021/8/9 13:50
@author: Chen
@contact: Afakerchen@em-data.com.cn
@software: PyCharm
"""
from fastapi import APIRouter

router = APIRouter(prefix="/cj",
                   tags=["车检"],
                   responses={404: {"description": "Not found"}})


@router.get('/collect', summary='车检压缩文件处理', description='将外来车检')
async def collectData():
    pass
    # start = time.time()
    # result = main()
    # return {"message": "success", 'time': time.time() - start, 'resultPath': result}