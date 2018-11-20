import threading
import time
import logging
import json
import re

from Classes.Response import Response

# from Classes.Sql import Sql


class Message:
	bot	= embedder = None
	message_log = {}
	bot_mention = "<@464113786899660800>"
	# Sql = Sql()

	def __init__(self, bot, embedder):
		self.bot 		= bot
		self.embedder 	= embedder
		try:
			with open('message_log.json') as saved_log:
				self.message_log = json.load(saved_log)
		except:
			self.message_log = {}

	async def read(self, message): #main initiation
		if message.author == self.bot.user:
			return #ignore Owlie-self
		# self.Sql.log_message(message)
		updt = threading.Thread(target=self.update_log_file)
		updt.start()
		print(self.message_log)
		await self.check_spam(message)
		if self.bot_mention in message.content:
			response = Response()
			words = self.parse_message(message.content.replace(self.bot_mention, ""))
			# words = self.parse_message(message)
			response = response.dig_for_response(words, at_word = 0, dirt = response.responses['general'])
			if response:
				await self.bot.send_message(message.channel, response)
			



	async def check_spam(self, message):
		author 		= str(message.author)

		if str(author) in self.message_log:
			if self.message_is_identical(message):
				if self.sent_within(message, 5):
					self.message_log[author]['log']['consecutive'] += 1
				else:
					self.message_log[author]['log']['consecutive'] = 0
			else:
				self.message_log[author]['log']['consecutive'] = 0

				if self.sent_within(message, 1):
					self.message_log[author]['log']['consecutive_random'] += 1
				else:
					self.message_log[author]['log']['consecutive_random'] = 0					
		else:
			self.new_log(message)

		if self.identical_count(message) == 2:
			await self.spam_warning(message)
		if self.identical_count(message) > 3:
			# await self.bot.send_message(message.channel, "Would kick "  + str(message.author) + " if i wasn't in test-mode...")			
			await self.bot.kick(message.author)
			await self.bot.send_message(message.channel, "Was nice knowing you, " + str(message.author))

		if self.random_count(message) == 3:
			await self.spam_warning(message)
		if self.random_count(message) > 4:
			# await self.bot.send_message(message.channel, "Would kick " + str(message.author) + " if i wasn't in test-mode...")			
			await self.bot.kick(message.author)
			await self.bot.send_message(message.channel, "Was nice knowing you, " + str(message.author))
		
		self.update_log(message)



	def identical_count(self, message):
		return int(self.message_log[str(message.author)]['log']['consecutive'])
	def random_count(self, message):
		return int(self.message_log[str(message.author)]['log']['consecutive_random'])

	def new_log(self, message):
		self.message_log[str(message.author)] = {}
		self.message_log[str(message.author)]['log'] = {}
		self.message_log[str(message.author)]['log']['last_message'] = ''
		self.message_log[str(message.author)]['log']['last_embed'] = ''
		self.message_log[str(message.author)]['log']['warnings'] = {}
		self.message_log[str(message.author)]['log']['consecutive'] = 0
		self.message_log[str(message.author)]['log']['consecutive_random'] = 0
		self.message_log[str(message.author)]['log']['warnings']['spam'] = 0
		self.message_log[str(message.author)]['log']['last_timestamp'] = 0


	def message_is_identical(self, message):
		attachments = []
		if message.attachments:
			for item in message.attachments:
				attachments.append(item['filename'])
		attachments = str(attachments)
		answer = (
			(self.message_log[str(message.author)]['log']['last_message'] == str(message.content) and str(message.content) != "")
			or
			(self.message_log[str(message.author)]['log']['last_embed'] == attachments and attachments!="[]")
		)
		return answer

	def sent_within(self, message, timeout):
		return time.time() < float(self.message_log[str(message.author)]['log']['last_timestamp'])+timeout

	async def spam_warning(self, message):
		logging.info(str(message.author)+ " warned for spam [identical message]: "+ str(message.content))
		await self.bot.send_message(message.channel, "Sorry, no spam allowed! " + message.author.mention)
		self.message_log[str(message.author)]['log']['warnings']['spam'] += 1

	def update_log_file(self):
		with open("message_log.json", 'w') as file_object:
			json.dump(self.message_log, file_object)

	def update_log(self, message):
		attachments = []
		if message.attachments:
			for item in message.attachments:
				attachments.append(item['filename'])
		attachments = str(attachments)
		self.message_log[str(message.author)]['log']['last_message'] = str(message.content)
		self.message_log[str(message.author)]['log']['last_embed'] = attachments
		self.message_log[str(message.author)]['log']['last_timestamp'] = time.time()


	#========================== interpretation ========================
	def parse_message(self, string):
		initial_string = str(string)
		pure_string = re.sub('[^A-Za-z0-9 ]+', '', initial_string)
		clean_string = re.sub(' +', ' ', pure_string)
		word_array = clean_string.split(" ")
		word_array = [x.lower() for x in word_array]
		return word_array

