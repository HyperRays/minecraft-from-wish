IMPORT_GRAPHICS_LIB = False
from prelude import *
from dataclasses import dataclass

class Shape:
    def furthest_in_dir(self, dir: vec2d) -> vec2d: ...

@dataclass
class Simplex2d(Shape): 
    a: vec2d
    b: vec2d
    c: vec2d

    def furthest_in_dir(self, dir: vec2d) -> vec2d:
        
        a_dot = dir.dot(self.a)
        b_dot = dir.dot(self.b)
        c_dot = dir.dot(self.c)

        #https://stackoverflow.com/a/11825864

        values = [a_dot, b_dot, c_dot]
        index_max = max(range(len(values)), key=values.__getitem__)

        match index_max:
            case 0: return self.a
            case 1: return self.b
            case 2: return self.c

@dataclass
class Quad(Shape): 
    a: vec2d
    b: vec2d
    c: vec2d
    d: vec2d

    def furthest_in_dir(self, dir: vec2d) -> vec2d:
        
        a_dot = dir.dot(self.a)
        b_dot = dir.dot(self.b)
        c_dot = dir.dot(self.c)
        d_dot = dir.dot(self.d)

        #https://stackoverflow.com/a/11825864

        values = [a_dot, b_dot, c_dot, d_dot]
        index_max = max(range(len(values)), key=values.__getitem__)

        match index_max:
            case 0: return self.a
            case 1: return self.b
            case 2: return self.c
            case 3: return self.d