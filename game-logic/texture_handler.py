"""
This class handles all the image loading from the assets folder, as well as image serving.
The purpose of this class is to maintain persistence between world loads and saves, 
since saving surfaces is not possible due to them being behind ffi bindings.
"""

import pickle
from prelude import *
class TextureHandler:

    __pickle_dict = dict()
    __texture_dict = dict()
    
    def load_texture(self, name: str, path: str):
        self.__pickle_dict.update({name: path})
        self.__texture_dict.update({name: GraphicsObject.load_texture(path)})

    def unload_texture(self, name):
        del self.__pickle_dict[name]
        del self.__texture_dict[name]

    def save(self):
        return pickle.dumps(self.__pickle_dict)
    
    @classmethod
    def load(cls, b: bytes):
        self = cls.__new__(cls)
        self.__pickle_dict: dict[str, str] = pickle.loads(b)
        for key,value in self.__pickle_dict.items():
            self.load_texture(key, value)

        return self
    
    def get_texture(self, name) -> pygame.Surface:
        return self.__texture_dict[name]

    # rescale the image to required size
    def rescale_image(self, name, height = None, width = None, factor = None) -> tuple[int, int]: 
        texture = self.get_texture(name)
        w,h, self.__texture_dict[name] = graphics._rescale_image(texture, height, width, factor)
        return w,h

