import flask
import os
from .utils import *
from PIL import Image, ImageDraw, ImageFont

# create the blueprint
poster = flask.Blueprint(
				'poster', 
				__name__, 
				template_folder='templates', 
				static_folder='static',
				url_prefix = '/poster'
			)

rfont = ImageFont.truetype('poster/Product Sans Regular.ttf', 36)
bfont = ImageFont.truetype('poster/Product Sans Bold.ttf', 36)

@poster.route('/', methods=['GET', 'POST'])
def create_poster():
	if flask.request.method == 'GET':
		return flask.render_template('poster.html')
	else:
		form = flask.request.form
		inputText = form['input']
		paragraphs = []
		height = 60;
		line_spacing = 20
		for paragraph in inputText.split('<--endblock-->')[:-1]:
			font = bfont if paragraph[0]=='t' else rfont
			color = paragraph[1:8]
			text = paragraph[8:]
			lines = wrapText(text, font, 840)
			paragraphs.append((height, lines, font, color))
			height += calcHeight(lines, font, line_spacing) + 60

		logo = Image.open('poster/logo.png')
		logo_w, logo_h = logo.size

		width = 960

		fg = Image.new('RGB', (width, height), color='white')
		bg = Image.new('RGB', (width, height), color='white')
		draw = ImageDraw.Draw(bg)
		fg.paste(logo, ((width-logo_w)//2, (height-logo_h)//2))
		Image.blend(bg, fg, 0.20).save('bg.png')
		
		image = Image.open('bg.png')
		for paragraph in paragraphs:
			print(paragraph)
			height, lines, font, color = paragraph
			draw_multiline_text(image, (60, height), lines, color, font, line_spacing)
		
		image.save('bg.png')

		# get the data url then delete the file
		data_url = getDataUrl('bg.png')
		os.remove('bg.png')

		# return the data url
		return '<img src="'+data_url+'"'+'>'