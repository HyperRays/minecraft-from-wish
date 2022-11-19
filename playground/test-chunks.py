import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),'../game-logic'))
sys.path.append(os.path.join(os.path.dirname(__file__),'../graphics'))
from dataclasses import dataclass
from prelude import *
from chunk_system import Chunk

import time

window.init((700,700),"test chunks")
window.camera = [-window.size[0]/2,-window.size[1]/2]

class Timed:
    def __init__(self, target_ns) -> None:
        self.current_time = time.process_time_ns()
        self.target_time = target_ns
        self.total_time = 0
    
    def poll(self) -> None:
        new_time = time.process_time_ns()
        self.total_time += new_time - self.current_time
        self.current_time = new_time
    
    def reached(self) -> bool:
        return self.total_time >= self.target_time
    
    def reset(self) -> None:
        self.total_time = 0


six_exe = Timed(1_000_000)

class Square(GraphicsObject):
    sq_size = 10

    def __init__(self, position: vec2d) -> None:
        self.position = position
        self.texture = self.textures[self.texture].copy()
    
    def render(self):
        self.screen.blit(self.texture.image, (self.position.x - self.camera[0], self.position.y - self.camera[1]))
    
    def update(self):
        self.render()

class Snow(Square):
    texture = GraphicsObject.add_texture("test_snow.png") 
    (a,b) = store.textures[texture].image.get_size()
    ratio = a/b
    (w,h) = (Square.sq_size,Square.sq_size/ratio)
    store.textures[texture].image = pygame.transform.scale(store.textures[texture].image, (w,h))
    del a,b,ratio

    

class Grass(Square):
    texture = GraphicsObject.add_texture("test_grass.png") 
    (a,b) = store.textures[texture].image.get_size()
    ratio = a/b
    (w,h) = (Square.sq_size,Square.sq_size/ratio)
    store.textures[texture].image = pygame.transform.scale(store.textures[texture].image, (w,h))
    del a,b,ratio


class Dirt(Square):
    texture = GraphicsObject.add_texture("test_dirt.png") 
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
        if six_exe.reached(): six_exe.reset()
        six_exe.poll()

        if six_exe.reached():
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
    coordinates = vec2d(x= (coordinates_glob.x*Snow.h), y= (coordinates_glob.y*Snow.w))
    if y > 5:
        return Dirt(coordinates)
    elif y == 5:
        return Grass(coordinates)

def under_surface(x,y,chunk):
    coordinates_glob = chunk.get_chunk_coordinates(vec2d(x,y))
    coordinates = vec2d(x= (coordinates_glob.x*Snow.h), y= (coordinates_glob.y*Snow.w))
    return Dirt(coordinates)

Player(vec2d(0,0))

for a in range(10):
    Chunk(vec2d(a,0), over_surface)

for a in range(10):
    for b in range(1,10):
        Chunk(vec2d(a,b), under_surface)

window.run()

