import threading
import time
import logging
import json
import re
from config import config
from Classes.Response import Response
from Classes.Holder import Holder
from Classes.Subject import Subject

class Reader:
	# Processes messages, initiates actions if needed
	# config = config()
	# bot	= embedder = None
	# message_log = {}

	def __init__(self, bot, embedder):
		self.bot 		= bot
		self.embedder 	= embedder
		self.Holder		= Holder()

	async def read(self, message): #main initiation
		if message.author.id not in self.Holder.subjects():
			self.Holder.add_subject(Subject(message))

		spam_check = await self.check_spam(message)

		if config.bot_mention in message.content or message.content.startswith("!"):
			#if a command is requested
			Response_prep = Response(self.bot, message) #prepare a response
			await Response_prep.respond() #send it

		self.Holder.update(message)
		#=================================================== console log
		last_msg_sub = self.Holder.sub(message.author.id)
		tmp_print_msg = str(last_msg_sub.name) + ": " +str(last_msg_sub.last_message) +"          [spm:I"+ str(last_msg_sub.identical_spam) +";R:"+ str(last_msg_sub.random_spam) +"] [W:"+str(last_msg_sub.warnings)+"]"
		print("\t\t"+str(tmp_print_msg)+" H.["+str(len(self.Holder.hold))+"]")
			

	async def check_spam(self, message):
		author = message.author.id

		#count spammy messages
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
		
		#take action against spam
		if self.Holder.identical_spam(author) == 2:
			await self.spam_warning(message)
		if self.Holder.identical_spam(author) > 3:	
			await self.kick_subject(message)

		if self.Holder.random_spam(author) == 3:
			await self.spam_warning(message)
		if self.Holder.random_spam(author) > 4:			
			await self.kick_subject(message)
		

	def message_is_identical(self, message):
		answer = (
			(self.Holder.last_message(message.author.id) == str(message.content) and str(message.content) != "")
			or
			(self.Holder.last_embed(message.author.id) == Subject.embed_str(message) and str(Subject.embed_str(message)) != "[]")
		)
		return answer

	def sent_within(self, message, timeout):
		#is time delta between last msg vs this one is greater than timeout (limit)
		return time.time() < self.Holder.last_timestamp(message.author.id) + timeout

	async def spam_warning(self, message):
		logging.info(str(message.author)+ " warned for spam [identical message]: "+ str(message.content))
		await self.bot.send_message(message.channel, "Sorry, no spam allowed! " + message.author.mention)
		self.Holder.add_warning('spam', message.author.id)

	async def kick_subject(self, message):
		if config.debuging:
			await self.bot.send_message(message.channel, "Would kick " + str(message.author))
		else :	
			self.Holder.add_action('kicked', message.author.id)
			await self.bot.kick(message.author)
			await self.bot.send_message(message.channel, "Was nice knowing you, " + str(message.author))

