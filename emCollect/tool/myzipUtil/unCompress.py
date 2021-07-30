# -*- encoding:utf-8 -*-
"""
@File   :unCompress.py
@Time   :2021/2/26 11:00
@Author :Chen
@Software:PyCharm
"""
import logging
import tarfile
import zipfile
import chardet
import rarfile
import gzip
from emCollect.tool.mybaseUtil.getBaseUtil import *
from emCollect.tool.mydirUtil.getDirUtil import *


def preStart(tmpDir):
    try:
        if os.path.exists(tmpDir):
            shutil.rmtree(tmpDir)
        os.makedirs(tmpDir)
    except Exception as e:
        logger.error("临时文件创建失败:{}".format(e))
        return False
    return True


def zip_garcode(dir):
    for temp_name in os.listdir(dir):
        name = os.path.join(dir, temp_name)
        try:
            new_name = name.replace(temp_name, temp_name.encode('cp437').decode('gbk'))
            os.rename(name, new_name)
            name = new_name
        except:
            pass
        if os.path.isdir(name):
            zip_garcode(name)


class Uncompress:
    def __init__(self, targetPath):
        self.fd = None
        self.tmpFilePath = ""
        self.targetPath = targetPath
        self.objProgress = None
        self.decodeVersion = ""

    def filterSpecialFIle(self, name, index):
        logger.debug("name:{}".format(name))
        if logger.level > logging.DEBUG:
            self.objProgress.progressBarFlush(index)

    def getFileList(self):
        return []

    def start(self, systemType='linux'):
        self.objProgress = BaseProgressBar(len(self.getFileList()))
        if checkDir(self.targetPath) < 0:
            return False
        index = 0
        for name in self.getFileList():
            self.filterSpecialFIle(name, index)
            # win系统特殊字符需要替换
            if systemType == 'windows':
                print(type(self.fd.namelist()))
                for fn in self.fd:
                    fn.name = re.sub(r'[\/:*?"<>|]', '_', fn.name)
                name = re.sub(r'[\/:*?"<>|]', '_', name)
            self.fd.extract(name, self.targetPath)
            index += 1
        self.fd.close()
        return self.targetPath


class unCompressZIP(Uncompress):
    """
        unCompressZIP
            解压zip压缩包
    Args:
        filePath: 原始路径
        targetPath: 目标路径
        specifiedDirectory: 指定解压路径（包含判断）
    """

    def __init__(self, filePath, targetPath, specifiedDirectory):
        super().__init__(targetPath)
        self.getHandle(filePath)
        self.specifiedDirectory = specifiedDirectory

    def getHandle(self, srcPath):
        self.fd = zipfile.ZipFile(srcPath)

    def getFileList(self):
        if self.specifiedDirectory is not None:
            return [file for file in self.fd.namelist() if self.specifiedDirectory in file]
        else:
            return self.fd.namelist()




class unCompressTGZ(Uncompress):
    """
        unCompressTGZ
            解压tgz压缩包
    Args:
        filePath: 原始路径
        targetPath: 目标路径
    """

    def __init__(self, filePath, targetPath):
        super().__init__(targetPath)
        self.getHandle(filePath)

    def getHandle(self, srcPath):
        self.fd = tarfile.open(srcPath)

    def getFileList(self):
        return self.fd.getnames()


class unCompressRAR(Uncompress):
    """
        unCompressRAR
            解压rar压缩包
    Args:
        filePath: 原始路径
        targetPath: 目标路径
    """

    def __init__(self, filePath, targetPath):
        super().__init__(targetPath)
        self.getHandle(filePath)

    def getHandle(self, srcPath):
        self.fd = rarfile.RarFile(srcPath)

    def getFileList(self):
        return self.fd.namelist()


class unCompressGZ(Uncompress):
    """
        unCompressGZ
            解压rar压缩包
    Args:
        filePath: 原始路径
        targetPath: 目标路径
    """

    def __init__(self, filePath, targetPath):
        super().__init__(targetPath)
        self.getHandle(filePath)

    def getHandle(self, srcPath):
        self.fd = gzip.GzipFile(srcPath)

    def getFileList(self):
        return self.fd.filename()


