# -*- encoding:utf-8 -*-
# coding=utf-8
import fnmatch
import glob
import os
import shutil
import tempfile

from emCollect.common.baselog import logger


def project_root_path(project_name=None):
    """
        获取当前项目根路径
        :param project_name:
        :return: 根路径
    """
    PROJECT_NAME = 'untitled' if project_name is None else project_name
    project_path = os.path.abspath(os.path.dirname(__file__))
    root_path = project_path[:project_path.find("{}\\".format(PROJECT_NAME)) + len("{}\\".format(PROJECT_NAME))]
    # print('当前项目名称：{}\r\n当前项目根路径：{}'.format(PROJECT_NAME, root_path))
    return root_path


def checkDir(targetPath):
    """
        判断目录是否存在，不存在则创建
    Args:
        targetPath: 路径

    Returns:成功：0 失败：-1

    """
    Flag = 0
    if os.path.isdir(targetPath):
        pass
    else:
        try:
            os.makedirs(targetPath)
        except Exception as e:
            logger.error("文件夹创建失败{}".format(targetPath))
            logger.error("error:{}".format(e))
            Flag = -1
        Flag = 1
    return Flag


def preStart(fun):
    """
    创建临时目录(函数运行结束，自动删除临时目录)
    Args:
        fun: 目录路径

    Returns:boolean

    """
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            fun(tmpdir)
    except Exception as e:
        logger.error("临时文件创建失败:{}".format(e))
        return False
    return True


def mvDirToDir(root_src_dir, root_dst_dir):
    """
        移动目录下所有文件到目录
    :param root_src_dir: 源目录
    :param root_dst_dir: 指定目录

    """
    root_src_dir = os.path.join(os.getcwd(), root_src_dir, '')
    root_dst_dir = os.path.join(os.getcwd(), root_dst_dir, '')
    print(str(root_src_dir) + " to " + str(root_dst_dir))
    for src_dir, dirs, files in os.walk(root_src_dir):
        dst_dir = src_dir.replace(root_src_dir, root_dst_dir, 1)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)
            if os.path.exists(dst_file):
                # in case of the src and dst are the same file
                if os.path.samefile(src_file, dst_file):
                    continue
                os.remove(dst_file)
            shutil.move(src_file, dst_file)
    delDir(root_src_dir)


def moveFileToDir(root_src_file, root_dst_dir):
    """
        移动文件到目录
    :param root_src_file: 源文件
    :param root_dst_dir: 指定目录
    """
    if os.path.isfile(root_src_file):
        if not os.path.exists(root_dst_dir):
            os.makedirs(root_dst_dir)
        root_dst_file = os.path.join(root_dst_dir, os.path.split(root_src_file)[-1])
        root_dst_lis = get_filelist(root_dst_dir)
        if root_dst_file in root_dst_lis:
            new_i = os.path.split(root_dst_file)
            new_root_src_file = os.path.join(new_i[0],
                                             os.path.split(os.path.split(root_dst_file)[0])[-1] + '_' + new_i[-1])
            os.renames(root_src_file, new_root_src_file)
        else:
            shutil.move(root_src_file, root_dst_file)


def get_filelist(dir, fileCondition='', topdown=True):
    """
            递归获取目录下所有后缀为suffix的路径
        :param fileCondition:后缀为(zip:压缩包, sql:sql文件, suffix:jpg路径和非jpg文件路径, '':所有文件路径)
        :param dir: 指定URL是目录（'dir'）
        :return: Filelist:list URL集合
        """
    Filelist = []
    suffix = ['.ini', '.local', 'log', '.log', '.DAT', '.xlsx', '.z01', '.json', '.rar', '.zip', '.cer', '.py', '.exe',
              '.sh',
              '.txt',
              '.html', '.dll', '.h', '.c',
              '.cpl', '.jsa', '.md', '.properties', '.jar', '.data', '.bfc', '.src', '.ja', '.dat', '.cfg',
              '.pf', '.gif', '.ttf', '.jfc', '.access', '.template', '.certs', '.policy', '.security', '.libraries',
              '.sym', '.idl', '.lib', '.clusters', '.conf', '.xml', '.tar', '.gz', '.csv', '.sql', '.xml_hidden',
              '.lic']
    list_jpg_dir = []
    for home, dirs, files in os.walk(dir, topdown=topdown):
        for filename in files:
            # 文件名列表，包含完整路径
            if fileCondition == 'zip':
                if filename.endswith('.rar') or filename.endswith('.gz') or filename.endswith('.tar') or \
                        os.path.splitext(filename)[-1].endswith('.z', 0, 2) and (
                        'sql' not in filename):
                    Filelist.append(os.path.join(home, filename))
            elif fileCondition == 'sql':
                if filename.endswith('.sql'):
                    Filelist.append(os.path.join(home, filename))
            elif fileCondition == 'rar':
                if filename[-3:] == 'rar':
                    Filelist.append(os.path.join(home, filename))
            elif fileCondition == 'suffix':
                if os.path.splitext(filename)[1] in suffix or filename[-3:] in suffix:
                    Filelist.append(os.path.join(home, filename))
                elif home not in list_jpg_dir:
                    list_jpg_dir.append(home)
            elif fileCondition == '':
                Filelist.append(os.path.join(home, filename))
    if fileCondition == 'suffix':
        return Filelist, list_jpg_dir
    else:
        return Filelist


def delDir(dirPath):
    """
        递归删除指定目录下空文件及目录
        :param dirPath:目录路径
    """
    for root, dirs, files in os.walk(dirPath, topdown=False):
        for file in files:
            src_file = os.path.join(root, file)
            if os.path.getsize(src_file) == 0:
                os.remove(src_file)
    for root, dirs, files in os.walk(dirPath, topdown=False):
        if not os.listdir(root):
            os.system('rmdir ' + root)


def getZipSubsection(sc, lis):
    lis_sub_zip = []
    sc_file = os.path.splitext(sc)[0]
    for k in lis:
        if sc_file in k and sc not in k:
            lis_sub_zip.append(k)
    return lis_sub_zip


def path_remake(path):
    """
        解决python读取linux路径中存在特殊字符无法识别的情况
    Args:
        path: 字符串或路径

    Returns:字符串或路径

    """
    return path.replace(' ', '\ ').replace('(', '\(').replace(')', '\)')


def dir_matches(matches: list = None):
    """
        匹配以点（。）开头的文件的情况; 像当前目录中的文件或基于Unix的系统上的隐藏文件，请使用os.walk下面的解决方案
    Args:
        matches:list

    Returns:

    """
    if matches is None:
        matches = []
    for root, dirnames, filenames in os.walk('src'):
        for filename in fnmatch.filter(filenames, '*.c'):
            matches.append(os.path.join(root, filename))
    return matches


if __name__ == '__main__':
    # 递归匹配后缀jp、pn文件
    for locationDir in glob.glob('F:\chejian\**\*.[jp][pn]g', recursive=True):
        print(locationDir)
    # print('葵花解压手')
    # sqlPath = os.path.join(os.path.abspath(os.path.dirname(os.getcwd())),'sql','')
    # decompressionZIP(os.getcwd(),sqlPath)
    # print('乾坤大挪移')
    # root_dst_dir={}
    # for root_src_dir in root_dst_dir:
    #     mvFileToDir(root_src_dir, root_dst_dir[root_src_dir])
    # print('佛山清空脚')
    # delDir(os.getcwd())
    # print('万花写轮眼')
    # dic = get_filelist(os.getcwd(), 'if')
    # print('------------------输出文件-------------------------------')
    # for i in dic:
    #     print(i)
    # print('------------------------------------------------------------')
