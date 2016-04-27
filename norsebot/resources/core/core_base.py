#!/usr/bin/python
# -*- coding: utf-8 -*-
# norsebot (c) 2016 by Andre Karlsson<andre.karlsson@protractus.se>
#
# NorseBot is licensed under a
# Creative Commons Attribution-NonCommercial-NoDerivs 5.0 Unported License.
#
# You should have received a copy of the license along with this
# work.  If not, see <http://creativecommons.org/licenses/by-nc-nd/3.0/>
#
#
# Filename: urlest by: andrek
# Timesamp: 4/25/16 :: 7:46 PM

from abc import abstractmethod, abstractproperty, ABCMeta
from norsebot.resources.helper_norse import compability_str
import os
import sys
import logging
from collections import deque, defaultdict

log = logging.getLogger(__name__)

class CoreBase(metaclass = ABCMeta):
	"""
	This class is only to as to what to expect from the CoreBase. Always use the properties of used class.
	Don't ever use this outside of the CoreEngine
	"""
	pass

class Message(object):
	def __init__(self, msg='', kind='chat', from_user='', to_user=''):
		self._msg = compability_str(msg)
		self._kind = kind
		self._from_user = from_user
		self._to_user = to_user

	def clone(self):
		return Message(self._msg, self._kind, self._from_user, self._to_user)

	@property
	def to(self):
		return self._to_user

	@to.setter
	def to(self, to):
		self._to_user = to

	@property
	def from_user(self):
		return self._from_user

	@from_user.setter
	def from_user(self, from_user):
		self._from_user = from_user

	@property
	def kind(self):
		return self._kind

	@kind.setter
	def kind(self, kind):
		self._kind = kind

	@property
	def msg(self):
		return self._msg

	@msg.setter
	def msg(self, message):
		self._msg = message

#States of chatbot
ONLINE = 'online'
OFFLINE = 'offline'

class Attendance(object):
	"""
	purpose of this class is to manifest the attendance of an single user or user in chat
	"""

	def __init__(self, nick=None, identifier=None, status=None, streamroom=None, message=None):
		if nick is None and identifier is None:
			raise ValueError('Both Nick and Identifier is None, --Attendance')
		if nick is None and streamroom is None:
			raise ValueError('Both nick and streamroom is None, --Attendance')
		if status is None and message is None:
			raise ValueError('As a minimu you need a message or a status present, --Attendance')
		self._nick = nick
		self._identifier = identifier
		self._status = status
		self._streamroom = streamroom
		self._message = message

	@property
	def streamroom(self):
		return self._streamroom

	@property
	def nick(self):
		return self._nick

	@property
	def identifier(self):
		return self._identifier

	@property
	def status(self):
		return self._status

	@property
	def message(self):
		return self._message

	def __str__(self):
		response = ''
		if self._nick:
			response += 'Nick:{0} '.format(self._nick)
		if self._streamroom:
			response += 'Room:{0} '.format(self._streamroom)
		if self._identifier:
			response += 'Identifier:{0} '.format(self._identifier)
		if self._status:
			response += 'Status:{0} '.format(self._status)
		if self._message:
			response += 'Message:{0} '.format(self._message)

	def __unicode__(self):
		return str(self.__str__())

class chatroom_MU(CoreBase):
	"""
	Manifistation/Interface of a chat room full of people (Multi User)
	"""

	@abstractmethod
	def join(self, username=None, password=None):
		pass

	@abstractmethod
	def leave(self, cause=None):
		pass

	@abstractmethod
	def create(self):
		pass

	@abstractmethod
	def shutdown(self):
		pass

	@abstractproperty
	def alreay_created(self):
		"""
		Boolean to indicate whether th chat already are created or not

		:getter
		:return: True if created already else False
		"""
		pass

	@abstractproperty
	def joined(self):
		"""
		Boolean to see if room is already joined

		:getter
		:return: True if already joined else False
		"""
		pass

	@property
	def topic(self):
		"""
		Topic of the chat room

		:getter
		TODO:: No idea if this will works as i hope :)

		:return: Topic as string or None
		"""
		raise NotImplementedError("This needs to be excplicitly created to the coreengine")

	@topic.setter
	@abstractmethod
	def topic(self, topic):
		"""
		See topic getter
		TODO:: No idea if this will works as i hope :)
		:param topic: Chat topic
		:setter:
		:return:
		"""
		pass

	@abstractproperty
	def members(self):
		"""
		Rooms current members

		:getter

		:return: A list with member identities
		"""
		pass

	@abstractmethod
	def invite(self, *args):
		"""

		:param args: One or more members/identifiers to invite to the chat
		:return:
		"""
		pass

class CoreEngine(CoreBase):
	"""
	Base for Bot logic i guess (norse.py)
	"""

	command_history = defaultdict(lambda: deque(maxlen=10))  #To use for per user cmd history (i hope)

	FUZZY_ERROR ="Sorry but I am confsed atm, Unexcpeted error"

	def __init__(self, _):
		log.debug("Initializing CoreEngine for NorseBot")

		#Reconnection variables
		self._reconnect_count = 0
		self._reconnect_delay = 1
		#More of these i guess from irc.py

	def send_message(self, message):
		"""
		Do your own....
		:param message:
		:return:
		"""
	@abstractmethod
	def make_reply(self, message, text=None, private=False):
		"""
		MUST be implemented in the CoreEngine
		:param message:
		:param text:
		:param private:
		:return:
		"""
		raise NotImplementedError("the make_reply must be created by the coreengine %s") % self.__class__

	def attendance_callback(self, attendance):
		"""
		To be implemented in norse.py
		:param attendance:
		:return:
		"""
		pass

	def chatjoined_callback(self, chat):
		"""
		To be implemented in norse.py
		:param chat:
		:return:
		"""
		pass

	def chatleft_callback(self):
		"""
		To be implemented in norse.py
		:return:
		"""
		pass

	def chattopic_callback(self, chat):
		"""
		To be implemented in norse.py
		:param chat:
		:return:
		"""
		pass

	def core_loop(self):
		"""
		This is the connection of the CoreEngine to the server/stream....
		BROKEN AS FOR NOW
		:return:
		"""
		while True:
			try:
				pass
				#if CONNECTION BASED ON PROTOCOL
			except KeyboardInterrupt:
				#LOG
				break
			except:
				log.exception("Can not start ...(core_loop)")

	def reset_connection_count(self):
		self._reconnect_count = 0
		self._reconnect_delay = 1

	@abstractmethod
	def connect(self):
		pass

	def join_chat(self, chat, username=None, password= None):
		"""
		Join a chat (chatroom_MU)
		:param chat: name/identifier of chat
		:param username: optional username
		:param password: optional password
		:return:
		"""
		self.query_chat(chat).join(username=username, password=password)

	@abstractmethod
	def query_chat(self, chat):
		"""
		I want this to get info from a chat room
		:param chat:
		:return:instance of chatroom_MU
		"""
		pass

	@abstractmethod
	def make_identifier(self, id_string):
		pass

	@abstractmethod
	def prefix_handler(self, message, identifier):
		pass

