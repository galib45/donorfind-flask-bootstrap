import flask
import os
import datetime
from .utils import *
from PIL import Image, ImageDraw, ImageFont
from github import Github

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

global repo

# initialize the github repository of the database
token = os.environ.get('github-access-token')
user = Github(token).get_user()
repo = user.get_repo('galib-cloud')

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
			# print(paragraph)
			height, lines, font, color = paragraph
			draw_multiline_text(image, (60, height), lines, color, font, line_spacing)
		
		filename = 'poster-' + datetime.datetime.utcnow().isoformat().replace(':', '-').replace('-', '') + '.png'
		image.save(filename)

		# save the file to Github
		with open(filename, 'rb') as file:
			content = file.read()
		repo.create_file(
			'posters/'+filename, 
			'Poster Created on UTC time - '+datetime.datetime.utcnow().isoformat(),
			content
		)

		# get the data url then delete the file
		# data_url = getDataUrl('bg.png')
		os.remove('bg.png')
		os.remove(filename)

		# return the data url
		# return '<img src="'+data_url+'"'+'>'
		githubURL = 'https://raw.githubusercontent.com/galib45/galib-cloud/master/posters/' + filename
		return flask.redirect(githubURL)