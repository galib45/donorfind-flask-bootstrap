import os
import operator
import flask
from github import Github
from .models import *

# create the blueprint
donorfind = flask.Blueprint(
				'donorfind', 
				__name__, 
				template_folder='templates', 
				static_folder='static',
				url_prefix = '/donorfind'
			)

def extract_num(value):
	return ''.join([c for c in value if c.isdigit()])

global repo

# initialize the github repository of the database
token = os.environ.get('github_access_token')
g = Github(token)
user = g.get_user()
repo = g.get_repo('galib45/galib-cloud')
database_file = repo.get_contents('database.db')

# download database if not found
if not os.path.isfile('donorfind/database.db'):
	file_content = database_file.decoded_content
	with open('donorfind/database.db', 'wb') as file:
		file.write(file_content)

# routing commands
@donorfind.route('/')
def index():
	categories = set([x.blood_group for x in Donor.select()])
	stat = [(cat, Donor.select().where(Donor.blood_group==cat).count()) for cat in categories]
	stat.append(('Total', Donor.select().count()))
	stat = sorted(stat, key=operator.itemgetter(1), reverse=True)
	
	return flask.render_template('index.html', data=stat)

@donorfind.route('/add', methods=['GET', 'POST'])
def add():
	if flask.request.method == 'GET':
		return flask.render_template('add.html')
	else:
		# getting data from the addform
		form = flask.request.form
		name = form['name']
		contact_no = form['contact_no']
		batch_type = form['batch_type']
		batch = form['batch']
		blood_group = form['blood_group']
		
		#formatting data for adding to database
		name = name.upper()
		contact_no = '0' + extract_num(contact_no)[-10:]
		batch = batch_type + '-' + extract_num(batch)
		blood_group = blood_group.upper()
		
		#db.add_data((name, contact_no, batch_type, batch, blood_group))
		print(name, contact_no, batch, blood_group)
		
		if Donor.select().where(Donor.phone==contact_no).exists():
			donor = Donor.get(Donor.phone==contact_no)
			donor.name = name
			donor.batch = batch
			donor.blood_group = blood_group
		else:
			donor = Donor.create(
						name=name, phone=contact_no, 
						batch=batch, blood_group=blood_group
					)
		donor.save()
		
		# updating the database on github repo
		with open('donorfind/database.db', 'rb') as file:
			new_content = file.read()
		sha_replaced = repo.get_contents('database.db').sha
		repo.update_file('database.db', 'data added', new_content, sha_replaced)

		return flask.redirect(flask.url_for('.index'))

@donorfind.route('/search', methods=['GET', 'POST'])
def search():
	if flask.request.method == 'GET':
		if 'q' in flask.request.args:
			qstring = flask.request.args['q']
			data = Donor.select().where(
					(Donor.blood_group==qstring) | 
					(Donor.name.contains(qstring)) |
					(Donor.phone.contains(qstring)) |
					(Donor.batch.contains(qstring))
				).order_by(Donor.name)
			return flask.render_template('results.html', qstring=qstring, data=data)
		return flask.render_template('search.html')
	else:
		qstring = flask.request.form['qstring']
		return flask.redirect(flask.url_for('.search', q=qstring))
