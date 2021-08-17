# from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
# from sqlalchemy.orm import relationship
import peewee
from .database import db


class User(peewee.Model):
    email = peewee.CharField(unique=True, index=True)
    hashed_password = peewee.CharField()
    is_active = peewee.BooleanField(default=True)

    class Meta:
        table_name = 'users'
        database = db


class Item(peewee.Model):
    title = peewee.CharField(index=True)
    description = peewee.CharField(index=True)
    owner = peewee.ForeignKeyField(User, backref="items")

    class Meta:
        table_name = 'items'
        database = db

# # 定义User对象:
# class User(peewee.Model):
#     # __tablename__ = "users"
#     id = Column(Integer(), primary_key=True, index=True)
#     email = Column(String(128), unique=True, index=True)
#     hashed_password = Column(String(128))
#     is_active = Column(Boolean, default=True)
#
#     items = relationship("Item", back_populates="owner")
#
#     class Meta:
#         database = db
#
#
# class Item(peewee.Model):
#     # __tablename__ = "items"
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String(128), index=True)
#     description = Column(String(128), index=True)
#     owner_id = Column(Integer, ForeignKey("users.id"))
#
#     owner = relationship("User", back_populates="items")
#
#     class Meta:
#         database = db
