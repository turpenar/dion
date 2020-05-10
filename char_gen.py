
import tkinter as tk
import pathlib as pathlib
import pickle as pickle

import player as player
import world as world


global terminal_output

def link_terminal(terminal):
    global terminal_output
    terminal_output = terminal

class General(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent

        self.first_name_label = tk.Label(self, text="First Name")
        self.first_name_label.grid(row=0, column=0)

        self.first_name_entry = tk.Entry(self, width=25)
        self.first_name_entry.grid(row=1, column=0)

        self.last_name_label = tk.Label(self, text="Last Name")
        self.last_name_label.grid(row=2, column=0)

        self.last_name_entry = tk.Entry(self, width=25)
        self.last_name_entry.grid(row=3, column=0)

        self.gender_label = tk.Label(self, text="Gender")
        self.gender_label.grid(row=4, column=0)

        self.genderVar = tk.StringVar(self.parent)
        gender_choices = {'male', 'female'}
        self.genderVar.set('male')

        self.gender_entry = tk.OptionMenu(self, self.genderVar, *gender_choices)
        self.gender_entry.grid(row=5, column=0)


class Stats(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent

        self.all_entries = {}

        self.strength_label = tk.Label(self, text="Strength")
        self.strength_label.grid(row=0, column=0)

        self.strength_entry = tk.Entry(self, width=8)
        self.strength_entry.grid(row=0, column=1)
        self.all_entries['Strength'] = self.strength_entry

        self.constitution_label = tk.Label(self, text="Constitution")
        self.constitution_label.grid(row=1, column=0)

        self.constitution_entry = tk.Entry(self, width=8)
        self.constitution_entry.grid(row=1, column=1)
        self.all_entries['Constitution'] = self.constitution_entry

        self.dexterity_label = tk.Label(self, text="Dexterity")
        self.dexterity_label.grid(row=2, column=0)

        self.dexterity_entry = tk.Entry(self, width=8)
        self.dexterity_entry.grid(row=2, column=1)
        self.all_entries['Dexterity'] = self.dexterity_entry

        self.agility_label = tk.Label(self, text="Agility")
        self.agility_label.grid(row=3, column=0)

        self.agility_entry = tk.Entry(self, width=8)
        self.agility_entry.grid(row=3, column=1)
        self.all_entries['Agility'] = self.agility_entry

        self.intelligence_label = tk.Label(self, text="Intelligence")
        self.intelligence_label.grid(row=0, column=3)

        self.intelligence_entry = tk.Entry(self, width=8)
        self.intelligence_entry.grid(row=0, column=4)
        self.all_entries['Intelligence'] = self.intelligence_entry

        self.wisdom_label = tk.Label(self, text="Wisdom")
        self.wisdom_label.grid(row=1, column=3)

        self.wisdom_entry = tk.Entry(self, width=8)
        self.wisdom_entry.grid(row=1, column=4)
        self.all_entries['Wisdom'] = self.wisdom_entry

        self.charisma_label = tk.Label(self, text="Charisma")
        self.charisma_label.grid(row=2, column=3)

        self.charisma_entry = tk.Entry(self, width=8)
        self.charisma_entry.grid(row=2, column=4)
        self.all_entries['Charisma'] = self.charisma_entry

        self.spirit_label = tk.Label(self, text="Spirit")
        self.spirit_label.grid(row=3, column=3)

        self.spirit_entry = tk.Entry(self, width=8)
        self.spirit_entry.grid(row=3, column=4)
        self.all_entries['Spirit'] = self.spirit_entry


class CharacterGenerator:
    def __init__(self, parent):

        self.parent = parent
        self.frame = tk.Frame(self.parent)

        self.general = General(self.parent)
        self.general.grid(row=0, column=0)

        self.stats = Stats(self.parent)
        self.stats.grid(row=2, column=0)

        self.label = tk.Label(self.frame)
        self.label.grid(row=3, column=0)
        self.button1 = tk.Button(self.frame, text="Create Character", command=self.create_character)
        self.button1.grid(row=4, column=0)
        self.frame.grid()

    def create_character(self):

        total_stats = 0
        available_stat_points = 100

        for entry in self.stats.all_entries:
            if not self.stats.all_entries[entry].get():
                self.popupmsg(entry + " has no value!")
                return

            total_stats += int(self.stats.all_entries[entry].get())

        if total_stats != available_stat_points:
            self.popupmsg("Your stats total does not equal " + str(available_stat_points))
            return

        world.load_tiles()
        player.create_character('new_player')

        player.character.name = self.general.first_name_entry.get()
        player.character.first_name = self.general.first_name_entry.get()
        player.character.last_name = self.general.last_name_entry.get()

        player.character.strength = int(self.stats.strength_entry.get())
        player.character.constitution = int(self.stats.constitution_entry.get())
        player.character.dexterity = int(self.stats.dexterity_entry.get())
        player.character.agility = int(self.stats.agility_entry.get())
        player.character.intelligence = int(self.stats.intelligence_entry.get())
        player.character.wisdom = int(self.stats.wisdom_entry.get())
        player.character.charisma = int(self.stats.charisma_entry.get())
        player.character.spirit = int(self.stats.spirit_entry.get())

        player.character.save()

        terminal_output.print_text('''
You have created {} {}

<Press Enter>
                                    \
                                    '''.format(player.character.first_name,
                                               player.character.last_name))

        # self.popupmsg("You have created " + self.character['first_name'] + " " + self.character['last_name'])

        self.frame.character_created = True

        self.close_window()

    def popupmsg(self, msg):
        self.popup = tk.Tk()
        self.popup.wm_title("Whoops!")
        label = tk.Label(self.popup, text=msg)
        label.pack(side="top", fill="x", pady=10)
        B1 = tk.Button(self.popup, text="Okay", command=self.popup.destroy)
        B1.pack()
        self.popup.mainloop()

    def close_window(self):
        self.parent.destroy()


class CharacterLoader:
    def __init__(self, parent):

        self.parent = parent
        self.frame = tk.Frame(self.parent)
        self.saved_characters = []

        self.gender_label = tk.Label(self.frame, text="Select a character")
        self.gender_label.grid(row=1, column=0)

        self.charVar = tk.StringVar(self.frame)
        self.char_choices = self.get_characters()
        self.charVar.set("Choose Character")

        self.gender_entry = tk.OptionMenu(self.frame, self.charVar, *self.char_choices)
        self.gender_entry.grid(row=2, column=0)

        self.label = tk.Label(self.frame)
        self.label.grid(row=3, column=0)
        self.button1 = tk.Button(self.frame, text="Load Character", command=self.load_character)
        self.button1.grid(row=4, column=0)
        self.frame.grid()

    def load_character(self):

        char_name = self.charVar.get()

        world.load_tiles()

        for char_data in self.saved_characters:
            if char_data['first_name'] == char_name:
                player.create_character("new_player")
                player.character.load(state=char_data)

        terminal_output.print_text('''
You have loaded {} {}

***  Type HELP for a list of commands available to you. Type HELP <command> for assistance with a particular
command usage.  ***

<Press Enter>
                                    \
                                    '''.format(player.character.first_name,
                                               player.character.last_name))

        self.close_window()

    def get_characters(self):

        path_load = pathlib.Path.cwd() / 'Profiles'
        filenames = path_load.glob('*.p')
        for filename in filenames:
            path_load_file = path_load / filename
            f = open(path_load_file.absolute().as_posix(), 'rb')
            self.saved_characters.append(pickle.load(f))

        saved_character_names = []

        for character in self.saved_characters:
            saved_character_names.append(character['first_name'])

        return saved_character_names

    def close_window(self):
        self.parent.destroy()