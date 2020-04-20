
"""


TODO:  Introduce stackable items
"""

import mixins as mixins


def link_terminal(terminal):
    global terminal_output
    terminal_output = terminal


def loot():
    pass


class Item(mixins.ReprMixin, mixins.DataFileMixin):
    def __init__(self, item_data, **kwargs):

        item_data = item_data

        self.name = item_data['name']
        self.description = item_data['description']
        self.value = item_data['value']
        self.handle = item_data['handle']
        self.adjectives = item_data['adjectives']
        self.container = item_data['container']
        self.wearable = item_data['wearable']
        self.stackable = item_data['stackable']
        self.capacity = item_data['capacity']
        self.visibility = item_data['visibility']
        self.category = item_data['category']
        self.level = item_data['level']
        self.loot = item_data['loot']
        self.area = item_data['area']
        self.items = []

    def contents(self):
        if self.container == False:
            return "A {} cannot hold anything".format(self.handle[0])
        all_items = []
        if len(self.items) == 0:
            return "{} are empty".format(self.name)
        for item in self.items:
            all_items.append(item.name)
        if len(all_items) > 1:
            all_items_output = ', '.join(all_items[:-1])
            all_items_output = all_items_output + ', and ' + all_items[-1]
        else:
            all_items_output = all_items[0]
        return "Inside {} you see {}".format(self.name, all_items_output)

    def view_description(self):
        return self.description

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class Clothing(Item):
    def __init__(self, item_name: str, **kwargs):
        category_data = self.get_item_by_name('Clothing')
        item_data = category_data[item_name]
        super().__init__(item_data=item_data, **kwargs)


class Weapon(Item):
    def __init__(self, item_name: str, **kwargs):
        category_data = self.get_item_by_name('Weapons')
        item_data = category_data[item_name]
        super().__init__(item_data=item_data, **kwargs)

        self.material = item_data['material']
        self.attack_modifier = item_data['attack_modifier']


class Money(Item):
    def __init__(self, item_name: str, **kwargs):
        category_data = self.get_item_by_name('Money')
        item_data = category_data[item_name]
        super().__init__(item_data=item_data, **kwargs)


class Armor(Item):
    def __init__(self, item_name: str, **kwargs):
        category_data = self.get_item_by_name('Armor')
        item_data = category_data[item_name]
        super().__init__(item_data=item_data, **kwargs)

        self.material = item_data['material']


class Ring(Item):
    def __init__(self, item_name: str, **kwargs):
        category_data = self.get_item_by_name('Rings')
        item_data = category_data[item_name]
        super().__init__(item_data=item_data, **kwargs)


class Neck(Item):
    def __init__(self, item_name: str, **kwargs):
        category_data = self.get_item_by_name('Neck')
        item_data = category_data[item_name]
        super().__init__(item_data=item_data, **kwargs)


class Skin(Item):
    def __init__(self, item_name: str, **kwargs):
        category_data = self.get_item_by_name('Skins')
        item_data = category_data[item_name]
        super().__init__(item_data=item_data, **kwargs)


class Miscellaneous(Item):
    def __init__(self, item_name: str, **kwargs):
        category_data = self.get_item_by_name('Miscellaneous')
        item_data = category_data[item_name]
        super().__init__(item_data=item_data, **kwargs)




