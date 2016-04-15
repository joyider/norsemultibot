global config

import globals
import norsebot.resources.commands.pokemon as pokemon
import norsebot.resources.commands.treats as treats
import norsebot.resources.core.twitch as twitch

channels_to_join = ['#joyider']

for channel in channels_to_join:
	channel = channel.lstrip('#')
	globals.CHANNEL_INFO[channel] = {'caught': True, 'pokemon': ''}

config = {
  # details required to login to twitch IRC server
	'username': 'joyhappybot',
	# get this from http://twitchapps.com/tmi/
	'oauth_password': 'oauth:npengw9ph20jkefte0t2fq7jbunpn6',

	'debug': True,
	'log_messages': True,


	'channels': channels_to_join,

	# Cron jobs.
	'cron': {
		'#joyider': [
			# time, run, callback
			(86400, True, pokemon.market_cron),  # reset market every 24 hours
			(24200, True, pokemon.cron),  # pokemon released every 20 minutes
			(600, True, treats.cron),  # treat handed out every 10 minutes
			(300, True, twitch.user_cron),  # update user list every 3 minutes
		],
	},
}
