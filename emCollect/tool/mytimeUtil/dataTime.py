# -*- encoding:utf-8 -*-
"""
@File   :dataTime.py
@Time   :2021/2/26 16:44
@Author :Chen
@Software:PyCharm
"""
import os
import re
from datetime import datetime
from dateutil.parser import parse
import time

from emCollect.tool.mystrUtil.getStrUtil import is_number


def getTime(timestamp=time.localtime(), timeformat="%Y-%m-%d %H:%M:%S"):
    """
    获取当前时间
    Args:
        timestamp: 时间戳
        timeformat: 时间格式

    Returns:格式化的时间

    """
    return time.strftime(timeformat, timestamp)


def getStampToTime(timestamp, timeformat="%Y-%m-%d %H:%M:%S"):
    """
    时间戳转换日期
    Args:
        timestamp: 时间戳
        timeformat: 时间格式

    Returns: 格式化的时间

    """
    timeStruct = time.localtime(timestamp)
    return getTime(timestamp=timeStruct, timeformat=timeformat)


def getTimeToStamp(times, timeformat="%Y-%m-%d %H:%M:%S"):
    """
        日期转换时间戳
        Args:
            times: 日期
            timeformat: 时间格式

        Returns: 时间戳

        """
    timeArray = time.strptime(times, timeformat)
    return int(time.mktime(timeArray))


def get_stamp13(datetime_obj=None):
    """

    Args:
        datetime_obj:

    Returns:

    """
    if datetime_obj is None:
        t = time.time()
        return int(round(t * 1000))
    # 生成13时间戳   eg:1557842280000
    datetime_obj = datetime.strptime(datetime_obj, '%Y-%m-%d %H:%M:%S.%f')
    # datetime_str = datetime.datetime.strftime(datetime_obj, '%Y-%m-%d %H:%M:%S.%f')
    # # 10位，时间点相当于从1.1开始的当年时间编号
    date_stamp = str(int(time.mktime(datetime_obj.timetuple())))
    # # 3位，微秒
    data_microsecond = str("%06d" % datetime_obj.microsecond)[0:3]
    date_stamp = date_stamp + data_microsecond
    return int(date_stamp)


def get_stamp13Totime(date_stamp):
    if is_number(date_stamp):
        d = datetime.fromtimestamp(int(date_stamp) / 1000)
        date_str = d.strftime("%Y-%m-%d %H:%M:%S.%f")
        return date_str
    else:
        raise ValueError('invalid literal for int() with base 10: {}' % date_stamp)


def getDate(time_dst_dir):
    """
    判断字符串中是否有符合时间规范的数据
    Args:
        time_dst_dir: 字符串或url

    Returns:字符串或url

    """
    time_t1 = re.search(r'^(\d{4}-\d{2}-\d{2})', str(time_dst_dir))
    time_t2 = re.search(r'^(\d{4}\d{2}\d{2})', str(time_dst_dir))
    time_t3 = re.search(r'^(\d{4}年\d{2}月\d{2}日)', str(time_dst_dir))
    time_t4 = re.search(r'^(\d{1,2}/\d{1,2}/\d{4})', str(time_dst_dir))
    time_t5 = re.search(r'^(\d{4}:\d{2}:\d{2})', str(time_dst_dir))
    if time_t1:
        return time_t1.group(1)
    elif time_t2 and validate(time_t2.group(1)):
        return parse(time_t2.group(1)).strftime('%Y-%m-%d')
    elif time_t3:
        return parse(re.sub(r'\D', "", time_t3.group(1))).strftime('%Y-%m-%d')
    elif time_t4:
        return parse(time_t4.group(1)).strftime('%Y-%m-%d')
    elif time_t5:
        return parse(time_t5.group(1)).strftime('%Y-%m-%d')
    else:
        return None


def get_time_difference(start_stamp, end_stamp=None, sub='s'):
    """
        获取时间差
    Args:
        sub: s：秒 M：分
        start_stamp: 开始时间
        end_stamp: 结束时间

    Returns: int

    """
    if end_stamp is None:
        end_stamp = get_stamp13()
    start_timeworn, end_timeworn = None, None
    if is_number(start_stamp) and is_number(end_stamp):
        if len(str(start_stamp)) == 13:
            start_stamp = get_stamp13Totime(start_stamp)
            start_timeworn = '%Y-%m-%d %H:%M:%S.%f'
        elif len(str(start_stamp)) == 10:
            start_stamp = getStampToTime(start_stamp)
            start_timeworn = '%Y-%m-%d %H:%M:%S'
        if len(str(end_stamp)) == 13:
            end_stamp = get_stamp13Totime(end_stamp)
            end_timeworn = '%Y-%m-%d %H:%M:%S.%f'
        elif len(str(end_stamp)) == 10:
            end_stamp = getStampToTime(end_stamp)
            end_timeworn = '%Y-%m-%d %H:%M:%S'
        time_1_struct = datetime.strptime(start_stamp, start_timeworn)
        time_2_struct = datetime.strptime(end_stamp, end_timeworn)
        total_seconds = (time_2_struct - time_1_struct).total_seconds()
        if sub == 's':
            return int(total_seconds)
        if sub == 'M':
            return int(total_seconds / 60)
        if sub == 'H':
            return round(total_seconds / 60 / 60)
        if sub == 'd':
            return round(round(total_seconds / 60 / 60) / 24)


def validate(date_text, timeworn='%Y-%m-%d'):
    """
        时间检验，注意文件时间要符合日期规则超出无效！
    :param timeworn:
    :param date_text: 字符串
    :return: boolean
    """
    try:
        datetime.strptime(date_text, timeworn)
        retie = True
    except ValueError:
        retie = False
    return retie


def getLisDirTime(zip_url, urllis):
    """
        递归算法获取当前目录下，所有符合时间校验的子目录的时间（默认是'%Y-%m-%d'格式，多个格式需修改）
    :param zip_url: url
    :param urllis: list
    :return:
    """
    for urlName in os.listdir(zip_url):
        url = os.path.join(zip_url, urlName)
        if os.path.isdir(url):
            if not validate(urlName):
                getLisDirTime(url, urllis)
            else:
                # 需要所有符合条件的子目录替换成url
                urllis.append(urlName)
    return urllis


if __name__ == '__main__':
    # print(get_time_difference('1614326441000', get_stamp13(), sub='H'))
    print(get_stamp13Totime(get_stamp13()))
