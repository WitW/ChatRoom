#coding:utf-8

import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options

import os.path
import sqlite3
import datetime
import time

from tornado.options import define, options
define("port", default=8000, help="run on given port", type=int)

conn = sqlite3.connect('chatroom.db')
cur  = conn.cursor()

class RegisterHandler(tornado.web.RequestHandler):
	
	#true: used
	def check_is_used(self, username):
		sql = "select username from user where username = '%s' " %(username)
		cur.execute(sql)

		if cur.fetchall():
			return True;
		return False;

	def get(self):
		self.render('register.html')
	
	def post(self):
		username = self.get_argument('username')
		password = self.get_argument('password')
		rep_password = self.get_argument('rep_password')
		email = self.get_argument('email')
		phone = self.get_argument('phone')
		if password != rep_password:
			self.write("两次密码输入不一致")

		if not self.check_is_used(username):
			sql = "insert into user (username, password, registed_time, email, phone) \
				   values ('%s', '%s', datetime('now'), '%s', '%s')" %(username, password, email, phone)
			conn.execute(sql)
			conn.commit()
			self.write("注册成功")

		else:
			self.write("该用户名已被使用")
			time.sleep(1)
			self.render('register.html')


if __name__ == '__main__':
	tornado.options.parse_command_line()
	app = tornado.web.Application(
		handlers=[(r'/', RegisterHandler)],
		template_path=os.path.join(os.path.dirname(__file__), "templates")
		)
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()
