import re
from norsebot.resources.probes.points import get_user_time_points

banned_words = {
    "boobs": True,
}


def spam_detector(username, message):
    # Determine if user is a 'regular' viewer
    points = get_user_time_points(username)  # int - time_points
    message_to_check = message.split()
    urls = re.compile(ur'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))').findall(message)

    if urls:
	    return True
    # TODO: Detect CAPS inside of a string
    if message.upper() == message:
        if points <= 1500:
            if len(message) > 8:
                return True  # True means message is spam
    for word in message_to_check:
                if word in banned_words:
                    return True
