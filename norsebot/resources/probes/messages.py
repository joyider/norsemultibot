#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime

from norsebot.resources.probes.connection import get_connection


def save_message(username, channel, message):
    con = get_connection()
    with con:
        cur = con.cursor()
        cur.execute(
            """INSERT INTO messages (
                username, channel, message, time
                ) VALUES (%s, %s, %s, %s)""", [
                username, channel.lstrip("#"),
                message, str(datetime.now())])
        cur.close()
