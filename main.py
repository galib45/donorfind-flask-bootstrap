import flask
import database

app = flask.Flask(__name__)
db = database.Database()

@app.route('/')
def index():
	db.sort()
	stat = db.stat
	return flask.render_template('index.html', data=stat)

@app.route('/add', methods=['GET', 'POST'])
def add():
	if flask.request.method == 'GET':
		return flask.render_template('add.html')
	else:
		form = flask.request.form
		name = form['name']
		contact_no = '0' + form['contact_no']
		blood_group = form['blood_group']
		remarks = form['remarks']

		db.add(name, contact_no, blood_group, remarks)

		return flask.redirect(flask.url_for('index'))

@app.route('/search', methods=['GET', 'POST'])
def search():
	if flask.request.method == 'GET':
		return flask.render_template('search.html')
	else:
		qstring = flask.request.form['qstring'].upper()
		if '+' in qstring or '-' in qstring:
			qstring = qstring.replace(' ', '')
			qstring = qstring.replace('(', '')
			qstring = qstring.replace(')', '')
			qstring = qstring.replace('VE', '')
			qstring = qstring.replace('+', '(+VE)')
			qstring = qstring.replace('-', '(-VE)')
			print(qstring)
		indexes = db.get_index(qstring)
		for index in indexes: 
			print(db.data[index])
		
		return flask.render_template('results.html', qstring=qstring, indexes=indexes, db=db.data)
		
@app.route('/bot')
def bot():
	if flask.request.method == 'GET':
		print("Got it...")
	return 'bot'
		
if __name__=='__main__':
	app.run()