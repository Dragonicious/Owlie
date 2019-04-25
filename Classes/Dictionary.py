import logging
logger = logging.getLogger('rpi')
import requests
import json
import discord
from config import config

class Dictionary:
	language = 'en'
	def __init__(self, words):
		self.words = words

	def embed(self):
		data 	= self.define()
		if not data:
			return False
		phrase 	= " ".join(data['word'].split("_"))  

		defs = ''
		nr = 1
		for definition in data['defs'] :
			if nr > 1:
				defs += "\n"
			defs += str(nr)+". "+ definition 
			nr += 1

		title = "**"+phrase+"**    "+data['pronoun']
		embed 	= discord.Embed(title=title, description=defs, color=0x824cb3)
		
		return embed

	def define(self):
		phrase = (" ".join([str(i) for i in self.words]))

		url = config.dict_link + self.language + '/' + phrase.lower()
		try:
			req = requests.get(url, headers= {'app_id':config.dict_app_id, 'app_key':config.dict_app_key})
		except:
			logger.warning('Dictionary error: ' + str(url) +'\n' + str(e.__class__.__name__)+'\n'+str(e.args))
			return False
		if (req.status_code == 404):
			raise Exception("404")

		try:
			json_response = req.json()
		except json.decoder.JSONDecodeError:
			logger.warning('Dictionary - bad JSON: ' + "URL: " + str(url) + "\nreq = "+ str(req))
			return False
		return self.serialized_result(json_response)
		
	def serialized_result(self, result):
		ret 			= {}
		ret['defs']		= []
		data 			= result['results'][0]
		ret['word'] 	= data['id']
		senses = data['lexicalEntries'][0]['entries'][0]['senses']


		for sense in senses:
			tmp_def = sense['definitions'][0]
			ret['defs'].append(tmp_def)		
			

		ret['definition'] 	= data['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions'][0]
		ret['pronoun'] 		= data['lexicalEntries'][0]['pronunciations'][0]['phoneticSpelling']
		# print 

		return ret

# testing 
# dic = Dictionary(['definition'])
# ret = dic.define()
# print(json.dumps(ret, indent=4, sort_keys=True))
# print(ret)