"""
File for basic units
"""
from math import sqrt
import time
from dataclasses import dataclass


@dataclass(slots=True, unsafe_hash=True)
class vec2d:
    x: float
    y: float

    def __add__(self, other):
        return vec2d(self.x+other.x, self.y+other.y)
    
    def __sub__(self, other):
        return vec2d(self.x-other.x, self.y-other.y)
    
    def __mul__(self, other):
        return vec2d(self.x*other, self.y*other)

    def __truediv__(self, other):
        return vec2d(self.x/other, self.y/other)
    
    def __neg__(self):
        return vec2d(-self.x,-self.y)
    
    #https://www.mathsisfun.com/algebra/vectors-dot-product.html
    def dot(self, other):
        return self.x*other.x+self.y*other.y
    
    def into_vec3d(self):
        return vec3d(self.x, self.y, 0)
    
    #https://www.khanacademy.org/computing/computer-programming/programming-natural-simulations/programming-vectors/a/vector-magnitude-normalization
    #magnitude
    def mag(self):
        return sqrt(self.x*self.x+self.y*self.y)

    def normalize(self):
        mag = self.mag()
        return vec2d(self.x/mag, self.y/mag)
    
    def into_tuple(self) -> tuple:
        return (self.x, self.y)
    


@dataclass(slots=True, unsafe_hash=True)
class vec3d:
    x: float
    y: float
    z: float

    def __add__(self, other):
        return vec3d(self.x+other.x, self.y+other.y, self.z+other.z)
    
    def __sub__(self, other):
        return vec3d(self.x-other.x, self.y-other.y, self.z+other.z)
    
    def __neg__(self):
        return vec3d(-self.x,-self.y,-self.z)
    
    def __mul__(self, other):
        return vec3d(self.x*other, self.y*other, self.z*other)

    def __truediv__(self, other):
        return vec3d(self.x/other, self.y/other, self.z/other)
    
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
    
    def into_tuple(self) -> tuple:
        return (self.x, self.y, self.y)
    
    

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
    
    def reset(self, new_target_ns=None) -> None:
        self.total_time = self.total_time - self.target_time
        if new_target_ns != None:
            self.target_time = new_target_ns
        


#colored output (print)
# https://stackoverflow.com/a/287944
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#https://stackoverflow.com/questions/14822184/is-there-a-ceiling-equivalent-of-operator-in-python
def ceildiv(a, b):
    return -(a // -b)
