"""
This is the container for the different blocks 
"""

IMPORT_GRAPHICS_LIB = False
import asyncio
from dataclasses import dataclass
import pickle

# from chunk_manager import ChunkManager

from prelude import *
import itertools
import blocks

window.init((300,300),"test objects")

class Chunk(GraphicsObject):
    # all chunks are squares, and predefined sizes


    # chunks have their own x,y coordinates relative to other chunks
    # in the chunks there is another coordinate system
    # this grid is the local coordinates of the individual tiles

    def __init__(self, vec: vec2d, mapping_func) -> None:
        # chunks do not get immediately added to the objects list, but get loaded in 
        # dynamicaly depending on the players coordinates
        self.internal_objects = [[None for _ in range(CHUNK_DIMENSIONS[1])] for _ in range(CHUNK_DIMENSIONS[0])]
        assert(vec.x%1==0 and vec.y%1==0)
        self.position = vec
        self.on_first_load(mapping_func)

    
    def get_chunk_coordinates(self, vec: vec2d) -> vec2d:
        """
        global coordinates based on current chunk and coordinates
        """
        # a bit of branchless programming
        return vec2d(   x= CHUNK_DIMENSIONS[0]*self.position.x+vec.x,

                        y = CHUNK_DIMENSIONS[1]*self.position.y+vec.y
                    )
    
    async def update(self):
        for object in itertools.chain(*self.internal_objects):
                if object != None:
                    await object.update()
    
    async def render(self):
        for object in itertools.chain(*self.internal_objects):
                if object != None:
                    await object.render()
            
    def get(self, location: vec2d):
        try:
            return self.internal_objects[location.x][location.y]
        except:
            return None

    def set(self, location: vec2d, setter: GraphicsObject):
        try:
            self.internal_objects[location.x][location.y] = setter
            return True
        except:
            return False

    def on_first_load(self, mapping_func):
        # I don't know if this function is here to stay
        # probably need to find a better way

        for x in range(CHUNK_DIMENSIONS[0]):
            for y in range(CHUNK_DIMENSIONS[1]):
                self.internal_objects[x][y] = mapping_func(x,y, self)
    
    def save(self) -> dict:
        save_dict = {
            "position": self.position,
            "internal_objects_pickled": [[y.save() for y in x] for x in self.internal_objects]
        }
        return pickle.dumps(save_dict)

    @classmethod
    def load(cls, b: bytes):

        self = cls.__new__(cls)
        save_dict = pickle.loads(b)
        self.internal_objects =  [[blocks.Material.return_material(y) for y in x] for x in save_dict["internal_objects_pickled"]]
        self.position = save_dict["position"]

        return self