import flask

from portfolio.routes import portfolio
from donorfind.routes import donorfind
from pathology.routes import pathology
from poster.routes import poster
from frame.routes import frame
from youtube.routes import youtube

# initialize the app
app = flask.Flask(__name__)
app.register_blueprint(portfolio)
app.register_blueprint(donorfind)
app.register_blueprint(pathology)
app.register_blueprint(poster)
app.register_blueprint(frame)
app.register_blueprint(youtube)

@app.route('/file/<path:path>')
def send_file(path):
	return flask.send_from_directory('', path)

if __name__=='__main__':
	app.run(debug=False)