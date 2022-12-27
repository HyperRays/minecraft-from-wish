IMPORT_GRAPHICS_LIB = False
import enum
from prelude import *

#https://en.wikipedia.org/wiki/Linear_interpolation
def lerp(v0, v1, t: int):
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

#https://blackpawn.com/texts/pointinpoly/
def triangle_contains_origin(A: vec2d, B: vec2d, C: vec2d) -> tuple[bool, vec2d | None]:

    v0 = C - A
    v1 = B - A
    # P = (0,0)
    v2 =  -A

    dot00 = v0.dot(v0)
    dot01 = v0.dot(v1)
    dot02 = v0.dot(v2)
    dot11 = v1.dot(v1)
    dot12 = v1.dot(v2)

    try:
        invDenom = 1 / (dot00 * dot11 - dot01 * dot01)
        u = (dot11 * dot02 - dot01 * dot12) * invDenom
        v = (dot00 * dot12 - dot01 * dot02) * invDenom
    except:
        u = 0
        v = 0

    match (u >= 0) and (v >= 0) and (u + v < 1):
        case True:
            return (True, None)
        case False:
            return (False, normal_dir_origin(B,C))

def mink_diff(shape1: Shape, shape2: Shape, dir, return_support_points = None) -> vec2d:
    if return_support_points != None:
        return (s1 := shape1.furthest_in_dir(dir)) - (s2 := shape2.furthest_in_dir(-dir)) , (s1,s2)
    else:
        return shape1.furthest_in_dir(dir) - shape2.furthest_in_dir(-dir)

def _intersect_only_check(shape1: Shape, shape2: Shape) -> bool:
    
    dir = vec2d(0,1)
    tri_points: list[vec2d] = []

    mink_point = mink_diff(shape1, shape2, dir)
    tri_points.append(mink_point)
    del dir

    vec_to_origin = vec2d(0,0) - mink_point
    mink_point = mink_diff(shape1, shape2, vec_to_origin)

    if not passes_origin(mink_point, vec_to_origin):
        return False
    
    tri_points.append(mink_point)
    del vec_to_origin
    
    norm_to_origin = normal_dir_origin(tri_points[1],tri_points[0])
    mink_point = mink_diff(shape1, shape2, norm_to_origin)

    if not passes_origin(mink_point, norm_to_origin):
        return False

    tri_points.append(mink_point)
    del norm_to_origin

    iterations = 10
    for _ in range(iterations):
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

        return False
 
#currently broken
#--- END GJK Algorithm ---#


shift = vec2d(300,300)

#https://dyn4j.org/2010/04/gjk-distance-closest-points/
#--- Distance GJK version ---#

#closest point on line to origin
def closest_point_on_line(A: vec2d, B: vec2d):

    #vector projection AO on AB to find vector to closest point
    #https://en.wikipedia.org/wiki/Vector_projection

    pygame.draw.circle(window.screen, (0,0,255), (A+shift).into_tuple(), 4)
    pygame.draw.circle(window.screen, (0,255,0), (B+shift).into_tuple(), 4)

    vecAB = B-A
    vecAO = -A
    
    proj = vecAO.dot(vecAB)
    sq = vecAO.dot(vecAO)
    
    if sq == 0:
        t = 0
    else:
        t = 1 - (proj / sq)
        if t < 0:
            t = 0
        elif t > 1:
            t = 1

    closest_point = (vecAB * t) + A

    return closest_point

shift = vec2d(250, 250)

def _intersect_with_dist(shape1: Shape, shape2: Shape) -> tuple[bool, vec2d]:
    
    does_not_intersect = False
    dir = vec2d(0,1)
    tri_points: list[vec2d] = []

    mink_point = mink_diff(shape1, shape2, dir)
    tri_points.append(mink_point)
    del dir

    vec_to_origin = vec2d(0,0) - mink_point
    mink_point = mink_diff(shape1, shape2, vec_to_origin)
    

    if not passes_origin(mink_point, vec_to_origin):
        does_not_intersect = True
    
    tri_points.append(mink_point)
    del vec_to_origin
    
    norm_to_origin = normal_dir_origin(tri_points[0], tri_points[1])
    mink_point = mink_diff(shape1, shape2, norm_to_origin)

    if not passes_origin(mink_point, norm_to_origin):
        does_not_intersect = True

    tri_points.append(mink_point)
    del norm_to_origin

    dir = None

    iterations = 10
    for _ in range(iterations):
        passed,new_dir = triangle_contains_origin(tri_points[0], tri_points[1], tri_points[2])
        if passed:
            return (not (False or does_not_intersect), closest_point_on_line(tri_points[1],tri_points[2]).mag())
        else:
            dir = new_dir
            prev_p = tri_points.pop(0)
            mink_point = mink_diff(shape1, shape2, dir)

            if not passes_origin(mink_point, dir):
                return (False, closest_point_on_line(prev_p , mink_point).mag())
            
            else: 
                tri_points.append(mink_point)
        
    return (False, closest_point_on_line(tri_points[1],tri_points[2]).mag())
 
