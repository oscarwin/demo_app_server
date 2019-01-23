#! /usr/bin/python3
# -*- coding:utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

# 初始化数据库连接
# mysql://用户名:密码@主机名:端口号/库名
engine = create_engine("mysql://admin:123456@localhost:3306/demo?", encoding = "utf8",echo = False)
BaseDB = declarative_base()

SERVER_HEADER = "http://47.107.41.24:80"
ERROR_CODE = {
    "0": "ok",
    #Users error code
    "1001": "参数错误",
	"1002": "用户已存在",
	"1003": "未注册用户",
	"2001": "上传图片为空"
}