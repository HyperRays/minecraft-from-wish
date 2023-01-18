"""
System to dynamically load in and out chunks
"""
IMPORT_GRAPHICS_LIB = False
import pickle
from prelude import *
from chunks_module import Chunk
import asyncio

def acending_range(a,b) -> range:
    if a > b:
        return range(int(b),int(a))
    else:
        return range(int(a),int(b))

class ChunkManager(GraphicsObject):

    chunks_layer = "chunks_layer"
    chunks_debug_layer = "chunks_debug"
    # chunks are stored in a dictonary with keys as the chunk's x,y coordinates
    # the chunk at the origin has x,y values 0,0, one to the right 1,0 one above 0,1 and vice-versa
    
    def __init__(self) -> None:
        super().__init__()
        self._renderables = []
        self._updateables = []
        self._chunk_dict: dict[vec2d, Chunk] = dict()
        graphics.create_layer(self.chunks_layer)
        graphics.create_layer(self.chunks_debug_layer)

    def chunk_exists(self, pos: vec2d) -> bool:
        return pos in self._chunk_dict
    
    def add_chunk(self, chunk: Chunk) -> None:
        self._chunk_dict.update({chunk.position: chunk})

    def set_renderables(self, bounds_min: vec2d, bounds_max: vec2d, terrain_gen_fn: any = None):
        #pos is the 0,0 value on the screen relative to the global position

        self._renderables = []
        for x in acending_range(bounds_min.x,bounds_max.x):
            for y in acending_range(bounds_max.y,bounds_min.y):
                pos = vec2d(x,y)
                if pos in self._chunk_dict:
                    self._renderables += [self._chunk_dict[pos]]
                else:
                    pass
                    self.add_chunk(Chunk(pos, terrain_gen_fn))
                    self._renderables += [self._chunk_dict[pos]]
    
    def set_updateables(self, bounds_min: vec2d, bounds_max: vec2d, terrain_gen_fn: any = None):

        self._updateables = []
        for x in acending_range(bounds_min.x,bounds_max.x):
            for y in acending_range(bounds_max.y,bounds_min.y):
                pos = vec2d(x,y)
                if pos in self._chunk_dict:
                    self._updateables += [self._chunk_dict[pos]]
                else:
                    pass
                    self.add_chunk(Chunk(pos, terrain_gen_fn))
                    self._updateables += [self._chunk_dict[pos]]
                
    def find_chunk_pos(self, pos: vec2d, size: vec2d) -> vec2d:
        x_chunk_pos = pos.x // size.x
        y_chunk_pos = pos.y // size.y
        return vec2d(x_chunk_pos, y_chunk_pos)
    
    def get_chunk(self, pos: vec2d) -> Chunk:
        return self._chunk_dict[pos]

    async def update(self):
        await asyncio.gather(*[updateable.update() for updateable in self._updateables])
    
    async def render(self):
        await asyncio.gather(*[renderable.render() for renderable in self._renderables])
            
    def get_layer(self):
        return self.layers[self.chunks_layer]
    
    def get_debug_layer(self):
        return self.layers[self.chunks_debug_layer]

    #only for debug
    def set_all(self):
        self._renderables = list(self._chunk_dict.values())
    
    def save(self, path):
        _chunk_dict_save = dict((key,item.save()) for (key,item) in self._chunk_dict.items())
        # pringt amount of blocks saved
        print(len(_chunk_dict_save)*16*16)
        with open(path, "wb") as f:
            pickle.dump(_chunk_dict_save, f, protocol=pickle.HIGHEST_PROTOCOL)

    def redefine(self, other):
        self._chunk_dict = other._chunk_dict 
        self._renderables = []

    @classmethod
    def load(cls, path: str):

        self = cls.__new__(cls)
        with open(path, "rb") as f:
            _chunk_dict_save: dict[vec2d, Chunk] = pickle.load(f)
        self._chunk_dict = dict((key,Chunk.load(item)) for (key,item) in _chunk_dict_save.items())
        self._renderables = []

        return self

