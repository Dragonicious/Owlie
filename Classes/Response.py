import re
import random
import discord
import sys
from config import config
# from Classes.Answer import Answer
from Classes.Interpreter import Interpreter
from Classes.Dictionary import Dictionary
from Classes.Reactions import Reactions

class Response:
	tree = {}

	def __init__(self, bot, message):
		self.bot = bot
		self.message = message
		self.words = Interpreter.parse(message.content.replace(config.bot_mention, ""))
		
		# print("words at init: ", self.words)


	class Action:
		def __init__(self,action_name):
			self.do = action_name
	class Reply:
		def __init__(self, possible_replies):
			self.answers = possible_replies
		def msg(self):
			return self.answers[random.randint(0, len(self.answers))-1] #return a random asnwer


	async def respond(self, next_word = 0, current_tree = None):
		#goes through pre-defined word tree, looking for message responses or actions to execute
		if current_tree == None:
			current_tree = self.word_tree

		# next_word = 0
		i_replied = False
		for expected_word in current_tree:
			#try to find a start of an expected phrase, starting with each word ?
			for actual_word_id in range(0, len(self.words)):
				actual_word = self.words[actual_word_id]
				
				if actual_word == expected_word and not i_replied:
					#if i find a matching key 
					next_tree = current_tree[expected_word]

					request = next_tree
					#check if type of matched key's value is an answer:
					if isinstance(request, self.Reply): 
						await self.bot.send_message(self.message.channel, request.msg())
						return True

					elif type(request) is self.Action:
						await self.execute_action(request, actual_word_id)
						return True

					elif type(next_tree) is dict or type(next_tree) is list:
						#look for next word in next tree = next expected word
						next_level = await self.respond(next_word+1, next_tree)
						if next_level == True:
							return True
							i_replied = True
							break
					else:
						pass 
				else:
					#look for next word in currnt tree
					pass
			if i_replied:
				break
		return False
				

	async def execute_action(self, action, next_word = None):
		#------------------------------- dictioanry
		if action.do == 'define':
			try:
				#request next words after 'define' 
				answer = Dictionary(self.words[int(next_word+1):]).embed()
			except Exception as ex:
				if (ex.args[0] == '404'):
					#phrase not found
					await Reactions(self.bot, self.message).add('huh?')
				else:
					#some other error
					print(ex.args)
					
				return None
			else:
				if answer:
					await self.bot.send_message(self.message.channel, "", embed = answer)
				return None
		#----------------------------------- dice roll
		elif action.do == 'roll':
			try:
				limit = re.findall(r'\d+', str(self.words[int(next_word+1):]))
				limit = limit[0]
				if (int(limit)):
					roll_embed 	= discord.Embed(title=random.randint(1,int(limit)), color=0x824cb3)
					await self.bot.send_message(self.message.channel, "", embed = roll_embed)
			except Exception as ex:
				print(ex.args)
				await Reactions(self.bot, self.message).add('error')
		else:
			return None


	my_maker_is = Reply([
		config.owner_mention + " is my daddy!"
		,config.owner_mention + " made me. ^^"
		,"I thank "+config.owner_mention+" for my artificial life."
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
		"In my free time i enjoy contemplating ones and zeroes."
	])

	define	= Action('define')
	roll	= Action('roll')


	word_tree = {
		'define' : define
		,'roll'  : roll

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
		,'whos':	{
			'owlie' : who_am_i
			,'your'	: {
				'creator maker coder owner'	: my_maker_is
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
