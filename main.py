#! /usr/bin/python3
# -*- coding:utf-8 -*-
# Author: demo
# Email: demo@demo.com
# Version: demo

import tornado.ioloop
import tornado.web
import os
import sys
from tornado.options import define, options
from common.url_router import include, url_wrapper
from sqlalchemy.orm import scoped_session, sessionmaker
from conf.base import engine, BaseDB

class Application(tornado.web.Application):
	def __init__(self):
		''' 根据url路径寻找需要加载的对应的模块
		'''
		handlers = url_wrapper([
		(r"/users/", include('views.users.users_urls')),
		(r"/upload/", include('views.upload.upload_urls'))
		])
		settings = dict(
			debug=True,
			static_path=os.path.join(os.path.dirname(__file__),"static"),
			template_path=os.path.join(os.path.dirname(__file__), "templates")
		)
		tornado.web.Application.__init__(self, handlers, **settings)
 
		# scoped_session 生成单例
		self.db = scoped_session(sessionmaker(bind=engine))
 
if __name__ == '__main__':
	print ("Tornado server is ready for service\r")
	tornado.options.parse_command_line()
	Application().listen(8000, xheaders=True)
	tornado.ioloop.IOLoop.instance().start()