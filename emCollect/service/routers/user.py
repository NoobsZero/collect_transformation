# encoding: utf-8
"""
@file: user.py
@time: 2021/8/12 16:15
@author: Chen
@contact: Afakerchen@em-data.com.cn
@software: PyCharm
"""
import time
from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from secrets import token_bytes
from base64 import b64encode
from emCollect.model import crud, schemas, database, models
from sqlalchemy.orm import Session
from emCollect.model.database import db_state_default

# 生成一个安全的随机密钥
SECRET_KEY = b64encode(token_bytes(32)).decode()
# 设定 JWT 令牌签名算法
ALGORITHM = "HS256"
# 设置令牌过期时间的变量
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 创建数据库
database.db.connect()
database.db.create_tables([models.User, models.Item])
database.db.close()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token/")

router = APIRouter(prefix="/users",
                   tags=["USERS"],
                   responses={404: {"description": "Not found"}})


async def reset_db_state():
    database.db._state._state.set(db_state_default.copy())
    database.db._state.reset()


def get_db(db_state=Depends(reset_db_state)):
    try:
        database.db.connect()
        yield
    finally:
        if not database.db.is_closed():
            database.db.close()


def verify_password(plain_password, hashed_password):
    # 校验接收的密码是否与存储的哈希值匹配
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    # 哈希来自用户的密码
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    # 生成新的访问令牌的工具函数
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = schemas.TokenData(username=username)
#     except JWTError:
#         raise credentials_exception
#     user = token_data
#     print("****************************")
#     print(user)
#     # user = crud.get_user_by_email(db, email=token_data.username)
#     if user is None:
#         raise credentials_exception
#     return user
#
#
# async def get_current_active_user(current_user: schemas.User = Depends(get_current_user)):
#     if current_user.is_active:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user
#
# , response_model=schemas.Token
@router.post("/token/", dependencies=[Depends(get_db)])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = crud.get_user_by_email(email=form_data.username)
    if (not user) or (not verify_password(form_data.password, user.hashed_password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# @router.get("/me/")
# async def read_users_me(current_user: str = Depends(get_current_active_user)):
#     return current_user


@router.post("/", response_model=schemas.User, dependencies=[Depends(get_db)])
def create_user(user: schemas.UserCreate):
    db_user = crud.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user.password = get_password_hash(user.password)
    return crud.create_user(user=user)


@router.get("/", response_model=List[schemas.User], dependencies=[Depends(get_db)])
def read_users(skip: int = 0, limit: int = 100):
    users = crud.get_users(skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=schemas.User, dependencies=[Depends(get_db)])
def read_user(user_id: int):
    db_user = crud.get_user(user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/{user_id}/items/", response_model=schemas.Item, dependencies=[Depends(get_db)])
def create_item_for_user(user_id: int, item: schemas.ItemCreate):
    return crud.create_user_item(item=item, user_id=user_id)


@router.get("/items/", response_model=List[schemas.Item], dependencies=[Depends(get_db)])
def read_items(skip: int = 0, limit: int = 100):
    items = crud.get_items(skip=skip, limit=limit)
    return items


@router.get(
    "/slowusers/", response_model=List[schemas.User], dependencies=[Depends(get_db)]
)
def read_slow_users(skip: int = 0, limit: int = 100):
    sleep_time = 0
    sleep_time = max(0, sleep_time - 1)
    time.sleep(sleep_time)  # Fake long processing request
    users = crud.get_users(skip=skip, limit=limit)
    return users
