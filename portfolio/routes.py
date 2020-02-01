import flask

portfolio = flask.Blueprint(
				'portfolio', 
				__name__, 
				template_folder='templates', 
				static_folder='static',
			)

@portfolio.route('/')
def index():
	return flask.render_template('portfolio-index.html')