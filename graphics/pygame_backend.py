import logging
from dataclasses import dataclass
from typing import Any
import os
# import numpy as np

# hide the pygame support prompt
# the enviroment variable didn't work for me
# do support tho
import contextlib
with contextlib.redirect_stdout(None):
    import pygame
    from pygame.locals import *
import copy

@dataclass(slots= True)
class Image:
    image: pygame.Surface
    name: str

    def copy(self):
        return Image(image=self.image.copy(), name= copy.deepcopy(self.name))

class fallbackDict(dict):
    """
    Dictionary with a default fallback
    """
    fallback = None
    def __missing__(self, key):
        if self.fallback:
            return self.fallback
        else:
            raise TypeError(f"key: {key} does not exist, a fallback has not been set")
    
    def setFallback(self, fallback):
        """
        Set a fallback for a missing key. \n
        If none is set, a nonexistant key will throw an exception.
        """
        self.fallback = fallback

class PygameBackend:
    screen: pygame.Surface | None = None
    backend = "pygame"

    background = None

    camera = [0,0]

    @staticmethod
    def load_texture(name):
        fullname = os.path.join("../assets", name)
        try:
            image = pygame.image.load(fullname)
            # checks if rgba format is met, otherwise adds a channel
            if image.get_alpha() is None:
                image = image.convert()
            else:
                image = image.convert_alpha()
            return image
        except FileNotFoundError:
            logging.error(f"Cannot load image: {fullname}")
            return None
    

    @classmethod
    # the render loop
    def event_loop(cls, update_closure: Any) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return

            cls.screen.blit(cls.background, (0, 0))
            #the update closure (function) is passed by the GraphicsObject function
            update_closure(cls)
            logging.debug("Updated Frame")
            pygame.display.flip()
    
    @classmethod
    def init(cls, size, title):

        pygame.init()   
        cls.screen = pygame.display.set_mode(size)
        pygame.display.set_caption(title)

        #Fill Background
        cls.background = pygame.Surface(cls.screen.get_size())
        cls.background = cls.background.convert()
        cls.background.fill((250, 250, 250))