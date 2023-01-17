"""
A class for the background, the idea is to expand this to make dynamically moving objects
"""

from prelude import *
from helper_functions import clamp
from math import pi,sin

_TIME_IN_NS = DAY_NIGHT_CYCLE_TIME_MIN*60_000_000_000*2
_timer = Timed(_TIME_IN_NS)

MAX_DARKNESS = 210

class Background(GraphicsObject):
    def __init__(self) -> None:
        super().__init__()
    
    async def render(self):
        # graphics.layers["bg"].fill((255,255,255,255))
        graphics.layers["bg"].fill((212, 234, 255, 255))

class DayCycle(GraphicsObject):
    
    def __init__(self) -> None:
        super().__init__()
    
    async def render(self):
        graphics.layers["day-night-overlay"].fill((0,0,0,sin(lerp(0,pi,(_timer.total_time/_TIME_IN_NS)))**(2<<5)*MAX_DARKNESS))
        # graphics.layers["bg"].fill((0,0,0,clamp(abs(sin(lerp(0,pi,(_timer.total_time/_TIME_IN_NS))))*MAX_DARKNESS,0,255)), special_flags=BLEND_RGBA_SUB)

    async def update(*_):
        _timer.poll()