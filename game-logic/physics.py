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
    


#https://www.youtube.com/watch?v=ajv46BSqcK4&t=468s
#--- GJK Algorithm ---#

def passes_origin(point1: vec2d, dir: vec2d) -> bool:
    return dir.dot(point1) >= 0

def normal_dir_origin(A: vec2d, B: vec2d) -> vec2d:
    vecAB = B-A
    #O: Null Vector at origin
    vecAO = vec2d(0,0)-A
    
    #vector AB/AO with z value 0
    vec3AB = vecAB.into_vec3d()
    vec3AO = vecAO.into_vec3d()

    #triple cross product and then truncate the z value (should be 0)
    #(AB x AO) x AB
    return vec3AB.cross(vec3AO).cross(vec3AB).trunc_z()

def triangle_contains_origin(A: vec2d, B: vec2d, C: vec2d) -> tuple[bool, vec2d | None]:

    vecAB = B-A
    vecAC = C-A

    vecAO = vec2d(0,0)-A
    
    vec3AB = vecAB.into_vec3d()
    vec3AC = vecAC.into_vec3d()

    dcross1 = vec3AC.cross(vec3AB).cross(vec3AB).trunc_z()
    dcross2 = vec3AB.cross(vec3AB).cross(vec3AB).trunc_z()

    dot1 = dcross1.dot(vecAO)
    dot2 = dcross2.dot(vecAO)

    match (dot1 <= 0,dot2 <= 0):
        case (True,True):
            return (True, None)
        case (True, False):
            return (False, dot2)
        case (False, True):
            return (False, dot1)

def mink_diff(shape1: Shape, shape2: Shape, dir) -> vec2d:
    return shape1.furthest_in_dir(dir) - shape2.furthest_in_dir(-dir)

def intersect(shape1: Shape, shape2: Shape) -> bool:
    
    dir = vec2d(0,1)
    tri_points = []

    mink_point = mink_diff(shape1, shape2, dir)
    tri_points.append(mink_point)
    del dir

    vec_to_origin = vec2d(0,0) - mink_point
    mink_point = mink_diff(shape1, shape2, vec_to_origin)
    

    if not passes_origin(mink_point, vec_to_origin):
        return False
    
    tri_points.append(mink_point)
    del vec_to_origin
    
    norm_to_origin = normal_dir_origin(tri_points[0], tri_points[1])
    mink_point = mink_diff(shape1, shape2, norm_to_origin)

    if not passes_origin(mink_point, norm_to_origin):
        return False

    tri_points.append(mink_point)
    del norm_to_origin

    dir = None

    while True:
        passed,new_dir = triangle_contains_origin(tri_points[0], tri_points[1], tri_points[2])
        if passed:
            return True
        else:
            dir = new_dir
            tri_points.pop(0)
            mink_point = mink_diff(shape1, shape2, dir)

            if not passes_origin(mink_point, dir):
                return False
            
            else: 
                tri_points.append(mink_point)
 
        