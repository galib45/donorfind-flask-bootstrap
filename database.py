import sqlite3 as lite
import db_helper

class Database:
	def __init__(self, filename='database.db'):
		self.connection = lite.connect(filename, check_same_thread=False)
		self.cursor = self.connection.cursor()
		
	def add_data(self, data):
		db_helper.add_to_db(data, self.cursor)
		self.connection.commit()

	def search_data(self, query_string):
		return db_helper.query(query_string, self.cursor)

	def statistics(self):
		return db_helper.statistics(self.cursor)