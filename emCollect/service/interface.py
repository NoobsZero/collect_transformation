# encoding: utf-8
"""
@file: interface.py
@time: 2021/7/16 11:08
@author: Chen
@contact: Afakerchen@em-data.com.cn
@software: PyCharm
"""
import uvicorn
from fastapi import FastAPI
from .routers import cvat, wf, cj, user
from ..model import models
from ..model.modelBase import engine

# 创建数据库表，具体生成表配置与model.__init__.py
# models.Base.metadata.create_all(engine)

app = FastAPI(title='数据部常用工具', description='''
                                1、CVAT:将老工具json或xml转为CVAT中COCO格式 
                                2、WF:违法数据
                                ''')

app.include_router(cvat.router)
app.include_router(wf.router)
app.include_router(cj.router)
app.include_router(user.router)


def main():
    # test()
    uvicorn.run(app=app, host="192.168.50.100", port=8000)
