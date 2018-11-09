import operator

class Database(object):
	"""docstring for Database"""
	def __init__(self, filename='database.db'):
		super(Database, self).__init__()
		self.filename = filename
		self.data = []

		with open(self.filename, 'r') as file:
			rows = file.read().split('\n')
			for row in rows:
				data = row.split(',')
				self.data.append(data)

		print('Total entries:', len(self.data))

	def get_index(self, query_string):
		indexes = []
		for row in self.data:
			for data in row:
				if query_string in data:
					indexes.append(self.data.index(row))
		return indexes

	def update(self):
		with open(self.filename, 'w') as file:
			for row in self.data:
				for data in row:
					file.write(data.upper())
					if row.index(data) != 3: file.write(',')
				if self.data.index(row) != len(self.data)-1:
					file.write('\n')
		self.__init__()

	def add(self, name, contact_no, blood_group, remarks):
		name = name.upper()
		contact_no = contact_no.upper()
		blood_group = '[' + blood_group.upper() + ']'
		remarks = remarks.upper()

		index = -1
		if len(self.get_index(name)):
			index = self.get_index(name)[0]
		elif len(self.get_index(contact_no)):
			index = self.get_index(contact_no)[0]

		if index == -1:
			self.data.append([name, contact_no, blood_group, remarks])
		else:
			self.data[index] = [name, contact_no, blood_group, remarks]

		self.update()

	def sort(self):
		categories = set()
		stat = []
		result = []
		for row in self.data:
			categories.add(row[2])
		categories = list(categories)
		for category in categories:
			segment = [self.data[index] for index in self.get_index(category)]
			stat.append([category, len(segment)])
		stat = sorted(stat, key=operator.itemgetter(1), reverse=True)
		self.stat = stat
		for category in stat:
			segment = [self.data[index] for index in self.get_index(category[0])]
			result += sorted(segment, key=operator.itemgetter(0))
		self.data = result
		for i in self.stat:
			i[0] = i[0][1:-1]
		self.stat.insert(0, ['Total', len(self.data)])
		for i in self.stat:
			i[0] = i[0].lower()
			i[0] = i[0][:1].upper() + i[0][1:]
			if i[0][1]=='b': i[0] = i[0][:2].upper() + i[0][2:]
		self.categories = []
		for i in self.stat:
			self.categories.append(i[0])

		self.categories = self.categories[1:]

		print('Categories', self.categories)
		self.update()