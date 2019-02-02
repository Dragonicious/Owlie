import json
import MySQLdb
import MySQLdb.cursors
from config import config


class Sql:
	db = cursor = None
	def __init__(self):
		self.db 	= MySQLdb.connect(
			host		= config.db_host
			,user		= config.db_user
			,passwd		= config.db_passwd
			,db			= config.db_db
			,connect_timeout = config.db_connect_timeout
			,cursorclass=MySQLdb.cursors.DictCursor
		)
		self.cursor = self.db.cursor()

	def get(self, query, arguments=[]):
			self.cursor.execute(query, arguments)
			result = self.cursor.fetchall()
			# cursor.close()
			# db.close()
			return result

	def put(self, query, arguments=[]):
		execute = self.cursor.execute(query, arguments)
		self.db.commit()
		return execute


	# def log_message(self, message):
	# 	user	= str(message.author)
	# 	msg		= str(message.content)

	# 	attachments = []
	# 	if message.attachments:
	# 		for item in message.attachments:
	# 			attachments.append(item['url'])

	# 	channel	= str(message.channel)
	# 	query = "INSERT INTO `MESSAGES`"\
	# 		"(`USER`, `CHANNEL`, `MESSAGE`, `ATTACHMENTS`)"\
	# 		"VALUES (%s, %s, %s, %s)"
	# 	arguments = (user, channel, msg, str(attachments))
	# 	self.put(query, arguments)

	def get_all_subjects(self):
		#get subject data
		data = self.get("SELECT * FROM `members`")
		print('INITIAL DATA: ',data)
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
		
		
		
		
		
		
		
		
		