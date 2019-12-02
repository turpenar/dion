
"""
"""

import pathlib as pathlib
import pickle as pickle
import os as os

import world as world
import player as player
import actions as actions

def play():

    world.load_tiles()

    path_load = pathlib.Path.cwd() / 'Profiles'
    filenames = path_load.glob('*.p')
    saved_characters = []
    for filename in filenames:
        path_load_file = path_load / filename
        f = open(path_load_file.absolute().as_posix(), 'rb')
        saved_characters.append(pickle.load(f))


    saved_character_names = []

    for character in saved_characters:
        saved_character_names.append(character['first_name'])

    saved_character_names_print = ""
    if len(saved_character_names) == 0:
        saved_character_names_print = "None"
    else:
        for name in saved_character_names:
            saved_character_names_print = saved_character_names_print + "[" + name + "]" + "\n\t"

    print("""\
    ################################################################
    ####                    Welcome to Dion                     ####
    ################################################################
    
    Please enter an option:
    
    [New] Character
    
    Load Character:
    {}
    \
    """.format(saved_character_names_print))

    char_data = None
    character = None
    char_found = False
    while char_found == False:
        option = input('> ')

        if option == 'New':
            character = player.Player(player_name='new_player')
            char_found = True

            first_name = input("Please provide a first name for your character:  ")
            last_name = input("Please provide a last name for your character:  ")

            character.first_name = first_name
            character.last_name = last_name

        elif set(saved_character_names) & {option}:
            for char_data in saved_characters:
                if char_data['first_name'] == option:
                    character = player.Player(player_name='new_player')
                    character.load(state=char_data)
                    char_found = True
        else:
            print("That is not an option. Please select from the available options.")


    room = world.tile_exists(x=character.location_x, y=character.location_y, area=character.area)
    room.fill_room(character=character)
    print(room.intro_text())
    actions.DoActions(character=character).cmdloop()
    return


if __name__=="__main__":
    play()

