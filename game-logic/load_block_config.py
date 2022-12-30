import toml
import os
from uuid import uuid4

BLOCKS_PATH = "../blocks/"

def load_block_properties(properties_file: str):

    with open(os.path.join(os.path.dirname(__file__),BLOCKS_PATH, properties_file)) as f:
        __config_block = toml.load(f)

    if "extends" in __config_block:
        with open(os.path.join(os.path.dirname(__file__),BLOCKS_PATH, __config_block["extends"])) as f:
            __config_blocks_base = toml.load(f)
        
            __config_blocks_base["properties"].update(__config_block["properties"])
            __config_block["properties"] = __config_blocks_base["properties"]

    return type(str(uuid4()), (object, ), __config_block["properties"])