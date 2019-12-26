
"""

TODO:  add containter limitationn
TODO:  add ability to look into containers
TODO:  Define dominant hand. Current default dominant hand is right hand
"""


import random as random
import time as time
import textwrap as textwrap
import threading as threading
import pathlib as pathlib
import pickle as pickle

import config as config
import world as world
import quests as quests
import combat as combat
import mixins

wrapper = textwrap.TextWrapper(width=config.TEXT_WRAPPER_WIDTH)

commands = {}

all_items = mixins.all_items
all_items_categories = mixins.items

lock = threading.Lock()


class Player(mixins.ReprMixin, mixins.DataFileMixin):
    def __init__(self, player_name: str, **kwargs):

        self.player_data = self.get_player_by_name(name=player_name)

        self.name = self.player_data['first_name']
        self.first_name = self.player_data['first_name']
        self.last_name = self.player_data['last_name']
        self.gender = self.player_data['gender']
        self.object_pronoun = None
        self.possessive_pronoun = None
        self.level = self.player_data['level']
        self.experience = self.player_data['experience']
        self.health = self.player_data['health']
        self.strength = self.player_data['strength']
        self.constitution = self.player_data['constitution']
        self.spirit = self.player_data['spirit']
        self.mana = self.player_data['mana']
        self.dexterity = self.player_data['dexterity']
        self.defense = self.player_data['defense']

        self.money = self.player_data['money']

        self.inventory = []

        for category in self.player_data['inventory']:
            for item_handle in self.player_data['inventory'][category]:
                for item in all_items_categories[category]:
                    if item_handle == item:
                        self.inventory.append(getattr(__import__('items'), category)(item_name=item_handle))

        self.right_hand_inv = False

        if len(self.player_data['right_hand']) != 0:
            self.right_hand_inv = getattr(__import__('items'), all_items[self.player_data['right_hand']]['category'])(item_name=self.player_data['right_hand'])

        self.left_hand_inv = False
        if len(self.player_data['left_hand']) != 0:
            self.left_hand_inv = getattr(__import__('items'), all_items[self.player_data['left_hand']]['category'])(item_name=self.player_data['left_hand'])

        self.location_x, self.location_y = world.starting_position
        self.room = world.tile_exists(x=self.location_x, y=self.location_y, area='Field')
        self.area = 'Field'

        self.target = None
        self.rt_start = 0
        self.rt_end = 0

        self.quests = {}

        for quest in self.player_data['quests']:
            self.quests[quest] = quests.Quest(quest_name=quest, character=self)
            self.quests[quest].start()

    def set_gender(self, gender):
        if gender == "female":
            self.gender = gender
            self.object_pronoun = "She"
            self.possessive_pronoun = "Her"
        if gender == "male":
            self.gender = gender
            self.object_pronoun = "He"
            self.possessive_pronoun = "His"

    def test(self, **kwargs):
        area_rooms = world.area_rooms(self.area)
        print(random.choice(list(area_rooms)))

    def add_money(self, amount):
        with lock:
            self.money += amount

    def subtract_money(self, amount):
        with lock:
            self.money -= amount

    def is_dead(self):
        if self.health > 0:
            return False
        else:
            print("You're dead! You will need to restart from your last saved point.")
            return True

    def status(self, **kwargs):
        print(
            "Name: {} \n"
            "Level:  {} \n"
            "Health:  {} \n"
            "Strength:  {} \n"
            "Constitution:  {} \n"
            "Spirit:  {} \n"
            "Mana:  {} \n"
            "Dexterity:  {} \n"
            "Quests: {} \n".format(self.name,
                                    self.level,
                                    self.health,
                                    self.strength,
                                    self.constitution,
                                    self.spirit,
                                    self.mana,
                                    self.dexterity,
                                   self.quests)
        )

    def set_round_time(self, seconds):
        with lock:
            self.rt_start = time.time()
            self.rt_end = self.rt_start + seconds
        return

    def check_round_time(self):
        with lock:
            round_time = False
            if time.time() < self.rt_end:
                print("Remaining round time: " + str(round(self.rt_end - time.time())) + " sec...")
                round_time = True
        return round_time

    def move(self, dx, dy):
        self.location_x += dx
        self.location_y += dy
        self.room = world.tile_exists(x=self.location_x, y=self.location_y, area=self.area)
        self.room.fill_room(character=self)
        print(self.room.intro_text())
        return

    def move_north(self, **kwargs):
        if self.check_round_time():
            return
        if self.is_dead():
            return
        self.move(dx=0, dy=-1)
        return

    def move_south(self, **kwargs):
        if self.check_round_time():
            return
        if self.is_dead():
            return
        self.move(dx=0, dy=1)
        return

    def move_east(self, **kwargs):
        if self.check_round_time():
            return
        if self.is_dead():
            return
        self.move(dx=1, dy=0)
        return

    def move_west(self, **kwargs):
        if self.check_round_time():
            return
        if self.is_dead():
            return
        self.move(dx=-1, dy=0)
        return

    def get_attack_modifier(self):
        with lock:
            return self.right_hand_inv.attack_modifier

    def go(self, **kwargs):
        if self.check_round_time():
            return
        if self.is_dead():
            return
        if not kwargs['direct_object']:
            print("Go where?")
            return
        else:
            object_found = False
            for room_object in self.room.objects:
                if set(room_object.handle) & set(kwargs['direct_object']):
                    new_location = room_object.go_object(character=self)
                    self.room = world.tile_exists(x=new_location['x'], y=new_location['y'], area=new_location['area'].replace(" ",""))
                    self.location_x = new_location['x']
                    self.location_y = new_location['y']
                    self.area = new_location['area']
                    self.room.fill_room(character=self)
                    print(self.room.intro_text())
                    self.room.run(character=self)
                    object_found = True
            if object_found == False:
                for room_item in self.room.items:
                    if set(room_item.handle) & set(kwargs['direct_object']):
                        print("You move toward {}.".format(room_item.name))
                        object_found = True
            if object_found == False:
                for room_npc in self.room.npcs:
                    if set(room_npc.handle) & set(kwargs['direct_object']):
                        print("You move toward {}.".format(room_npc.name))

    def look(self, **kwargs):
        if self.check_round_time():
            return
        if self.is_dead():
            return
        if not kwargs['indirect_object']:
            print(self.room.intro_text())
        elif kwargs['preposition'][0] == 'in':
            item_found = False
            for item in self.room.items + self.inventory:
                if item.container == True:
                    if set(item.handle) & set(kwargs['indirect_object']):
                        print(item.contents())
                        return
            if item_found == False:
                print("A {} is nowhere to be found".format(kwargs['indirect_object']))
                return
        elif kwargs['preposition'][0] == 'at':
            item_found = False
            for item in self.room.items + self.room.objects + self.room.npcs + self.inventory:
                if set(item.handle) & set(kwargs['indirect_object']):
                    print(item.view_description())
                    return
            for item in self.inventory:
                if set(item.handle) & set(kwargs['indirect_object']):
                    print(item.view_description)
                    return
            for object in self.room.objects:
                if set(object.handle) & set(kwargs['indirect_object']):
                    print(object.view_description())
                    return
            for npc in self.room.npcs:
                if set(npc.handle) & set(kwargs['indirect_object']):
                    npc.view_description()
                    return
            if item_found == False:
                print("At what did you want to look?")
                return
        else:
            print("I'm sorry, I didn't understand you.")
            return

    def see_inventory(self, **kwargs):
        with lock:
            if self.right_hand_inv:
                right_hand = "You have {} in your right hand.".format(self.right_hand_inv.name)
            else:
                right_hand = "Your right hand is empty."
            if self.left_hand_inv:
                left_hand = "You have {} in your left hand.".format(self.left_hand_inv.name)
            else:
                left_hand = "Your left hand is empty."
            inventory_clothing = [x.name for x in self.inventory if x.category == 'Clothing']
            if len(inventory_clothing) > 1:
                inventory_clothing = "You are wearing {} and {}.".format(', '.join(inventory_clothing[:-1]), inventory_clothing[-1])
            elif len(inventory_clothing) == 1:
                inventory_clothing = "You are wearing {}.".format(inventory_clothing[0])
            else:
                inventory_clothing = "You are wearing nothing."
            inventory_armor = [x.name for x in self.inventory if x.category == 'Armor']
            if len(inventory_armor) > 1:
                inventory_armor ="You are also wearing {} and {}.".format(self.object_pronoun, ', '.join(inventory_armor[:-1]), inventory_armor[-1])
            elif len(inventory_armor) == 1:
                inventory_armor = "You are also wearing {}.".format(self.object_pronoun, inventory_armor[0])
            else:
                inventory_armor = "You are also wearing no armor.".format(self.object_pronoun)
            wealth = "You have {} gulden.".format(self.money)
            print(right_hand)
            print(left_hand)
            print(wrapper.fill(inventory_clothing))
            print(wrapper.fill(inventory_armor))
            print(wrapper.fill(wealth))

    def check_inventory_for_item(self, item):
        with lock:
            for inv_item in self.inventory:
                if inv_item == item:
                    return True
                if inv_item.container == True:
                    for sub_inv_item in inv_item.items:
                        if sub_inv_item == item:
                            return True
            if self.right_hand_inv:
                if item == self.right_hand_inv:
                    return True
            if self.left_hand_inv:
                if item == self.left_hand_inv:
                    return True
            return False

    def all_inventory_handles(self):
        with lock:
            all_inventory_handles = []
            for item in self.inventory:
                all_inventory_handles.append(item.handle)
                if item.container == True:
                    for sub_item in item.items:
                        all_inventory_handles.append(sub_item.handle)
            return all_inventory_handles

    def get(self, **kwargs):
        if self.check_round_time():
            return
        if self.is_dead():
            return
        if not kwargs['direct_object']:
            print("I'm sorry, I could not understand what you wanted.")
            return
        for room_object in self.room.objects:
            if set(room_object.handle) & set(kwargs['direct_object']):
                print("Perhaps picking up {} is not a good idea.".format(room_object.name))
                return
        if not self.right_hand_inv:
            item_found = False
            for room_item in self.room.items:
                if set(room_item.handle) & set(kwargs['direct_object']):
                    self.right_hand_inv = room_item
                    self.room.items.remove(room_item)
                    print("You pick up {}.".format(room_item.name))
                    return
            if not item_found:
                for inv_item in self.inventory:
                    if inv_item.container:
                        for sub_item in inv_item.items:
                            if set(sub_item.handle) & set(kwargs['direct_object']):
                                self.right_hand_inv = sub_item
                                inv_item.items.remove(sub_item)
                                print("You take {} from {}.".format(sub_item.name, inv_item.name))
                                return
            if not item_found:
                print("A " + kwargs['direct_object'][0] + " is nowhere to be found")
        else:
            print('You already have something in your right hand')

    def put(self, **kwargs):
        if self.check_round_time():
            return
        if self.is_dead():
            return
        if not kwargs['direct_object']:
            print("What is it you're trying to put down?")
            return
        elif not self.right_hand_inv:
            print("You do not have that item in your hand.")
            return
        elif not set(self.right_hand_inv.handle) & set(kwargs['direct_object']):
            print("You do not have that item in your right hand.")
            return
        elif kwargs['preposition'][0] == "in":
            for inv_item in self.inventory:
                if set(inv_item.handle) & set(kwargs['indirect_object']):
                    if inv_item.container == False:
                        print("{} won't fit in there.".format(self.right_hand_inv.name))
                        return
                    if len(inv_item.items) == inv_item.capacity:
                        print("{} can't hold any more items".format(inv_item.name))
                        return
                    inv_item.items.append(self.right_hand_inv)
                    print("You put {} {} {}".format(self.right_hand_inv.name, kwargs['preposition'][0], inv_item.name))
                    self.right_hand_inv = False
                    return
            for room_item in self.room.items:
                if set(room_item.handle) & set(kwargs['indirect_object']):
                    if room_item.container == False:
                        print("{} won't fit {} there.".format(self.right_hand_inv.name, kwargs['preposition'][0]))
                        return
                    room_item.items.append(self.right_hand_inv)
                    print("You put {} {} {}".format(self.right_hand_inv.name, kwargs['preposition'][0], room_item.name))
                    self.right_hand_inv = False
                    return
        elif kwargs['preposition'][0] == "on":
            print("You cannot stack items yet.")
            return
        else:
            print("That item is not around here, unfortunately.")
            return

    def give(self, **kwargs):
        if self.check_round_time():
            return
        if self.is_dead():
            return
        elif not kwargs['direct_object']:
            print("What are you trying to give?")
            return
        elif not self.right_hand_inv:
            print("You don't seem to be holding that item in your hand.")
            return
        elif not set(self.right_hand_inv.handle) & set(kwargs['direct_object']):
            print("You don't seem to be holding that item in your hand.")
            return
        elif not kwargs['indirect_object']:
            print("To whom do you want to give?")
            return
        else:
            for npc in self.room.npcs:
                if {npc.first_name.lower()} & set(kwargs['indirect_object']):
                    if npc.give_item(self.right_hand_inv):
                        self.right_hand_inv = False
                        return
                    else:
                        return
            print("That didn't seem to work.")
            return

    def drop_item(self, **kwargs):
        if self.check_round_time():
            return
        if self.is_dead():
            return
        elif not kwargs['direct_object']:
            print("I'm sorry, I could not understand what you wanted.")
            return
        elif not self.right_hand_inv:
            print("You do not have that item in your hand")
            return
        elif not set(self.right_hand_inv.handle) & set(kwargs['direct_object']):
            print("You do not have that item in your right hand.")
            return
        else:
            self.room.items.append(self.right_hand_inv)
            print("You drop " + self.right_hand_inv.name)
            self.right_hand_inv = False
            return

    def target_enemy(self, **kwargs):
        if not kwargs['direct_object']:
            print("What do you want to target?")
            return
        else:
            self.target = kwargs['direct_object']
            print("You are now targeting {}".format(self.target[0]))
            return

    def attack(self, **kwargs):
        if self.check_round_time():
            return
        if self.is_dead():
            return
        elif kwargs['direct_object']:
            self.target = kwargs['direct_object']
            return
        elif not self.target:
            print("Who are you going to attack? You do not have a target.")
            return
        else:
            for npc in self.room.npcs:
                if set(npc.handle) & set(self.target):
                    print("{} will probably not appreciate that.".format(npc.name))
                    return
            enemy_found = False
            for enemy in self.room.enemies:
                if set(enemy.handle) & set(self.target):
                    enemy_found= True
                    combat.do_physical_damage_to_enemy(self, enemy)
                    self.set_round_time(3)
                    return
            if not enemy_found:
                print("{} is not around here.".format(kwargs['direct_object']))
                return

    def skin(self, **kwargs):
        if self.check_round_time():
            return
        if self.is_dead():
            return
        elif not kwargs['direct_object']:
            print("What are you trying to skin?")
            return
        else:
            for object in self.room.objects:
                if set(object.handle) & set(kwargs['direct_object']):
                    object.skin_corpse()
                    return
            for item in self.room.items:
                if set(item.handle) & set(kwargs['direct_object']):
                    print("You can seem to find any way to skin {}.".format(item.name))
                    return
            for npc in self.room.npcs:
                if set(npc.handle) & set(kwargs['direct_object']):
                    print("You approach {}, but think better of it.".format(npc.name))
                    return

    def search(self, **kwargs):
        if self.check_round_time():
            return
        if self.is_dead():
            return
        if not kwargs['direct_object']:
            items_found = 0
            for hidden_item in self.room.hidden:
                if 100 - self.level >= hidden_item.visibility:
                    self.room.add_item(hidden_item)
                    self.room.remove_hidden_item(hidden_item)
                    print('You found {}!'.format(hidden_item.name))
                    items_found += 1
            if items_found == 0:
                print("There doesn't seem to be anything around here.")
            return
        else:
            for object in self.room.objects:
                if set(object.handle) & set(kwargs['direct_object']):
                    object.search(character=self)
                    return
            for item in self.room.items:
                if set(item.handle) & set(kwargs['direct_object']):
                    print("Searching {} will not do you much good.".format(item.name))
                    return
            for char in self.room.enemies + self.room.npcs:
                if set(char.handle) & set(kwargs['direct_object']):
                    print("{} probably will not appreciate that.".format(char.name))
                    return
            else:
                print("That doesn't seem to be around here.")
                return

    def sell(self, **kwargs):
        """Determines if an item can be sold as well as calls the npc's sell function"""
        if self.check_round_time():
            return
        if self.is_dead():
            return
        elif not kwargs['direct_object']:
            print("What is it you are trying to sell?")
            return
        for npc in self.room.npcs:
            if set(npc.handle) & {kwargs['indirect_object']}:
                npc.sell_item(item=self.right_hand_inv)
                return
        else:
            print("Who are you trying to sell to?")

    def flee(self, **kwargs):
        """Moves the player randomly to an adjacent tile"""
        if self.check_round_time():
            return
        if self.is_dead():
            return
        available_moves = self.room.adjacent_moves()
        r = random.randint(0, len(available_moves) - 1)
        self.do_action(available_moves[r])
        return

    def ask(self, **kwargs):
        if self.check_round_time():
            return
        if self.is_dead():
            return
        elif not kwargs['direct_object']:
            print("Who are you trying to ask?")
            return
        elif not kwargs['indirect_object']:
            print("What are you trying to ask about?")
            return
        else:
            for npc in self.room.npcs:
                if set(npc.handle) & set(kwargs['direct_object']):
                    npc.ask_about(object=kwargs['indirect_object'])
                    return
            else:
                print("That doesn't seem to do any good.")

    def check_quest(self, quest):
        with lock:
            for quest_self in self.quests:
                if self.quests[quest_self].name == quest.name:
                    return True
            return False

    def add_quest(self, quest_name, quest):
        with lock:
            self.quests[quest_name] = quest

    def __getstate__(self):
        """Copy the object's state from self.__dict__ which contains all our instance attributes. Always use the
        dict.copy() method to avoid modifying the original state."""
        state = self.__dict__.copy()
        del state['room']
        quests_data = {}
        for quest in self.quests:
            quests_data[quest] = self.quests[quest].save()
        state['quests'] = quests_data
        return state

    def __setstate__(self, state):
        """Set the object's state in self.__dict__ which contains all our instance attributes."""
        for quest in state['quests']:
            self.quests[quest] = quests.Quest(quest_name=quest, character=self)
            self.quests[quest].load(state=state['quests'][quest])
            self.quests[quest].start()
        del state['quests']
        self.__dict__.update(state)

    def save(self):
        save_data = self.__getstate__()
        character_name = "{}_{}.p".format(self.first_name, self.last_name)
        path_save = pathlib.Path.cwd() / 'Profiles' / character_name
        pickle.dump(save_data, open(file=path_save.absolute().as_posix(), mode='wb'))
        print("Progress saved.")

    def load(self, state):
        self.__setstate__(state)







