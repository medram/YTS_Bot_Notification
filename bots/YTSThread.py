import sys
import os
import glob
import requests
import plyer

from requests.exceptions import HTTPError, ConnectTimeout, ConnectionError, RequestException
from bs4 import BeautifulSoup
from PIL import Image

from bots.utils.common import download
from bots.botThread import BotThread


class YTSThread(BotThread):

	def __init__(self, sleep=5, notif_timeout=60, debug=False, cookies={}, url=None):
		super().__init__(sleep, notif_timeout, debug, cookies)
		if url:
			self._url = url
		else:
			self._url = 'https://yts.lt/browse-movies/0/all/animation/0/latest'


	def run(self):
		self.show('is running...', force=True)
		while not self.stopped():
			posts = self._getLastMovies()
			if posts:
				self.show('New movies have been posted.')
				self._notifyMe(posts)
			else:
				self.show('Nothing new.')

			#raise KeyboardInterrupt('Stop this thread')
			#time.sleep(self._sleep)
			self._stop.wait(self._sleep)
		self.show('was stopped.', force=True)

	def _getLastMovies(self):
		
		posts = []
		try:
			#jar = requests.cookies.RequestsCookieJar()
			res = requests.get(self._url, timeout=(5, 30), cookies=self._cookies)
			soup = BeautifulSoup(res.text, 'lxml')

			boxes = soup.findAll('div', class_='browse-movie-wrap')
			
			for box in boxes:
				title = box.find('a', class_='browse-movie-title').text.strip()
				released = box.find('div', class_='browse-movie-year').text.strip()
				cover = box.find('img').attrs.get('src').strip()
				link = box.find('a', class_='browse-movie-title').attrs.get('href').strip()
				try:
					availableIn = [child.text.strip() for child in box.find('div', class_='browse-movie-tags').children if child.name == 'a']
				except AttributeError:
					availableIn = '--'

				post = {}
				# fill in the post.
				post['title'] = title
				post['link'] = link
				post['released'] = released
				post['cover'] = cover
				post['availableIn'] = availableIn
				post['downloaded_cover'] = ''

				posts.append(post)

			# filter the newest movies.
			for i, post in enumerate(posts):
				if not self._checkSaveNewMovie(post):
					del posts[i:]
					break

			if posts:
				# clean up old covers
				for file in glob.glob(f'images/{self.getName()}_*'):
					try:
						os.remove(file)
					except IsADirectoryError:
						pass

				if len(posts) > 15:
					posts = posts[0:4]

				# download new covers
				for post in posts:
					# download new movie cover
					post['downloaded_cover'] = download(post['cover'], rename_to=f"{self.getName()}_{post['title']}")

				# save the lastest post.
				self._checkSaveNewMovie(posts[0], save=True)

			return posts

		except ConnectionError:
			self.show('Connection failed: Please check your internet connection.')
		except ConnectTimeout:
			self.show('Connection timeout.')
		except HTTPError:
			self.show('Connection timeout.')
		except RequestException as e:
			self.show(e)

		return False

	def _checkSaveNewMovie(self, post:list, save=False):
		post_from_json = self._config.get('last_post')

		if post_from_json is None or post_from_json['link'] != post['link']:
			if save:
				data = self._config.get()
				# download new movie cover
				#post['downloaded_cover'] = download(post['cover'], rename_to=f"{self.getName()}_{post['title']}")
				data['last_post'] = post
				self._config.save(data)
			return True
		return False

	def _notifyMe(self, posts:dict):		
		for post in posts:
			cover = os.path.abspath(post['downloaded_cover'])
			
			if sys.platform == 'win32':
				cover = self._convertToICO(cover)

			try:
				plyer.notification.notify(
						title=f"[YTS] {post.get('title')}.",
						message=f"Released in: {post.get('released')}\nAvailable in: {', '.join(post.get('availableIn'))}",
						timeout=self._notif_timeout,
						app_name=self.getName(),
						app_icon=cover
						#ticker=True
					)
			except NotImplementedError as e:
				self.show(e, force=True)

	def _convertToICO(self, path):
		try:
			image = Image.open(path)
			#image.resize((image.width // 2, image.height // 2))
			#im = imageio.imread(path)

			new_path = os.path.splitext(path)[0] + '.ico'
			image.save(new_path, sizes=[(128, 128)])
			#imageio.imwrite(new_path, im)
			return new_path
		except (IOError, ValueError) as e:
			self.show(e)
		return path