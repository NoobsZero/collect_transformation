# encoding: utf-8
"""
@file: schemas.py
@time: 2021/8/13 18:05
@author: Chen
@contact: Afakerchen@em-data.com.cn
@software: PyCharm
"""
from typing import Any, List, Optional

import peewee
from pydantic import BaseModel
from pydantic.utils import GetterDict


class PeeweeGetterDict(GetterDict):
    """
        Pydantic 默认情况下不知道如何将其转换list为 Pydantic模型/模式。
        创建一个自定义PeeweeGetterDict类并在所有相同的 Pydantic模型/模式中使用它orm_mode
        创建一个PeeweeGetterDict类，就可以在所有 Pydantic模型/模式中使用它。
    """
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res


class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
