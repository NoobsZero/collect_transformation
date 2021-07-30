# -*- coding: UTF-8 -*-
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

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


def engine_connection(mysqlUrl, future=False, echo=False):
    maxconnections = 15  # 最大连接数
    return create_engine(
        mysqlUrl,
        max_overflow=0,  # 超过连接池大小外最多创建的连接
        pool_size=maxconnections,  # 连接池大小
        pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
        pool_recycle=-1,  # 多久之后对线程池中的线程进行一次连接的回收(重置)
        pool_pre_ping=True,
        encoding='utf-8',
        future=future,
        echo=echo
    )


def initOrmHandle(mysqlUrl):
    # 初始化数据库连接:
    engine = engine_connection(mysqlUrl, future=True, echo=False)
    Base.metadata.create_all(engine)
    # # 创建DBSession类型:
    DBSession = sessionmaker(bind=engine, future=True)
    return DBSession()
