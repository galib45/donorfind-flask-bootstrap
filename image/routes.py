import flask
import uuid

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
	randomfilename = uuid.uuid4().hex + '.' + inputFile.filename.split('.')[-1]
	if inputFile.filename != '':
		inputFile.save('image/uploads/' + randomfilename)
	return randomfilename