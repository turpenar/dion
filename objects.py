

import random as random
import mixins as mixins
import items as items

all_items_categories = mixins.items


def link_terminal(terminal):
    global terminal_output
    terminal_output = terminal


class Object(mixins.ReprMixin, mixins.DataFileMixin):
    def __init__(self, object_data, **kwargs):

        self.object_data = object_data

        self.name = self.object_data['name']
        self.description = self.object_data['description']
        self.handle = self.object_data['handle']
        self.adjectives = self.object_data['adjectives']
        self.container = self.object_data['container']

    def contents(self):
        # Currently there are no objects that are containters.
        if self.container == False:
            return "{} cannot hold anything".format(self.name)

    def go_object(self, **kwargs):
        terminal_output.print_text("I'm not sure how you intend on doing that.")

    def view_description(self):
        return "{}".format(self.description)

    def skin(self, room):
        terminal_output.print_text("You cannot skin {}.".format(self.name))

    def search(self, character):
        NotImplementedError()


class Door(Object):
    def __init__(self, object_name, room, **kwargs):
        object_data = self.get_object_by_name(object_name)
        super().__init__(object_data=object_data, **kwargs)

        self.room = room

    def go_object(self, character):
        if character.room.room_name == self.object_data['location_1']['name']:
            return self.object_data['location_2']
        elif character.room.room_name == self.object_data['location_2']['name']:
            return self.object_data['location_1']

    def search(self, character):
        pass


class Corpse(Object):
    def __init__(self, object_name, room, **kwargs):
        object_data = self.get_object_by_name(object_name)
        super().__init__(object_data=object_data, **kwargs)

        self.room = room

        self.level = self.object_data['level']

        self.skin = self.object_data['skin']
        self.loot_drop_rate = self.object_data['loot']['drop_rate']
        self.loot_categories = self.object_data['loot']['items']
        self.loot_money = self.object_data['loot']['money']

    def skin_corpse(self):
        if self.skin == None:
            terminal_output.print_text("You cannot skin {}".format(self.name))
        else:
            terminal_output.print_text("You skin {} to yield {}.".format(self.name, all_items_categories['Skins'][self.skin]['name']))
            self.room.add_item(items.Skin(item_name=self.skin))
        return

    def search(self, character):
        possible_items = {}
        area = "Wilds"
        for category in self.loot_categories:
            for item in all_items_categories[category]:
                if all_items_categories[category][item]['level'] <= self.level and all_items_categories[category][item]['area'] == area:
                    possible_items[item] = all_items_categories[category][item]
        if len(possible_items) == 0:
            terminal_output.print_text("You did not find any items on {}.".format(self.name))
        else:
            found_item = random.choice(list(possible_items))
            found_item = getattr(__import__('items'), possible_items[found_item]['category'])(item_name=found_item)
            terminal_output.print_text("You found {}!".format(found_item.name))
            self.room.add_item(found_item)
        if self.loot_money == 0:
            terminal_output.print_text("You did not find any gulden on {}.".format(self.name))
        else:
            character.add_money(self.loot_money)
            terminal_output.print_text("You found {} gulden on {}!".format(self.loot_money, self.name))
        self.room.remove_object(self)
        self.room = None
        return

