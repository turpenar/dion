
import random as random
import threading as threading

import items as items

lock = threading.Lock()


def success(strength, attack_modifier, defense, att_random):
    return int((strength + attack_modifier - defense + att_random - 100))

def damage(success, constitution):
    return int(success / constitution)

def get_experience(character_level, target_level):
    if character_level > target_level + 5:
        return 0



def do_physical_damage_to_enemy(self, target):
    if isinstance(self.right_hand_inv, items.Weapon):
        attack_modifier = self.right_hand_inv.attack_modifier
    else:
        attack_modifier = 0

    with lock:
        att_random = random.randint(0,100)
        att_success = success(self.strength, attack_modifier, target.defense, att_random)
        att_damage = damage(att_success, self.constitution)

        print("""\
{} attacks {}!
STR {} + ATTMOD {} - DEF {} + RAND {} = {}\
        """.format(self.name, target.name, self.strength, attack_modifier, target.defense, att_random, success))

        if att_damage < 0:
            print("""\
{} evades the attack.\
                """.format(target.name))
        else:
            target.health = target.health - damage
            print("""\
{} damages {} by {}.\
                """.format(self.name, target.name, damage))
            if target.health <= 0:
                target.is_dead()
                self.experience += get_experience(character_level=self.level, target_level=target.level)
        return target

def do_physical_damage_to_character(self, character):
    if isinstance(self.right_hand_inv, items.Weapon):
        attack_modifier = self.right_hand_inv.attack_modifier
    else:
        attack_modifier = 0

    with lock:
        att_random = random.randint(0,100)
        att_success = success(self.strength, attack_modifier, character.defense, att_random)
        att_damage = damage(att_success, self.constitution)

        print("""\
{} attacks {}!
STR {} + ATTMOD {} - DEF {} + RAND {} = {}\
        """.format(self.name, character.name, self.strength, attack_modifier, character.defense, att_random, success))

        if att_damage < 0:
            print("""\
{} evades the attack.\
                """.format(character.name))
        else:
            character.health = character.health - damage
            print("""\
{} damages {} by {}.\
                """.format(self.name, character.name, damage))
            if character.health <= 0:
                character.is_dead()
        return character



