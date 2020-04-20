
"""


TODO: Insert player name in combat text
"""


import random as random
import threading as threading
import config as config

import items as items

lock = threading.Lock()

def link_terminal(terminal):
    global terminal_output
    terminal_output = terminal


def success(strength, attack_modifier, defense, att_random):
    return int((strength + attack_modifier - defense + att_random - 100))

def damage(success, constitution):
    return int(success / constitution)

def get_experience(character_level, target_level):
    if character_level > target_level + 5:
        return 0
    level_differential = character_level - target_level
    base_experience = float(config.EXPERIENCE_FILE.at[target_level,"Experience_Per_Enemy"])
    if level_differential >= 0:
        adjusted_experience = base_experience - 0.2 * base_experience * level_differential
    elif level_differential < 0:
        adjusted_experience = base_experience + 0.1 * base_experience * level_differential * -1
    else:
        adjusted_experience = base_experience
    random_modifier = -1 + (random.random() * 2)
    experience = int(adjusted_experience * random_modifier)
    return experience


def do_physical_damage_to_enemy(self, target):
    if isinstance(self.right_hand_inv, items.Weapon):
        attack_modifier = self.right_hand_inv.attack_modifier
    else:
        attack_modifier = 0

    with lock:
        att_random = random.randint(0,100)
        att_success = success(self.strength, attack_modifier, target.defense, att_random)
        att_damage = damage(att_success, self.constitution)

        terminal_output.print_text("""\
{} attacks {}!
STR {} + ATTMOD {} - DEF {} + RAND {} = {}\
        """.format(self.name, target.name, self.strength, attack_modifier, target.defense, att_random, att_success))

        if att_damage < 0:
            terminal_output.print_text("""\
{} evades the attack.\
                """.format(target.name))
        else:
            target.health = target.health - att_damage
            terminal_output.print_text("""\
{} damages {} by {}.\
                """.format(self.name, target.name, att_damage))
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

        terminal_output.print_text("""\
{} attacks {}!
STR {} + ATTMOD {} - DEF {} + RAND {} = {}\
        """.format(self.name, character.name, self.strength, attack_modifier, character.defense, att_random, att_success))

        if att_damage < 0:
            terminal_output.print_text("""\
{} evades the attack.\
                """.format(character.name))
        else:
            character.health = character.health - att_damage
            terminal_output.print_text("""\
{} damages {} by {}.\
                """.format(self.name, character.name, att_damage))
            if character.health <= 0:
                character.is_dead()
        return character



