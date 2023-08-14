import flask

# create the blueprint
image = flask.Blueprint(
				'image', 
				__name__, 
				template_folder='templates', 
				static_folder='static',
				url_prefix = '/image'
			)

@image.route('/', methods=['GET'])
def index():
	return flask.render_template('image.html')


@image.route('/', methods=['POST'])
def process_image():
	inputFile = flask.request.files['file']
	if inputFile.filename != '':
		inputFile.save(inputFile.filename)
	return flask.redirect(flask.url_for('.index'))