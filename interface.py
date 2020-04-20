
"""
This module creates the user interface for the program.
"""

import tkinter.scrolledtext as tkscrolledtext
import pathlib as pathlib
import pickle as pickle
import time as time
import tkinter as tk


import world as world
import player as player
import actions as actions
import enemies as enemies
import combat as combat
import npcs as npcs
import objects as objects


class Main(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.text_box = tkscrolledtext.ScrolledText(self, width = 120, height = 20)
        self.text_box.pack()
        self.text_box.insert("end-1c", "> ")

    def print_command(self, text):
        self.text_box.insert("end-1c", text + "\n")
        self.text_box.see(tk.END)

    def print_text(self, text):
        self.text_box.insert("end-1c", text + "\n")
        self.text_box.insert("end-1c", "> ")
        self.text_box.see(tk.END)


class CommandBox(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.user_entry = tk.Entry(self, width=100)
        self.user_entry.pack()


class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.main = Main(self)
        self.commandbox = CommandBox(self)

        player.link_terminal(self.main)
        actions.link_terminal(self.main)
        enemies.link_terminal(self.main)
        combat.link_terminal(self.main)
        npcs.link_terminal(self.main)
        objects.link_terminal(self.main)

        world.load_tiles()
        self.character = player.Player(player_name='new_player')
        room = world.tile_exists(x=self.character.location_x, y=self.character.location_y, area=self.character.area)
        room.fill_room(character=self.character)
        self.main.print_text(room.intro_text())

        self.main.pack(side=tk.TOP)
        self.commandbox.pack(side=tk.BOTTOM)
        self.commandbox.user_entry.bind("<Return>", self.submit_command)


    def submit_command(self, event = None):
        entry = self.commandbox.user_entry.get()
        self.main.print_command(entry)
        self.commandbox.user_entry.delete(0,"end")

        actions.do_action(action_input=entry, character=self.character)


if __name__ == "__main__":

    root = tk.Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()


