# encoding: utf-8
"""
@file: getStrUtil.py
@time: 2021/6/23 10:48
@author: Chen
@contact: Afakerchen@em-data.com.cn
@software: PyCharm
"""

import re
import xpinyin


def getPinyin(charStr):
    """
        获取中文拼音
    Returns: 拼音
    """
    ret = ""
    if len(charStr) > 0:
        ret = xpinyin.Pinyin().get_pinyin(charStr, "")
    return ret


def is_all_chinese(charStr):
    """
        判断是否是中文
    :return: boolean
    """
    for _char in charStr:
        if not '\u4e00' <= _char <= '\u9fa5':
            return False
    return True


def is_number(charStr):
    """
        判断字符串是否为数字
    Returns:bool

    """
    try:
        float(charStr)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(charStr)
        return True
    except (TypeError, ValueError):
        pass
    return False


def numChineseCharacters(charStr):
    """
        接收一个字符串返回该字符串中有多少中文字符
    Returns: int
    """
    return len(re.findall('([\u4e00-\u9fa5])', charStr))


def numNumbers():
    """
        接收一个字符串返回该字符串中有多少数字
    Returns: int
    """
    str_sum = 0
    dig_sum = 0
    spa_sum = 0
    for strs in str1:
        if strs.isalpha():
            str_sum += 1
        elif strs.isdigit():
            dig_sum += 1
        elif strs == ' ':
            spa_sum += 1
        else:
            dig_sum += 1
    return dig_sum


if __name__ == '__main__':
    print(numChineseCharacters('中国'))
