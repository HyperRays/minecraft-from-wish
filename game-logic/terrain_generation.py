from math import floor
from blocks import *
from random import choice
#the chunk manager takes in a function which return a block

def grassland(x,y, pixelpos):
    if y == 1:
        return Grass(pixelpos)
    elif y < 1:
        return Dirt(pixelpos)
    else:
        return Air(pixelpos)
        

def desert(x,y, pixelpos):
    if y == 0:
        return Sand(pixelpos)
    elif y < 0:
        return Sand(pixelpos)
    else:
        return Air(pixelpos)

def polar(x,y, pixelpos):
    if y == 0:
        return Ice(pixelpos)
    elif y < 0:
        return Water(pixelpos)
    else:
        return Air(pixelpos)

Biomes = [grassland, desert, polar]
    
biome_spacing = 9

def test_render(x,y, chunk: Chunk):
    coordinates_glob = chunk.get_chunk_coordinates(vec2d(x,y))
    coordinates = vec2d(x= (coordinates_glob.x*BLOCK_DIMENSIONS[0]), y= (coordinates_glob.y*BLOCK_DIMENSIONS[1]))
    chunk_coords = chunk.position

    match floor(chunk_coords.x*(1/biome_spacing+1) % 3):
        case 0: return grassland(coordinates_glob.x, coordinates_glob.y, coordinates)
        case 1: return desert(coordinates_glob.x, coordinates_glob.y, coordinates)
        case 2: return polar(coordinates_glob.x, coordinates_glob.y, coordinates)

    return Air(coordinates)


    # return grassland(chunk_coords.x, chunk_coords.y, coordinates)


terrain_gen = test_render