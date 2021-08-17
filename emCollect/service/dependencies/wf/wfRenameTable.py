# encoding: utf-8
"""
@file: wfRenameTable.py
@time: 2021/8/2 10:37
@author: Chen
@contact: Afakerchen@em-data.com.cn
@software: PyCharm
"""
import os
import re
from emCollect.tool.mybaseUtil.getBaseUtil import generateUUID
from emCollect.tool.mytimeUtil.dataTime import getDate


def tableFileHandle(weifa_pd):
    """
        将DataFrame处理后，返回字典集合[{'原图片名': '新图片名'}, ...]
    """
    if 'zpstr1' in list(weifa_pd):
        weifa_tupian_lis = [i for i in list(weifa_pd) if 'zpstr' in i]
        weifa_pd = weifa_pd.rename(
            columns={'sbbh': '设备编号', 'hpzl': '车牌类型', 'hphm': '号牌号码', 'wfsj': '违法时间', 'wfxw': '违法类型代码'})
        weifa_pd['人工结果'] = 0
    else:
        if '违法代码' in list(weifa_pd):
            weifa_pd = weifa_pd.rename(columns={'违法代码': '违法类型代码'})
        if '违法code' in list(weifa_pd):
            weifa_pd = weifa_pd.rename(columns={'违法code': '违法类型代码'})
        if 'uuid' not in list(weifa_pd):
            weifa_pd['uuid'] = weifa_pd.index.to_series().map(lambda x: generateUUID())
        if '车牌类型' not in list(weifa_pd):
            weifa_pd['车牌类型'] = ''
        weifa_tupian_lis = [i for i in list(weifa_pd) if '图片名称' in i]
    weifa_tupian = weifa_pd[weifa_tupian_lis].stack().reset_index(level=1)
    weifa_tupian.columns = ['图片ID', '图片名称']
    weifa_tupian = weifa_tupian[(weifa_tupian['图片名称'] != '') & (weifa_tupian['图片名称'] != 'NULL')]
    weifa_pd.drop(list(set(weifa_pd) - {'uuid', '设备编号', '号牌号码', '违法类型代码', '车牌类型', '违法时间', '人工结果'}),
                  axis=1, inplace=True)
    weifa_pd = weifa_pd.join(weifa_tupian)
    weifa_pd = weifa_pd.reindex(
        columns=['uuid', '设备编号', '号牌号码', '违法类型代码', '车牌类型', '违法时间', '人工结果', '图片ID', '图片名称']).astype(
        str)
    weifa_pd.loc[:, '违法时间'] = weifa_pd['违法时间'].apply(lambda x: re.sub(r'[- ]', '#', str(getDate(x))))
    weifa_pd.loc[:, '人工结果'] = weifa_pd['人工结果'].apply(
        lambda x: str(x.replace('nan', '0').replace('不违法', '2').replace('未违法', '2').replace('违法', '1')))
    weifa_pd.loc[:, '图片ID'] = weifa_pd['图片ID'].apply(lambda x: 'a' + str(re.sub(r'\D', '', x)))
    weifa_pd.loc[:, '新图片名称'] = weifa_pd['违法类型代码'] + '/' + weifa_pd['设备编号'] + '/' + weifa_pd['设备编号'] + '+' + weifa_pd[
        '号牌号码'] + '+' + weifa_pd['违法类型代码'] + '+' + weifa_pd['设备编号'] + '+' + weifa_pd['车牌类型'] + '+0+@' + weifa_pd[
                                   'uuid'] + '@@@' + weifa_pd['违法时间'] + '+' + weifa_pd['图片ID'] + '+' + weifa_pd[
                                   '人工结果'] + '.jpg'
    weifa_pd.loc[:, '新图片名称'] = weifa_pd['新图片名称'].apply(lambda x: x.replace('nan', ''))
    weifa_pd = weifa_pd.reindex(columns=['图片名称', '新图片名称'])
    weifa_pd.loc[:, '图片名称'] = weifa_pd['图片名称'].apply(lambda x: os.path.split(x)[-1])
    weifa_pd_index_lis = weifa_pd.index.tolist()
    for i in [i for i in weifa_pd_index_lis if weifa_pd_index_lis.count(i) < 2]:
        weifa_pd.loc[i, '新图片名称'] = weifa_pd.loc[i, '新图片名称'].replace('a', 'a0').replace('a1', 'a0')
    weifa_pd_dic = weifa_pd.set_index("图片名称").to_dict()["新图片名称"]
    return weifa_pd_dic
