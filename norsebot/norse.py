import sys
from threading import Thread

import resources.helper_command as commands
import norsebot.resources.parser_commands as command_list
import norsebot.resources.core.cron as cron
import norsebot.resources.core.rive as rive
import norsebot.resources.core.twitch as twitch
from resources.helper_norse import *
from norsebot.config.config import config
from norsebot.resources.core.irc import IRC
from norsebot.resources.core.spam_detector import spam_detector
from norsebot.resources.probes.blacklists import check_for_blacklist
from norsebot.resources.probes.commands import *
from norsebot.resources.probes.messages import save_message
from norsebot.resources.probes.moderators import get_moderator
from norsebot.resources.probes.points import *

reload(sys)
sys.setdefaultencoding("utf8")

PRIMARY_CHANNEL = "joyider"
BOT_USER = config["username"]
SUPERUSER = "joyider"
TEST_USER = "azzaruz"
EXTRA_CHANNEL = "stronglegss"

NICKNAME = config["username"]
PASSWORD = config["oauth_password"]

ECHOERS = {}


class norse(object):    #Change cname to twitch

    def __init__(self):
        self.IRC = IRC(config)
        self.nickname = NICKNAME
        self.password = PASSWORD
        self.config = config
        self.crons = self.config.get("cron", {})
        cron.initialize(self.IRC, self.crons)
        command_list.initalizeCommands(config)
        self.run()

    def get_custom_command(self, channel, message, username):
        chan = channel.lstrip("#")
        elements = get_custom_command_elements(
            chan, message[0])
        replacement_user = username
        if len(message) > 1:
            replacement_user = message[1]
        resp = elements[1].replace(
            "{}", replacement_user).replace("[]", str(elements[2] + 1))
        if elements[0] == "mod":
            moderator = get_moderator(username, chan)
            if moderator:
                increment_command_counter(chan, message[0])
                save_message(BOT_USER, channel, resp)
                print("!-> " + resp)
                return resp
        elif elements[0] == "reg":
            increment_command_counter(chan, message[0])
            save_message(BOT_USER, channel, resp)
            print("!-> " + resp)
            return resp

    def ban_for_spam(self, channel, user, message):
		timeout = "/timeout {0} 1".format(user)
		self.IRC.send_message(channel, timeout)
		save_message(BOT_USER, channel, message)

      def join_part(self, action, channel):
        if action == "join":
            self.IRC.join_channels(
                self.IRC.channels_to_string([channel]), "chat")
            command_list.initalizeCommandsAfterRuntime(channel)
            self.IRC.send_message(channel, "Hi HeyGuys")
            print "JOINING", channel
        if action == "leave":
            self.IRC.send_message(channel, "Bye HeyGuys")
            self.IRC.leave_channels(
                self.IRC.channels_to_string([channel]), "chat")
            command_list.deinitializeCommandsAfterRuntime(channel)
            print "LEAVING", channel

    def handle_command(self, command, channel, username, message):
        if command == message:
            args = []
        elif command == message and command in commands.keys():  # pragma: no cover
            pass
        else:
            args = [message[len(command) + 1:]]
        if not commands.check_is_space_case(command) and args:
            args = args[0].split(" ")
        if (command == "!join" or command == "!leave") and channel == "#" + BOT_USER:
            self.join_part(command.lstrip("!"), "#" + username)
        if commands.is_on_cooldown(command, channel):
            pbot('Command is on cooldown. (%s) (%s) (%ss remaining)' % (
                command, username, commands.get_cooldown_remaining(
                    command, channel)), channel)
            self.IRC.send_whisper(
                username, "Sorry! " + command +
                " is on cooldown for " + str(
                    commands.get_cooldown_remaining(
                        command, channel)
                ) + " more seconds in " + channel.lstrip("#") +
                ". Can I help you?")
            return
        if commands.check_has_user_cooldown(command):
            if commands.is_on_user_cooldown(command, channel, username):
                self.IRC.send_whisper(
                    username, "Slow down! Try " + command +
                    " in " + channel.lstrip("#") + " in another " + str(
                        commands.get_user_cooldown_remaining(
                            command, channel, username)) + " seconds or just \
ask me directly?")
                return
            commands.update_user_last_used(command, channel, username)
        if check_for_blacklist(username):
            return
        pbot('Command is valid and not on cooldown. (%s) (%s)' %
             (command, username), channel)
        cmd_return = commands.get_return(command)
        if cmd_return != "command":
            resp = '(%s) : %s' % (username, cmd_return)
            commands.update_last_used(command, channel)
            self.IRC.send_message(channel, resp)
            return
        command_has_ul = commands.check_has_ul(username, command)
        if command_has_ul:
            user_data, __ = twitch.get_dict_for_users(channel)
            if command_has_ul == "superuser":
                if username == SUPERUSER:
                    return commands.pass_to_function(
                        command, args, username=username,
                        channel=channel.lstrip("#"))
                else:
                    return
            try:
                moderator = get_moderator(username, channel.lstrip("#"))
                if not moderator and username != SUPERUSER:
                    resp = '(%s) : %s' % (
                        username, "This is a moderator-only command!")
                    pbot(resp, channel)
                    self.IRC.send_whisper(username, resp)
                    return
            except Exception as error:  # pragma: no cover
                with open("errors.txt", "a") as f:
                    error_message = "{0} | {1} : {2}\n{3}\n{4}".format(
                        username, channel, command, user_data, error)
                    f.write(error_message)
        approved_channels = [
            PRIMARY_CHANNEL, BOT_USER, SUPERUSER, TEST_USER, EXTRA_CHANNEL]
        if channel.lstrip("#") not in approved_channels:
            prevented_list = ['songrequest', 'request', 'shots', 'donation',
                              'welcome', 'rules', 'gt',
                              'llama', 'loyalty', 'uptime', 'highlight',
                              'weather', 'treats', 'wins', 'subcount']
            if command.lstrip("!") in prevented_list:
                return
        result = commands.pass_to_function(
            command, args, username=username, channel=channel.lstrip("#"))
        commands.update_last_used(command, channel)
        if result:
            resp = '(%s) : %s' % (username, result)
            pbot(resp, channel)
            save_message(BOT_USER, channel, resp)  # pragma: no cover
            return resp[:350]

    def check_for_sub(self, channel, username, message):
        try:
            message_split = message.rstrip("!").split()
            subbed_user = message_split[0]
            if message_split[1] == "just" and len(message_split) < 4:
                modify_user_points(subbed_user, 100)
                resp = "/me {0} vouchers for {1} for a first \
time subscription!".format(100, subbed_user)
                self.IRC.send_message(channel, resp)
                save_message(BOT_USER, channel, resp)
            elif message_split[1] == "subscribed" and len(message_split) < 9:
                months_subbed = message_split[3]
                modify_user_points(subbed_user, int(months_subbed) * 100)
                resp = "/me {0} has just resubscribed for {1} \
months straight and is getting {2} vouchers for loyalty!".format(
                    subbed_user, months_subbed, int(months_subbed) * 100)
                self.IRC.send_message(channel, resp)
                save_message(BOT_USER, channel, resp)
        except Exception as error:  # pragma: no cover
            print error
