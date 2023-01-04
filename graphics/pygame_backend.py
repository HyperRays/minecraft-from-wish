"""
this file is the pygame version of the backend
"""
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
    
    def reset(self, new_target_time = None) -> None:
        self.total_time = self.total_time - self.target_time
        if new_target_time != None:
            self.target_time = new_target_time
            
class PygameBackend:
    screen: pygame.Surface | None = None
    size: tuple[float, float] | None = None
    backend = "pygame"

    layers: dict[str,pygame.Surface] = dict()
    render_order: list = []
    background = None

    characters = {'a': 97, 'b': 98, 'c': 99, 'd': 100, 'e': 101, 'f': 102, 'g': 103, 'h': 104, 'i': 105, 'j': 106, 'k': 107, 'l': 108, 'm': 109, 'n': 110, 'o': 111, 'p': 112, 'q': 113, 'r': 114, 's': 115, 't': 116, 'u': 117, 'v': 118, 'w': 119, 'x': 120, 'y': 121, 'z': 122, '1': 49, '2': 50, '3': 51, '4': 52, '5': 53, '6': 54, '7': 55, '8': 56, '9': 57, '0': 48, 'escape': 27, 'tab': 9, 'left shift': 1073742049, 'right shift': 1073742053, 'return': 13, 'backspace': 8, 'space': 32, 'up': 1073741906, 'down': 1073741905, 'left': 1073741904, 'right': 1073741903, '.': 46, ',': 44, ';': 59, ':': 58, '-': 45, '_': 95, '?': 63, "'": 39, '!': 33, '&': 38, '/': 47, '(': 40, ')': 41, '=': 61, '+': 43, '|': 124, '"': 34, '*': 42, '#': 35, '[': 91, ']': 93, '\\': 92, '{': 123, '}': 125}

    @staticmethod
    def load_texture(path):
        fullname = os.path.join("../assets/images", path)
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
    async def event_loop(cls, update_closure: Any, input_closure: Any, render_closure: Any) -> None:
        sync = _Timed(1_000_000_000/60)
        clock = pygame.time.Clock()
        while True:
            # sync.poll()
            # clock.tick_busy_loop()
            keys = pygame.key.get_pressed()
            pygame.event.poll()
            for event in pygame.event.get():
                if event.type == QUIT:
                    return

            cls.screen.blit(cls.background, (0, 0))
            # the update closure (function) is passed by the GraphicsObject function
            await asyncio.gather(input_closure(cls, keys), update_closure(cls))
            await render_closure(cls)
            for order in cls.render_order:
                if order in cls.layers:
                    cls.screen.blit(cls.layers[order], (0,0))
                    cls.layers[order].fill((0,0,0,0))
            pygame.display.update()
            # if sync.reached():
            #     logging.debug(f"Updated Frame")
            #     pygame.display.update()
            #     if (fps := clock.get_fps()) != 0:
            #         sync.reset(new_target_time=1_000_000_000/fps)
            #     else:
            #         sync.reset()

    @classmethod
    def init(cls, size: tuple[float, float], title: str, fullscreen = False):

        pygame.init()   
        cls.screen = pygame.display.set_mode(size, DOUBLEBUF, 64)
        pygame.event.set_allowed([QUIT, pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d])
        cls.size = size
        pygame.display.set_caption(title)

        #Fill Background
        cls.background = pygame.Surface(size)
        cls.background = cls.background.convert()
        #this is temporary, we will have a bg class
        cls.background.fill((255,255,255))
        
    
    @classmethod
    def create_layer(cls, layer_name: str):
        cls.layers[layer_name] = cls.create_empty_texture(cls.size)

    @classmethod
    def set_render_layers(cls, render_layers: list):
        cls.render_order = render_layers
    
    @staticmethod 
    def create_empty_texture(size) -> pygame.surface.Surface:
        surface = pygame.surface.Surface(size).convert_alpha()
        surface.fill((0,0,0,0))
        return surface