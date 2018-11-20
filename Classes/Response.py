import re
import random
class Response:
	def __init__(self):
		pass
	
	owlies_maker = [
		"<@308661300039385088> is my daddy!"
		,"<@308661300039385088> made me. ^^"
		,"I thank <@308661300039385088> for my artificial life."
	]
	introduction = [
		"I'm a friendly owl, who looks over this server. My job is to get rid of spammers, mostly."
	]
	who_are_you = [
		"Just a friendly neighborhood owl. ^^"
		,"I'm an owl, duh.."
		,"I'm a cyborg-owl *beep boop*."
		,"I bet you'd like to know.."
		,"Just an artificial owl."
		,"*I AM YOUR GOD!*"
		,"None of your business >.>"
	]
	responses = {
		'general' : {
			'who what' : {
				'are is' : {
					'you owlie' : who_are_you
				}
			}
			,"who's who" : {
				"is " : {
					"your ur thy owlie's" : {
						"owner creator maker programmer coder" : owlies_maker
					}
				}
				,"made created coded programmed" : {
					"you owlie u" : owlies_maker
				}
			}
			,'introduce tell-us-about ' : {
				'yourself thyself' : introduction
			}

		}
	}

	def dig_for_response(self, words, at_word = 0, dirt = None):
		if dirt == None and at_word == 0:
			dirt = self.responses['general']

		for check in dirt:
			print("CHECKING IN: ", check)
			for word in words:
				word_checks = check.split(' ')
				print("LOOKING FOR: ", word)
				if word in word_checks:
					if word == '':
						continue 
					print("IS IN CHECK: ", word)
					# print("NEXT TO CALL: ", dirt[check], type(dirt[check]))
					# if isinstance(dirt[check],(list,)):
					if type(dirt[check]) is list:
						print("RETURNING")
						return dirt[check][random.randint(0, len(dirt[check]))-1]
					else:
						print("LOOKING FOR NEXT")
						if dirt[check]:
							further_check = self.dig_for_response(words, at_word+1, dirt[check])
							if further_check == False:
								continue
							else:
								return further_check 
				else:
					at_word += 1
					continue
		return False

		
#========================================= testing 
# import re

# def prase_message(message):
# 	initial_string = str(message)
# 	pure_string = re.sub('[^A-Za-z0-9 ]+', '', initial_string)
# 	clean_string = re.sub(' +', ' ', pure_string)
# 	word_array = clean_string.split(" ")
# 	return word_array


# words = prase_message("Hi owlie,	  introduce yourself, please ^^")
# print(words)

# re = Response();
# re.respond_to(words)
