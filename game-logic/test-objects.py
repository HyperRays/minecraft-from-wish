"""
test if inheriting GraphicsObject will work and display correctly
"""
from dataclasses import dataclass
from prelude import *
import numpy as np


GraphicsObject.init((300,300),"test objects")
@dataclass(slots=True)
class vec2d:
    x: int
    y: int

class Ball(GraphicsObject):
    # __dtype = np.dtype({"names": ["x","y"], "formats": ["f4","f4"]})
    __texture = GraphicsObject.add_texture("hi-res-stickman.jpg")
    def __init__(self) -> None:
        super().__init__()
        self.texture = self.textures[self.__texture].copy()
        self.position = vec2d(self.size[0]/2,self.size[1]/2)
    

    def render(self):
        self.screen.blit(self.texture.image, (self.position.x - self.camera[0],self.position.y - self.camera[1]))
    
    def update(self):
        self.render()


Ball()


GraphicsObject.run()