import flask

# create the blueprint
poster = flask.Blueprint(
				'image', 
				__name__, 
				template_folder='templates', 
				static_folder='static',
				url_prefix = '/image'
			)

@poster.route('/', methods=['GET', 'POST'])
def create_poster():
	if flask.request.method == 'GET':
		return flask.render_template('image.html')
	else:
		print("POST - not implemented")