import os
import flask
from github import Github
from . import database
from . import db_helper

# create the blueprint
donorfind = flask.Blueprint(
				'donorfind', 
				__name__, 
				template_folder='templates', 
				static_folder='static'
			)

# initialize the github repository of the database
user = Github('galib45', 'ribosome80S').get_user()
repo = user.get_repo('galib-cloud')
database_file = repo.get_contents('database.db')

# download database if not found
if not os.path.isfile('donorfind/database.db'):
	file_content = database_file.decoded_content
	with open('donorfind/database.db', 'wb') as file:
		file.write(file_content)

# initialize the database
db = database.Database()

# routing commands
@donorfind.route('/')
def index():
	stat = db.statistics()
	return flask.render_template('index.html', data=stat)

@donorfind.route('/add', methods=['GET', 'POST'])
def add():
	if flask.request.method == 'GET':
		return flask.render_template('add.html')
	else:
		form = flask.request.form
		name = form['name']
		contact_no = form['contact_no']
		batch_type = form['batch_type']
		batch = form['batch']
		blood_group = form['blood_group']
		
		db.add_data((name, contact_no, batch_type, batch, blood_group))
		with open('database.db', 'rb') as file:
			new_content = file.read()
		sha_replaced = repo.get_contents('database.db').sha
		repo.update_file('database.db', 'data added', new_content, sha_replaced)

		return flask.redirect(flask.url_for('index'))

@donorfind.route('/search', methods=['GET', 'POST'])
def search():
	if flask.request.method == 'GET':
		if 'q' in flask.request.args:
			qstring = flask.request.args['q']
			data = db.search_data(qstring)
			return flask.render_template('results.html', qstring=qstring, data=data)
		return flask.render_template('search.html')
	else:
		qstring = flask.request.form['qstring']
		return flask.redirect(flask.url_for('search', q=qstring))

@donorfind.route('/file/<path:pathOftheFile>')
def send_file(pathOftheFile):
	return flask.send_from_directory('', pathOftheFile)