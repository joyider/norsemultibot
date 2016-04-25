import time

red = "\033[01;31m{0}\033[00m"
grn = "\033[01;36m{0}\033[00m"
blu = "\033[01;34m{0}\033[00m"
cya = "\033[01;36m{0}\033[00m"


def pp(message, mtype='INFO'):
	mtype = mtype.upper()

	if mtype == "ERROR":
		mtype = red.format(mtype)

	print '[%s] [%s] %s' % (time.strftime('%H:%M:%S', time.gmtime()), mtype, message)


def pbot(message, channel=''):
	if channel:
		msg = '[%s %s] [%s] %s' % (
			time.strftime('%H:%M:%S', time.gmtime()), channel, 'BOT', message)
	print msg


def compability_str(s):
	""" Detect if s is a string and convert it to unicode if it is a byte or
		py2 string
		:param s: the string to ensure compatibility from."""
	if isinstance(s, str):
		return s
	elif isinstance(s, bytes):
		return s.decode('utf-8')
	else:
		return str(s)
