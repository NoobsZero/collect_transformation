from .modelBase import *
from ..common.baseDBOperate import DbConfigure
from ..common.baselog import *


class OrmOperateDB:
    def __init__(self, configPath='./conf/db.conf.json'):
        self.dbConf = DbConfigure(configPath)
        url = self.getMysqlUrl()
        print("url:", url)
        try:
            self.sess = initOrmHandle(url)
        except Exception as e:
            print("orm 数据库连接失败")
            print("异常信息", e)

    def getMysqlUrl(self):
        return f'mysql+pymysql://{self.dbConf.user}:{self.dbConf.passwd}@{self.dbConf.host}:{self.dbConf.port}/' \
               f'{self.dbConf.db}?charset=utf8'

    def insert(self, ormObj):
        try:
            self.sess.add(ormObj)
            self.sess.commit()
        except Exception as ex:
            logger.error(ex)
            return False
        return True

    def select(self, ormClazz):
        # orm.Query().filter()
        # return orm.Query( self.sess.query(ormClazz) )
        return self.sess.query(ormClazz)

    def delete(self, ormClazz):
        pass

    def getSession(self):
        return self.sess

    def __del__(self):
        self.sess.close()
        pass
