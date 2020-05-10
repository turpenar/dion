

import tkinter as tk
import tkinter.scrolledtext as tkscrolledtext

import world as world
import player as player
import actions as actions
import enemies as enemies
import combat as combat
import npcs as npcs
import objects as objects
import game as game
import char_gen as character_generator
import tiles as tiles


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
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.master = master
        self.new = None
        self.load = None
        self.character_created = tk.BooleanVar(self, value=False)
        self.game_start = tk.BooleanVar(self, value=False)

        self.terminal_window = TerminalWindow(self)
        self.commandbox = CommandBox(self)

        self.terminal_window.pack(side=tk.TOP)
        self.commandbox.pack(side=tk.BOTTOM)

        player.link_terminal(self.terminal_window)
        actions.link_terminal(self.terminal_window)
        enemies.link_terminal(self.terminal_window)
        combat.link_terminal(self.terminal_window)
        npcs.link_terminal(self.terminal_window)
        objects.link_terminal(self.terminal_window)
        game.link_terminal(self.terminal_window)
        character_generator.link_terminal(self.terminal_window)
        tiles.link_terminal(self.terminal_window)

        self.splash_screen()

        self.commandbox.user_entry.bind("<Return>", func=self.game_menu)

    def game_menu(self, event):

        if not self.character_created.get():
            entry = self.submit_command()

            if (entry == "New Character") or (entry == "1"):
                self.new_character()
                self.character_created.set(True)
                return

            if (entry == "Load Character") or (entry == "2"):
                self.load_character()
                self.character_created.set(True)
                return

            else:
                self.terminal_window.print_text("That is not a valid entry. Please enter [1] for [New Character] or [2] for [Load Character]")
                return

        if not self.game_start.get():
            entry = self.submit_command()
            self.begin_game()
            self.game_start.set(True)
            return

        if self.game_start.get():
            entry = self.submit_command()

            actions.do_action(action_input=entry, character=player.character)

    def submit_command(self):
        entry = self.commandbox.user_entry.get()
        self.terminal_window.print_command(entry)
        self.commandbox.user_entry.delete(0, "end")
        return entry

    def new_character(self):
        if not self.new:
            self.new = tk.Toplevel(self.master)
            character_generator.CharacterGenerator(self.new)

    def load_character(self):
        if not self.load:
            self.load = tk.Toplevel(self.master)
            character_generator.CharacterLoader(self.load)

    def begin_game(self):

        if self.new:
            self.new_character_introduction()

        world.load_tiles()

        player.character.room = world.tile_exists(x=player.character.location_x, y=player.character.location_y, area=player.character.area)
        player.character.room.fill_room(character=player.character)
        player.character.room.intro_text()

    def splash_screen(self):
        welcome_screen = """\
        ################################################################
        ####                    Welcome to Dion                     ####
        ################################################################

                                [1] New Character
                                [2] Load Character
        \
        """

        self.terminal_window.print_text(welcome_screen)

    def new_character_introduction(self):
        self.terminal_window.print_text('''\n
    The beast becomes restless...  hungry and tired...

                        ...it trembles with anger, and the earth shakes...

    Far away, you lay in a field surrounded by trees.    
    You close your eyes and an unsettling feeling comes over you. You dread having to go back into town and resume a 
    day you already know is going to be a waste. But you know that people rely on you and your resolve. They trust you,
    at least that's what they say. "{} really knows how to get things done," they would say.

    You open your eyes...
        \
        '''.format(player.character.object_pronoun))


if __name__ == "__main__":

    root = tk.Tk()
    app = MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
