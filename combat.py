
import random as random
import threading as threading

import items as items

lock = threading.Lock()


def do_physical_damage(self, target):
    if isinstance(self.right_hand_inv, items.Weapon):
        attack_modifier = self.right_hand_inv.attack_modifier
    else:
        attack_modifier = 0

    with lock:
        att_random = random.randint(0,100)
        success = int((self.strength + attack_modifier - target.defense + att_random - 100))

        print("""\
{} attacks {}!
STR {} + ATTMOD {} - DEF {} + RAND {} = {}\
        """.format(self.name, target.name, self.strength, attack_modifier, target.defense, att_random, success))
        damage = int(success / self.constitution)

        if damage < 0:
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
        return target


