import pathlib as pathlib
import pandas as pd

DATA_DIR = pathlib.Path(__file__).parent / "Resources"
DATA_FORMAT = "json"

ROOM_FILE = str(DATA_DIR / f"tiles.{DATA_FORMAT}")
ITEM_FILE = str(DATA_DIR / f"items.{DATA_FORMAT}")
ENEMY_FILE = str(DATA_DIR / f"enemies.{DATA_FORMAT}")
NPC_FILE = str(DATA_DIR / f"npcs.{DATA_FORMAT}")
QUEST_FILE = str(DATA_DIR / f"quests.{DATA_FORMAT}")
OBJECT_FILE = str(DATA_DIR / f"objects.{DATA_FORMAT}")
PLAYER_FILE = str(DATA_DIR / f"players.{DATA_FORMAT}")

TEXT_WRAPPER_WIDTH = 100

EXPERIENCE_FILE = pd.read_csv(DATA_DIR / "Game_Data.csv")