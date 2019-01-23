#! /usr/bin/python3
# -*- coding:utf-8 -*-

import json
import os

def http_response(self, msg, code):
	''' 
	desc: 输出渲染函数，将数据渲染成json格式返回给前端
	input.self: self变量
	input.msg: 返回字符串
	input.code: 返回码
	output: None
	'''
	self.write(json.dumps({"data":{"msg":msg, "code":code}}))

def save_files(file_metas, in_rel_path, type = 'image'):
	'''
	desc: 保存文件到服务器
	'''
	file_path = ""
	file_name_list = []
	for meta in file_metas:
		file_name = meta['filename']
		file_path = os.path.join(in_rel_path, file_name)
		file_name_list.append(file_name)
		# save image as binary
		with open(file_path, 'wb') as up:
			up.write(meta['body'])
	
	return file_name_list
		
if __name__ == "__main__":
	http_response()
	