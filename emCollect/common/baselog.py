import logging
import time
import logging.handlers
import os
import shutil

# 初始化设置

logging.basicConfig(level=logging.INFO, format='[%(asctime)s%(levelname)s%(filename)s%(lineno)s]:%(message)s')
# 创建
logger = logging.getLogger("collect_tool")
logger.setLevel(logging.INFO)


# 创建handler
def registerLoggerHandle(fileName):
    dirStr = os.path.dirname(fileName)
    if not os.path.exists(dirStr):
        os.makedirs(dirStr)
    handler1 = logging.FileHandler(fileName)
    handler1.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '[%(asctime)s_%(name)-8s-%(levelname)-8s-%(filename)s %(funcName)s %(lineno)s]:%(message)s')
    handler1.setFormatter(formatter)

    handler2 = logging.StreamHandler()
    handler2.setLevel(logging.ERROR)
    logger.addHandler(handler1)
    logger.addHandler(handler2)


registerLoggerHandle(fileName="log/base-log.log")

if __name__ == '__main__':
    test = "widbwfue"
    logger.info("info{}".format(test))
    logger.warning("warning")
    logger.error("error")
