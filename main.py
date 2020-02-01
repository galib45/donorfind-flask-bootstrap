#import sys
import flask
from donorfind.routes import donorfind

# initialize the app
app = flask.Flask(__name__)
app.register_blueprint(donorfind)

if __name__=='__main__':
	app.run()