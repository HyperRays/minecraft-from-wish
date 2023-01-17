from shapes import *
from physics import Directions
# creates a collider for the tiles and player on update
def create_collider(position, w, h, collider: Quad = None) -> Quad:
    if collider != None:
        collider.a,collider.b,collider.c,collider.d = position, position + vec2d(w, 0), position + vec2d(0,h), position + vec2d(w,h)
        return collider
    else:
        return Quad(position, position + vec2d(w, 0), position + vec2d(0,h), position + vec2d(w,h))

# the Directions are actually just vectors, so they have to be turned into names
def _repr_Directions(dir: Directions) -> str:
    match dir:
        case Directions.up: return "up"
        case Directions.down: return "down"
        case Directions.left: return "left"
        case Directions.right: return "right"

def clamp(n, smallest, largest): return max(smallest, min(n, largest))