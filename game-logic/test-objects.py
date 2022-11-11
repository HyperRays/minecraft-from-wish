"""
test if inheriting GraphicsObject will work and display correctly
"""
from prelude import *
import logging


GraphicsObject.init((300,300),"test objects")

class Ball(GraphicsObject):
    
    __texture = GraphicsObject.add_texture("test_snow.png")
    def __init__(self) -> None:
        super().__init__()
        self.texture = self.textures[self.__texture].copy()
    

    def render(self):
        self.screen.blit(self.texture.image, (0,0))
    
    def update(self):
        self.render()


Ball()


GraphicsObject.run()