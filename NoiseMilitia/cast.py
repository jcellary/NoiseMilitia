import time
import pychromecast

class ChromeCast(object):

	def display_warning(self):
		
		self.cast = pychromecast.get_chromecast(friendly_name="Dat API")
		
		print(self.cast.device)
		self.cast.play_media("https://dl.dropboxusercontent.com/u/94890729/warning.mp4", pychromecast.STREAM_TYPE_BUFFERED, "video/mp4")
