import requests
import json
import discord
from config import config

class Dictionary:
	language = 'en'
	def __init__(self, words):
		self.words = words

	def define(self):
		phrase = (" ".join([str(i) for i in self.words]))

		url = config.dict_link + self.language + '/' + phrase.lower()
		try:
			req = requests.get(url, headers= {'app_id':config.dict_app_id, 'app_key':config.dict_app_key})
		except:
			return False
			print("Dictionary error:")
			print("URL: " + str(url) + "\nreq = "+ str(req))
		if (req.status_code == 404):
			print("Dictionary error:")
			print("URL: " + str(url) + "\nreq = "+ str(req))
			raise Exception("404")
		
		try:
			json_response = req.json()
		except json.decoder.JSONDecodeError:
			print("JSON undecodable")
			print("URL: " + str(url) + "\nreq = "+ str(req))
			return False

		return self.serialized_result(json_response)
		
	def serialized_result(self, result):
		ret 			= {}
		data 			= result['results'][0]
		ret['word'] 	= data['id']
		ret['definition'] = data['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions'][0]

		return ret

	def embed(self):
		data 	= self.define()
		if not data:
			return False
		phrase 	= " ".join(data['word'].split("_"))
		embed 	= discord.Embed(title=phrase+":", description=data['definition'], color=0x824cb3)
		return embed
