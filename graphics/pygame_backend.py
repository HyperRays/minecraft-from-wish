import logging
from dataclasses import dataclass
from typing import Any
import os
import time
# hide the pygame support prompt
# the enviroment variable didn't work for me
# do support tho
import contextlib
with contextlib.redirect_stdout(None):
    import pygame
    from pygame.locals import *
    
import copy

import asyncio
class _Timed:
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
        self.total_time = self.total_time - self.target_time

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

    characters = {'a': 97, 'b': 98, 'c': 99, 'd': 100, 'e': 101, 'f': 102, 'g': 103, 'h': 104, 'i': 105, 'j': 106, 'k': 107, 'l': 108, 'm': 109, 'n': 110, 'o': 111, 'p': 112, 'q': 113, 'r': 114, 's': 115, 't': 116, 'u': 117, 'v': 118, 'w': 119, 'x': 120, 'y': 121, 'z': 122, '1': 49, '2': 50, '3': 51, '4': 52, '5': 53, '6': 54, '7': 55, '8': 56, '9': 57, '0': 48, 'escape': 27, 'tab': 9, 'left shift': 1073742049, 'right shift': 1073742053, 'return': 13, 'backspace': 8, 'space': 32, 'up': 1073741906, 'down': 1073741905, 'left': 1073741904, 'right': 1073741903, '.': 46, ',': 44, ';': 59, ':': 58, '-': 45, '_': 95, '?': 63, "'": 39, '!': 33, '&': 38, '/': 47, '(': 40, ')': 41, '=': 61, '+': 43, '|': 124, '"': 34, '*': 42, '#': 35, '[': 91, ']': 93, '\\': 92, '{': 123, '}': 125}

    @staticmethod
    def load_texture(name):
        fullname = os.path.join("../assets/images", name)
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
    async def event_loop(cls, update_closure: Any, input_closure: Any) -> None:
        timer = _Timed(16_000_000)
        while True:
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == QUIT:
                    return

            cls.screen.blit(cls.background, (0, 0))
            # the update closure (function) is passed by the GraphicsObject function
            await input_closure(cls, keys)
            await update_closure(cls)
            logging.debug(f"Updated Frame")
            pygame.display.update()

    @classmethod
    def init(cls, size, title):

        pygame.init()   
        cls.screen = pygame.display.set_mode(size, flags= SCALED, vsync= 1)
        pygame.display.set_caption(title)

        #Fill Background
        cls.background = pygame.Surface(cls.screen.get_size())
        cls.background = cls.background.convert()
        cls.background.fill((250, 250, 250))