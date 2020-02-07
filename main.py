import flask
from portfolio.routes import portfolio
from donorfind.routes import donorfind
from pathology.routes import pathology

# initialize the app
app = flask.Flask(__name__)
app.register_blueprint(portfolio)
app.register_blueprint(donorfind)
app.register_blueprint(pathology)

@app.route('/file/<path:path>')
def send_file(path):
	return flask.send_from_directory('', path)

if __name__=='__main__':
	app.run()