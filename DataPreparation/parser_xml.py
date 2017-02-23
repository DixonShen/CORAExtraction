#coding=utf8

import os, sys
import xml.sax
import re
import mysql_util
from mysql_util import mysqlutil

reload(sys)
sys.setdefaultencoding('utf-8')

paper_tags = ('article', 'inproceedings')   ##only parse these tags
sub_tags = ('publisher', 'journal', 'booktitle')


class MyHandler(xml.sax.ContentHandler):
	def __init__(self):
		self.id = 1
		self.kv = {}
		self.reset()
		self.util = mysqlutil()
		self.params = []
		self.batch_len = 10
		
	def reset(self):
		self.curtag = None
		self.pid = None
		self.ptag = None
		self.title = None
		self.author = None
		self.tag = None
		self.subtag = None
		self.subtext = None
		self.year = None
		self.url = None
		self.mdate = None
		self.key = None
		self.publtype = None
		self.kv = {}
		
	#元素开始时间处理
	def startElement(self, tag, attrs):
		if tag is not None and len(tag.strip()) > 0 :
			self.curtag = tag
			
			if tag in paper_tags:
				self.reset()
				self.pid = self.id
				self.kv['ptag'] = str(tag)
				self.kv['id'] = self.id
				self.id += 1
				
				if attrs.has_key('key'):
					self.key = str(attrs['key'])
					
				if attrs.has_key('mdate'):
					self.mdate = str(attrs['mdate'])
					
				if attrs.has_key('publtype'):
					self.publtype = str(attrs['publtype'])
			elif tag in sub_tags:
				self.kv['sub_tag'] = str(tag)
				
	#元素结束事件处理
	def endElement(self, tag):
		if tag == 'title':
			self.kv['title'] = str(self.title)
		elif tag == 'author':
			self.author = re.sub(' ', '_', str(self.author))
			if self.kv.has_key('author') == False:
				self.kv['author'] = []
				self.kv['author'].append(str(self.author))
			else:
				self.kv['author'].append(str(self.author))
				
		elif tag in sub_tags:
			self.kv['sub_detail'] = str(self.subtext)
			
		elif tag == 'url':
			self.kv['url'] = str(self.url)
			
		elif tag == 'year':
			self.kv['year'] = str(self.year)
			
		elif tag in paper_tags:
			tid = int(self.kv['id']) if self.kv.has_key('id') else 0
			ptag = self.kv['ptag'] if self.kv.has_key('ptag') else 'NULL'
			
			try:
				title = self.kv['title'] if self.kv.has_key('title') else 'NULL'
			except Exception, e:
				title = ''
			author = self.kv['author'] if self.kv.has_key('author') else 'NULL'
			author = ','.join(author) if author is not None else 'NULL'
			subtag = self.kv['subtag'] if self.kv.has_key('subtag') else 'NULL'
			sub_detail = self.kv['sub_detail'] if self.kv.has_key('sub_detail') else 'NULL'
			year = self.kv['year'] = self.kv['year'] if self.kv.has_key('year') else 0
			url = self.kv['url'] if self.kv.has_key('url') else 'NULL'
			mdate = self.kv['mdate'] if self.kv.has_key('mdate') else 'NULL'
			pkey = self.kv['pkey'] if self.kv.has_key('pkey') else 'NULL'
			publtype = self.kv['publtype'] if self.kv.has_key('publtype') else 'NULL'
			param = (str(tid), ptag, title, author, subtag, sub_detail, year, url, mdate, pkey, publtype)
			print param
			# 只抽取其中的会议论文
			if url.find('db/conf') >= 0 or url.find('db/journals') >= 0:
				self.params.append(param)

			if len(self.params) == self.batch_len:
				print len(self.params)
				sql = "insert into paper(id, ptag, title, author, subtag, sub_detail, pyear, url, mdate, pkey, publtype) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
				self.util.execute_sql_params(sql, self.params)
				self.params = []
				
	# 内容事件处理
	def characters(self, content):
		if self.curtag == "title":
			self.title = content.strip()
		elif self.curtag == "author":
			self.author = content.strip()
		elif self.curtag in sub_tags:
			self.subtext = content.strip()
		elif self.curtag == "year":
			self.year = content.strip()
		elif self.curtag == "url":
			self.url = content.strip()
	
if __name__ == "__main__":
	filename = 'E:\\DataSets\\dblp.xml'
		
	# 创建一个XMLReader
	parser = xml.sax.make_parser()
		
	# turn off namespces
	parser.setFeature(xml.sax.handler.feature_namespaces, 0)
		
	# 重写Contexthandler
	Handler = MyHandler()
	parser.setContentHandler(Handler)
		
	parser.parse(filename)
	print 'Parser Complete!'
