import re
import random

import sys
from config import config
# from Classes.Answer import Answer
from Classes.Interpreter import Interpreter
from Classes.Dictionary import Dictionary

class Response:
	tree = {}

	def __init__(self, bot, message):
		self.bot = bot
		self.message = message
		self.words = Interpreter.parse(message.content.replace(config.bot_mention, ""))
		print("words at init: ", self.words)


	class Action:
		def __init__(self,action_name):
			self.do = action_name
	class Reply:
		def __init__(self, possible_replies):
			self.answers = possible_replies
		def msg(self):
			return self.answers[random.randint(0, len(self.answers))-1] #return a random asnwer


	async def pick_response(self, at_word = 0, tree = None):
		init_at_word = at_word
		# words = self.words
		if tree == None and at_word == 0:
			tree = self.tree
		print(tree);
		# print(at_word)
		for branch in tree:
			print("Checking in : ", branch)
			for word in self.words:
				word_checks = branch.split(' ')
				if word in word_checks and word != '':
					print('Found: ', word)
					#____________________________ things to do _________________________
					if type(tree[branch]) is self.Reply:
						print('replying')
						await self.bot.send_message(self.message.channel, tree[branch].msg())
						# return None

					elif type(tree[branch]) is self.Action:
						print("------- Executing: ", tree[branch].do)
						if tree[branch].do == 'define':
							await self.bot.send_message(self.message.channel, "", embed = Dictionary(self.words[int(at_word+1):]).embed())
					#__________________________________________________________________
					else:
						print("LOOKING FOR NEXT")
						if tree[branch]:
							further_check = await self.pick_response(at_word+1, tree[branch])
							if further_check == False:
								continue
							else:
								return further_check 
				else:	
					at_word += 1
					continue
			at_word = 0
		return False

		
	my_maker_is = Reply([
		config.owner_mention + " is my daddy!"
		,config.owner_mention + " made me. ^^"
		,"I thank <@308661300039385088> for my artificial life."
	])
	introduction = Reply([
		"I'm a friendly owl, who looks over this server. My job is to get rid of spammers, mostly."
	])
	who_am_i = Reply([
		"Just a friendly neighborhood owl. ^^"
		,"I'm an owl, duh.."
		,"I'm a cyborg-owl *beep boop*."
		,"I bet you'd like to know.."
		,"Just an artificial owl."
		,"*I AM YOUR GOD!*"
		,"None of your business >.>"
	])
	what_i_do = Reply([
		"Whatever i want!"
	])

	define = Action('define')


	tree = {
		'define' : define

		,'who'	: {
			'are'	: {
				'you' : who_am_i
			}
			,'is'	: {
				'owlie' : who_am_i
				,'your'	: {
					'creator maker coder owner'	: my_maker_is
				}
			}
			,'made'	: {
				'you' : my_maker_is
			}
		}
		,'what'	: {
			'are'	: {
				'you' : {
					who_am_i
				}
			}
			,'do'	: {
				'you'	: {
					'do'	: what_i_do
				}
			}
		}
	}
