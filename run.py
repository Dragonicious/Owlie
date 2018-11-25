import discord
import logging
from Classes.Reader import Reader
from config import config

bot 		= discord.Client()
config		= config()
Reader 		= Reader(bot, None)

logging.basicConfig(filename='events.log', 			format='%(asctime)s %(levelname)s:%(message)s', level=logging.INFO)

@bot.event
async def on_ready():
	print('Owlie: Ready!')

@bot.event
async def on_message(message):
	if message.server.id == config.server:
		await Reader.read(message)

@bot.event
async def on_member_join(member):
	await bot.send_message(discord.Object(id=config.main_channel), "Hi "+member.mention+"! Nepamiršk paskaityti #info ir prisistatyti ^^ !")

bot.run(config.bot_key)

logging.info('Owlie: Ready!')