import os
from typing import Any
import logging
from dataclasses import dataclass
import numpy as np
import pygame
from pygame.locals import *

@dataclass(slots= True)
class Image:
    image: pygame.Surface
    name: str

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

    @staticmethod
    def load_texture(name):
        # currently works only for pngs
        fullname = os.path.join("../assets", name)
        try:
            image = pygame.image.load(fullname)
            # checks if rgba format is met, otherwise adds a channel
            if image.get_alpha() is None:
                image = image.convert()
            else:
                image = image.convert_alpha()
        except FileNotFoundError:
            logging.error(f"Cannot load image: {fullname}")
        return image
    

    @classmethod
    def event_loop(cls, update_closure: Any) -> None:
        update_closure()
    
    @classmethod
    def init(cls, size, title):
        pygame.init()   
        cls.screen = pygame.display.set_mode(size)
        pygame.display.set_caption(title)


class GraphicsObject(PygameBackend):
    objects = np.array(object = [], dtype = object)
    texturess = np.array(object = [], dtype = object)

    def __init__(self) -> None:
        self.objects = np.append(self.objects, [self])

    @classmethod
    def init(cls, size: tuple[float,float], title: str) -> None:
        """
        Initialize the screen with given parameters
        """

        cls.size = size
        logging.info(f"creating window with size (height:{size[0]}, width:{size[1]})")

        super(GraphicsObject, cls).init(size,title)
        logging.info(f"successfully created window")

        # Fill background
        background = pygame.Surface(cls.screen.get_size())
        background = background.convert()
        background.fill((250, 250, 250))
    
    def update_callback_pygame(self) -> None:
        for object in self.objects:
            object.update()

    @classmethod
    def add_texture(cls, name) -> int:
        """
        load in texture, and return the id
        """
        cls.textures = np.append(cls.textures, [Image(image=cls.load_texture(name), name=name)])
        return len(cls.textures)-1

    @classmethod
    def run(cls) -> None:
        match cls.backend:
            case ["pygame"]:
                callback_fn = cls.update_callback_pygame
            case unimpl_backend:
                raise NotImplementedError(f"The backend {unimpl_backend} has not been implemented yet")
        cls.event_loop(callback_fn)

