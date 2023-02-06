import os
import threading

from bots.utils.common import FileConfig

class BotThread(threading.Thread):

	def __init__(self, sleep=5, notif_timeout=60, debug=False, cookies={}):
		super().__init__()
		self.setName(self.__class__.__qualname__)
		self._url = ''
		self._debug = debug
		self._stop = threading.Event()
		self._sleep = sleep
		self._notif_timeout = notif_timeout
		self._config = FileConfig(f'data/{self.__class__.__qualname__}_data.json')
		self._cookies = {} # for default values
		self._cookies.update(cookies)
		self._image_path = 'images'

		# create 'images' folder if not found.
		if not os.path.isdir(self._image_path):
			try:
				os.mkdir(self._image_path)
			except IOError:
				print('Oops, cannot create images folder, please try to create it manually.')

	def run():
		pass

	def stop(self):
		self._stop.set()

	def stopped(self):
		return self._stop.is_set()

	def show(self, msg='', echo=True, force=False):
		message = f'[{self.getName()}]: {msg}'

		if not self._debug and not force:
			return None

		if not echo:
			return message
		print(message)
