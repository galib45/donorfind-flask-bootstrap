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