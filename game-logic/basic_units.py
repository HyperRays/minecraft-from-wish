"""
File for basic units
"""

import time
from dataclasses import dataclass
@dataclass(slots=True, unsafe_hash=True)
class vec2d:
    x: int
    y: int

    def __add__(self, other):
        return vec2d(self.x+other.x, self.y+other.y)
    
    def __sub__(self, other):
        return vec2d(self.x-other.x, self.y-other.y)
    

class Timed:
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
        self.total_time = 0
