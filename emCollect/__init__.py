# encoding: utf-8
"""
@file: __init__.py.py
@time: 2021/7/28 10:48
@author: Chen
@contact: Afakerchen@em-data.com.cn
@software: PyCharm
"""
from emCollect.common.baseConfig import BaseConfig
# 初始化配置信息
Normal = BaseConfig().loadConf('./conf/normal.conf.json').objMap