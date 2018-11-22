import threading
import time
import logging
import json
import re
from config import config
from Classes.Response import Response
from Classes.Holder import Holder
from Classes.Subject import Subject
# from Classes.Sql import Sql


class Reader:
	config = config()
	# Holder = None
	bot	= embedder = None
	message_log = {}
	
	# Sql = Sql()

	def __init__(self, bot, embedder):
		self.bot 		= bot
		self.embedder 	= embedder
		self.Holder		= Holder()


	async def read(self, message): #main initiation
		if message.author == self.bot.user:
			return #ignore myself


		# PERDETI I HOLDER 
		updt = threading.Thread(target=self.update_log_file)
		updt.start() #keep dat shit up to date

		await self.check_spam(message)

		if self.config.bot_mention in message.content:
			response = Response()
			words = self.parse_message(message.content.replace(self.bot_mention, ""))

			response = response.dig_for_response(words, at_word = 0, dirt = response.responses['general'])
			if response:
				await self.bot.send_message(message.channel, response)

		self.Holder.save_data();
		print([subj.__dict__ for subj in self.Holder.hold])
			



	async def check_spam(self, message):
		author = message.author.id

		if author in self.Holder.subjects():
			if self.message_is_identical(message):
				if self.sent_within(message, 5):
					self.Holder.inc_identical_spam(author)
				else:
					self.Holder.reset_identical_spam(author)
			else:
				self.Holder.reset_identical_spam(author)
				# check for "random" spam - lower timescale
				if self.sent_within(message, 1):
					self.Holder.inc_random_spam(author)
				else:
					self.Holder.reset_random_spam(author)
		else:
			self.Holder.add_subject(Subject(message))

		self.Holder.update(message)

		if self.Holder.identical_spam(author) == 2:
			await self.spam_warning(message)
		if self.Holder.identical_spam(author) > 3:
			# await self.bot.send_message(message.channel, "Would kick "  + str(message.author) + " if i wasn't in test-mode...")		
			if config.debuging:
				await self.bot.send_message(message.channel, "Would kick " + str(message.author))
			else :	
				await self.bot.kick(message.author)
				await self.bot.send_message(message.channel, "Was nice knowing you, " + str(message.author))

		if self.Holder.random_spam(author) == 3:
			await self.spam_warning(message)
		if self.Holder.random_spam(author) > 4:
			# await self.bot.send_message(message.channel, "Would kick " + str(message.author) + " if i wasn't in test-mode...")			
			if config.debuging:
				await self.bot.send_message(message.channel, "Would kick " + str(message.author))
			else :	
				await self.bot.kick(message.author)
				await self.bot.send_message(message.channel, "Was nice knowing you, " + str(message.author))
		
		self.Holder.update(message)

	def message_is_identical(self, message):
		answer = (
			(self.Holder.last_message(message.author.id) == str(message.content) and str(message.content) != "")
			or
			(self.Holder.last_embed(message.author.id) == Subject.embed_str(message) and str(Subject.embed_str(message)) != "[]")
		)
		return answer

	def sent_within(self, message, timeout):
		return time.time() < self.Holder.last_timestamp(message.author.id) + timeout

	async def spam_warning(self, message):
		logging.info(str(message.author)+ " warned for spam [identical message]: "+ str(message.content))
		await self.bot.send_message(message.channel, "Sorry, no spam allowed! " + message.author.mention)
		self.Holder.add_warning('spam', message.author.id)
		# self.message_log[str(message.author)]['log']['warnings']['spam'] += 1

	def update_log_file(self):
		with open("message_log.json", 'w') as file_object:
			json.dump(self.message_log, file_object)

	#========================== interpretation ========================
	def parse_message(self, string):
		initial_string = str(string)
		pure_string = re.sub('[^A-Za-z0-9 ]+', '', initial_string)
		clean_string = re.sub(' +', ' ', pure_string)
		word_array = clean_string.split(" ")
		word_array = [x.lower() for x in word_array]
		return word_array

