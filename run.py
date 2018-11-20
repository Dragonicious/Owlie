import discord
import logging
from Classes.Message import Message
# global bot, embedder

try:
	logging.basicConfig(filename='discord/events.log', format='%(asctime)s %(levelname)s:%(message)s', level=logging.INFO)
except FileNotFoundError:
	logging.basicConfig(filename='events.log', format='%(asctime)s %(levelname)s:%(message)s', level=logging.INFO)


logging.info('________________________ OWLIE STARTED __________________________')


bot 		= discord.Client()
embedder 	= discord.Embed()

Message 	= Message(bot, embedder)

# print(bot.servers)
@bot.event
async def on_ready():
	print('____ Owlie ____')

@bot.event
async def on_message(message):
	if message.server.id == '233671291838660608':
		await Message.read(message)

# @bot.event
# async def when_mentioned(bot, message):
# 	await bot.send_message(message.channel, "Who poked me!?")

@bot.event
async def on_member_join(member):
	await bot.send_message(discord.Object(id="461535258819690499"), "Hi "+member.mention+"! Nepamiršk paskaityti #info ir prisistatyti ^^ !")

# @bot.event
# async def on_member_remove(member):
# 	await bot.send_message(discord.Object(id="461535258819690499"), "Pasiilgsim tavęs, "+member.mention)


bot.run(':^)')