import os
import sys
import time
sys.path.append(os.path.join(os.path.dirname(__file__),'../game-logic'))
sys.path.append(os.path.join(os.path.dirname(__file__),'../graphics'))
from prelude import *
from chunks_module import Chunk
from chunk_manager import ChunkManager



window.init((700,700),"test chunks")

#https://stackoverflow.com/questions/14822184/is-there-a-ceiling-equivalent-of-operator-in-python
def ceildiv(a, b):
    return -(a // -b)

class Timed:
    def __init__(self, target_ns) -> None:
        self.current_time = time.process_time_ns()
        self.target_time = target_ns
        self.total_time = 0
        self.dx = 0
    
    def poll(self) -> None:
        new_time = time.process_time_ns()
        self.total_time += new_time - self.current_time
        self.dx = new_time - self.current_time
        self.current_time = new_time
    
    def reached(self) -> bool:
        return self.total_time >= self.target_time
    
    def reset(self) -> None:
        self.total_time = 0


timer = Timed(1_000_000)

class Square(GraphicsObject):
    sq_size = 17

    def __init__(self, position: vec2d) -> None:
        self.position = position
        self.texture = self.textures[self.texture].copy()
    
    def render(self):
        self.screen.blit(self.texture.image, (self.position.x - self.camera[0], self.position.y + self.camera[1]))
    
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


chunk_manager = ChunkManager()



def chekered(x,y, chunk):
    coordinates_glob = chunk.get_chunk_coordinates(vec2d(x,y))
    coordinates = vec2d(x= (coordinates_glob.x*Ice.h), y= (coordinates_glob.y*Ice.w))
    if -coordinates_glob.y < 0:
        return Dirt(coordinates)
    if -coordinates_glob.y == 0:
        return Grass(coordinates)


for a in range(-10,10):
    for b in range(-10,10):
        chunk_manager.add_chunk(Chunk(vec2d(a,b), chekered))


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
                self.camera[1] -= speed

            elif keys[self.characters["w"]]:
                self.camera[1] += speed
            
            if keys[self.characters["d"]]:
                self.camera[0] += speed

            elif keys[self.characters["a"]]:
                self.camera[0] -= speed
            
            self.position = vec2d(self.camera[0],self.camera[1])-vec2d(-window.size[0]/2,-window.size[1]/2)
            
            chunk_total_size = Square.sq_size*Chunk._chunk_size

            bounds_window = vec2d(ceildiv(window.size[0],chunk_total_size)+1, ceildiv(window.size[1],chunk_total_size)+1)
            min_bounds = vec2d(ceildiv(window.camera[0],chunk_total_size)-1, ceildiv(window.camera[1],chunk_total_size)+1)
            
            max_bounds = vec2d(min_bounds.x+bounds_window.x,min_bounds.y-bounds_window.y)
            chunk_manager.set_renderables(min_bounds, max_bounds)

Player(vec2d(0,0))
# chunk_manager.set_renderables(vec2d(1,1),vec2d(3,3))
chunk_total_size = Square.sq_size*Chunk._chunk_size

bounds_window = vec2d(ceildiv(window.size[0],chunk_total_size)+1, ceildiv(window.size[1],chunk_total_size)+1)
min_bounds = vec2d(ceildiv(window.camera[0],chunk_total_size)-1, ceildiv(window.camera[1],chunk_total_size)+1)

max_bounds = vec2d(min_bounds.x+bounds_window.x,min_bounds.y-bounds_window.y)
print(min_bounds, max_bounds)
chunk_manager.set_renderables(min_bounds, max_bounds)

window.run()

