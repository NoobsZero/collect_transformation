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
from emCollect import Normal
from emCollect.tool.myzipUtil.unCompress import parseSourceFile, zip_garcode

specifiedDir = Normal['wfTem']
sourceDir = Normal['wfSource']


def unzipFile(fileDir, jpgFilePathLists=None, sqlFilePathLists=None, tableFilePathLists=None):
    filterLists = ['现场违法审核准确率统计']
    if tableFilePathLists is None:
        tableFilePathLists = []
    if sqlFilePathLists is None:
        sqlFilePathLists = []
    if jpgFilePathLists is None:
        jpgFilePathLists = []
    for home, dirs, files in os.walk(fileDir, topdown=True):
        for file in files:
            filePath = os.path.join(home, file)
            if file.endswith(('.rar', '.gz', '.tar', '.zip')):
                res, unCompressObj = parseSourceFile(filePath=filePath)
                if res:
                    targetPath = unCompressObj.start()
                    if file.endswith('.zip'):
                        zip_garcode(targetPath)
                    os.remove(filePath)
                    jpg, sql, table = unzipFile(targetPath)
                    jpgFilePathLists.extend(jpg), sqlFilePathLists.extend(sql), tableFilePathLists.extend(table)
            elif file == 'ivvs_source_data.sql':
                sqlFilePathLists.append(filePath)
            elif file.endswith('.jpg'):
                jpgFilePathLists.append(filePath)
            elif file.endswith(('.xls', '.xlsx')) and any([x not in file for x in filterLists]):
                tableFilePathLists.append(filePath)
            else:
                os.remove(filePath)
    return jpgFilePathLists, sqlFilePathLists, tableFilePathLists


def tableFileHandle(weifa_pd):
    weifa_tupian_lis = [i for i in list(weifa_pd) if '图片名称' in i]
    weifa_tupian = weifa_pd[weifa_tupian_lis].stack().reset_index(level=1)
    weifa_tupian.columns = ['图片ID', '图片名称']
    weifa_pd = weifa_pd.drop(weifa_tupian_lis, axis=1).join(weifa_tupian)
    weifa_pd = weifa_pd.reindex(
        columns=['uuid', '设备编号', '号牌号码', '违法类型代码', '车牌类型', '违法时间', '人工结果', '图片ID', '图片名称']).astype(
        str)
    weifa_pd.loc[:, '违法时间'] = weifa_pd['违法时间'].apply(lambda x: re.sub(r':| ', '#', x))
    weifa_pd.loc[:, '人工结果'] = weifa_pd['人工结果'].apply(
        lambda x: str(x.replace('nan', '0').replace('不违法', '2').replace('未违法', '2').replace('违法', '1')))
    weifa_pd.loc[:, '图片ID'] = weifa_pd['图片ID'].apply(lambda x: 'a' + str(re.sub(r'\D', '', x)))
    weifa_pd.loc[:, '新图片名称'] = weifa_pd['违法类型代码'] + '/' + weifa_pd['设备编号'] + '/' + weifa_pd['设备编号'] + '+' + weifa_pd[
        '号牌号码'] + '+' + weifa_pd['违法类型代码'] + '+' + weifa_pd['设备编号'] + '+' + \
                               weifa_pd[
                                   '车牌类型'] + '+0+@' + weifa_pd['uuid'] + '@@@' + weifa_pd['违法时间'] + '+' + weifa_pd[
                                   '图片ID'] + '+' + weifa_pd[
                                   '人工结果'] + '.jpg'
    weifa_pd.loc[:, '新图片名称'] = weifa_pd['新图片名称'].apply(lambda x: x.replace('nan', ''))
    weifa_pd = weifa_pd.reindex(columns=['图片名称', '新图片名称'])
    weifa_pd.loc[:, '图片名称'] = weifa_pd['图片名称'].apply(lambda x: os.path.split(x)[-1])
    weifa_pd_index_lis = weifa_pd.index.tolist()
    for i in [i for i in weifa_pd_index_lis if weifa_pd_index_lis.count(i) < 2]:
        weifa_pd.loc[i, '新图片名称'] = weifa_pd.loc[i, '新图片名称'].replace('a', 'a0').replace('a1', 'a0')
    weifa_pd_dic = weifa_pd.set_index("图片名称").to_dict()["新图片名称"]
    return weifa_pd_dic


def arrangementHandle(weifa_pd_dic, jpgFilePathLists, specifiedDir):
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
        except Exception as e:
            continue


def un():
    jpgFilePathLists, sqlFilePathLists, tableFilePathLists = unzipFile(specifiedDir)
    filename = sorted(os.listdir(specifiedDir), key=lambda fn: os.path.getmtime(os.path.join(specifiedDir, fn)),
                      reverse=True)[0]
    wfTemplate = ['uuid', '设备编号', '号牌号码', '违法时间', '违法类型代码', '图片名称', '人工结果']
    for tableFilePath in tableFilePathLists:
        weifa_pd = pandas.read_excel(tableFilePath)
        if set(weifa_pd) >= set(wfTemplate):
            weifa_pd_dic = tableFileHandle(weifa_pd)
            arrangementHandle(weifa_pd_dic, jpgFilePathLists, os.path.join(sourceDir, filename))
    # print(len(jpgFilePathLists))
    # print(sqlFilePathLists)
    # print(tableFilePathLists)
