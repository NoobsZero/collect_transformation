#!/usr/bin/python3
import sys
import os

if not __package__:
    # 1、返回脚本的路径, os.pardir:返回当前目录的父目录默认 ..
    path = os.path.join(os.path.dirname(__file__), os.pardir)
    # 2、将emCollect/..目录插入第一位，会优先于其他目录被import检查
    sys.path.insert(0, path)

from emCollect.service.interface import main

# 3、解析参数
# commandParam = ReadCommandParameter().parseCommandArgs(sys.argv[1:])
# 4、匹配功能模块
# if isinstance(commandParam, TransForm):
#     tfMain(commandParam)
main()
