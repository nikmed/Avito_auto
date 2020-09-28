import datetime
import sqlite3 as sql
from queue import Queue

import base62


class db:
	def __init__(self, dbname):
		self.dbname = dbname
		self.q = Queue()
		self.conn = sql.connect(self.dbname, check_same_thread=False)
		self.opened = True
		self.cursor = self.conn.cursor()
		self.cursor.execute('''CREATE TABLE IF NOT EXISTS URL 
			(short text primary key, num integer, long text)''')
		self.conn.commit()
		self.log = 'database_log.txt'

	def open_db(self):
		if self.opened == False:
			self.conn = sql.connect(self.dbname, check_same_thread=False)
			self.cursor = self.conn.cursor()
			self.opened = True

	def close_db(self):
		if self.opened == True:
			self.conn.close()
			self.opened = False

	def insert(self, url):
		try:
			self.id = self.cursor.execute("SELECT COUNT(*) FROM URL").fetchone()[0]
			link = base62.base62encode(self.id + 1)
			query = f"INSERT INTO URL (short, num, long) values ('{link}', '{self.id + 1}', '{url}')"
			self.cursor.execute(query)
			self.conn.commit()
			return link, True
		except sql.Error as e:
			f = open(self.log, 'a')
			f.write(str(datetime.datetime.now()) + '  Error:  ' + str(e) + '\n')
			f.close()
			if 'UNIQUE' in str(e):
				return 'This id alrady taken.', False
			else:
				return str(e), False

	def insert_custom(self, url, custom_short_url):
		try:
			self.id = self.cursor.execute("SELECT COUNT(*) FROM URL").fetchone()[0]
			link = custom_short_url
			query = f"INSERT INTO URL (short, num, long) values ('{custom_short_url}', '{self.id + 1}', '{url}')"
			self.cursor.execute(query)
			self.conn.commit()
			return link, True
		except sql.Error as e:
			f = open(self.log, 'a')
			f.write(str(datetime.datetime.now()) + '  Error:  ' + str(e) + '\n')
			f.close()
			if 'UNIQUE' in str(e):

				return 'This short url alrady taken.', False
			else:
				return str(e), False

	def sequental_read(self, id):
		try:
			query = f"SELECT long FROM URL WHERE short = '{id}'"
			self.cursor.execute(query)
			link = self.cursor.fetchone()
			if link is not None:
				link = link[0]
			else:
				return 'Page not found', False
			return link, True
		except sql.Error as e:
			f = open(self.log, 'a')
			f.write(str(datetime.datetime.now()) + '  Error:  ' + str(e) + '\n')
			f.close()
			return str(e), False

	def read_task(self, id):
		try:
			conn = sql.connect(self.dbname, check_same_thread=False)
			query = f"SELECT long FROM URL WHERE short = '{id}'"
			cursor = conn.execute(query)
			link = cursor.fetchone()
			if link is not None:
				link = link[0]
			else:
				return 'Page not found', False
			return link, True
		except sql.Error as e:
			f = open(self.log, 'a')
			f.write(str(datetime.datetime.now()) + '  Error:  ' + str(e) + '\n')
			f.close()
			return str(e), False

	def queue_read(self, id):
		try:
			self.q.put(self.read_task(id))
			res = self.q.get()
			return res
		except Exception as e:
			f = open(self.log, 'a')
			f.write(str(datetime.datetime.now()) + '  Error:  ' + str(e) + '\n')
			f.close()
			
