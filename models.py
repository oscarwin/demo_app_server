#! /usr/bin/python3
# -*- coding:utf-8 -*-

from conf.base import BaseDB, engine
import sys
from sqlalchemy import (Column, Integer, String, DateTime)

class Users(BaseDB):
	'''table for users
	'''
	__tablename__ = "users"
	id = Column(Integer, primary_key = True)
	phone = Column(String(20))
	password = Column(String(20))
	createTime = Column(DateTime)
	
	def __init__(self, phone, password, createTime):
		self.phone = phone
		self.password = password
		self.createTime = createTime

if __name__ == '__main__':
	print ("Init database")
	#user = User('12314', 'hksggs', '')