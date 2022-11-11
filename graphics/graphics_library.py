import os
from typing import Any
import logging
from dataclasses import dataclass
import pygame
from pygame.locals import *

@dataclass
class Image:
    __slots__ = ("image", "name")
    image: Any
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
    screen: Any|None = None
    backend = "pygame"

    @staticmethod
    def load_texture(name):
        # currently works only for pngs
        fullname = os.path.join("../assets", name)
        try:
            image = pygame.image.load(fullname)
            if image.get_alpha() is None:
                image = image.convert()
            else:
                image = image.convert_alpha()
        except FileNotFoundError:
            print(f"Cannot load image: {fullname}")
            raise SystemExit
        return image, image.get_rect()
    

    @classmethod
    def event_loop(cls, update_closure: Any) -> None:
        update_closure()


class GraphicsObject(PygameBackend):
    objects: list[Any] = list()
    textures: list[Image] = list()

    def __init__(self) -> None:
        self.objects += [self]

    @classmethod
    def init(cls, size: tuple[float,float], title: str) -> None:
        """
        Initialize the screen with given parameters
        """

        cls.size = size
        logging.info(f"creating window with size (height:{size[0]}, width:{size[1]})")

        pygame.init()   
        cls.screen = pygame.display.set_mode(size)
        pygame.display.set_caption(title)

        logging.info(f"successfully created window")

        # Fill background
        background = pygame.Surface(cls.screen.get_size())
        background = background.convert()
        background.fill((250, 250, 250))
    
    def update_callback_pygame(self) -> None:
        for object in self.objects:
            object.update()

    @classmethod
    def run(cls) -> None:
        match cls.backend:
            case ["pygame"]:
                callback_fn = cls.update_callback_pygame
            case unimpl_backend:
                raise NotImplementedError(f"The backend {unimpl_backend} has not been implemented yet")
        cls.event_loop(callback_fn)