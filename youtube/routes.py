import flask
from datetime import timedelta
from pytube import YouTube, Playlist
from humanfriendly import format_size

youtube = flask.Blueprint(
				'youtube', 
				__name__, 
				template_folder='templates', 
				static_folder='static',
				url_prefix='/youtube'
			)

@youtube.route('/', methods=['GET', 'POST'])
def index():
	if flask.request.method == 'GET':
		return flask.render_template('youtube-index.html')
	else:
		form = flask.request.form
		url = form['url']

		if url.find('list=') != -1:
			pl = Playlist(url)
			files = [file for file in pl.videos]
			playlist = (pl.title, len(files), files)
			return flask.render_template('youtube-index.html', playlist=playlist, format_size=format_size)

		else:
			yt = YouTube(url)
			title = yt.title
			duration = timedelta(seconds=yt.length)
			
			audios = yt.streams.filter(type='audio').order_by('filesize')
			videos = yt.streams.filter(
				type='video', 
				custom_filter_functions=[lambda s: s.includes_audio_track]
			).order_by('filesize')

			data = (title, duration, audios, videos, yt)
			
			return flask.render_template('youtube-index.html', data=data, format_size=format_size)