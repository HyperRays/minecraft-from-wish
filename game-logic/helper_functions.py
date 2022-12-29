from prelude import *
# creates a collider for the tiles and player on update
def create_collider(position, w, h, collider: Quad = None) -> Quad:
    if collider != None:
        collider.a = position
        collider.b = position + vec2d(w, 0)
        collider.c = position + vec2d(0,h)
        collider.d = position + vec2d(w,h)
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
