#!/usr/bin/python
# -*- coding: utf-8 -*-
# norsebot (c) 2016 by Andre Karlsson<andre.karlsson@protractus.se>
#
# NorseBot is licensed under a
# Creative Commons Attribution-NonCommercial-NoDerivs 3.0 Unported License.
#
# You should have received a copy of the license along with this
# work.  If not, see <http://creativecommons.org/licenses/by-nc-nd/3.0/>
#
#
# Filename: urlest by: andrek
# Timesamp: 4/27/16 :: 10:23 PM
from abc import ABCMeta, abstractmethod

SUPPORTED_PROTOCOLS=['IRC', 'XMPP']

class Stream(metaclass=ABCMeta):
	def __init__(self):
		self.protocols = []
		self.createStream()
	@abstractmethod
	def createStream(self):
		pass
	@property
	def chatprotocols(self):
		return self.protocols
	def addProtocol(self, protocollist):
		for protocol in protocollist:
			if protocol.upper().title() in SUPPORTED_PROTOCOLS:
				self.protocols.append(protocol.upper().title())

class TwitchStream(Stream):
	def __init__(self, *args):
		super(TwitchStream, self).__init__()
		self.protocollist=args
