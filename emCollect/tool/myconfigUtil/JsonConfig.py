# -*- encoding:utf-8 -*-
"""
@File   :JsonConfig.py
@Time   :2021/2/8 15:21
@Author :Chen
@Software:PyCharm
"""
import sys
import traceback
import json

from emCollect.common.baselog import logger


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
            logger.error("读取文件失败:[{}][{}] ".format(filePath, ex))
            sys.exit(1)
        self.str = fd.read()
        # print "conf_content:", self.str
        return True

    def getReadData(self):
        return self.str


def parseInputParameter(filePath):
    rc = ReadConfigure()
    if not rc.read(filePath):
        logger.error("error 文件不可访问:[{}]".format(filePath))
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


if __name__ == '__main__':
    oldjson = JsonConfig.loadConf(
        r'\\192.168.30.41\0_.算法部\panliuhua\up\路口分割2021-04-26\2-2-2\标注员\test\json\4370.jpg.json')
    data = oldjson.getValue('objects')[0]
    # data['lable']
    # data['polygon']
