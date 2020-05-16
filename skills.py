

import tkinter as tk
import pathlib as pathlib
import pickle as pickle

import player as player
import world as world


global terminal_output

def link_terminal(terminal):
    global terminal_output
    terminal_output = terminal


class TrainingPoints(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent

        self.physical_points_var = tk.IntVar()
        self.physical_points_var.set(player.character.physical_points)
        self.physical_points_label = tk.Label(self, text="Physical Training Points = ")
        self.physical_points_label.grid(row=0, column=0)
        self.physical_points = tk.Label(self, textvariable=self.physical_points_var)
        self.physical_points.grid(row=0, column=1)

        self.mental_points_var = tk.IntVar()
        self.mental_points_var.set(player.character.mental_points)
        self.mental_points_label = tk.Label(self, text="Mental Training Points = ")
        self.mental_points_label.grid(row=0, column=2)
        self.mental_points = tk.Label(self, textvariable=self.mental_points_var)
        self.mental_points.grid(row=0, column=3)


class WeaponSkills(tk.Frame):
    def __init__(self, parent, training_points, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent
        self.training_points = training_points

        self.weapon_skills_label = tk.Label(self, text="Weapons Skills")
        self.weapon_skills_label.grid(row=0, column=0)

        self.edged_weapon_var_start = tk.IntVar(self)
        self.edged_weapon_var_start.set(player.character.skill_edged_weapons)

        self.edged_weapon_var = tk.IntVar(self)
        self.edged_weapon_var.set(player.character.skill_edged_weapons)

        self.edged_weapon_label = tk.Label(self, text="Edged Weapons")
        self.edged_weapon_label.grid(row=1, column=0)

        self.edged_weapon_decrease = tk.Button(self, text="-", command=lambda: self.decrease_skill(self.edged_weapon_var))
        self.edged_weapon_decrease.grid(row=1, column=1)

        self.edged_weapon_value = tk.Label(self, textvariable=self.edged_weapon_var)
        self.edged_weapon_value.grid(row=1, column=2)

        self.edged_weapon_increase = tk.Button(self, text="+", command=lambda: self.increase_skill(self.edged_weapon_var, self.edged_weapon_var_start))
        self.edged_weapon_increase.grid(row=1, column=3)


        self.blunt_weapon_var_start = tk.IntVar(self)
        self.blunt_weapon_var_start.set(player.character.skill_blunt_weapons)

        self.blunt_weapon_var = tk.IntVar(self)
        self.blunt_weapon_var.set(player.character.skill_blunt_weapons)

        self.blunt_weapon_label = tk.Label(self, text="Blunt Weapons")
        self.blunt_weapon_label.grid(row=2, column=0)

        self.blunt_weapon_decrease = tk.Button(self, text="-", command=lambda: self.decrease_skill(self.blunt_weapon_var))
        self.blunt_weapon_decrease.grid(row=2, column=1)

        self.blunt_weapon_value = tk.Label(self, textvariable=self.blunt_weapon_var)
        self.blunt_weapon_value.grid(row=2, column=2)

        self.blunt_weapon_increase = tk.Button(self, text="+", command=lambda: self.increase_skill(self.blunt_weapon_var, self.blunt_weapon_var_start))
        self.blunt_weapon_increase.grid(row=2, column=3)


        self.polearm_weapon_var_start = tk.IntVar(self)
        self.polearm_weapon_var_start.set(player.character.skill_polearm_weapons)

        self.polearm_weapon_var = tk.IntVar(self)
        self.polearm_weapon_var.set(player.character.skill_polearm_weapons)

        self.polearm_weapon_label = tk.Label(self, text="Polearm Weapons")
        self.polearm_weapon_label.grid(row=3, column=0)

        self.polearm_weapon_decrease = tk.Button(self, text="-",
                                               command=lambda: self.decrease_skill(self.polearm_weapon_var))
        self.polearm_weapon_decrease.grid(row=3, column=1)

        self.polearm_weapon_value = tk.Label(self, textvariable=self.polearm_weapon_var)
        self.polearm_weapon_value.grid(row=3, column=2)

        self.polearm_weapon_increase = tk.Button(self, text="+",
                                               command=lambda: self.increase_skill(self.polearm_weapon_var, self.polearm_weapon_var_start))
        self.polearm_weapon_increase.grid(row=3, column=3)

    def increase_skill(self, skill_var, skill_var_start):
        if skill_var.get() > skill_var_start.get() + 1:
            return

        self.training_points.physical_points_var.set(self.training_points.physical_points_var.get() - 2)
        self.training_points.mental_points_var.set(self.training_points.mental_points_var.get() - 1)
        skill_var.set(skill_var.get() + 1)

    def decrease_skill(self, skill_var):
        self.training_points.physical_points_var.set(self.training_points.physical_points_var.get() + 2)
        self.training_points.mental_points_var.set(self.training_points.mental_points_var.get() + 1)
        skill_var.set(skill_var.get() - 1)

    def calculate_increment(self):
        pass


class ArmorSkills(tk.Frame):
    def __init__(self, parent, training_points, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent
        self.training_points = training_points

        self.armor_skills_label = tk.Label(self, text="Armor Skills")
        self.armor_skills_label.grid(row=0, column=0)

        self.armor_var_start = tk.IntVar(self)
        self.armor_var_start.set(player.character.skill_armor)

        self.armor_var = tk.IntVar(self)
        self.armor_var.set(player.character.skill_armor)

        self.armor_label = tk.Label(self, text="Armor")
        self.armor_label.grid(row=1, column=0)

        self.armor_decrease = tk.Button(self, text="-", command=lambda: self.decrease_skill(self.armor_var))
        self.armor_decrease.grid(row=1, column=1)

        self.armor_value = tk.Label(self, textvariable=self.armor_var)
        self.armor_value.grid(row=1, column=2)

        self.armor_increase = tk.Button(self, text="+", command=lambda: self.increase_skill(self.armor_var, self.armor_var_start))
        self.armor_increase.grid(row=1, column=3)


        self.shield_var_start = tk.IntVar(self)
        self.shield_var_start.set(player.character.skill_shield)

        self.shield_var = tk.IntVar(self)
        self.shield_var.set(player.character.skill_shield)

        self.shield_label = tk.Label(self, text="Shield")
        self.shield_label.grid(row=2, column=0)

        self.shield_decrease = tk.Button(self, text="-", command=lambda: self.decrease_skill(self.shield_var))
        self.shield_decrease.grid(row=2, column=1)

        self.shield_value = tk.Label(self, textvariable=self.shield_var)
        self.shield_value.grid(row=2, column=2)

        self.shield_increase = tk.Button(self, text="+", command=lambda: self.increase_skill(self.shield_var, self.shield_var_start))
        self.shield_increase.grid(row=2, column=3)

    def increase_skill(self, skill_var, skill_var_start):
        if skill_var.get() > skill_var_start.get() + 1:
            return

        self.training_points.physical_points_var.set(self.training_points.physical_points_var.get() - 2)
        self.training_points.mental_points_var.set(self.training_points.mental_points_var.get() - 1)
        skill_var.set(skill_var.get() + 1)

    def decrease_skill(self, skill_var):
        self.training_points.physical_points_var.set(self.training_points.physical_points_var.get() + 2)
        self.training_points.mental_points_var.set(self.training_points.mental_points_var.get() + 1)
        skill_var.set(skill_var.get() - 1)


class SurvivalSkills(tk.Frame):
    def __init__(self, parent, training_points, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent
        self.training_points = training_points

        self.survival_skills_label = tk.Label(self, text="Survival Skills")
        self.survival_skills_label.grid(row=0, column=0)

        self.physical_fitness_var_start = tk.IntVar(self)
        self.physical_fitness_var_start.set(player.character.skill_physical_fitness)

        self.physical_fitness_var = tk.IntVar(self)
        self.physical_fitness_var.set(player.character.skill_physical_fitness)

        self.physical_fitness_label = tk.Label(self, text="Physical Fitness")
        self.physical_fitness_label.grid(row=1, column=0)

        self.physical_fitness_decrease = tk.Button(self, text="-", command=lambda: self.decrease_skill(self.physical_fitness_var))
        self.physical_fitness_decrease.grid(row=1, column=1)

        self.physical_fitness_value = tk.Label(self, textvariable=self.physical_fitness_var)
        self.physical_fitness_value.grid(row=1, column=2)

        self.physical_fitness_increase = tk.Button(self, text="+", command=lambda: self.increase_skill(self.physical_fitness_var, self.physical_fitness_var_start))
        self.physical_fitness_increase.grid(row=1, column=3)


        self.skinning_var_start = tk.IntVar(self)
        self.skinning_var_start.set(player.character.skill_skinning)

        self.skinning_var = tk.IntVar(self)
        self.skinning_var.set(player.character.skill_skinning)

        self.skinning_label = tk.Label(self, text="Skinning")
        self.skinning_label.grid(row=2, column=0)

        self.skinning_decrease = tk.Button(self, text="-", command=lambda: self.decrease_skill(self.skinning_var))
        self.skinning_decrease.grid(row=2, column=1)

        self.skinning_value = tk.Label(self, textvariable=self.skinning_var)
        self.skinning_value.grid(row=2, column=2)

        self.skinning_increase = tk.Button(self, text="+", command=lambda: self.increase_skill(self.skinning_var, self.skinning_var_start))
        self.skinning_increase.grid(row=2, column=3)

    def increase_skill(self, skill_var, skill_var_start):
        if skill_var.get() > skill_var_start.get() + 1:
            return

        self.training_points.physical_points_var.set(self.training_points.physical_points_var.get() - 2)
        self.training_points.mental_points_var.set(self.training_points.mental_points_var.get() - 1)
        skill_var.set(skill_var.get() + 1)

    def decrease_skill(self, skill_var):
        self.training_points.physical_points_var.set(self.training_points.physical_points_var.get() + 2)
        self.training_points.mental_points_var.set(self.training_points.mental_points_var.get() + 1)
        skill_var.set(skill_var.get() - 1)


class Skills:
    def __init__(self, parent):

        self.parent = parent
        self.frame = tk.Frame(self.parent, width=100)

        self.training_points = TrainingPoints(self.parent)
        self.training_points.grid(row=0, column=0)

        self.weapons_skills = WeaponSkills(self.parent, self.training_points)
        self.weapons_skills.grid(row=1, column=0)

        self.armor_skills = ArmorSkills(self.parent, self.training_points)
        self.armor_skills.grid(row=2, column=0)

        self.survival_skills = SurvivalSkills(self.parent, self.training_points)
        self.survival_skills.grid(row=3, column=0)

        self.label = tk.Label(self.frame)
        self.label.grid(row=4, column=0)
        self.button1 = tk.Button(self.frame, text="Update Skills", command=self.update_skills)
        self.button1.grid(row=5, column=0)
        self.frame.grid()

    def update_skills(self):

        player.character.skill_edged_weapons = self.weapons_skills.edged_weapon_var.get()
        player.character.skill_blunt_weapons = self.weapons_skills.blunt_weapon_var.get()
        player.character.skill_polearm_weapons = self.weapons_skills.polearm_weapon_var.get()

        player.character.skill_armor = self.armor_skills.armor_var.get()
        player.character.skill_shield = self.armor_skills.shield_var.get()

        player.character.skill_physical_fitness = self.survival_skills.physical_fitness_var.get()
        player.character.skill_skinning = self.survival_skills.skinning_var.get()

        self.close_window()

    def close_window(self):
        self.parent.destroy()

