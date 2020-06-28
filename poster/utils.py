from PIL import Image, ImageDraw, ImageFont
import os
import mimetypes
import base64

def getDataUrl(filename):
	if os.path.isfile(filename):
		with open(filename, 'rb') as file:
			data = b''.join(base64.encodebytes(file.read()).splitlines()).decode()
		mimetype = mimetypes.guess_type(filename)[0]
		prefix = 'data:,' if mimetype==None else 'data:'+mimetype+';base64,'
		return prefix + data
	else:
		return None

def wrapText(text, font, max_width):
	lines = text.split('\n')
	output = []
	for line in lines:
		if line:
			# do processing
			if font.getsize(line)[0] <= max_width: 
				output.append(line)
			else:
				words = line.split(' ')
				wrapped = ''
				for word in words:
					if font.getsize(word)[0] > max_width: 
						output.append(word)
					else:
						if wrapped:
							wrapped += ' ' + word
						else:
							wrapped = word
						if font.getsize(wrapped)[0] > max_width:
							wrapped = wrapped[:len(wrapped)-len(word+' ')]
							output.append(wrapped)
							wrapped = word
				output.append(wrapped)
		else:
			output.append(line)
	return output

def calcHeight(lines, font, line_spacing):
	num_lines = len(lines)
	line_height = font.getsize('hg')[1]
	total_height = line_height * num_lines + line_spacing * (num_lines-1)
	return total_height

def draw_multiline_text(image, position, lines, color, font, line_spacing):
	num_lines = len(lines)
	line_height = font.getsize('hg')[1]
	total_height = line_height * num_lines + line_spacing * (num_lines-1)
	multiline_text = '\n'.join(lines)

	draw = ImageDraw.Draw(image)
	draw.multiline_text(position, multiline_text, color, font=font, spacing=line_spacing)