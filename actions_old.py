
"""


TODO: Exit out of all demon programs when quit
TODO: Attack doesn't seem to work at the moment.

"""


import cmd as cmd

import world as world
import player as player
import enemies as enemies
import command_parser as command_parser



class DoActions(cmd.Cmd):
    def __init__(self, character):
        super().__init__()
        self.character = character

    prompt = '> '

    def default(self, line):
        print('I am sorry, I did not understand that.')

    def do_ask(self, line):
        """\
        Certain npcs have information that is valuable for you. The ASK verb allows you to interact with these npcs
        and obtain that information.

        Usage:
        ASK <npc> about <subject>\
        """
        kwargs = command_parser.parser(line)
        self.character.ask(**kwargs)

    def do_attack(self, line):
        """\
        ATTACK allows you to engage in combat with an enemy. Provided you are not in round time, ATTACK swings
        the weapon in your right hand (or your bare fist if there is no weapon) at the enemy. You will not be able
        to attack anyone other than enemies.

        Usage:
        ATTACK <enemy> : Engages an enemy and begins combat.\
        """
        kwargs = command_parser.parser(line)
        self.character.attack(**kwargs)

    def do_drop(self, line):
        """\
        DROP sets an object within your environment. This verb works the same as PUT <item>.

        Usage:
        DROP <item> : Places an item within an environment.
        DROP <item> in <object/item> : Will put an item within an object or within another item if that object or item
        is a container and if that object or item has enough room within it.
        DROP <item> on <object/item> : Will put an item on top of an object or on top of another item if that object
        or item is stackable.\
        """
        kwargs = command_parser.parser(line)
        self.character.put(**kwargs)

    def do_east(self, line):
        """\
        Moves you east, if you can move in that direction.\
        """
        if world.tile_exists(x=self.character.location_x + 1, y=self.character.location_y, area=self.character.area):
            self.character.move_east()
        else:
            print("You cannot find a way to move in that direction.")

    def do_flee(self, line):
        """\
        FLEE sends you in a random direction in your environment. FLEE can only be used when not in round time.\
        """
        kwargs = command_parser.parser(line)
        self.character.flee(**kwargs)

    def do_get(self, line):
        """\
        GET retrieves an item from your surroundings. Many objects cannot be moved from their current position.
        The item will be taken by your right hand, therefore you right hand will need to be empty. This
        verb functions the same as TAKE.

        Usage:
        GET <item>\
        """
        kwargs = command_parser.parser(line)
        self.character.get(**kwargs)

    def do_give(self, line):
        """\
        GIVE allows you to exchange items between you and various npcs. In order to give an item to an npc, you
        must have the item in your right hand.

        Usage:
        GIVE <item> to <npc> : Gives the item to the npc if the npc has the ability to accept the item.\
        """
        kwargs = command_parser.parser(line)
        self.character.give(**kwargs)

    def do_go(self, line):
        """\
        GO allows you to move toward a certain object. If the object can be passed through, you will pass through it.

        Usage:

        GO <object> : move toward or through an object.\
        """
        kwargs = command_parser.parser(line)
        self.character.go(**kwargs)

    def complete_go(self, text, line, begidx, endidx):
        possible_objects = []
        text = text.lower()

        if not text:
            return self.character.room.all_object_handles()

    def do_inventory(self, line):
        """\
        INVENTORY allows you to view your inventory. It will list all items you have in your possession.  INVENTORY
        will not list the items within any containers you have.\
        """
        kwargs = command_parser.parser(line)
        self.character.see_inventory(**kwargs)

    def do_look(self, line):
        """\
        View the environment and objects or items within your environment.

        Usage:
        LOOK : shows the descriptions of the environment around you.
        LOOK <object/item> : shows the description of the object at which you want to look.
        LOOK <npc> : shows the description of the npc at which you want to look.\
        """
        kwargs = command_parser.parser(line)
        self.character.look(**kwargs)

    def do_north(self, line):
        """\
        Moves you north, if you can move in that direction.\
        """
        if world.tile_exists(x=self.character.location_x, y=self.character.location_y - 1, area=self.character.area):
            self.character.move_north()
        else:
            print('You cannot find a way to move in that direction.')

    def do_put(self, line):
        """\
        PUT sets an object within your environment.  This usage works the same as DROP <item>.

        Usage:
        PUT <item> : Places an item within an environment.
        PUT <item> in <object/item> : Will put an item within an object or within another item if that object or item
        is a container and if that object or item has enough room within it.
        PUT <item> on <object/item> : Will put an item on top of an object or on top of another item if that object
        or item is stackable.\
        """
        kwargs = command_parser.parser(line)
        self.character.put(**kwargs)

    def do_quit(self, line):
        """\
        Exits the game.\
        """
        print("You have exited the game.")
        return True

    def do_save(self, line):
        """\
        \
        """
        kwargs = command_parser.parser(line)
        self.character.save()

    def do_search(self, line):
        """\
        SEARCH allows you to explore your environment if the object, enemy, or area can be explored.

        Usage:
        SEARCH : Searches the environment around you and uncovers hidden items or objects.
        SEARCH <enemy> : Searches an enemy, uncovers any potential items that the enemy could be hiding, and places
        them in your environment.\
        """
        kwargs = command_parser.parser(line)
        self.character.search(**kwargs)

    def do_sell(self, line):
        """\
        SELL allows you to exchange items for gulden. Certain merchants look for items you may find in the wilds.
        Different merchants look for different items. The item must be in your right hand.

        Usage:
        SELL <item> to <npc>  : Exchanges items for gulden with an npc if an item can be exchanged.
        """
        kwargs = command_parser.parser(line)
        self.character.search(**kwargs)

    def do_skills(self, line):
        """\
        SKILLS displays the skills available to you as well as the skill rating for your character. Different skills
        allow you to accomplish different tasks.

        Usage:
        SKILLS:  Shows your available skills and their rating.
        """
        kwargs = command_parser.parser(line)
        self.character.skills(**kwargs)

    def do_skin(self, line):
        """\
        Many enemies are able to be skinned for various pelts, hides, etc. The SKIN verb allows you to skin enemies.
        if successful the resulting item will be places within the environment. Not all enemies are able to be skinned.

        Usage:
        SKIN <enemy> : Skins an enemy and, if successful, leaves a skin.\
        """
        kwargs = command_parser.parser(line)
        self.character.skin(**kwargs)

    def do_south(self, line):
        """\
        Moves you south, if you can move in that direction.\
        """
        if world.tile_exists(x=self.character.location_x, y=self.character.location_y + 1, area=self.character.area):
            self.character.move_south()
        else:
            print("You cannot find a way to move in that direction.")

    def do_stats(self, line):
        """\
        Displays your general statistics.\
        """
        kwargs = command_parser.parser(line)
        self.character.stats(**kwargs)

    def do_take(self, line):
        """\
        TAKE retrieves an item from your surroundings. Many objects cannot be moved from their current position.
        The item will be taken by your right hand, therefore you right hand will need to be empty. This
        verb functions the same as GET.

        Usage:
        TAKE <item>\
        """
        kwargs = command_parser.parser(line)
        self.character.get(**kwargs)

    def do_target(self, line):
        """\
        When in combat, you must TARGET an enemy before you can ATTACK them. Use the TARGET verb to set the enemy
        for which you want to ATTACK. TARGET only needs to be set once for the duration of the combat. The enemy
        does not have to be within sight in order for you to TARGET it.

        Usage:
        TARGET <enemy> : Targets an enemy.\
        """
        kwargs = command_parser.parser(line)
        self.character.target_enemy(**kwargs)

    def do_west(self, line):
        """\
        Moves you west, if you can move in that direction.\
        """
        if world.tile_exists(x=self.character.location_x - 1, y=self.character.location_y, area=self.character.area):
            self.character.move_west()
        else:
            print("You cannot find a way to move in that direction.")

    do_n = do_north
    do_e = do_east
    do_s = do_south
    do_w = do_west

    do_l = do_look


