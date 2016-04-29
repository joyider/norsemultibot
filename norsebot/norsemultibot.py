import threading
import logging
import Queue
import os

from norsebot.resources.core.protocol.irc import Irc

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s', )

# If This is True then information about bots comes from database
USE_FRONTEND = False

# Move the following to config
if USE_FRONTEND == False:
	BOT_LIST = [{'bot_name': 'joyhappybot',
	             'password': 'oauth:npengw9ph20jkefte0t2fq7jbunpn6',
	             'channels': {'twitch': ['#beyondthesummit']}}]
else:
	pass

for i, val in enumerate(BOT_LIST):
	for stream in val['channels'].keys():
		print "For Stream provider is {0}: " \
		      "Channel are: {1} ".format(stream,
		                                 val['channels'][stream])

class NorseBot:
	def __init__(self):
		self.queue = Queue.Queue(0)
		self.main()

	def main(self):
		print"Staring main"
		print BOT_LIST[0]['channels']['twitch']
		p_chat = Irc('joyhappybot', 'oauth:npengw9ph20jkefte0t2fq7jbunpn6', 'twitch',
		             BOT_LIST[0]['channels']['twitch'], 'chat', self.queue)
		p_whisper = Irc('joyhappybot', 'oauth:npengw9ph20jkefte0t2fq7jbunpn6', 'twitch',
		             BOT_LIST[0]['channels']['twitch'], 'whisper', self.queue)
		p_chat.start()
		p_whisper.start()

		while True:
			if not self.queue.empty():
				item = self.queue.get()
				print item
		return
