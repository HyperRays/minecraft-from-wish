import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),'../game-logic'))
sys.path.append(os.path.join(os.path.dirname(__file__),'../graphics'))
from prelude import *
from chunks_module import Chunk

import time

window.init((700,700),"test chunks")
window.camera = [-window.size[0]/2,-window.size[1]/2]



class Square(GraphicsObject):
    sq_size = 17

    def __init__(self, position: vec2d) -> None:
        self.position = position
        self.texture = self.textures[self.texture].copy()
    
    def render(self):
        self.screen.blit(self.texture.image, (self.position.x - self.camera[0], self.position.y - self.camera[1]))
    
    def update(self):
        self.render()

class Ice(Square):
    texture = GraphicsObject.add_texture("ice_block.png") 
    (a,b) = store.textures[texture].image.get_size()
    ratio = a/b
    (w,h) = (Square.sq_size,Square.sq_size/ratio)
    store.textures[texture].image = pygame.transform.scale(store.textures[texture].image, (w,h))
    del a,b,ratio

    

class Grass(Square):
    texture = GraphicsObject.add_texture("grass_block.png") 
    (a,b) = store.textures[texture].image.get_size()
    ratio = a/b
    (w,h) = (Square.sq_size,Square.sq_size/ratio)
    store.textures[texture].image = pygame.transform.scale(store.textures[texture].image, (w,h))
    del a,b,ratio


class Dirt(Square):
    texture = GraphicsObject.add_texture("dirt_block.png") 
    (a,b) = store.textures[texture].image.get_size()
    ratio = a/b
    (w,h) = (Square.sq_size,Square.sq_size/ratio)
    store.textures[texture].image = pygame.transform.scale(store.textures[texture].image, (w,h))
    del a,b,ratio

class Player(GraphicsObject):

    texture = GraphicsObject.add_texture("hi-res-stickman.png") 
    (a,b) = store.textures[texture].image.get_size()
    ratio = a/b
    (w,h) = (40,40/ratio)
    store.textures[texture].image = pygame.transform.scale(store.textures[texture].image, (w,h))
    del a,b,ratio

    def __init__(self, position: vec2d) -> None:
        super().__init__()
        self.position = position
        self.texture = self.textures[self.texture].copy()
    
    def render(self):
        self.screen.blit(self.texture.image, (self.position.x - self.camera[0], self.position.y - self.camera[1]))
    
    def update(self):
        self.render()
    
    def input(self, keys):


        speed = 10
        if timer.reached(): timer.reset()
        timer.poll()

        if timer.reached():
            if keys[self.characters["s"]]:
                self.position.y += speed
                self.camera[1] += speed
            elif keys[self.characters["w"]]:
                self.position.y -= speed
                self.camera[1] -= speed
            
            if keys[self.characters["d"]]:
                self.position.x += speed
                self.camera[0] += speed
            elif keys[self.characters["a"]]:
                self.position.x -= speed
                self.camera[0] -= speed
            
            if keys[self.characters["escape"]]:
                print(self.camera)



def over_surface(x,y, chunk):
    coordinates_glob = chunk.get_chunk_coordinates(vec2d(x,y))
    coordinates = vec2d(x= (coordinates_glob.x*Ice.h), y= (coordinates_glob.y*Ice.w))
    if y > 5:
        return Dirt(coordinates)
    elif y == 5:
        return Grass(coordinates)

def under_surface(x,y,chunk):
    coordinates_glob = chunk.get_chunk_coordinates(vec2d(x,y))
    coordinates = vec2d(x= (coordinates_glob.x*Ice.h), y= (coordinates_glob.y*Ice.w))
    return Dirt(coordinates)


Player(vec2d(0,0))

for a in range(10):
    Chunk(vec2d(a,0), over_surface)

for a in range(10):
    for b in range(1,10):
        Chunk(vec2d(a,b), under_surface)

window.run()