class Action:
    def __init__(self, method, name, action, **kwargs):
        self.method = method
        self.name = name
        self.action = action
        self.kwargs = kwargs

    def __str__(self):
        return "{}: {}".format(self.action, self.name)


class EnemyAction(Action):
    def __init__(self, method, name, action, kwargs):
        super().__init__(method, name, action, **kwargs)


class MoveNorthEnemy(Action):
    def __init__(self, **kwargs):
        super().__init__(method=enemies.Enemy.move_north,
                         name='Move North',
                         action=['north'],
                         kwargs=kwargs)


class MoveSouthEnemy(Action):
    def __init__(self, **kwargs):
        super().__init__(method=enemies.Enemy.move_south,
                         name='Move South',
                         action=['south'],
                         kwargs=kwargs)


class MoveEastEnemy(Action):
    def __init__(self, **kwargs):
        super().__init__(method=enemies.Enemy.move_east,
                         name='Move East',
                         action=['east'],
                         kwargs=kwargs)


class MoveWestEnemy(Action):
    def __init__(self, **kwargs):
        super().__init__(method=enemies.Enemy.move_west,
                         name='Move West',
                         action=['west'],
                         kwargs=kwargs)


class PlayerAction(Action):
    def __init__(self, method, name, action, kwargs):
        super().__init__(method, name, action, **kwargs)


class MoveNorth(Action):
    def __init__(self, **kwargs):
        super().__init__(method=player.Player.move_north,
                         name='Move North',
                         action=['north'],
                         kwargs=kwargs)


class MoveSouth(Action):
    def __init__(self, **kwargs):
        super().__init__(method=player.Player.move_south,
                         name='Move South',
                         action=['south'],
                         kwargs=kwargs)


class MoveEast(Action):
    def __init__(self, **kwargs):
        super().__init__(method=player.Player.move_east,
                         name='Move East',
                         action=['east'],
                         kwargs=kwargs)


class MoveWest(Action):
    def __init__(self, **kwargs):
        super().__init__(method=player.Player.move_west,
                         name='Move West',
                         action=['west'],
                         kwargs=kwargs)

