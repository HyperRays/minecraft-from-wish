"""
Pre-Import all the necessary modules
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__),".."))
#set default of IMPORT_GRAPHICS_LIB to True if not already set
try: IMPORT_GRAPHICS_LIB
except: IMPORT_GRAPHICS_LIB = True

if IMPORT_GRAPHICS_LIB:
    from graphics.graphics_library import GraphicsObject
    import pygame
    from pygame.locals import *

    #type aliases for better readability
    window = GraphicsObject
    store = GraphicsObject

from basic_units import *
from shapes import Shape, Simplex2d, Quad
from physics import intersect


