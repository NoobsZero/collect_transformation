# encoding: utf-8
"""
@file: wfRenameFuntion.py
@time: 2021/7/29 9:06
@author: Chen
@contact: Afakerchen@em-data.com.cn
@software: PyCharm
"""
import os
import re
import shutil
import pandas
from emCollect.common.baselog import logger
from emCollect.common.readSQLFile import ReadSQLFile
from emCollect.service.dependencies.wf.wfRenameTable import tableFileHandle
from emCollect.tool.mytimeUtil.dataTime import get_time_difference, get_stamp13
from emCollect.tool.myzipUtil.unCompress import parseSourceFile, zip_garcode


def unzipFile(fileDir, jpgFilePathLists=None, tableFilePathLists=None):
    """
        递归解压并返回图片集合和数据集合
    """
    filterLists = ['现场违法审核准确率统计']
    if tableFilePathLists is None:
        tableFilePathLists = []
    if jpgFilePathLists is None:
        jpgFilePathLists = []
    for home, dirs, files in os.walk(fileDir, topdown=True):
        for file in files:
            filePath = os.path.join(home, file)
            if file.endswith(('.rar', '.gz', '.tar', '.zip')):
                res, unCompressObj = parseSourceFile(filePath=filePath)
                if res:
                    if not isinstance(unCompressObj, str):
                        targetPath = unCompressObj.start()
                    else:
                        targetPath = unCompressObj
                    if file.endswith('.zip'):
                        # 处理中文乱码
                        zip_garcode(targetPath)
                    # 删除压缩包
                    os.remove(filePath)
                    jpg, table = unzipFile(targetPath)
                    jpgFilePathLists.extend(jpg), tableFilePathLists.extend(table)
            elif file.endswith('.jpg'):
                jpgFilePathLists.append(filePath)
            elif (file.endswith(('.xls', '.xlsx', '.csv')) or file.startswith('ivvs_source_data')) and any(
                    [x not in file for x in filterLists]):
                tableFilePathLists.append(filePath)
    return jpgFilePathLists, tableFilePathLists


def arrangementHandle(weifa_pd_dic, jpgFilePathLists, specifiedDir):
    """
        根据字典集合[{'原图片名': '新图片名'}, ...]，将原图片改名并移动
    """
    letter_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                   'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    newFileCont = 0
    for jpgFilePath in jpgFilePathLists:
        try:
            oldJpgFilePath = jpgFilePath
            oldJpgPath, oldJpgFileName = os.path.split(oldJpgFilePath)
            newJpgFilePath = os.path.join(specifiedDir, weifa_pd_dic[oldJpgFileName])
            if not os.path.isdir(os.path.dirname(newJpgFilePath)):
                os.makedirs(os.path.dirname(newJpgFilePath))
            shutil.move(oldJpgFilePath, newJpgFilePath)
            newFileCont += 1
        except Exception:
            continue
    # 根据车牌号
    if newFileCont == 0 and re.search(
            r"[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁台琼使领军北南成广沈济空海]{1}[A-Z]{1}[A-Z0-9]{4}[A-Z0-9挂领学警港澳]{1}(?!\d)",
            os.path.split(jpgFilePathLists[0])[1]):
        for jpgFilePath in jpgFilePathLists:
            try:
                oldJpgFilePath = jpgFilePath
                oldJpgPath, oldJpgFileName = os.path.split(oldJpgFilePath)
                for weifaName in weifa_pd_dic.values():
                    newJpgFilePath = os.path.join(specifiedDir, weifaName)
                    if str(weifaName).split('+')[1] in oldJpgFileName:
                        if len(oldJpgFileName.split('_')) == 4 and re.search(r"[a-z]", oldJpgFileName.split('_')[1]):
                            tem_data = newJpgFilePath.split('+')
                            tem_data[-2]: str = 'a' + str(letter_list.index(oldJpgFileName.split('_')[1])+1)
                            newJpgFilePath = '+'.join(tem_data)
                        if not os.path.isdir(os.path.dirname(newJpgFilePath)):
                            os.makedirs(os.path.dirname(newJpgFilePath))
                        shutil.move(oldJpgFilePath, newJpgFilePath)
            except Exception:
                continue
    return specifiedDir


def wfTemplateCheck(pandasHeader):
    wfTemplateOne = ['uuid', '设备编号', '号牌号码', '违法时间', '违法类型代码', '图片名称', '人工结果']
    wfTemplateTwo = ['uuid', 'sbbh', 'hphm', 'wfsj', 'wfxw']
    wfTemplateThree = ['设备编号', '号牌号码', '违法时间', '违法代码', '图片名称', '人工结果']
    wfTemplateFour = ['uuid', '设备编号', '违法时间', '号牌号码', '违法code', '图片名称1']
    return (True if set(pandasHeader) >= set(wfTemplateOne) or set(pandasHeader) >= set(wfTemplateTwo) or set(
        pandasHeader) >= set(wfTemplateThree) or set(pandasHeader) >= set(wfTemplateFour) else False)


def getWeifaPD(filePath):
    """
        通过pandas读取文件中的内容返回DataFrame
    """
    weifa_pd = None
    if filePath.endswith('.sql'):
        sqldata = ReadSQLFile(filePath, sqlHader=('CREATE', 'INSERT'))
        weifa_pd = pandas.DataFrame(sqldata.get_SQL_data(), columns=sqldata.get_SQL_columns())
    elif filePath.endswith('.csv') and wfTemplateCheck(pandas.read_csv(filePath, sep='\t', header=0, nrows=0)):
        weifa_pd = pandas.read_csv(filePath, sep='\t')
    elif wfTemplateCheck(pandas.read_excel(filePath, header=0, nrows=0)):
        weifa_pd = pandas.read_excel(filePath)
    elif wfTemplateCheck(pandas.read_excel(filePath, skiprows=1, header=0, nrows=0)):
        weifa_pd = pandas.read_excel(filePath, skiprows=1)
    return weifa_pd


def run(filePathLists, jpgFilePathLists, specifiedDir, sourceDir):
    """
        主程序
    """
    resourceDir = None
    data = None
    filenames = os.listdir(specifiedDir)
    start = get_stamp13()
    for tableFilePath in filePathLists:
        filename = [filename for filename in filenames if filename in tableFilePath][0]
        try:
            weifa_pd = getWeifaPD(tableFilePath)
            weifa_pd_dic = tableFileHandle(weifa_pd)
            resourceDir = arrangementHandle(weifa_pd_dic, jpgFilePathLists, os.path.join(sourceDir, filename))
            data = {"message": "success", 'time': str(get_time_difference(start))+'s', 'filename': tableFilePath}
        except Exception as e:
            data = {"message": str(e), 'time': str(get_time_difference(start))+'s', 'filename': tableFilePath}
        finally:
            logger.info("info{}".format(data))
            # 删除处理后的文件夹
            shutil.rmtree(os.path.join(specifiedDir, filename))
    return resourceDir


def main(specifiedDir, sourceDir):
    jpgFilePathLists, tableFilePathLists = unzipFile(specifiedDir)
    return run(tableFilePathLists, jpgFilePathLists, specifiedDir, sourceDir)
