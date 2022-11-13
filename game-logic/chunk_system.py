from dataclasses import dataclass
from prelude import *


window.init((300,300),"test objects")


class Chunk(GraphicsObject):
    # all chunks are squares, and predefined sizes
    __chunk_size = 16
    # chunks are stored in a dictonary with keys as the chunk's x,y coordinates
    __chunk_dict = dict()

    # chunks have their own x,y coordinates, in the chunks there is another grid
    # this grid is the local coordinates of the individual tiles
    # get_global_coordinates() gets the global coordinates of the tile
    # get_local_coordinates() local coordinates of the tile
    # get_chunk() gets the chunk from a global coordinates

    def __init__(self, vec: vec2d) -> None:
        # chunks do not get immediately added to the objects list, but get loaded in 
        # dynamicaly depending on the players coordinates
        self.internal_objects = [[None]*self.__chunk_size]*self.__chunk_size
        assert(vec.x%1==0 and vec.y%1==0)
        self.__chunk_dict.update({vec: self})
        self.position = vec

    
    def get_global_coordinates(self, vec: vec2d) -> vec2d:
        """
        global coordinates based on current chunk and coordinates
        """
        # a bit of branchless programming
        return vec2d(   x= (vec.x>0)*(
                                self.__chunk_size*self.position.x + vec.x)
                                +
                            (vec.x<0)*(
                                self.__chunk_size*self.position.x - vec.x),

                        y = (vec.y>0)*(
                                self.__chunk_size*self.position.x + vec.y)
                            +
                            (vec.y<0)*(
                                self.__chunk_size*self.position.x - vec.y)
                    )
    
    def get_local_position(self, vec: vec2d):
        """
        gets chunk coordinates/key and local coordinates
        """

        vec2d(x=vec.x%self.__chunk_size ,y= vec.y%self.__chunk_size)


