import json
from Classes.Sql import Sql
from Classes.Subject import Subject

class Holder:
	# holds data of subjects(class) in-memmory

	def __init__(self):
		self.Sql = Sql()
		self.hold = []
		self.hold = self.load_data()

	def load_data(self):
		# load all subject data from db
		loaded_data = self.Sql.get_all_subjects()
		if loaded_data:
			for row in loaded_data:
				self.add_subject(Subject(row, True), True)
			return self.hold
		else:
			return []

	# def save_data(self):
	# 	#deprecated 
	# 	try:
	# 		with open('holder.json', 'w') as file:
	# 			file.write(json.dumps([subject.__dict__ for subject in self.hold]))
	# 	except Exception as inst:
	# 		print('Failed to save', inst)

	def add_subject(self, subject, loading = False):
		if subject.id not in self.subjects():
			self.hold.append(subject)
			if not loading:
				self.Sql.add_subject(subject)

	def update(self, message):
		self.sub(message.author.id).renew(message)

	def subjects(self):
		#returns list of authorid's currently in hold
		subject_array = [subject.id for subject in self.hold]
		return subject_array

	def sub(self, sub_id):
		# return subject data from hold, based on authorid
		for subject in self.hold:
			if subject.id == sub_id:
				return subject
		return None

	def last_message(self, author):
		return self.sub(author).last_message
	def last_timestamp(self, author):
		return float(self.sub(author).last_timestamp)
	def last_embed(self, author):
		return self.sub(author).last_embed


	def identical_spam(self, author):
		return self.sub(author).identical_spam
	def inc_identical_spam(self, author):
		self.sub(author).identical_spam += 1
	def reset_identical_spam(self, author):
		self.sub(author).identical_spam = 0

	def random_spam(self, author):
		return self.sub(author).random_spam
	def inc_random_spam(self, author):
		self.sub(author).random_spam += 1
	def reset_random_spam(self, author):
		self.sub(author).random_spam = 0

	def add_warning(self, category, author):
		self.sub(author).add_warning(category)
	def add_action(self, category, author):
		self.sub(author).add_action(category)