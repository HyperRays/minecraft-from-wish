IMPORT_GRAPHICS_LIB = False
from prelude import *

class Camera:

    def __init__(self):
        self.position = vec2d(0,0)
    
    def screen_position(self, other: vec2d) -> vec2d:
        return vec2d(other.x - self.position.x, -other.y + self.position.y)
    
    def update_position(self, position: vec2d) -> vec2d:
        self.position = position
    
    def get_position(self) -> vec2d:
        return self.position
    
def invert_y(vec: vec2d) -> vec2d:
    return vec2d(vec.x, -vec.y)
