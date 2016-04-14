import globals
from norsebot.resources.core.twitch import get_dict_for_users
from norsebot.resources.probes.moderators import get_moderator
from norsebot.resources.probes.pokemons import *


def tallgrass_release(generated_pokemon, channel):
    globals.CHANNEL_INFO[channel]['caught'] = False
    globals.CHANNEL_INFO[channel]['pokemon'] = generated_pokemon
    return "A wild " + generated_pokemon + " appeared!"


def user_is_moderator(username):
    if username in get_dict_for_users()[0]["chatters"]["moderators"]:
        return True
    else:
        return False


def tallgrass(args, **kwargs):
    username = kwargs.get("username", "testuser")
    channel = kwargs.get("channel", "testchannel")
    points_to_sacrifice = abs(int(args[0])) * -1
    points = get_user_points(username)
    moderator = get_moderator(username, channel)
    treats_removed = ""
    if not moderator:
        if type(points) != str:
            treats_removed = " " + str(points_to_sacrifice) + " treats from " + str(username) + "!"
        else:
            points = ""
    if isinstance(points, long):
        if abs(points_to_sacrifice) >= 1000:
            if points >= abs(points_to_sacrifice):
                generated_pokemon = spawn_tallgrass(0)
                if not moderator:
                    modify_user_points(username, points_to_sacrifice)
                return tallgrass_release(
                    generated_pokemon, channel) + treats_removed
            else:
                return "Sorry, but you need more treats to do that."
        elif abs(points_to_sacrifice) >= 100:
            if abs(points_to_sacrifice) <= 500:
                if points >= abs(points_to_sacrifice):
                    generated_pokemon = spawn_tallgrass(1)
                    if not moderator:
                        modify_user_points(username, points_to_sacrifice)
                    return tallgrass_release(
                        generated_pokemon, channel) + treats_removed
                else:
                    return "Sorry, but you need more treats to do that."
            else:
                return "You're in an open field. No tall grass between 501 and 999 Treats!"
        elif abs(points_to_sacrifice) < 100:
            if abs(points_to_sacrifice) >= 25:
                "abs(points_to_sacrifice) >= 25:", abs(points_to_sacrifice)
                if points >= abs(points_to_sacrifice):
                    generated_pokemon = spawn_tallgrass(2)
                    if not moderator:
                        modify_user_points(username, points_to_sacrifice)
                    return tallgrass_release(
                        generated_pokemon, channel) + treats_removed
                else:
                    return "Sorry, but you need more treats to do that."
            elif abs(points_to_sacrifice) > 4:
                "abs(points_to_sacrifice) > 4:", abs(points_to_sacrifice)
                if points >= abs(points_to_sacrifice):
                    generated_pokemon = spawn_tallgrass(3)
                    if not moderator:
                        modify_user_points(username, points_to_sacrifice)
                    return tallgrass_release(
                        generated_pokemon, channel) + treats_removed
                else:
                    return "Sorry, but you need more treats to do that."
            else:
                return "Dude, don't be cheap. Spare 5 treats."
    return "Sorry. That won't work. You need more treats! Stay tuned!"
