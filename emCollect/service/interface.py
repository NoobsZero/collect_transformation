# encoding: utf-8
"""
@file: interface.py
@time: 2021/7/16 11:08
@author: Chen
@contact: Afakerchen@em-data.com.cn
@software: PyCharm
"""
import uvicorn
from fastapi import FastAPI, Body
from typing import Optional
from pydantic import BaseModel

from .dependencies.wf.wfRenameFuntion import un
from .routers import cvat, wf
from ..common.baseConfig import BaseConfig

app = FastAPI(title='数据部常用工具', description='''
                                1、CVAT:将老工具json或xml转为CVAT中COCO格式 
                                2、WF:违法数据''')

app.include_router(cvat.router)
app.include_router(wf.router)


# class JiekouCanshuJieshi(BaseModel):
#     para1: str
#     para2: int
#     para3: Optional[str] = None
#     para4: Optional[str] = '自己添加'
#     para5: Optional[int] = 110
#
#
# @app.post(path='/api6', summary='接口参数注释2', description='接口6描述', tags=['评论交流'])
# def fun6(inputData: JiekouCanshuJieshi = Body(..., example={'para1': "必填，格式要求是字符串",
#                                                             'para2': "必填,格式要求是整型",
#                                                             'para3': "选填，格式要求是字符串,默认值是None",
#                                                             'para4': "选填，格式要求是字符串,默认值是'自己添加'",
#                                                             'para5': "选填，格式要求是整型,默认值是110"})):
#     return inputData


def main():
    un()
    # uvicorn.run(app=app, host="192.168.50.100", port=8000)
