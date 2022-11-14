import os
import logging
from typing import Any
from pygame_backend import PygameBackend, Image


class GraphicsObject(PygameBackend):
    objects = list()
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

        super(GraphicsObject, cls).init(size,title)
        logging.info(f"successfully created window")
    
    def update_callback_pygame(self) -> None:
        for object in self.objects:
            object.update()

    @classmethod
    def add_texture(cls, name: str) -> int:
        """
        load in texture, and return the id
        """
        cls.textures += [Image(image=cls.load_texture(name), name=name)]
        return len(cls.textures)-1

    @classmethod
    def run(cls) -> None:
        match cls.backend:
            case "pygame":
                callback_fn = cls.update_callback_pygame
            case unimpl_backend:
                raise NotImplementedError(f"The backend {unimpl_backend} has not been implemented yet")
        cls.event_loop(callback_fn)

    #placeholder update fn
    #runs every renderpass/flip
    def update(*_): ...
