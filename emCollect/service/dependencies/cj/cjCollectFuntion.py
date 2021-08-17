# encoding: utf-8
"""
@file: cjCollectFuntion.py
@time: 2021/8/9 13:55
@author: Chen
@contact: Afakerchen@em-data.com.cn
@software: PyCharm
"""
import os

from emCollect import Normal
from emCollect.common.baselog import logger
from emCollect.tool.mytimeUtil.dataTime import getTime
from emCollect.tool.myzipUtil.unCompress import parseSourceFile, zip_garcode

cj = Normal['cj']


def unzipFile(dirPath, srcFilePaths=None):
    if srcFilePaths is None:
        srcFilePaths = []
    if os.path.exists(dirPath):
        for home, dirs, files in os.walk(dirPath, topdown=True):
            for file in files:
                filePath = os.path.join(home, file)
                if file.endswith('.zip'):
                    res, unCompressObj = parseSourceFile(filePath=filePath)
                    if res:
                        if not isinstance(unCompressObj, str):
                            targetPath = unCompressObj.start()
                        else:
                            targetPath = unCompressObj
                        # 处理中文乱码
                        zip_garcode(targetPath)
                        # 删除压缩包
                        os.remove(filePath)
                        srcFilePaths.extend(unzipFile(targetPath))
                elif file.endswith('.tar.gz'):
                    srcFilePaths.append(filePath)
    return srcFilePaths


class UnCompressCenter:
    def __init__(self, dirPath):
        self.srcFilePaths = unzipFile(dirPath)
        self.LOCAL_TIME_NAME = getTime(timeformat="%Y%m%d_%H%M%S")
        self.dbConfPath = Normal['db']['conf']

    def printProcessList(self):
        logger.info("处理文件列表如下:")
        logger.info("")
        logger.info(self.srcFilePaths)

    def start(self):
        logger.info("start .....")
        li_result = []
        countSuccess = 0
        for item in self.srcFilePaths:
            pass
            # isOk, message = self.UnCompressStart(item)
        #     li_result.append((isOk, item, message))
        #     if self.CommandParameter.noMove:
        #         continue
        #     if isOk:
        #         countSuccess += 1
        #         moveTarget2Dir(item, self.getSuccessDir())
        #     else:
        #         moveTarget2Dir(item, self.getFailureDir())
        #         pass
        #
        # if len(li_result) > 0:
        #     ResultContent = []
        #     ResultContent.append("")
        #     ResultContent.append("")
        #     ResultContent.append("处理文件共计:{}个, 成功数量:{}个".format(len(li_result), countSuccess))
        #     ResultContent.append("")
        #     ResultContent.append("the result:")
        #     ResultContent.append("")
        #     ResultContent.append("处理是否成功\t\t\t文件\t\t\t错误信息")
        #     for item in li_result:
        #         ResultContent.append("{}\t{}\t{}".format(item[0], item[1], item[2]))
        #     ResultContent.append("---------------------------the end------------------------------------------")
        #     # 修改不备份
        #     checkDir(self.getResultPath())
        #     fdHandle = open(self.getResultPath() + "/report.txt", 'w')
        #     for item in ResultContent:
        #         logger.info(item)
        #         fdHandle.write(item + "\n")
        #     fdHandle.close()
        # else:
        #     logger.warn("没有 处理结束的压缩文件")

    def UnCompressStart(self, filePath):
        retCode = False
        retMessage = "数据归档失败"
        # try:
        isWuPan = os.path.basename(filePath).find("CJWP") > 0
        isWebExport = os.path.basename(filePath).startswith("emData_")
        upc = None
        if not isWebExport:
            upc = UnCompressItem(filePath=filePath, normalConfPath=normalConfPath, dbConfFile=self.dbConfPath)
            # else:
            #     if isWuPan:
            #         upc = UnCompressItemWebExportWuPan(filePath=filePath, normalConfPath=self.normalConfPath,
            #                                   dbConfFile=self.dbConfPath).setOrmSess(sessOrm)
            #     else:
            #         upc = UnCompressItemWebExport(filePath=filePath, normalConfPath=self.normalConfPath,
            #                                   dbConfFile=self.dbConfPath)
            # if not isWuPan:
            #     upc.callBackGenerateRecord = self.generateRecord
            #     upc.cbInsertFunc = insertMapperCityDataBaseName
            # else:
            #     upc.callBackGenerateRecord = self.generateRecordWuPan
        #         upc.cbInsertFunc = insertMapperCityDataBaseNameWuPan
        #     isOk, mc = upc.start()
        #     if isOk:
        #         #print("@@@@@@@@@@@@@@@@@@@@@@@:",dict(mc) )
        #         retMessage="城市:{} ,日期: {} 归档完毕！".format(mc.cityName,mc.generateDate)
        #         retCode = upc.insertOrmRecordObj(sessOrm, mc)
        #         if not retCode:
        #             retMessage ="{}:映射表_{} 插入失败".format(retMessage,"City_DataBaseName")
        # except TarContentError as ex:
        #     logger.error(ex)
        #     retMessage = "{}:{}".format(retMessage, ex)
        # except Exception as ex:
        #     logger.error(ex)
        #     retMessage = "{}:{}".format(retMessage, ex)
        #     traceback.print_exc()
        # return retCode, retMessage


def test():
    pcenter = UnCompressCenter(cj['tem'])
    pcenter.printProcessList()
    pcenter.start()
