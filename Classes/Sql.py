import json
# try:
try:
	from config import config
except SystemError:
	from .config import config

try:
	import MySQLdb
	import MySQLdb.cursors
	db_module = 'mysqldb'
except ModuleNotFoundError:
	try:
		import pymysql
		import pymysql.cursors
		db_module = 'pymysql'
	except:
		db_module = None
		print("SQL MODULE NOT FOUND")



class Sql:
	db = cursor = None
	def __init__(self, keepalive = False, database=config.db_db):
		self.keepalive = keepalive 
		self.db_db = database
		if keepalive:
			self.connect()

		

	def connect(self):
		# print('Db type: ', db_module)
		if db_module == 'pymysql':
			self.db = pymysql.connect(host='192.168.1.188',
				user=config.db_user,
				password=config.db_passwd,
				db=self.db_db,
				charset='utf8mb4',
				cursorclass=pymysql.cursors.DictCursor)
			# self.db.set_character_set('utf8')

		elif db_module == 'mysqldb':
			self.db 	= MySQLdb.connect(
				host		= config.db_host
				,user		= config.db_user
				,passwd		= config.db_passwd
				,db			= self.db_db
				,connect_timeout = config.db_connect_timeout
				,cursorclass=MySQLdb.cursors.DictCursor
			)
			self.db.set_character_set('utf8')
		self.cursor = self.db.cursor()

	def disconnect (self):
		self.db.close()
		if db_module == 'pymysql':
			self.cursor.close()
			self.cursor = None

	def get(self, query, arguments=[]):
		if not self.keepalive:
			self.connect()

		try:
			with self.db.cursor() as cursor:
				cursor.execute(query, arguments)
				result = cursor.fetchall()
		finally:
			pass
			# self.db.close

		
		if not self.keepalive:		
			self.disconnect()
		return result

	def put(self, query, arguments=[]):		
		if not self.keepalive:
			self.connect()
		execute = self.cursor.execute(query, arguments)
		self.db.commit()
		if not self.keepalive:
			self.disconnect()
		return execute

	def get_all_subjects(self):
		#get subject data
		# try:
			data = self.get("SELECT * FROM `members`")
		# except Exception as ex:
			# print("!!!!!!!!!!!!!!!!!!!!!!!! LOAD error",ex.args)
		# else:
			return data

	def renew(self, subject):
		query = "UPDATE `members` "\
			"SET `NAME`=%s,`LAST_MESSAGE`=%s,`LAST_EMBED`=%s,`LAST_TIMESTAMP`=%s, `WARNINGS`=%s, `ACTIONS` = %s "\
			"WHERE `AUTHOR` = %s"

		warnings = json.dumps(subject.warnings)
		actions = json.dumps(subject.actions)
		vals = (subject.name, subject.last_message, subject.last_embed, subject.last_timestamp, warnings, actions, subject.id)
		self.put(query, vals)

	def add_subject(self, subject):
		query = "INSERT INTO `members` "\
			"(`AUTHOR`, `NAME`, `SPAM_IDENT`, `SPAM_RND`, `LAST_MESSAGE`, `LAST_EMBED`, `LAST_TIMESTAMP`, `WARNINGS`, `ACTIONS`) "\
			"VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
		vals = (subject.id, subject.name, subject.identical_spam, subject.random_spam, subject.last_message, subject.last_embed, subject.last_timestamp, subject.warnings, subject.actions)
		self.put(query, vals)

	def log_stats(self, message):
		query = "INSERT INTO `stats` "\
			"(`CHANNEL`, `LENGTH`, `EMBEDS`) "\
			"VALUES (%s, %s, %s)"
		embeds = 0
		for item in message.attachments:
			embeds+=1
		vals = (str(message.channel), len(str(message.content)), int(embeds))
		self.put(query, vals)
		
		
		
		
		
		
		
		
		