import toml
import os
from uuid import uuid4

BLOCKS_PATH = "../assets/blocks/"

def load_block_properties(properties_file: str):

    with open(os.path.join(os.path.dirname(__file__),BLOCKS_PATH, properties_file)) as f:
        __config_properties = toml.load(f)

    if "extends" in __config_properties:
        with open(os.path.join(os.path.dirname(__file__),BLOCKS_PATH, __config_properties["extends"])) as f:
            __config_base = toml.load(f)
        
            __config_base["properties"].update(__config_properties["properties"])
            __config_properties["properties"] = __config_base["properties"]

    return type(str(uuid4()), (object, ), __config_properties["properties"])

PLAYER_CONFIG_PATH = "../assets/config/player.toml"

def load_player_properties():

    with open(os.path.join(os.path.dirname(__file__),PLAYER_CONFIG_PATH)) as f:
        __config_properties = toml.load(f)

    return type(str(uuid4()), (object, ), __config_properties["properties"])