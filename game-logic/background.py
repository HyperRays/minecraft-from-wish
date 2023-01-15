"""
A class for the background, the idea is to expand this to make dynamically moving objects
"""

from prelude import *

class Background(GraphicsObject):
    def __init__(self) -> None:
        super().__init__()
    
    async def render(self):
        graphics.layers["bg"].fill((212, 234, 255))