"""
test if inheriting GraphicsObject will work and display correctly
"""
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),'../game-logic'))
from dataclasses import dataclass
from prelude import *


window.init((300,300),"test objects")

@dataclass(slots=True)
class vec2d:
    x: int
    y: int


class Ball(GraphicsObject):
    __texture = GraphicsObject.add_texture("test_snow.png") 
    (a,b) = store.textures[__texture].image.get_size()
    ratio = a/b
    store.textures[__texture].image = pygame.transform.scale(store.textures[__texture].image, (100,100/ratio))
    del a,b,ratio
    
    def __init__(self) -> None:
        super().__init__()
        self.texture = self.textures[self.__texture].copy()
        (h,w) = self.texture.image.get_size()
        self.position = vec2d((self.size[0]-h)/2,(self.size[1]-w)/2)
    

    def render(self):
        self.screen.blit(self.texture.image, (self.position.x - self.camera[0],self.position.y - self.camera[1]))
    
    def update(self):
        self.render()


Ball()


window.run()