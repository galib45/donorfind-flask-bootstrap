import os
import datetime
import random
import operator
import flask
from github import Github
from .models import *

# create the blueprint
ecg = flask.Blueprint(
				'ecg', 
				__name__, 
				template_folder='templates', 
				static_folder='static',
				url_prefix = '/ecg'
			)

global repo
global alltags

alltags = [
		'Normal ECG', 'Left Ventricular Hypertrophy',
		'Right Ventricular Hypertrophy', 'Biventricular Hypertrophy',
		'Left Atrial Enlargement', 'Right Atrial Enlargement',
		'Biatrial Enlargement', 'SA Block', 'AV Block',
		'Nodal Rhythm',
		'Myocardial Infarction', 'Pericarditis',
		'Right Bundle Branch Block', 'Left Bundle Branch Block', 
		'Hemiblocks', 'Sinus Arrhythmia',
		'Sinus Tachycardia', 'Sinus Bradycardia',
		'Atrial Ectopic', 'Atrial Fibrillation', 'Atrial Flutter',
		'Supraventricular Tachycardia', 'Atrial Tachycardia',
		'Ventricular Ectopic',
		'Ventricular Tachycardia', 'Ventricular Fibrillation',
		'Pulmonary Embolism',		
		'WPW Syndrome', 'LGL Syndrome'
	]


# initialize the github repository of the database
token = os.environ.get('github-access-token')
user = Github(token).get_user()
repo = user.get_repo('galib-cloud')

try:
	database_file = repo.get_contents('ecg/database.db')
except:
	with open('ecg/database.db', 'rb') as file:
		contents = file.read()
		repo.create_file(
			'ecg/database.db', 
			'Created database file',
			contents
		)

# download database if not found
if not os.path.isfile('ecg/database.db'):
	file_content = database_file.decoded_content
	with open('ecg/database.db', 'wb') as file:
		file.write(file_content)

def updateDatabaseInRepo(commitMessage):
	# updating the database on github repo
	with open('ecg/database.db', 'rb') as file:
		new_content = file.read()
	sha_replaced = repo.get_contents('ecg/database.db').sha
	repo.update_file('ecg/database.db', commitMessage, new_content, sha_replaced)

# routing commands
@ecg.route('/')
def index():
	data = ECG.select()
	ecg_list = []
	for entry in data:
		ecg_list.append([
			entry.image_id, entry.dx, 
			entry.expl, entry.tags
		])
	random.shuffle(ecg_list)
	return flask.render_template('ecg-index.html', data=ecg_list)

@ecg.route('/library')
def library():
	return flask.render_template('ecg-library.html', tags=alltags)

@ecg.route('/create-test', methods=['GET', 'POST'])
def createTest():
	if flask.request.method == 'GET':
		return flask.render_template('create-test.html', tags=alltags)
	else:
		# getting data from the form
		form = flask.request.form
		code = form['code']
		return flask.redirect(flask.url_for('.test', code=code))

@ecg.route('/test/<int:code>')
def test(code):
	binary_code = bin(code)[2:].zfill(29)
	indices = [i for i, x in enumerate(binary_code) if x == '1']
	id_list = []
	ecg_list = []

	for index in indices:
		data = ECG.select().where(ECG.tags.contains(alltags[index]))
		for entry in data:
			if entry.image_id not in id_list:
				id_list.append(entry.image_id)
				ecg_list.append([
					entry.image_id, entry.dx, 
					entry.expl, entry.tags
				])
	random.shuffle(ecg_list)
	return flask.render_template('test.html', data=ecg_list, code=code)

@ecg.route('/add-ecg', methods=['GET', 'POST'])
def add_ecg():
	if flask.request.method == 'GET':
		return flask.render_template('add-ecg.html', tags=alltags)
	else:
		# getting data from the form
		form = flask.request.form
		image = flask.request.files['image']
		imagefile = image.stream
		imagefile.seek(0)
		content = imagefile.read()
		dx = form['dx']
		expl = form['expl']
		tags = form['tags']

		extension = os.path.splitext(image.filename)[1]

		filename = datetime.datetime.utcnow().isoformat()
		filename = filename.replace(':', '-').replace('-', '')
		filename = filename.split('.')[0]
		filename += extension
		filename = 'ecg-' + filename
		
		repo.create_file(
			'ecg/' + filename, 
			'ECG Uploaded on UTC time - '+datetime.datetime.utcnow().isoformat(),
			content
		)

		githubURL = 'https://raw.githubusercontent.com/galib45/galib-cloud/master/ecg/' + filename
		
		ecg = ECG.create(
			image_id=githubURL, 
			dx=dx, expl=expl, tags=tags
		)
		ecg.save()

		# update database in repo
		updateDatabaseInRepo('Added ' + filename)

		return flask.redirect(flask.url_for('.add_ecg'))

@ecg.route('/delete/<string:id>')
def delete(id):
	# delete the image file in github
	contents = repo.get_contents('ecg/' + id)
	repo.delete_file(contents.path, 'Deleted ' + id, contents.sha)

	# check if ecg exists
	ghBaseURL = githubURL = 'https://raw.githubusercontent.com/galib45/galib-cloud/master/ecg/'
	image_id = ghBaseURL + id
	if ECG.select().where(ECG.image_id==image_id).exists():
		# delete the database entry
		ecg = ECG.get(id)
		ecg.delete_instance()

		# update database in repo
		updateDatabaseInRepo('Deleted ' + id)
	
	return flask.redirect(flask.url_for('.add_ecg'))

@ecg.route('/search', methods=['GET', 'POST'])
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
