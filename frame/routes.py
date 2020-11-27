import flask
import os
from datetime import datetime, timedelta
import glob
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

@frame.route('/withoutprogress', methods=['GET', 'POST'])
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

@frame.route('/get/<datetime>/<name>')
def get(datetime, name):
	filename = 'frame/framed-' + datetime + '.jpg'
	return flask.send_from_directory(
		'', filename, as_attachment=True, mimetype='image/jpeg', 
		attachment_filename='framed-'+name
	)

@frame.route('/', methods=['GET', 'POST'])
def create_poster_withprogress():
	now = datetime.utcnow()
	filelist = glob.glob('frame/framed-*.jpg')
	for filename in filelist:
		timestamp = float(filename.split('framed-')[-1][:-4])
		file_ctime = datetime.fromtimestamp(timestamp)
		if now - file_ctime > timedelta(minutes=5):
			os.remove(filename)
	
	if flask.request.method == 'POST':
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

		creation_time = datetime.utcnow()
		timestamp = datetime.timestamp(creation_time)
		filename = 'frame/framed-' + str(timestamp) + '.jpg'
		print(filename)
		background.convert('RGB').save(filename, format='JPEG')
		return str(timestamp) + '||' + file.filename
	
	else:
		return flask.render_template('frame-progress.html')