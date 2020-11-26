import flask
import os
import datetime
from PIL import Image, ImageOps, ImageFilter
from github import Github

# create the blueprint
frame = flask.Blueprint(
				'frame', 
				__name__, 
				template_folder='templates', 
				static_folder='static',
				url_prefix = '/frame'
			)

global repo

# initialize the github repository of the database
token = os.environ.get('github-access-token')
user = Github(token).get_user()
repo = user.get_repo('galib-cloud')

@frame.route('/', methods=['GET', 'POST'])
def create_poster():
	if flask.request.method == 'GET':
		return flask.render_template('frame-index.html')
	else:
		file = flask.request.files['imagefile']
		filename = 'frame/image.' + file.filename.split('.')[-1] 
		file.save(filename)

		foreground = Image.open(filename).convert('RGB')
		if foreground.size[0] > foreground.size[1]:
			# landscape
			bgfilename = 'frame/landscape.png'
			thumbnailSize = (1100, 650)
			foreground.thumbnail(thumbnailSize)
			if foreground.size[0] > 1000:
				thumbnailSize = (1100, 600)
				foreground.thumbnail(thumbnailSize)
			if foreground.size[0] > 1050:
				thumbnailSize = (1100, 580)
				foreground.thumbnail(thumbnailSize)
		else:
			bgfilename = 'frame/portrait.png'
			thumbnailSize = (760, 880)

		background = Image.open(bgfilename).convert('RGBA')
		foreground.thumbnail(thumbnailSize)
		print(foreground.size)

		# white border
		bordered = ImageOps.expand(foreground, border=10, fill=0xffffff);

		# shadow
		size = (bordered.size[0]+100, bordered.size[1]+100)
		back = Image.new('RGBA', size, 0x00000000)
		shadow = Image.new('RGB', (size[0]-100, size[1]-100), 0xbbbbbb)
		back.paste(shadow, (50, 50))
		shadow = back.filter(ImageFilter.GaussianBlur(10))

		# paste the shadow
		pos = (
			(background.size[0] - shadow.size[0])//2, 
			(background.size[1] - shadow.size[1])//2
		)
		background.paste(shadow, pos, shadow)

		# paste the bordered image
		pos = (
			(background.size[0] - bordered.size[0])//2, 
			(background.size[1] - bordered.size[1])//2
		)
		background.paste(bordered, pos)

		filename = 'frame/framed-image.jpg'
		print(filename)
		background.convert('RGB').save(filename, format='JPEG')

		return flask.send_from_directory(
			'', filename, as_attachment=True, mimetype='image/jpeg', 
			attachment_filename='framed-'+file.filename
		)
		#return flask.redirect(flask.url_for('.create_poster'))
		'''form = flask.request.form
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
		return flask.redirect(githubURL)'''