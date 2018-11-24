import requests
import json
import discord
from config import config

class Dictionary:
	language = 'en'
	def __init__(self, words):
		self.words = words

	def define(self):
		url = config.dict_link + self.language + '/' + str(self.words[0]).lower()
		req = requests.get(url, headers= {'app_id':config.dict_app_id, 'app_key':config.dict_app_key})
		return self.serialized_result(req.json())
		
	def serialized_result(self, result):
		ret 			= {}
		data 			= result['results'][0]
		ret['word'] 	= data['id']
		ret['definition'] = data['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions'][0]

		return ret

	def embed(self):
		data 	= self.define()
		embed 	= discord.Embed(title=data['word']+":", description=data['definition'], color=0x824cb3)
		return embed
