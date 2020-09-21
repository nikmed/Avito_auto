import sqlite3 as sql
import base62
import datetime

class db:
	def __init__(self):	
		self.dbname = 'database.db'
		self.conn = sql.connect(self.dbname, check_same_thread = False)
		self.cursor = self.conn.cursor()
		self.cursor.execute('''CREATE TABLE IF NOT EXISTS URL 
			(short text primary key, num integer, long text)''')
		self.conn.commit()
		self.log = 'database_log.txt'
	
	def insert(self, url):
		try:
			self.id = self.cursor.execute("SELECT COUNT(*) FROM URL").fetchone()[0]
			link = base62.base62encode(self.id + 1)
			query = f"INSERT INTO URL (short, num, long) values ('{link}', '{self.id + 1}', '{url}')"
			self.cursor.execute(query)
			self.conn.commit()
			return link
		except sql.Error as e:
			f = open(self.log, 'a')
			f.write(str(datetime.datetime.now()) + '  Error:  ' + str(e) + '\n')
			f.close()
			if 'UNIQUE' in str(e):
				return 'Error: This short url alrady taken.'
			else:
				return str(e)



	def insert_custom(self, url, custom_short_url):
		try:
			self.id = self.cursor.execute("SELECT COUNT(*) FROM URL").fetchone()[0]
			link = custom_short_url
			query = f"INSERT INTO URL (short, num, long) values ('{custom_short_url}', '{self.id + 1}', '{url}')"
			self.cursor.execute(query)
			self.conn.commit()
			return link
		except sql.Error as e:
			f = open(self.log, 'a')
			f.write(str(datetime.datetime.now()) + '  Error:  ' + str(e) + '\n')
			f.close()
			if 'UNIQUE' in str(e):
				return 'Error: This short url alrady taken.'
			else:
				return str(e)

	def longurl(self, id):
		try:
			query = f"SELECT long FROM URL WHERE short = '{id}'"
			print(query)
			self.cursor.execute(query)
			return self.cursor.fetchone()[0]
		except sqlite3.Error as e:
			self.log.write(str(datetime.datetime.now()) + '  Error:  ' + e + '\n')
			return str(e)





