#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# norsebot (c) 2016 by Andre Karlsson<andre.karlsson@protractus.se>
#
# This file is part of norsebot.
#
#    norsebot is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    norsebot is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with norsebot.  If not, see <http://www.gnu.org/licenses/>.
#
# Filename:  by: andrek
# Timesamp: 4/29/16 :: 10:34 PM


import threading
import argparse
import Queue

import norsemultibot.resources.core.cron as cron
import norsemultibot.resources.core.streams.twitch as twitch
import norsemultibot.resources.parser_commands as command_list
import norsebot.resources.helper_command as commands
from norsebot.config.config import config
from norsebot.resources.core.protocol.irc import IRC
from norsebot.resources.probes.blacklists import check_for_blacklist
from norsebot.resources.probes.commands import *
from norsebot.resources.probes.messages import save_message
from norsebot.resources.probes.moderators import get_moderator
from norsebot.resources.probes.points import *
from norsebot.resources.helper_norse import *

def return_custom_command(protocol, stream, channel, message, username):
	if protocol == 'Irc':
		chan = channel.lstrip("#")
	elements = get_custom_command_elements(
		stream, chan, message[0])
	replacement_user = username
	if len(message) > 1:
		replacement_user = message[1]
	resp = elements[1].replace(
		"{}", replacement_user).replace("[]", str(elements[2] + 1))
	if elements[0] == "mod":
		moderator = get_moderator(username, chan, stream)
		if moderator:
			increment_command_counter(chan, message[0])
			#save_message(BOT_USER, channel, resp)
			print("!-> " + resp)
			return resp
	elif elements[0] == "reg":
		increment_command_counter(stream, chan, message[0])
		#save_message(BOT_USER, channel, resp)
		print("!-> " + resp)
		return resp

class Chat(threading.Thread):
	def __init__(self, queue, *args, **kwargs):
		#List of streams and protocols
		self._queue = queue
		for arg in args:
			#do some stuff
		for var, value in kwargs.items():
			#find key words
	def chat_message(self, messageFrame):
		#Irc : twitch : chat : #beyondthesummit : notsewxela : A Message man!!
		if messageFrame[0] == 'Irc':
			chan_short = messageFrame[3].lstrip('#')
			if messageFrame[5][0] == '!':
				command_split = messageFrame[5].split()
				my_command = get_custom_command(messageFrame[1], chan_short, command_split[0])
				if len(my_command) > 0:
					if command_split[0] == my_command[0][1]:
						resp = return_custom_command(messageFrame[0],messageFrame[1],
						                             chan_short, command_split, messageFrame[4])
						if resp:
							#Send message with response to channel (messageFrame[3])
			partial = messageFrame[5].split('')
			valid = False
			if commands.is_valid_command(messageFrame[5]):
				valid = True
			if commands.is_valid_command(partial):
				valid = True
			if not valid:
				return
			print "Handle the command: {0}".format(partial)
			#response = handle_command(partial, messageFrame)
			if response :
				#Send message with response to channel (messageFrame[3])
				print "Got response"
			return

	def handle_command(self, *args, **kwargs):
		# Todo:: Handle the command in a generic way to cap for multiple protcols


