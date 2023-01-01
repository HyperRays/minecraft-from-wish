from blocks import *
#the chunk manager takes in a function which return a block
def test_render(x,y, chunk):
    coordinates_glob = chunk.get_chunk_coordinates(vec2d(x,y))
    coordinates = vec2d(x= (coordinates_glob.x*BLOCK_DIMENSIONS[0]), y= (coordinates_glob.y*BLOCK_DIMENSIONS[1]))

    if coordinates_glob.y < 0:
        return Water(coordinates)
    elif coordinates_glob.y == 0:
        return Ice(coordinates)
    else:
        return Air(coordinates)


terrain_gen = test_render