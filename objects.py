

import pathlib as pathlib
import json as json
import random as random
import sys as sys

import mixins as mixins
import items as items

all_items_categories = mixins.items


class Object(mixins.ReprMixin, mixins.DataFileMixin):
    def __init__(self, object_data, **kwargs):

        self.object_data = object_data

        self.name = self.object_data['name']
        self.description = self.object_data['description']
        self.handle = self.object_data['handle']
        self.adjectives = self.object_data['adjectives']

    def go_object(self, **kwargs):
        print("I'm not sure how you intend on doing that.")

    def view_description(self):
        return "{}".format(self.description)

    def skin(self, room):
        print("You cannot skin {}.".format(self.name))

    def search(self):
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

    def search(self):
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

    def skin_corpse(self):
        if self.skin == None:
            print("You cannot skin {}".format(self.name))
        else:
            print("You skin {} to yield {}.".format(self.name, all_items_categories['Skins'][self.skin]['name']))
            self.room.add_item(items.Skin(item_name=self.skin))
        return

    def search(self):
        possible_items = {}
        area = "Wilds"
        for category in self.loot_categories:
            for item in all_items_categories[category]:
                if all_items_categories[category][item]['level'] <= self.level and all_items_categories[category][item]['area'] == area:
                    possible_items[item] = all_items_categories[category][item]
        if len(possible_items) == 0:
            print("You did not find anything on {}.".format(self.name))
        else:
            found_item = random.choice(list(possible_items))
            found_item = getattr(__import__('items'), possible_items[found_item]['category'])(item_name=found_item)
            print("You found {}!".format(found_item.name))
            print(self)
            print(self.handle)
            self.room.add_item(found_item)
        self.room.remove_object(self)
        self.room = None
        return