def parseSourceFile(filePath, targetPath=None, specifiedDirectory=None):
    """
        解压源文件
    Args:
        specifiedDirectory: 指定解压路径（包含判断）
        filePath: 原始路径
        targetPath: 目标路径

    Returns:

    """
    if not os.path.isfile(filePath):
        print("不是一个压缩文件", filePath)
        return False, None
    print("开始解析文件 ...", filePath)

    strTail = ""
    if filePath.endswith(".zip"):
        if targetPath is None:
            targetPath = filePath.rstrip('.zip')
        un_compress_obj = unCompressZIP(filePath, targetPath, specifiedDirectory)
        strTail = ".zip"
    elif filePath.endswith(".tar.gz"):
        if targetPath is None:
            targetPath = filePath.rstrip('.tar.gz')
        un_compress_obj = unCompressTGZ(filePath, targetPath)
        strTail = ".tar.gz"
    elif filePath.endswith(".rar"):
        if targetPath is None:
            targetPath = filePath.rstrip('.rar')
        un_compress_obj = unCompressRAR(filePath, targetPath)
        strTail = ".rar"
    elif filePath.endswith(".gz"):
        if targetPath is None:
            targetPath = filePath.rstrip('.gz')
        un_compress_obj = unCompressGZ(filePath, targetPath)
        strTail = ".gz"
    else:
        print("文件格式无法进行处理,[%s]{}", strTail, filePath)
        return False, None
    fileName = os.path.basename(filePath)
    fendNameLi = fileName.split("V.")
    decodeVersion = ""
    if len(fendNameLi) == 2:
        tmpVersion = fendNameLi[1]
        if tmpVersion.endswith(strTail):
            decodeVersion = tmpVersion.split(".")[0]
    un_compress_obj.decodeVersion = decodeVersion
    return True, un_compress_obj


def decompressionZIP(dirs):
    """
        linux压缩包解压
            注意：由于目录中存在一些特殊字符全部替换成'_'，避免后续操作带来不便（可以使用path_remake解决后续也需使用）
    :param dirs: 扫描目录
    """
    index = 0
    while True:
        index += 1
        zip = get_filelist(dirs, 'zip')
        for i in zip:
            new_file_name = i.split('/')[-1]
            old_file_name = i.split('/')[-1]
            for tu in ['(', ')', ' ', '-', '#', ';', '$', '!', '@', '&', '\\', '"']:
                new_file_name = new_file_name.replace(tu, '_')
            new_file_name = i.replace(old_file_name, new_file_name)
            if i != new_file_name:
                os.system('mv ' + "'" + i + "'" + ' ' + new_file_name)
            i = new_file_name
            pathname, filename = os.path.split(i)
            newpath = os.path.join(pathname, filename.split('.')[0], '')
            if not os.path.isdir(newpath):
                os.system('mkdir ' + newpath)
            os.system('echo ' + i + ' ... ...')
            if filename.endswith('.gz') or filename.endswith('tar'):
                os.system('tar -xf ' + i + ' -C ' + newpath + ' && rm ' + i)
            elif filename.endswith('zip'):
                lis_sub_zip = getZipSubsection(filename, zip)
                if len(lis_sub_zip) > 0:
                    i_pathname, i_filename = os.path.split(i)
                    new_i = os.path.join(i_pathname[0], 'all_' + i_filename[-1])
                    os.system('mv ' + i + ' ' + new_i)
                    for sub_zip in lis_sub_zip:
                        os.system('cat ' + sub_zip + ' > ' + i + ' && rm ' + sub_zip)
                    os.system('unzip -O gbk ' + new_i + ' -d ' + newpath + ' && rm ' + new_i)
                else:
                    os.system('unzip -O gbk ' + i + ' -d ' + newpath + ' && rm ' + i)
            elif filename.endswith('.rar') and ('.part' not in filename):
                os.system('rar e -o+ -y ' + i + ' -C ' + newpath + ' && rm ' + i)
            os.system('echo ' + i + ' ok')
        delDir(dirs)
        if len(get_filelist(dirs, 'zip')) == 0 or index >= 3:
            break


if __name__ == '__main__':
    downloadDir = r'G:\chejian'
    specifiedDir = r'G:\test'
    for dirname in os.listdir(downloadDir):
        downloadFile = os.path.join(downloadDir, dirname)
        if dirname.endswith(".zip") and os.path.isfile(downloadFile):
            # PLUS
            res, unCompressObj = parseSourceFile(filePath=downloadFile,
                                                 targetPath=specifiedDir,
                                                 specifiedDirectory='/CONUS/MergedReflectivityQC/')
            if res:
                unCompressObj.start()
