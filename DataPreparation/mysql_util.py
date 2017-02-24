#coding=utf-8

import MySQLdb
import MySQLdb.cursors

class mysqlutil():
	def __init__(self):
		try:
			self.connection = MySQLdb.connect('127.0.0.1', 'root', '123456', 'dblp_test', charset = 'utf8')
		except:
			print "ERROR CONNECTING TO MYSQL"
			pass
		finally:
			print type(self.connection)
			self.cursor = self.connection.cursor()
			print type(self.cursor)
	
	def execute_sql_params(self, sql, params):
		for param in params:
			self.cursor.execute(sql, (param[0], param[1], param[2],
			                          param[3], param[4], param[5],
			                          param[6], param[7], param[8],
			                          param[9], param[10], param[11],
			                          param[12]))
			# print "title: " + param[2]
		self.connection.commit()
		
		
	def __exit__(self, exc_type, exc_val, exc_tb):
		self.cursor.close()
