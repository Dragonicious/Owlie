import json
from Classes.Subject import Subject

class Holder:
	hold = []
	def __init__(self):
		if not self.hold:
			self.hold = self.load_data()
		pass

	def load_data(self):
		loaded_data = None
		try:
			with open('holder.json', 'r') as file:
				loaded_data = json.load(file)
		except:
			return []
		if loaded_data:
			for subject in loaded_data:
				self.add_subject(Subject(subject, True))
			return self.hold
		else:
			return []

	def save_data(self):
		try:
			with open('holder.json', 'w') as file:
				file.write(json.dumps([subject.__dict__ for subject in self.hold]))
		except Exception as inst:
			print('Failed to save', inst)

	def add_subject(self, subject):
		if subject.id not in self.subjects():
			self.hold.append(subject)

	def update(self, message):
		self.sub(message.author.id).renew(message)

	def subjects(self):
		subject_array = [subject.id for subject in self.hold]
		return subject_array

	def sub(self, sub_id):
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