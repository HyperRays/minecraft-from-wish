import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__),'../graphics'))
from prelude import *
from chunks_module import Chunk
from chunk_manager import ChunkManager
import itertools
from random import randint

import pickle

from helper_functions import *
# initialize the window
window.init(WINDOW_DIMENSIONS,"test chunk mgr")

texture_handler = TextureHandler()

# create a camera
camera = Camera()

# the chunk_manager stores all of the chunks
chunk_manager = ChunkManager()