#--- END Distance GJK version ---#


#---- Closest points GJK version ---#

def closest_points_on_shapes(pshape1: tuple[vec2d, vec2d], pshape2: tuple[vec2d, vec2d], l: vec2d, a: vec2d) -> tuple[vec2d, vec2d]:

    # pshape is organized like this:
    # pshape1 = (a.shape1, a.shape2)
    # pshape2 = (b.shape1, b.shape2)

    ldotl = l.dot(l)
    if (ldotl == 0):
        return pshape1
    ldota = l.dot(a)

    lambda2 = -(ldota/ldotl)
    lambda1 = 1 - lambda2

    if (lambda1 < 0):
        return pshape2
    elif (lambda2 < 0):
        return pshape1
    else:
        aClosest = pshape1[0] * lambda1 + pshape2[0] * lambda2
        bClosest =  pshape1[1] * lambda1 + pshape2[1] * lambda2
        return (aClosest, bClosest)




def _itersect_with_points(shape1: Shape, shape2: Shape) -> tuple[bool, int, tuple[vec2d, vec2d]]:
    does_not_intersect = False
    dir = vec2d(0,1)
    tri_points: list[vec2d] = []
    # (shape1, shape2)
    support_points: list[tuple[vec2d]] = []

    mink_point = mink_diff(shape1, shape2, dir)
    tri_points.append(mink_point)
    del dir

    vec_to_origin = vec2d(0,0) - mink_point
    mink_point, sp = mink_diff(shape1, shape2, vec_to_origin, return_support_points=True)
    support_points += [sp]

    if not passes_origin(mink_point, vec_to_origin):
        does_not_intersect = True
    
    tri_points.append(mink_point)
    del vec_to_origin
    
    norm_to_origin = normal_dir_origin(tri_points[0], tri_points[1])
    mink_point, sp = mink_diff(shape1, shape2, norm_to_origin, return_support_points=True)
    support_points += [sp]

    if not passes_origin(mink_point, norm_to_origin):
        does_not_intersect = True

    tri_points.append(mink_point)
    del norm_to_origin

    dir = None

    iterations = 10
    for _ in range(iterations):
        passed,new_dir = triangle_contains_origin(tri_points[0], tri_points[1], tri_points[2])

        p1 = closest_point_on_line(tri_points[0], tri_points[2])
        p2 = closest_point_on_line(tri_points[2], tri_points[1])

        if p1.dot(p1) < p2.dot(p2):
            l = p1
        else:
            l = p2

        pygame.draw.polygon(window.screen, (255,0,255), [(tri_points[0]+shift).into_tuple(),(tri_points[1]+shift).into_tuple(),(tri_points[2]+shift).into_tuple()])
        pygame.draw.circle(window.screen, (0,0,255), shift.into_tuple(), 3)

        if passed:
            pygame.draw.line(window.screen, (255,0,0), (l + shift).into_tuple(), shift.into_tuple())
            return (not (False or does_not_intersect), l.mag(), closest_points_on_shapes(
                (support_points[0][0],support_points[0][1]), 
                (support_points[1][0],support_points[1][1]), 
                l, 
                tri_points[1]))
        else:
            dir = new_dir
            prev_p = tri_points.pop(0)
            mink_point, sp = mink_diff(shape1, shape2, dir, return_support_points=True)
            support_points.pop(0)
            support_points += [sp]

            if not passes_origin(mink_point, dir):
                pygame.draw.line(window.screen, (255,0,0), (l + shift).into_tuple(), shift.into_tuple())
                return (False, l.mag(), closest_points_on_shapes(
                    (support_points[0][0],support_points[0][1]), 
                    (support_points[1][0],support_points[1][1]), 
                    l,
                    prev_p))
            
            else: 
                tri_points.append(mink_point)
    
    pygame.draw.line(window.screen, (255,0,0), (l + shift).into_tuple(), shift.into_tuple())
    return (False, l.mag(), closest_points_on_shapes(
        (support_points[0][0],support_points[0][1]), 
        (support_points[1][0],support_points[1][1]), 
        l, 
        tri_points[1]
        ))


# "overload" the different GJK versions
def intersect(shape1: Shape, shape2: Shape, dist=None, points=None):
    if points != None:
        return _itersect_with_points(shape1, shape2)
    if dist != None:
        return _intersect_with_dist(shape1, shape2)
    else:
        return _intersect_only_check(shape1, shape2)


class Directions:
    left = vec2d(-1,0)
    right = vec2d(1,0)
    up = vec2d(0,1)
    down = vec2d(0,-1)





