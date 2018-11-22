
import time

class Subject:
	def __init__(self, message, loading= False):
		if loading:
			self.load(message) #message = json data
		else:
			self.new(message)
	
	def new(self, message):
		self.id 			= message.author.id
		self.name			= str(message.author)
		self.identical_spam = 0
		self.random_spam	= 0
		self.last_message 	= str(message.content)
		self.last_embed		= self.embed_str(message)
		self.last_timestamp = time.time()
		self.warnings 		= {}
	
	@staticmethod
	def embed_str(message):
		string = str([item['filename'] for item in message.attachments])
		return string

	def renew(self, message):
		self.last_message 	= str(message.content)
		self.last_embed		= self.embed_str(message)
		self.last_timestamp = time.time()

	def add_warning(self, category):
		if category not in self.warnings:
			self.warnings[category] = 1
		else:
			self.warnings[category] += 1

	def load(self, message):
		self.id 			= message['id']
		self.name			= message['name']
		self.identical_spam = message['identical_spam']
		self.random_spam	= message['random_spam']
		self.last_message 	= message['last_message']
		self.last_embed		= message['last_embed']
		self.last_timestamp = message['last_timestamp']
		self.warnings 		= message['warnings']
