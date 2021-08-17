# encoding: utf-8
"""
@file: database.py
@time: 2021/8/16 17:26
@author: Chen
@contact: Afakerchen@em-data.com.cn
@software: PyCharm
"""
from contextvars import ContextVar
import peewee
from emCollect.common.baseDBOperate import DbConfigure

dbBase = DbConfigure()
DATABASE_NAME = dbBase.db
db_state_default = {"closed": None, "conn": None, "ctx": None, "transactions": None}
db_state = ContextVar("db_state", default=db_state_default.copy())


class PeeweeConnectionState(peewee._ConnectionState):
    def __init__(self, **kwargs):
        super().__setattr__("_state", db_state)
        super().__init__(**kwargs)

    def __setattr__(self, name, value):
        self._state.get()[name] = value

    def __getattr__(self, name):
        return self._state.get()[name]


db = peewee.MySQLDatabase(dbBase.db, host=dbBase.host, port=dbBase.port, user=dbBase.user, passwd=dbBase.passwd)

db._state = PeeweeConnectionState()
