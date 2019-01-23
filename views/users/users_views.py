#!/usr/bin/python3
# -*- coding:utf-8 -*-

import tornado.web
import sys
from tornado.escape import json_decode
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

from common.commons import (
    http_response,
)

# 从配置文件中导入错误码
from conf.base import (
    ERROR_CODE,
)

from models import (
    Users,
)

# configure logging
logFilePath = "log/users/users.log"
logger = logging.getLogger("Users")  
logger.setLevel(logging.DEBUG)  
handler = TimedRotatingFileHandler(logFilePath,  
                                   when="D",  
                                   interval=1,  
                                   backupCount=30)  
formatter = logging.Formatter('%(asctime)s \
%(filename)s[line:%(lineno)d] %(levelname)s %(message)s',)  
handler.suffix = "%Y%m%d"
handler.setFormatter(formatter)
logger.addHandler(handler)

class RegistHandle(tornado.web.RequestHandler):
    '''
    Handle /user/regist post request
    '''
    @property
    def db(self):
        return self.application.db
        
    def post(self):
        try:
            # 从post的body获取数据
            args = json_decode(self.request.body)
            phone = args['phone']
            password = args['password']
            verify_code = args['code']
        except:
            # 获取入参失败时，抛出错误码及错误信息
            logger.info("RegistHandle: param error, phone[%s], password[%s], verify_code[%s]" % (phone, password, verify_code))
            http_response(self, ERROR_CODE['1001'], 1001)
            return 
        
        ex_user = self.db.query(Users).filter_by(phone = phone).first()
        if ex_user:
            # 如果用户已经存在返回用户信息
            logger.info("RegistHandle: user is existed, phone[%s], password[%s], verify_code[%s]" % (phone, password, verify_code))
            http_response(self, ERROR_CODE['1002'], 1002)
            self.db.close()
            return
        else:
            # 如果用户信息不存在则查询用户信息
            logger.debug("RegistHandle: insert user start, user[%s]" % phone)
            create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            add_user = Users(phone, password, create_time)
            self.db.add(add_user)
            self.db.commit()
            self.db.close()
            
            # 处理成功后，返回成功码“0”及成功信息“ok”
            logger.debug("RegistHandle: regist successfully")
            http_response(self, ERROR_CODE['0'], 0)


class LoginHandle(tornado.web.RequestHandler):
    '''
    Handle /user/login get request
    '''
    @property
    def db(self):
        return self.application.db
    
    def get(self):
        try:
            phone = self.get_argument("phone")
            password = self.get_argument("password")
        except:
            logger.info("LoginHandle: param error")
            http_response(self, ERROR_CODE['1001'], 1001)
            return
        
        ex_user = self.db.query(Users).filter_by(phone = phone, password = password).first()
        if ex_user:
            logger.debug("LoginHandle: login success, phone[%s]" % phone)
            self.render("index.html")
            self.db.close()
            return
        else:
            logger.info("LoginHandle: login error, phone[%s], password[%s]" % (phone, password))
            self.db.close()
            http_response(self, ERROR_CODE['1003'], 1003)
            return