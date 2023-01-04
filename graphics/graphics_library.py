"""
This file acts like a compatibility layer between any chosen backend.
Currently there is only one (pygame) but the plan is to expand this and make it possible/somewhat resonable.
"""

import os
import logging
from typing import Any
from pygame_backend import PygameBackend
import asyncio

class GraphicsObject(PygameBackend):
    objects = list()
    textures: list = list()

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
    
    async def update_callback_pygame(self):
        await asyncio.gather(*[object.update() for object in self.objects])
           
    
    async def input_callback_pygame(self, keys):
        await asyncio.gather(*[object.input(keys) for object in self.objects])
    
    async def render_callback_pygame(self):
        await asyncio.gather(*[object.render() for object in self.objects])

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
                update_callback_fn = cls.update_callback_pygame
                input_callback_fn = cls.input_callback_pygame
                render_callback_fn = cls.render_callback_pygame
            case unimpl_backend:
                raise NotImplementedError(f"The backend {unimpl_backend} has not been implemented yet")
        
        loop = asyncio.new_event_loop()
        loop.run_until_complete(cls.event_loop(update_callback_fn, input_callback_fn, render_callback_fn))

    #placeholder update fn
    #runs every renderpass/flip
    async def update(*_): pass

    async def input(*_): pass

    async def render(*_): pass