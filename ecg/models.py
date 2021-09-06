import peewee

db = peewee.SqliteDatabase('ecg/database.db')

class BaseModel(peewee.Model):
	class Meta:
		database = db

class ECG(BaseModel):
	image_id = peewee.CharField(max_length=110, primary_key=True, unique=True)
	dx = peewee.CharField(max_length=80)
	expl = peewee.TextField()
	tags = peewee.TextField()

	def __repr__(self):
		return 'Image ID: {}\nDx: {}\nExplanation: {}\nTags: {}'.format(
			self.image_id, self.dx, self.expl, self.tags
		)
