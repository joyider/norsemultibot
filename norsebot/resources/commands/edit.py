import norsebot.resources.parser_commands as command_headers
from norsebot.resources.probes.commands import edit_command


def edit(args, **kwargs):
    command = args[0].lower()
    user_level = args[1]
    response = " ".join(args[2:])
    creator = kwargs.get("username", "testuser")
    channel = kwargs.get("channel", "testchannel")
    if command[0] is "!":
        if command not in command_headers.commands:
            if user_level == "reg" or user_level == "mod":
                return edit_command(command, creator, user_level, response, channel)
            else:
                return "User level must be 'reg' or 'mod'"
        else:
            return "{} Is already implemnted in NorseBot.".format(command)
    else:
        return "Command must begin with '!'"
