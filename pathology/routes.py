import os
import math
import datetime
import flask
import werkzeug
from github import Github
from bs4 import BeautifulSoup
from .utils import *
from .models import *

# create the blueprint
pathology = flask.Blueprint(
				'pathology', 
				__name__, 
				template_folder='templates', 
				static_folder='static',
				url_prefix = '/pathology'
			)

global repo

# initialize the github repository of the database
user = Github('galib45', 'ribosome80S').get_user()
repo = user.get_repo('galib-cloud')
database_file = repo.get_contents('pathology/database.db')

# download database if not found
if not os.path.isfile('pathology/database.db'):
	file_content = database_file.decoded_content
	with open('pathology/database.db', 'wb') as file:
		file.write(file_content)

def update_repo():
	# updating the database on github repo
	print('updating repo ...')
	with open('pathology/database.db', 'rb') as file:
		new_content = file.read()
	sha_replaced = repo.get_contents('pathology/database.db').sha
	repo.update_file('pathology/database.db', 'data added', new_content, sha_replaced)
	print('done.')

def addIds(html):
	# add ids to h1, h2, h3, h4 tags for internal links
	soup = BeautifulSoup(html, 'html.parser')
	selector = 'h1, h2, h3, h4'
	headings = soup.select(selector)
	print(headings)
	for heading in headings:
		heading['id'] = heading.get_text().strip().replace(' ', '_').lower()
	return str(soup)

@pathology.route('/')
def index():
	recents = Article.select().order_by(Article.id.desc()).paginate(1, 5)
	return flask.render_template('patho-index.html', recents=recents)

@pathology.route('/about')
def about():
	return flask.render_template('about.html')

@pathology.route('/delete/<int:id>')
def delete(id):
	if Article.select().where(Article.id==id).exists():
		article = Article.get(id)
		article.delete_instance()
		update_repo()
	return flask.redirect(flask.url_for('.index'))

@pathology.route('/post/<int:id>')
def post(id):
	if Article.select().where(Article.id==id).exists():
		article = Article.get(id)
		article.view_count += 1
		article.save()
		
		update_repo()
		
		return flask.render_template('post.html', article=article)
	else:
		return flask.redirect(flask.url_for('.index')) 

@pathology.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
	if Article.select().where(Article.id==id).exists():
		article = Article.get(id)
		if flask.request.method == 'GET':
			content = [article.title, article.subtitle, article.author, article.content]
			return flask.render_template('create.html', content=content)
		else:
			form = flask.request.form
			article.title = form['title']
			article.subtitle = form['subtitle']
			article.author = form['author']
			article.content = addIds(form['content'])
			article.save()
		
			print(article.title + ', ' + article.subtitle + ', ' + article.author + ', ' + article.content)

			update_repo()
			return flask.redirect(flask.url_for('.index'))
	else:
		return flask.redirect(flask.url_for('.index'))

@pathology.route('/json')
def json():
	articles = Article.select().order_by(Article.id.desc())
	articles_list = []
	for article in articles:
		article_dict = article.__dict__['__data__']
		article_dict['date_created'] = article_dict['date_created'].strftime('%B %d, %Y %I:%M %p')
		article_dict['text'] = BeautifulSoup(article_dict['content'], 'html.parser').get_text()
		articles_list.append(article_dict)
	data = {'articles': articles_list}
	return flask.jsonify(data)

@pathology.route('/articles')
def articles():
	if 'page' in flask.request.args:
		page_num = int(flask.request.args['page'])
	else: page_num = 1
	if page_num<1: page_num=1

	if 'q' in flask.request.args:
		qstring = flask.request.args['q']
	else: qstring = ''
	
	items_per_page = 10
	articles = Article.select().where(
		Article.title.contains(qstring) |
		Article.subtitle.contains(qstring) |
		Article.content.contains(qstring)
		)
	total = articles.count()
	max_pages = math.ceil(total / items_per_page)

	articles = articles \
				.order_by(Article.id.desc()) \
				.paginate(page_num, items_per_page)	
	
	return flask.render_template(
		'articles.html', articles=articles, qstring=qstring,
		page_num=page_num, total=total, max_pages=max_pages)

@pathology.route('/create', methods=['GET', 'POST'])
def add():
	if flask.request.method == 'GET':
		return flask.render_template('create.html', content=['', '', '', ''])
	else:
		form = flask.request.form
		title = form['title']
		subtitle = form['subtitle']
		author = form['author']
		content = addIds(form['content'])
		date_created = datetime.datetime.now() + datetime.timedelta(hours=6)

		article = Article.create(title=title, subtitle=subtitle, author=author, content=content, date_created=date_created)
		article.save()
		
		print(title + ', ' + subtitle + ', ' + author + ', ' + content)

		update_repo()
		return flask.redirect(flask.url_for('.index'))

@pathology.route('/upload', methods=['GET', 'POST'])
def upload():
	if flask.request.method == 'GET':
		return flask.render_template('upload.html')
	else:
		# getting the file data & saving it
		file = flask.request.files['file']
		filename = 'pathology/' + werkzeug.secure_filename(file.filename)
		file.save(filename)

		# get the data url then delete the file
		data_url = getDataUrl(filename)
		os.remove(filename)

		# return the data url
		return data_url
		
		'''
		# reading the saved file and saving the content
		with open(filename, 'rb') as file:
			contents = file.read()
		upload_filename = filename[0:10] + str(os.path.getsize(filename)) + filename[10:]
		
		# removing the saved file
		os.remove(filename)
		filename = upload_filename
		fileExists = False
		for contentFile in repo.get_contents('pathology/'):
			if contentFile.path == filename:
				fileExists = True
		if fileExists:
			print('updating... ' + filename)
			sha_replaced = repo.get_contents(filename).sha
			repo.update_file(filename, 'update', contents, sha_replaced)
		else:
			print('uploading... ' + filename)
			repo.create_file(filename, 'upload', contents)
		base_url = 'https://raw.githubusercontent.com/galib45/galib-cloud/master/'
		return base_url + filename'''