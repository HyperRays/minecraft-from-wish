"""
This file imports constants from TOML config files
"""

import toml
import sys
import os

with open(os.path.join(os.path.dirname(__file__),"../assets/config/chunk.toml")) as f:
    __config_chunks = toml.load(f)

with open(os.path.join(os.path.dirname(__file__),"../assets/config/block.toml")) as f:
    __config_blocks = toml.load(f)

with open(os.path.join(os.path.dirname(__file__),"../assets/config/player.toml")) as f:
    __config_player = toml.load(f)

with open(os.path.join(os.path.dirname(__file__),"../assets/config/general.toml")) as f:
    __config_general = toml.load(f)

CHUNK_DIMENSIONS = tuple(__config_chunks["dimensions"].values())
BLOCK_DIMENSIONS = list(__config_blocks["dimensions"].values())
PLAYER_SPEED = __config_player["player-speed"]
PLAYER_HEIGHT = __config_player["dimensions"]["height"]
PLAYER_WIDTH = __config_player["dimensions"]["width"]
GRAVITY_ACCEL = __config_general["gravity"]

WINDOW_DIMENSIONS = (__config_general["window"]["width"],__config_general["window"]["height"])
DAY_NIGHT_CYCLE_TIME_MIN = __config_general["day_night_cycle_time_min"]