import re
class Interpreter:
	def __init__():
		pass

	@staticmethod
	def parse(string):
		initial_string = str(string)
		pure_string = re.sub('[^A-Za-z0-9 ]+', '', initial_string)
		clean_string = re.sub(' +', ' ', pure_string)
		word_array = clean_string.split(" ")
		word_array = [x.lower() for x in word_array]
		return word_array