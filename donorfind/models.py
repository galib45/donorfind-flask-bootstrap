import peewee

db = peewee.SqliteDatabase('donorfind/database.db')

class BaseModel(peewee.Model):
	class Meta:
		database = db

class Donor(BaseModel):
	name = peewee.CharField(max_length=80)
	phone = peewee.CharField(max_length=15, primary_key=True, unique=True)
	batch = peewee.CharField(max_length=10)
	blood_group = peewee.CharField(max_length=10)

	def __repr__(self):
		return 'Name: {}\nPhone: {}\nBatch: {}\nBlood Group: {}'.format(self.name, self.phone, self.batch, self.blood_group)
