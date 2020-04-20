
import pathlib as pathlib

import mixins as mixins

# importing all prepositions and prepositional phrases

verbs_path = pathlib.Path.cwd() / 'Resources' / 'verbs.txt'
with verbs_path.open(mode='r') as file:
    verbs = file.readlines()
verbs = [x.strip() for x in verbs]

prepositions_path = pathlib.Path.cwd() / 'Resources' / 'prepositions.txt'
with prepositions_path.open(mode='r') as file:
    prepositions = file.readlines()
prepositions = [x.strip() for x in prepositions]

# importing all articles
articles_path = pathlib.Path.cwd() / 'Resources' / 'articles.txt'
with articles_path.open(mode='r') as file:
    articles = file.readlines()
articles = [x.strip() for x in articles]

# importing all determiners
determiners_path = pathlib.Path.cwd() / 'Resources' / 'determiners.txt'
with determiners_path.open(mode='r') as file:
    determiners = file.readlines()
determiners = [x.strip() for x in determiners]

# importing all nouns
nouns_path = pathlib.Path.cwd() / 'Resources' / 'nouns.txt'
with nouns_path.open(mode='r') as file:
    nouns = file.readlines()
nouns = [x.strip() for x in nouns]

objects = mixins.objects
items = mixins.items
npcs = mixins.npcs
enemies = mixins.enemies

adjectives = []

for object in objects:
    nouns.extend(objects[object]['handle'])
    adjectives.extend(objects[object]['adjectives'])

for category in items:
    for item in items[category]:
        nouns.extend(items[category][item]['handle'])
        adjectives.extend(items[category][item]['adjectives'])

for npc in npcs:
    nouns.extend(npcs[npc]['handle'])
    adjectives.extend(npcs[npc]['adjectives'])

for enemy in enemies:
    nouns.extend(enemies[enemy]['handle'])
    adjectives.extend(enemies[enemy]['adjectives'])



def find_index(input_list, list_of_matches):
    return [i for i, item in enumerate(input_list) if item in list_of_matches]


def parser(input):
    input = input.lower()
    tokens = input.split()
    tokens = [x for x in tokens if x not in articles]

    relevant_verbs = set(tokens).intersection(verbs)
    relevant_nouns = set(tokens).intersection(nouns)
    relevant_adjectives = set(tokens).intersection(adjectives)
    relevant_prepositions = set(tokens).intersection(prepositions)
    relevant_determiners = set(tokens).intersection(determiners)

    verb_index = find_index(tokens, relevant_verbs)
    noun_index = find_index(tokens, relevant_nouns)
    adjective_index = find_index(tokens, relevant_adjectives)
    preposition_index = find_index(tokens, relevant_prepositions)
    determiners_index = find_index(tokens, relevant_determiners)

    kwargs = {}

    if len(verb_index) > 0:
        kwargs['action_verb'] = tokens[verb_index[0]]
        kwargs['subject_verb'] = None
    if len(verb_index) > 1:
        kwargs['subject_verb'] = tokens[verb_index[1]]
    if len(noun_index) == 0:
        kwargs['direct_object'] = None
        kwargs['indirect_object'] = None
    elif len(noun_index) == 1:
        if len(preposition_index) > 0:
                kwargs['direct_object'] = None
                kwargs['indirect_object'] = [tokens[noun_index[0]]]
        else:
            kwargs['direct_object'] = [tokens[noun_index[0]]]
            kwargs['indirect_object'] = None
    else:
        kwargs['direct_object'] = [tokens[noun_index[0]]] or None
        kwargs['indirect_object'] = [tokens[noun_index[1]]] or None

    if len(preposition_index) < 1:
        kwargs['preposition'] = None
    elif len(preposition_index) == 1:
        kwargs['preposition'] = [tokens[preposition_index[0]]] or None
    return kwargs

