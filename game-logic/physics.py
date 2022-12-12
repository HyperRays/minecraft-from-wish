IMPORT_GRAPHICS_LIB = False
from prelude import *

#https://en.wikipedia.org/wiki/Linear_interpolation
def lerp(v0: int, v1: vec2d, t: int):
    return (1 - t) * v0 + t * v1


#https://www.youtube.com/watch?v=ajv46BSqcK4
#--- GJK Algorithm ---#

def passes_origin(point1: vec2d, dir: vec2d) -> bool:
    return dir.dot(point1) >= 0

def normal_dir_origin(A: vec2d, B: vec2d) -> vec2d:
    vecAB = B-A
    # O: Null Vector at origin
    # O-A = -A
    vecAO = -A
    
    #vector AB/AO with z value 0
    vec3AB = vecAB.into_vec3d()
    vec3AO = vecAO.into_vec3d()

    #triple cross product and then truncate the z value (z should be 0)
    #(AB x AO) x AB
    return vec3AB.cross(vec3AO).cross(vec3AB).trunc_z()

def triangle_contains_origin(A: vec2d, B: vec2d, C: vec2d) -> tuple[bool, vec2d | None]:

    vecAB = B-A
    vecAC = C-A

    vecAO = -A
    
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

def _intersect_only_check(shape1: Shape, shape2: Shape) -> bool:
    
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
 

#--- END GJK Algorithm ---#



#https://dyn4j.org/2010/04/gjk-distance-closest-points/
#--- Distance GJK version ---#

#closest point on line to origin
def closest_point_on_line(A: vec2d, B: vec2d):

    #vector projection AO on AB to find vector to closest point
    #https://en.wikipedia.org/wiki/Vector_projection

    vecAB = B-A
    vecAO = -A
    
    proj = vecAO.dot(vecAB)
    sq = vecAO.dot(vecAO)

    
    t = proj / sq
    closest_point = (vecAB * t) + A

    return closest_point.mag()

def _intersect_with_dist(shape1: Shape, shape2: Shape) -> tuple[bool, vec2d]:
    
    dir = vec2d(0,1)
    tri_points = []

    mink_point = mink_diff(shape1, shape2, dir)
    tri_points.append(mink_point)
    del dir

    vec_to_origin = vec2d(0,0) - mink_point
    mink_point = mink_diff(shape1, shape2, vec_to_origin)
    

    if not passes_origin(mink_point, vec_to_origin):
        return (False, closest_point_on_line(tri_points[0],mink_point))
    
    tri_points.append(mink_point)
    del vec_to_origin
    
    norm_to_origin = normal_dir_origin(tri_points[0], tri_points[1])
    mink_point = mink_diff(shape1, shape2, norm_to_origin)

    if not passes_origin(mink_point, norm_to_origin):
        return (False, closest_point_on_line(tri_points[1],mink_point))

    tri_points.append(mink_point)
    del norm_to_origin

    dir = None

    while True:
        passed,new_dir = triangle_contains_origin(tri_points[0], tri_points[1], tri_points[2])
        if passed:
            return (True, closest_point_on_line(tri_points[1],tri_points[2]))
        else:
            dir = new_dir
            tri_points.pop(0)
            mink_point = mink_diff(shape1, shape2, dir)

            if not passes_origin(mink_point, dir):
                return (False, closest_point_on_line(tri_points[2], mink_point))
            
            else: 
                tri_points.append(mink_point)
 



# "overload" the different GJK versions
def intersect(shape1: Shape, shape2: Shape, dist=None):
    if dist != None:
        return _intersect_with_dist(shape1, shape2)
    else:
        return _intersect_only_check(shape1, shape2)