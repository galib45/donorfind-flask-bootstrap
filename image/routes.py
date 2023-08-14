import os
import flask
import uuid
import cv2
import numpy
import rembg

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
		face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
		face = face_classifier.detectMultiScale(grayscale, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))
		x, y, w, h = face[0]
		face_width = w
		face_center_x, face_center_y = int(x + w//2), int(y + h//2)
		# expand horizontally by 150% of the face_width
		expanded_left = max(0, int(face_center_x - face_width*1.5)) 
		expanded_right = min(cols, int(face_center_x + face_width*1.5))
		expanded_width = expanded_right - expanded_left
		# expand upwards by 1/3 of the face width
		up_exp = max(0, int(y-face_width//3))
		expanded_top = 0 if up_exp + expanded_width >= rows else up_exp
		expanded_bottom = min(up_exp+expanded_width, rows)
		# if rows == cols: final = img
		# elif rows > cols: final = img[top:top+cols, 0:cols]
		# else: 
		# 	colstart = cols//2 - (rows - top)//2
		# 	colend = cols//2 + (rows - top)//2
		# 	final = img[top:rows, colstart:colend]
		final = img[expanded_top:expanded_bottom, expanded_left:expanded_right]
		print(final.shape)
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
	removebg = flask.request.form['removebg']
	inputFile = flask.request.files['file']
	if inputFile.filename != '':
		# save the file with a random name
		extension = '.' + inputFile.filename.split('.')[-1]
		randomname = uuid.uuid4().hex
		filename = randomname + extension
		filepath = 'image/uploads/' + filename
		inputFile.save(filepath)
		if removebg == 'on':
			image = cv2.imread(filepath)
			session = rembg.new_session('u2netp')
			output = rembg.remove(image, session=session, bgcolor=(255, 255, 255, 255))
			cv2.imwrite(filepath, output)
		crop_image(filepath, imagetype)
		return filename		
	return 'Error - no file specified'