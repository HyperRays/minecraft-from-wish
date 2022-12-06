from dataclasses import dataclass
from prelude import *
import itertools


window.init((300,300),"test objects")


class Chunk(GraphicsObject):
    # all chunks are squares, and predefined sizes
    __chunk_size = 16


    # chunks have their own x,y coordinates, in the chunks there is another grid
    # this grid is the local coordinates of the individual tiles
    # *() gets the global coordinates of the tile
    # get_local_coordinates() local coordinates of the tile
    # get_chunk() gets the chunk from a global coordinates

    def __init__(self, vec: vec2d, mapping_func) -> None:
        # chunks do not get immediately added to the objects list, but get loaded in 
        # dynamicaly depending on the players coordinates
        self.internal_objects = [[[None] for _ in range(self.__chunk_size)] for _ in range(self.__chunk_size)]
        assert(vec.x%1==0 and vec.y%1==0)
        self.position = vec
        self.on_load(mapping_func)

    
    def get_chunk_coordinates(self, vec: vec2d) -> vec2d:
        """
        global coordinates based on current chunk and coordinates
        """
        # a bit of branchless programming
        return vec2d(   x= self.__chunk_size*self.position.x+vec.x,

                        y = self.__chunk_size*self.position.y+vec.y
                    )
    
    def get_local_position(self, vec: vec2d):
        """
        gets chunk coordinates/key and local coordinates
        """

        vec2d(x=vec.x%self.__chunk_size ,y= vec.y%self.__chunk_size)
    
    def update(self):
        for object in list(itertools.chain(*self.internal_objects)):
            try:
                object.update()
            except AttributeError:
                pass

        

    def on_load(self, mapping_func):
        # I don't know if this function is here to stay
        # probably need to find a better way

        for x, obj_x in enumerate(self.internal_objects):
            for y, obj in enumerate(self.internal_objects):
                self.internal_objects[x][y] = mapping_func(x,y, self)

