from threading import Thread

from rivescript import RiveScript

bot = RiveScript(utf8=True)
bot.load_directory("./norsebot/resources/rive_AI")
bot.sort_replies()


class Conversation(Thread):

    def __init__(self, chat):
        self.thread = Thread.__init__(self)
        self.daemon = True
        self.chat = chat

    def run(self, username, message):
        reply = bot.reply(username, message)
        if reply == "[ERR: No reply matched]":
            return "Your words make no sense to me!"
        return str(reply)
