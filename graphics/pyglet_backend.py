import asyncio
import os
from typing import Any
import pyglet

def __event_loop(window: pyglet.window.Window, cls, update_closure: Any, input_closure: Any, render_closure: Any):
    loop = asyncio.get_event_loop()
    @window.event
    def on_draw():
        loop.run_until_complete(update_closure(cls))
        loop.run_until_complete(render_closure(cls))
        window.clear()
    
    @window.event
    def on_key_press(symbol, modifiers):
        loop.run_until_complete(input_closure(cls, symbol))
    
    pyglet.app.run()

class PygletBackend:
    backend = "pyglet"
    window: pyglet.window.Window | None = None
    size: tuple[float, float] | None = None

    @staticmethod
    def load_texture(path):
        fullname = os.path.join("../assets/images", path)
        fullname = os.path.join("../assets/images", path)
        return pyglet.image.load(fullname)

    @classmethod
    def init(cls, size: tuple[float, float], title: str):

        cls.window = pyglet.window.Window(size[0], size[1], title)
        cls.size = size
