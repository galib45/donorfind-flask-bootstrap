import os
import flask
import mistune
from github import Github
from .models import *

# create the blueprint
pathology = flask.Blueprint(
				'pathology', 
				__name__, 
				template_folder='templates', 
				static_folder='static',
				url_prefix = '/pathology'
			)

# initialize the github repository of the database
user = Github('galib45', 'ribosome80S').get_user()
repo = user.get_repo('galib-cloud')
database_file = repo.get_contents('pathology/database.db')

# download database if not found
if not os.path.isfile('pathology/database.db'):
	file_content = database_file.decoded_content
	with open('pathology/database.db', 'wb') as file:
		file.write(file_content)


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

		# updating the database on github repo
		with open('pathology/database.db', 'rb') as file:
			new_content = file.read()
		sha_replaced = repo.get_contents('pathology/database.db').sha
		repo.update_file('pathology/database.db', 'data added', new_content, sha_replaced)
	return flask.redirect(flask.url_for('.index'))

@pathology.route('/post/<int:id>')
def post(id):
	if Article.select().where(Article.id==id).exists():
		article = Article.get(id)
		article.view_count += 1
		article.save()
		
		# updating the database on github repo
		with open('pathology/database.db', 'rb') as file:
			new_content = file.read()
		sha_replaced = repo.get_contents('pathology/database.db').sha
		repo.update_file('pathology/database.db', 'data added', new_content, sha_replaced)
		
		return flask.render_template('post.html', article=article)
	else:
		return flask.redirect(flask.url_for('.index')) 

@pathology.route('/articles')
def articles():
	articles = Article.select().order_by(Article.id.desc()).paginate(1, 10)
	total = Article.select().count()
	if 'page' in flask.request.args:
		page_num = flask.request.args['page']
	else: page_num = 1
	max_pages = total // 10 + 1
	return flask.render_template('articles.html', articles=articles, page_num=page_num, total=total, max_pages=max_pages)

@pathology.route('/create', methods=['GET', 'POST'])
def add():
	if flask.request.method == 'GET':
		return flask.render_template('create.html')
	else:
		form = flask.request.form
		title = form['title']
		subtitle = form['subtitle']
		author = form['author']
		content = mistune.markdown(form['content'])

		article = Article.create(title=title, subtitle=subtitle, author=author, content=content)
		article.save()
		
		print(title + ', ' + subtitle + ', ' + author + ', ' + content)

		# updating the database on github repo
		with open('pathology/database.db', 'rb') as file:
			new_content = file.read()
		sha_replaced = repo.get_contents('pathology/database.db').sha
		repo.update_file('pathology/database.db', 'data added', new_content, sha_replaced)

		return flask.redirect(flask.url_for('.index'))