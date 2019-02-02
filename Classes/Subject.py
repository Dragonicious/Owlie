from Classes.Sql import Sql
import json
import time

class Subject:
	def __init__(self, message, loading= False):
		self.Sql = Sql()
		if loading:
			self.load(message) #message = db data row
		else:
			self.new(message)
	
	def new(self, message):
		#create a "blank" subject from message
		self.id 			= message.author.id
		self.name			= str(message.author)
		self.identical_spam = 0
		self.random_spam	= 0
		self.last_message 	= str(message.content)
		self.last_embed		= self.embed_str(message)
		self.last_timestamp = time.time()
		self.warnings 		= {}
		self.actions		= {}

	def load(self, message):
		self.id 			= message['AUTHOR']
		self.name			= message['NAME']
		self.identical_spam = message['SPAM_IDENT']
		self.random_spam	= message['SPAM_RND']
		self.last_message 	= message['LAST_MESSAGE']
		self.last_embed		= message['LAST_EMBED']
		self.last_timestamp = message['LAST_TIMESTAMP']
		self.warnings 		= json.loads(message['WARNINGS'])
		self.actions 		= json.loads(message['ACTIONS'])

	@staticmethod
	def embed_str(message):
		#stringify embed contents
		string = str([item['filename'] for item in message.attachments])
		return string

	def renew(self, message):
		#update subject in-memmory
		self.last_message 	= str(message.content)
		self.last_embed		= self.embed_str(message)
		self.last_timestamp = time.time()
		#and in-db
		self.Sql.renew(self)

	def add_warning(self, category):
		if category not in self.warnings:
			self.warnings[category] = 1
		else:
			self.warnings[category] += 1

	def add_action(self, action):
		if action not in self.actions:
			self.actions[action] = {
				'count'		: 0
				,'timestamp' : time.time()
			}
		else:
			self.actions[action]['count'] += 1
			self.actions[action]['timestamp'] = time.time()
		


