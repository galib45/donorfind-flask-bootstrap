import os
import flask
import uuid
import cv2
import numpy

# create the blueprint
image = flask.Blueprint(
				'image', 
				__name__, 
				template_folder='templates', 
				static_folder='static',
				url_prefix = '/image'
			)

def bounding_box(img):
	grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	rows, cols = grayscale.shape
	edges = cv2.Canny(grayscale, threshold1=30, threshold2=100)
	top = edges.flatten().nonzero()[0][0] // cols
	bottom = edges.flatten().nonzero()[0][-1] // cols
	left = edges.transpose().flatten().nonzero()[0][0] // rows
	right = edges.transpose().flatten().nonzero()[0][-1] // rows
	return left, top, right, bottom

def crop_image(filepath, imagetype):
	img = cv2.imread(filepath)
	grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	rows, cols = grayscale.shape

	left, top, right, bottom = bounding_box(img)
	# print(left, top, right, bottom)

	if imagetype == 'photo':
		if rows == cols: final = img
		elif rows > cols: final = img[top:top+cols, 0:cols]
		else: 
			colstart = cols//2 - (rows - top)//2
			colend = cols//2 + (rows - top)//2
			final = img[top:rows, colstart:colend]
		resize_down = cv2.resize(final, (300, 300), interpolation=cv2.INTER_LINEAR)
	elif imagetype == 'sign':
		box_width = right - left
		box_height = bottom - top
		recommended_height = box_width/300*80
		print(box_height, box_width)
		if box_height <= recommended_height:
			expansion = recommended_height - box_height
			rowstart = top - int(expansion//2)
			rowend = bottom + int(expansion//2)
			colstart, colend = left, right
		else:
			recommended_width = box_height/80*300
			expansion = recommended_width - box_width
			colstart = left - int(expansion//2)
			colend = right + int(expansion//2)
			rowstart, rowend = top, bottom
		# print(rowstart, rowend, colstart, colend)
		final = img[rowstart:rowend, colstart:colend]
		resize_down = cv2.resize(final, (300, 80), interpolation=cv2.INTER_LINEAR)
	cv2.imwrite(filepath, resize_down)

@image.route('/', methods=['GET'])
def index():
	dirpath = 'image/uploads'
	for filename in os.listdir(dirpath):
		filepath = os.path.join(dirpath, filename)
		if filename != '.gitignore' and os.path.isfile(filepath): os.remove(filepath)

	return flask.render_template('image.html')

@image.route('/', methods=['POST'])
def process_image():
	imagetype = flask.request.form['imagetype']
	inputFile = flask.request.files['file']
	if inputFile.filename != '':
		# save the file with a random name
		extension = '.' + inputFile.filename.split('.')[-1]
		randomname = uuid.uuid4().hex
		filename = randomname + extension
		filepath = 'image/uploads/' + filename
		inputFile.save(filepath)
		crop_image(filepath, imagetype)
		return filename		
	return 'Error - no file specified'