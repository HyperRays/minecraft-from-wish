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
    
    def __neg__(self):
        return vec2d(-self.x,-self.y)
    
    def dot(self, other):
        return self.x*other.x+self.y*other.y
    
    def into_vec3d(self):
        return vec3d(self.x, self.y, 0)
    
    #https://www.khanacademy.org/computing/computer-programming/programming-natural-simulations/programming-vectors/a/vector-magnitude-normalization
    #magnitude
    def mag(self):
        return (self.x*self.x+self.y*self.y)**(0.5)

    def normalize(self):
        mag = self.mag()
        return vec2d(self.x/mag, self.y/mag)


@dataclass(slots=True, unsafe_hash=True)
class vec3d:
    x: int
    y: int
    z: int

    def __add__(self, other):
        return vec3d(self.x+other.x, self.y+other.y, self.z+other.z)
    
    def __sub__(self, other):
        return vec3d(self.x-other.x, self.y-other.y, self.z+other.z)
    
    def __neg__(self):
        return vec3d(-self.x,-self.y,-self.z)
    
    def dot(self, other):
        return self.x*other.x+self.y*other.y+self.z*other.z
    
    #https://www.mathsisfun.com/algebra/vectors-cross-product.html
    def cross(self, other):
        cx = self.y*other.z - self.z*other.y
        cy = self.z*other.x - self.x*other.z
        cz = self.x*other.y - self.y*other.x

        return vec3d(cx, cy, cz)
    
    def trunc_z(self) -> vec2d:
        return vec2d(self.x, self.y)

    
    

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
