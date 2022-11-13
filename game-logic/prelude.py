"""
Pre-Import all the necessary modules
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__),".."))
from graphics.graphics_library import GraphicsObject
import pygame
from pygame.locals import *
from basic_units import *

#type aliases for better readability
window = GraphicsObject
store = GraphicsObject
