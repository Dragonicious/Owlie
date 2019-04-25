import discord 
import logging
logger = logging.getLogger('rpi')

class Reactions:
	types			= {}
	types['huh?'] 	= '❓'
	types['error']	= '❗'

	def __init__(self, bot, message):
		self.bot 		= bot
		self.message  	= message
		self.all_emojis = bot.get_all_emojis()

	async def add(self, emote):
		try:
			await self.bot.add_reaction(self.message, self.types[emote])
		except discord.errors.Forbidden:
			logger.warning("Can't add reaction - missing permissions")
			pass 
			# write to admin server for permissions

