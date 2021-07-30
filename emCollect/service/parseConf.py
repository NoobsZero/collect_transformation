import os
from ..common import baseTool
from ..common.baselog import logger

#
# {
#     "basePath": "/opt/vehicle/rawdata",
#     "photoDir":"photos",
#     "cityConfDir":"CheJianConfig",
#
# }
ROOT_TMP_DATA_PATH = "../_Data_emCollect"
ROOT_TMP_DATA_PHOTOS = ROOT_TMP_DATA_PATH + "/_Data_photos/"


class RawDataBaseInfo:
    """
        RawDataBaseInfo
        原始数据库信息
        deviceType 设备类型
        cityCode   城市代码
        dateStr    导出日期
        datePhotoDirs 照片日期
        tmpRoot 临时图片存储目录
    """

    def __init__(self):
        self.deviceType = "None"
        self.cityCode = "None"
        # // 导出日期
        self.dateStr = "None"
        # // 照片日期   "误判数据会有多个目录" 而且日期一般和导出日期不同
        self.datePhotoDirs = []
        self.tmpRoot = ROOT_TMP_DATA_PHOTOS


class DataSaveConf:
    def __init__(self, confPath):
        """
            DataSaveConf
            读取数据存储配置文件
            basePath 数据存储目录路径
            photoDir 图片存储目录路径
            videoDir 视频存储目录路径(None)
            photoPath 图片路径
            cityConfPath
            baseCityInfo
            format 所有配置信息
        Args:
            confPath: [basePath（数据存储目录路径）、photoDir（图片存储目录路径）、nginxRoot（本服务目录所在路径）]文件路径
        """
        bconf = baseTool.BaseConfig().loadConf(confPath)
        print(bconf.__dict__)
        self.basePath = bconf.objMap["basePath"]
        self.photoDir = bconf.objMap["photoDir"]
        self.videoDir = "videos"
        self.cityConfDir = "CheJianConfig"
        self.tmpDir = ROOT_TMP_DATA_PHOTOS  # ROOT_TMP_DATA_PATH+"/_Data_photos/"
        self.videoPath = None
        self.photoPath = None
        self.cityConfPath = None
        self.baseCityInfo = RawDataBaseInfo()
        self.format()

    def basePathRename(self, addName):
        self.basePath = os.path.join(self.basePath, addName + "/")
        pass

    def setBaseCityInfo(self, baseCityInfo):
        self.baseCityInfo = baseCityInfo
        self.printBaseInfo()
        return self

    def format(self):
        self.photoPath = self.basePath + "/" + self.baseCityInfo.deviceType + "/" + self.photoDir + "/" + self.baseCityInfo.cityCode
        self.cityConfPath = self.basePath + "/" + self.baseCityInfo.deviceType + "/" + self.cityConfDir + "/" \
                            + self.baseCityInfo.cityCode + "/" + self.baseCityInfo.dateStr

        self.videoPath = self.basePath + "/" + self.baseCityInfo.deviceType + "/" + self.videoDir + "/" + self.baseCityInfo.cityCode
        return self

    def printBaseInfo(self):
        logger.info("self.baseCityInfo.deviceType:{},self.baseCityInfo.cityCode:{},self.baseCityInfo.dateStr:{}".
                    format(self.baseCityInfo.deviceType, self.baseCityInfo.cityCode, self.baseCityInfo.dateStr))

    def getNewTableName(self):
        """
            获取新的表名
        Returns:
            str 表名
        """
        tableName = "emTest_{deviceType}_{cityCpde}_{dataStr}".format(deviceType=self.baseCityInfo.deviceType,
                                                                      cityCpde=self.baseCityInfo.cityCode,
                                                                      dataStr=self.baseCityInfo.dateStr.replace("-",
                                                                                             ""))
        return tableName

    def getTmpVideoBase(self, isEncode=False):
        EncodeName = ""
        return self.tmpDir + "/" + EncodeName + self.baseCityInfo.deviceType + "/video/" + self.baseCityInfo.cityCode

    def getTmpPhotoBase(self, isEncode=False):
        EncodeName = ""
        if isEncode:
            EncodeName = "encode/"
        return self.tmpDir + "/" + EncodeName + self.baseCityInfo.deviceType + "/" + self.baseCityInfo.cityCode

    def getTmpPhotoPath(self, dateStr=""):
        dateDirName = ""
        if len(dateStr) > 0:
            dateDirName = dateStr
        else:
            dateDirName = self.baseCityInfo.dateStr

        return self.getTmpPhotoBase() + "/" + dateDirName

    def getTmpPhotoDecodePath(self, dateStr=""):
        dateDirName = ""
        if len(dateStr) > 0:
            dateDirName = dateStr
        else:
            dateDirName = self.baseCityInfo.dateStr
        return self.getTmpPhotoBase(True) + "/" + dateDirName

    def getTmpAlgConfPath(self):
        return "{}/{}/{}".format(self.tmpDir, self.baseCityInfo.deviceType, "CheJianConfig")

    def getRootVideoPath(self):
        return self.videoPath

    def getRootPhotoPath(self):
        return self.photoPath

    def getRootAlgConfPath(self):
        return self.cityConfPath

    def getTmpDir(self):
        return self.tmpDir

    def printValue(self):
        print(self.__dict__)


class ReadCompressData:
    def __init__(self, filePath):
        if not os.path.isfile(filePath):
            print("文件格式无法进行处理,{}", filePath)
        print("开始解析文件{} ...", filePath)
        pass


def test_normalConfigure(filepath):
    dsc = DataSaveConf(filepath)
    dsc.printValue()


if __name__ == '__main__':
    # ReadCompressData("/home/public/software/test_photo/bak/chejian.zip")
    test_normalConfigure("./conf/normal.conf.json")
    pass
