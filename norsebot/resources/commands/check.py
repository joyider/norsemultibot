from norsebot.resources.probes.pokemons import *


def check(args, **kwargs):
    inquirer = kwargs.get("username", "testuser")
    if args[0] == 'trades':
        all_tradable_pokemon = show_all_tradable_pokemon()
        all_tradable_pokemon_comprehension = [
            "{}".format(user) for user,
            giverpoke,
            pos,
            askingpoke,
            askinglevel in all_tradable_pokemon]
        return " | ".join(all_tradable_pokemon_comprehension)
        # ('singlerider', 'Vaporeon', 1, 'Psyduck', 14L)
    elif args[0] == 'market':
        return get_market_listings()
    elif args[0] == 'items':
        for_sale = check_items()
        for_sale_comprehension = ["({}) {}, {}".format(
            int(x), y, int(z)) for x, y, z in for_sale]
        return " | ".join(for_sale_comprehension)
    elif args[0] == 'inventory':
        inventory = check_inventory(inquirer)
        if len(inventory) > 0:
            inventory_comprehension = ["({}) {}, {}".format(
                int(x), y, int(z)) for x, y, z in inventory]
            return " | ".join(inventory_comprehension)
        else:
            return "You have no items"
    else:
        username = args[0].lower()
        user_tradable_pokemon = show_user_tradable_pokemon(username)
        if len(user_tradable_pokemon) > 0:
            user_tradable_pokemon_comprehension = [
                "({}) {}, {}, lvl {})".format(
                    int(pos),
                    str(giverpoke),
                    str(askingpoke),
                    int(askinglevel)) for user,
                giverpoke,
                pos,
                askingpoke,
                askinglevel in user_tradable_pokemon]
            return username + "'s listings ordered by position, listed Pokemon, asking Pokemon, asking level: " + \
                str(" | ".join(user_tradable_pokemon_comprehension))
        else:
            return "No trades available from the selected user."
