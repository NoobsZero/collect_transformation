# encoding: utf-8
"""
@file: baseDBOperate.py
@time: 2021/7/27 17:36
@author: Chen
@contact: Afakerchen@em-data.com.cn
@software: PyCharm
"""
import os
import pymysql
from .baseConfig import BaseConfig
from .baselog import logger


class DbConfigure:
    def __init__(self, configPath='./conf/db.conf.json'):
        """
        DbConfigure类
            读取数据库配置文件
        Args:
            configPath: 数据库配置文件路径
        """
        self.host = "127.0.0.1"
        self.port = 3306
        self.user = "root"
        self.passwd = "root"
        self.db = "test"

        self.objMap = BaseConfig().loadConf(configPath).objMap
        self.InitFromConfigure(self.objMap)

    def getSource(self):
        """
            获取数据库字符连接
        Returns:数据库字符连接

        """
        return "mysql://{user}:{password}@{ipaddr}:{port}/{dbname}?charset=utf8". \
            format(user=self.user, password=self.passwd, ipaddr=self.host, port=self.port, dbname=self.db)

    def InitFromConfigure(self, dbconf):
        """
            重新初始化数据库配置
        Args:
            dbconf: {} 数据库配置

        Returns:boolean

        """
        self.host = dbconf["dbHost"]
        self.port = int(dbconf["dbPort"])
        self.passwd = dbconf["dbPass"]
        self.db = dbconf["dbName"]
        return True


class OperateDB:
    def __init__(self, configPath, isUsedDB=True, renameDb=""):
        """
            OperateDB类
                获取数据库连接、增删改查等操作
        Args:
            configPath: 数据库配置文件路径
            isUsedDB: boolean 数据库配置是否指定数据库名（默认为True）
            renameDb: 重命名数据库名称（默认为'')
        """
        self.dbconf = DbConfigure(configPath)
        if len(renameDb) > 0:
            self.dbconf.db = renameDb
        self.cursor = None
        self.dbhandle = None
        self.connect(self.dbconf, isUsedDB)

    @classmethod
    def InitByConfObj(cls, dbconf, isUsedDB=True):
        """
            数据库连接初始化（不需要实例化）
                每次调用OperateDB都会创建一个新的连接返回给客户端
        Args:
            dbconf: 数据库配置
            isUsedDB: boolean 数据库配置是否指定数据库名（默认为True）

        Returns:self

        """
        self = cls.__new__(cls)
        self.dbconf = dbconf
        self.connect(dbconf, isUsedDB)
        return self

    def connect(self, dbconf, isUsedDB):
        """
            数据库连接
        Args:
            dbconf:数据库配置
            isUsedDB:数据库配置是否指定数据库名

        Returns:cursor 连接对象

        """
        if isUsedDB:
            self.dbhandle = pymysql.connect(host=dbconf.host, port=dbconf.port, user=dbconf.user, passwd=dbconf.passwd,
                                            db=dbconf.db, charset='utf8')
        else:
            self.dbhandle = pymysql.connect(host=dbconf.host, port=dbconf.port, user=dbconf.user, passwd=dbconf.passwd,
                                            charset='utf8')
        # self.dbhandle = MySQLdb.connect("192.168.20.115", "root", "em-data-9527", "chejian_refactor", charset='utf8')
        self.cursor = self.dbhandle.cursor()

    def select(self, sqlstr):
        """
            查询数据
        Args:
            sqlstr:

        Returns:

        """
        try:
            self.cursor.execute(sqlstr)
        except Exception as e:
            logger.error("error： 查询操作出错")
            logger.error("error:[{}]".format(e))
            return ""
        return self.cursor.fetchall()

    def db_cj_dropTables(self, lisTable):
        """
            删除表
        Args:
            lisTable: [表名, ......]

        Returns:boolean
        """
        result = self.select('show tables')
        tablses_lis = [list(i)[0] for i in result]
        for table in lisTable:
            try:
                if table in tablses_lis:
                    self.cursor.execute('DROP TABLE `%s`;' % table)
                    print('删除成功,删除表名：%s' % table)
            except Exception as e:
                print('删除失败, 失败表名：%s' % table)
                print('失败原因：%s' % e)
                return False
            return True

    def insert(self, sqlStr):
        """
            插入数据
        Args:
            sqlStr: sql语句

        Returns:boolean

        """
        try:
            self.cursor.execute(sqlStr)
            self.dbhandle.commit()
        except Exception as e:
            logger.error("error： 插入操作失败：[{}]".format(sqlStr))
            logger.error("error reason:{}".format(e))
            self.dbhandle.rollback()
            return False
        return True

    def insertList(self, table, keyList: [], valueList: []):
        """
            批量插入数据（待验证需测试）
        Args:
            valueList: 数据列表
            keyList: 字段列表
            table: 表名
        Returns:boolean

        """
        keys = ', '.join(keyList)
        values = ', '.join(['%s'] * len(keyList))
        sql = f'insert ignore into {table}({keys}) values({values})'
        item_tup = [tuple(info) for info in valueList]
        try:
            self.cursor.executemany(sql, item_tup)
            self.dbhandle.commit()
            print('插入成功: %s' % table)
        except Exception as e:
            print('插入失败, 失败表名：%s' % table)
            print('失败原因：%s' % e)
            self.dbhandle.rollback()
            return False
        return True

    def impDBFile(self, filepath, max_allowed_packet=4194304, net_buffer_length=16384):
        """
            sql文件导入数据库
        Args:
            net_buffer_length: 最大条数（依据数据库参数）
            max_allowed_packet: 最大缓存（依据数据库参数）
            filepath: sql文件地址

        Returns:

        """
        sh = f'mysql -h {self.dbconf.host} -P {str(self.dbconf.port)} ' \
             f'-u {self.dbconf.user} -p{self.dbconf.passwd} -B {self.dbconf.db} ' \
             f'--max_allowed_packet={max_allowed_packet} --net_buffer_length={net_buffer_length} < {filepath} '
        print("command:", sh)
        return os.system(sh)

    def impDBFileList(self, fileList):
        """
            批量sql文件导入数据库
        Args:
            fileList: [sql文件地址, ......]

        Returns:

        """
        for item in fileList:
            self.impDBFile(item)

    def __del__(self):
        """
            关闭数据库链接
        Returns:

        """
        self.dbhandle.close()
        pass


def createDataBase(configPath, dbname=""):
    """
        创建数据库
    Args:
        configPath: 配置文件位置
        dbname: 数据库名

    Returns:结果

    """
    try:
        odb = OperateDB(configPath, isUsedDB=False)
        if len(dbname) == 0:
            dbname = odb.dbconf.db
        val = odb.insert("create database IF NOT EXISTS " + dbname + " default charset utf8 collate utf8_general_ci;")
    except Exception as e:
        val = False
        logger.error("数据库创建失败:[{}]".format(dbname))
        logger.error("error:{}".format(e))
    print("创建数据库:", dbname)
    return val


def test_select(sqlStr):
    dbHandle = OperateDB(r'G:\JetBrains\PycharmProjects\untitled\source\mydb.conf.json')
    result = dbHandle.select(sqlStr)
    print([list(i)[0] for i in result])


def test_create():
    createDataBase(r'E:\JetBrains\PycharmProjects\untitled\source\db.conf.json', "test_01")


if __name__ == '__main__':
    test_select('show tables')
