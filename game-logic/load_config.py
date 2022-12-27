import toml
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__),"../config"))


with open(os.path.join(os.path.dirname(__file__),"../config/chunk.toml")) as f:
    __config_chunks = toml.load(f)

with open(os.path.join(os.path.dirname(__file__),"../config/block.toml")) as f:
    __config_blocks = toml.load(f)

with open(os.path.join(os.path.dirname(__file__),"../config/player.toml")) as f:
    __config_player = toml.load(f)

with open(os.path.join(os.path.dirname(__file__),"../config/general.toml")) as f:
    __config_gravity = toml.load(f)

CHUNK_DIMENSIONS = tuple(__config_chunks["dimensions"].values())
block_dimensions = list(__config_blocks["dimensions"].values())
PLAYER_SPEED = __config_player["player-speed"]
PLAYER_HEIGHT = __config_player["dimensions"]["height"]
PLAYER_WIDTH = __config_player["dimensions"]["width"]
GRAVITY_ACCEL = __config_gravity["gravity"]
