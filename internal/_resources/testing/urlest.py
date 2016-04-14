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
# Timesamp: 2016-04-14 :: 15:54

import re, urllib

GRUBER_URLINTEXT_PAT = re.compile(ur'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))')

for line in urllib.urlopen("http://daringfireball.net/misc/2010/07/url-matching-regex-test-data.text"):
    print [ mgroups[0] for mgroups in GRUBER_URLINTEXT_PAT.findall(line) ]