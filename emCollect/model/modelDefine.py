from sqlalchemy import Column, String, Date, Integer, Text, DATETIME
from .modelBase import *


# 定义User对象:
class MapperCityDataBaseName(Base):
    # 表的名字:

    __tablename__ = 'City_DataBaseName'
    # 表的结构:
    mID = Column(Integer(), primary_key=True)
    dbname = Column(String(64))
    cityCode = Column(String(4))
    cityName = Column(String(32))
    cityPinYin = Column(String(32))
    generateDate = Column(Date())
    index = Column(String(2))
    subPath = Column(String(128))
    otherInfo = Column(Text())
    inDbTime = Column(DATETIME())
    deviceType = Column(String(20))
    algConfPath = Column(String(128))
    photoPath = Column(String(128))

    def __init__(self, mid=0, dbname="", cityCode="", cityName="", cityPinYin="", generateDate="", index="", subPath="",
                 otherinfo="", inDbTime="", deviceType="chejian", algConfPath="", photoPath=""):
        self.generateDate = generateDate
        self.mID = mid
        self.cityCode = cityCode
        self.cityName = cityName
        self.index = index
        self.cityPinYin = cityPinYin
        self.algConfPath = algConfPath
        self.photoPath = photoPath
        self.deviceType = deviceType
        self.inDbTime = inDbTime
        self.otherInfo = otherinfo
        self.subPath = subPath
        self.dbname = dbname
        self.otherInfo = otherinfo
        # self.inDbTime =

    def generateDbName(self, baseName):
        self.dbname = baseName
        if len(self.cityCode) > 0:
            self.dbname += "-" + self.cityCode
        if len(self.cityPinYin) > 0:
            self.dbname += "-" + self.cityPinYin
        if len(self.index):
            self.dbname += "-" + self.index
        if len(self.generateDate):
            self.dbname += "-" + self.generateDate

        return self

    def toString(self):
        print(self.__dict__)


# 定义User对象:
class MapperCityDataBaseNameWuPan(Base):
    # 表的名字:

    __tablename__ = 'City_DataBaseName_WuPan'
    # 表的结构:
    mID = Column(Integer(), primary_key=True)
    dbname = Column(String(64))
    cityCode = Column(String(4))
    cityName = Column(String(32))
    cityPinYin = Column(String(32))
    generateDate = Column(Date())
    # 设备编号
    index = Column(String(2))
    subPath = Column(String(128))
    otherInfo = Column(Text())
    inDbTime = Column(DATETIME())
    deviceType = Column(String(20))
    algConfPath = Column(String(128))
    photoPath = Column(String(128))
    # 压缩包名称
    packageName = Column(String(128))
    # number  导入编号
    number = Column(String(2))

    def __init__(self, mid=0, dbname="", cityCode="", cityName="", cityPinYin="", generateDate="", index="", subPath="",
                 otherinfo="", inDbTime="", deviceType="chejian", algConfPath="", photoPath="", packageName="",
                 number="00"):
        self.generateDate = generateDate
        self.mID = mid

        self.cityCode = cityCode
        self.cityName = cityName
        self.index = index
        self.cityPinYin = cityPinYin
        self.algConfPath = algConfPath
        self.photoPath = photoPath
        self.deviceType = deviceType
        self.inDbTime = inDbTime
        self.otherInfo = otherinfo
        self.subPath = subPath
        self.dbname = dbname
        self.otherInfo = otherinfo

        self.packageName = packageName
        self.number = number

    def generateDbName(self, baseName):
        self.dbname = baseName
        if len(self.cityCode) > 0:
            self.dbname += "-" + self.cityCode
        if len(self.cityPinYin) > 0:
            self.dbname += "-" + self.cityPinYin
        if len(self.index):
            self.dbname += "-" + self.index
        if len(self.generateDate):
            self.dbname += "-" + self.generateDate

        return self

    def toString(self):
        print(self.__dict__)
