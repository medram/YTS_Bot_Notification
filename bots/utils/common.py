import os
import sys
import json
import requests

from json.decoder import JSONDecodeError

def get_argv(key):
	#return argv[argv.index(f'--{key}')+1]
	result = None
	try:
		result = sys.argv[sys.argv.index(key)+1]
	except ValueError:
		pass

	return result


class FileConfig:

	def __init__(self, filename):
		self.filename = filename
		self._loaded = False
		self._data = None

	def get(self, key=None):
		self._load()
		if key:
			return self._data.get(key, None)
		return self._data

	def _load(self):
		mode = 'r' if os.path.exists(self.filename) else 'w+'
		if not self._loaded:
			with open(self.filename, mode, encoding='utf-8') as file:
				try:
					filedata = file.read()

					if len(filedata):
						self._data = json.loads(filedata)
					else:
						self._data = {}
				except JSONDecodeError as e:
					print(f'{self.filename} Failed to load the json file.')
					#print(e)


	def save(self, data=None):
		try:
			with open(self.filename, 'w', encoding='utf-8') as f:
				json.dump(data, f, indent=2)
				#print('Saved Successfully.')
			return True
		except KeyError as e:
			print(f'{self.filename}', e)
		return False


def download(file_url, rename_to=None, chunk_size=10):
	ext = os.path.splitext(file_url)[1]
	rename_to = (rename_to + ext) if rename_to else os.path.dirname(file_url)
	done = False
	with requests.get(file_url, timeout=(5, 30)) as res:
		with open(os.path.join('images', rename_to), 'wb') as f:
			for chunk in res.iter_content(chunk_size=chunk_size):
				f.write(chunk)
				
	return os.path.join('images', rename_to)

