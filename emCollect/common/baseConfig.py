import sys
from .baselog import logger
import traceback
import json


class ReadConfigure:
    def __init__(self):
        self.str = ""
        pass

    def read(self, filePath):
        try:
            fd = open(filePath)
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
    # print (self.objMap)


class BaseConfig:
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
