
"""
This module creates the user interface for the program.
"""

import tkinter.scrolledtext as tkscrolledtext
import tkinter as tk

import world as world
import player as player
import actions as actions
import enemies as enemies
import combat as combat
import npcs as npcs
import objects as objects
import game as game
import char_gen as character_generator



class Main(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.wm_title("Dion")


class TerminalWindow(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.text_box = tkscrolledtext.ScrolledText(self, width = 120, height = 20)
        self.text_box.pack()

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

        self.terminal_window = TerminalWindow(self)
        self.commandbox = CommandBox(self)

        self.terminal_window.pack(side=tk.TOP)
        self.commandbox.pack(side=tk.BOTTOM)

        self.char_gen = None

        player.link_terminal(self.terminal_window)
        actions.link_terminal(self.terminal_window)
        enemies.link_terminal(self.terminal_window)
        combat.link_terminal(self.terminal_window)
        npcs.link_terminal(self.terminal_window)
        objects.link_terminal(self.terminal_window)
        game.link_terminal(self.terminal_window)
        character_generator.link_terminal(self.terminal_window)

        game.splash_screen()

        self.commandbox.user_entry.bind("<Return>", self.char_gen_start(character_generator.CharacterGenerator))


    def begin_game(self):
        world.load_tiles()
        player.create_character(character_name="new_player")

        room = world.tile_exists(x=player.character.location_x, y=player.character.location_y, area=player.character.area)
        room.fill_room(character=player.character)
        self.terminal_window.print_text(room.intro_text())

        self.commandbox.user_entry.bind("<Return>", self.submit_command)


    def submit_command(self, event = None):
        entry = self.commandbox.user_entry.get()
        self.terminal_window.print_command(entry)
        self.commandbox.user_entry.delete(0,"end")

        actions.do_action(action_input=entry, character=player.character)

    def char_gen_start(self, _class, event=None,):
        if not self.char_gen:
            self.char_gen = character_generator.CharacterGenerator(self.parent)

    def char_gen_end(self, event=None):
        self.char_gen.withdraw()


class IntroductionApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)


if __name__ == "__main__":

    root = tk.Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()