def quad_quad_intersection(quad1: Quad, quad2: Quad) -> tuple[bool, tuple | Directions]:

    left = quad1.furthest_in_dir(Directions.left).x < quad2.furthest_in_dir(Directions.right).x
    right = quad1.furthest_in_dir(Directions.right).x > quad2.furthest_in_dir(Directions.left).x

    up = quad1.furthest_in_dir(Directions.up).y > quad2.furthest_in_dir(Directions.down).y
    down = quad1.furthest_in_dir(Directions.down).y < quad2.furthest_in_dir(Directions.up).y



    return up and down and left and right


def relative_position(shape1: Shape, shape2: Shape):
    center1 = shape1.center_of_mass()
    center2 = shape2.center_of_mass()

    dirC1C2 = (center2 - center1).normalize()

    dirs = [Directions.down, Directions.up, Directions.left, Directions.right]
    dots = [dirC1C2.dot(ddir) for ddir in dirs]

    index_max = 0
    for i, val in enumerate(dots):
        if dots[index_max] < val:
            index_max = i
    
    return dirs[index_max]

# # voronoi regions

# class QuadRegions:
    
#     top_left = 0
#     top = 1
#     top_right = 2

#     middle_left = 3
#     middle_right = 4

#     bottom_left = 5
#     bottom = 6
#     bottom_right = 7

# class RangeType:
#     lower_bound = 0
#     upper_bound = 1
#     full_range = 2

# class Axis:
#     x = 0
#     y = 1

# # programmiticaly get the x or y value helper fn
# def _get_axis_from_vec(vec: vec2d, axis: Axis) -> float:
#     if axis == Axis.x:
#         return vec.x
#     else:
#         return vec.y

# def quad_in_range(range_type: RangeType, bounds: tuple | float, axis: Axis, shape: Quad) -> tuple[bool, float | None]:
#     if axis == Axis.x:
#         directions = (Directions.left, Directions.right)
#     elif axis == Axis.y:
#         directions = (Directions.down, Directions.up)
#     else:
#         raise ValueError("Incorrect axis type provided")
    
#     if range_type == RangeType.lower_bound:
#         lower_bound_point = _get_axis_from_vec(shape.furthest_in_dir(directions[0]), axis)
#         upper_bound_point = _get_axis_from_vec(shape.furthest_in_dir(directions[1]), axis)

#         if lower_bound_point > bounds:
#             return (True, 1)
#         elif upper_bound_point > bounds:
#             return (True, (bounds - lower_bound_point)/(upper_bound_point-lower_bound_point))
#         else:
#             return (False, 0)

#     if range_type == RangeType.upper_bound:
#         lower_bound_point = _get_axis_from_vec(shape.furthest_in_dir(directions[0]), axis)
#         upper_bound_point = _get_axis_from_vec(shape.furthest_in_dir(directions[1]), axis)

#         if lower_bound_point < bounds:
#             return (True, 1)
#         elif upper_bound_point < bounds:
#             return (True, (bounds - upper_bound_point)/(lower_bound_point-upper_bound_point))
#         else:
#             return (False, 0)
    
#     if range_type == RangeType.full_range:

#         if not (bounds[0] < bounds[1]):
#             raise ValueError("lower bound must be greater than upper bound")

#         lower_bound_point = _get_axis_from_vec(shape.furthest_in_dir(directions[0]), axis)
#         upper_bound_point = _get_axis_from_vec(shape.furthest_in_dir(directions[1]), axis)

#         if upper_bound_point < bounds[0] or lower_bound_point > bounds[1]:
#             return (False, 0)
#         elif bounds[0] < lower_bound_point and bounds[1] > upper_bound_point:
#             return (True,1)
#         elif bounds[0] > lower_bound_point and bounds[1] < upper_bound_point:
#             return (True, (bounds[1]-bounds[0])/(upper_bound_point-lower_bound_point))
#         elif bounds[1] > lower_bound_point:
#             return (True, (bounds[1] - upper_bound_point)/(lower_bound_point-upper_bound_point))
#         else:
#             return (True, (bounds[0] - lower_bound_point)/(upper_bound_point-lower_bound_point))


 

# #asumming that the other shape isn't bigger or overlapping too much
# def quad_partial_voroni_regions(shape1: Quad, shape2: Quad) -> QuadRegions:

#     up = (RangeType.lower_bound, shape1.furthest_in_dir(Directions.up).y ,Axis.y, shape2)
#     down = (RangeType.upper_bound, shape1.furthest_in_dir(Directions.down).y ,Axis.y, shape2)

#     left = (RangeType.upper_bound, shape1.furthest_in_dir(Directions.left).x ,Axis.x, shape2)
#     right = (RangeType.lower_bound, shape1.furthest_in_dir(Directions.right).x ,Axis.x, shape2)

    
#     inputs = [up, down, left, right]
#     ratios = list(quad_in_range(*args) for args in inputs)

#     match max(range(len(ratios)), key=ratios.__getitem__):
#         case 0: return Directions.up
#         case 1: return Directions.down
#         case 2: return Directions.left
#         case 3: return Directions.right
    
