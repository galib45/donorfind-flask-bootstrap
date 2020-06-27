import flask
from portfolio.routes import portfolio
from donorfind.routes import donorfind
from pathology.routes import pathology

import datetime
import textwrap
from PIL import Image, ImageDraw, ImageFont

font = ImageFont.truetype('Product Sans Regular.ttf', 36)
def wrapText(text, width):
	text_array = []
	for line in text.split('\n'):
		text_array.extend(textwrap.wrap(line, width=width))
	text = "\n".join(text_array)
	lines = len(text_array)
	text_height = font.getsize(text)[1]*lines + 20*lines
	return text, text_height

# initialize the app
app = flask.Flask(__name__)
app.register_blueprint(portfolio)
app.register_blueprint(donorfind)
app.register_blueprint(pathology)

@app.route('/file/<path:path>')
def send_file(path):
	return flask.send_from_directory('', path)

@app.route('/poster', methods=['GET', 'POST'])
def create_poster():
	if flask.request.method == 'GET':
		return flask.render_template('poster.html')
	else:
		form = flask.request.form
		question = form['question']
		special_line = form['special']
		options = form['options']

		date_created = datetime.datetime.now() + datetime.timedelta(hours=6)
		date_created = str(date_created)
		filename = 'poster-' + date_created.replace(':', '').replace(' ', '').replace('-', '')[:14] + '.png'
		print(filename)

		que_text, que_h = wrapText(question, 50)
		spe_text, spe_h = wrapText(special_line, 50)
		opt_text, opt_h = wrapText(options, 50)

		logo = Image.open('logo.png')
		logo_w, logo_h = logo.size

		width = 960
		height = 60 + que_h + 60 + spe_h + 60 + opt_h + 120 + logo_h + 30

		image = Image.new('RGB', (width, height), color='white')
		draw = ImageDraw.Draw(image)
		draw.multiline_text((60, 60), que_text, (0, 0, 0), font=font, spacing=20)
		draw.multiline_text((60, 60+que_h+60), spe_text, (0, 0, 255), font=font, spacing=20)
		draw.multiline_text((100, 60+que_h+60+spe_h+60), opt_text, (0, 0, 0), font=font, spacing=20)
		image.paste(logo, ((width-logo_w)//2, (height-logo_h-30)))
		image.save(filename)

		return flask.send_from_directory('', filename, as_attachment=True)

if __name__=='__main__':
	app.run()