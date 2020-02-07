from datetime import datetime
import peewee

db = peewee.SqliteDatabase('pathology/database.db')

class BaseModel(peewee.Model):
	class Meta:
		database = db

class Article(BaseModel):
	id = peewee.AutoField(primary_key=True)
	title = peewee.CharField()
	subtitle = peewee.CharField()
	author = peewee.CharField()
	content = peewee.TextField()
	date_created = peewee.DateTimeField(default=datetime.now())
	view_count = peewee.IntegerField(default=0)

	def __repr__(self):
		return 'Title: {}\nSubtitle: {}\nAuthor: {}\nContent: {}\nDate Created: {}\n{} views'.format(self.title, self.subtitle, self.author, self.content, self.date_created, self.view_count)
