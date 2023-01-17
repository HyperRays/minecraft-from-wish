import sys
import os
from prelude import *
from chunks_module import Chunk
from chunk_manager import ChunkManager
import itertools
from random import randint

import pickle

from helper_functions import *


# initialize the window
window.init(WINDOW_DIMENSIONS,"test chunk mgr", fullscreen=False)

window.size = WINDOW_DIMENSIONS

texture_handler = TextureHandler()

# create a camera
camera = Camera()

# the chunk_manager stores all of the chunks
chunk_manager = ChunkManager()