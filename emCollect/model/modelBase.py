# -*- coding: UTF-8 -*-
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from emCollect.common.baseDBOperate import DbConfigure
basedir = os.path.abspath(os.path.dirname(__file__))
# SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# 创建对象的基类:
Base = declarative_base()
# Alembic 和 SQLAlchemy-Migrate
# alembic revision --autogenerate -m "first commit"
# alembic upgrade head
# alembic downgrade base
# alembic current
# alembic history
# setattr(MapperCityDataBaseName, "cityPinYin", (Column("cityPinYin", String(32), comment="啥也不是")))


SQLALCHEMY_DATABASE_URL = DbConfigure().getEngine()
maxconnections = 15  # 最大连接数
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    max_overflow=0,  # 超过连接池大小外最多创建的连接
    pool_size=maxconnections,  # 连接池大小
    pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
    pool_recycle=-1,  # 多久之后对线程池中的线程进行一次连接的回收(重置)
    pool_pre_ping=True,
    future=False,
    echo=False
)


def initOrmHandle():
    # # 创建DBSession类型:
    DBSession = sessionmaker(bind=engine, future=True)
    return DBSession()
