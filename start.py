import os
import time

from dotenv import load_dotenv
from bots import YTSThread
from bots.utils.common import get_argv

# load env variables form .env
load_dotenv()

# amount of time in seconds
SLEEP_TIME = int(get_argv('--sleep')) if get_argv('--sleep') is not None else 60
# 1 hour
NOTIF_TIMEOUT = int(get_argv('--notif')) if get_argv('--notif') is not None else 1*60*60
DEBUG = True if get_argv('--debug') == 'true' else False

#url = 'https://yts.lt/browse-movies'
YTS_cookies = {
	'uid': os.environ.get('YTS_UID'),
	'uhh': os.environ.get('YTS_UHH')
}

threads_list = [
		YTSThread(SLEEP_TIME, NOTIF_TIMEOUT, DEBUG, cookies=YTS_cookies)
	]

try:
	# start the all threads
	for t in threads_list:
		t.start()

	# for cron job (no need for threads)
	time.sleep(2)
	for t in threads_list:
		t.stop()

	# make the all threads finish.
	# for t in threads_list:
	# 	t.join()
except KeyboardInterrupt:
	for t in threads_list:
		t.stop()
	print(f'\rStopping...')


#plyer.filechooser.choose_dir()
