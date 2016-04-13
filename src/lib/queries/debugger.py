import warnings

import globals
import MySQLdb as mdb

def get_connection():
	login = globals.mysql_credentials
	print(login[0])
	print(login[1])
	print(login[3])
	connection = mdb.connect(login[0], login[1], login[2], login[3])
	return connection

def my_query():
	con = get_connection()
	with con:
		with warnings.catch_warnings():
			cursor=con.cursor()
			cursor.execute("""
			SELECT username, points FROM `users`
			""")
			user = cursor.fetchall()
			print(user)
			cursor.close()

my_query()