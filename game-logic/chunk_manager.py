"""
System to dynamically load in and out chunks
"""
IMPORT_GRAPHICS_LIB = False
from prelude import *
from chunks_module import Chunk
import asyncio

def acending_range(a,b) -> range:
    if a > b:
        return range(int(b),int(a))
    else:
        return range(int(a),int(b))

class ChunkManager(GraphicsObject):

    # chunks are stored in a dictonary with keys as the chunk's x,y coordinates
    
    def __init__(self) -> None:
        super().__init__()
        self.__renderables = []
        self.__chunk_dict = dict()
    

    def add_chunk(self, chunk: Chunk) -> None:
        self.__chunk_dict.update({chunk.position: chunk})

    def set_renderables(self, bounds_min: vec2d, bounds_max: vec2d):
        #pos is the 0,0 value on the screen relative to the global position

        self.__renderables = []
        for x in acending_range(bounds_min.x,bounds_max.x):
            for y in acending_range(bounds_max.y,bounds_min.y):
                self.__renderables += [self.__chunk_dict[vec2d(x,y)]]
                
    def find_chunk(self, pos: vec2d, size: vec2d) -> Chunk:
        x_chunk_pos = pos.x // size.x
        y_chunk_pos = pos.y // size.y
        return self.__chunk_dict[vec2d(x_chunk_pos, y_chunk_pos)]
    
    async def update(self):
        await self.render()
    
    async def render(self):
        await asyncio.gather(*[renderable.update() for renderable in self.__renderables])
            

    #only for debug
    def set_all(self):
        self.__renderables = list(self.__chunk_dict.values())
