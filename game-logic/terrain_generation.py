from math import floor, pi, sin
from blocks import *
from random import choice
#the terrain genarator takes in a position which return a block

# Biomes = [grassland, desert, polar]
    
biome_spacing = 9

#stone depth
stone_de = -33

def grassland(x,y, pixelpos):
    if y == 1:
        return Grass(pixelpos)
    elif stone_de-1 < y < 1:
        return Dirt(pixelpos)
    elif y < stone_de:


        return Stone(pixelpos)
    else:
        return Air(pixelpos)
        

def desert(x,y, pixelpos):
    if y == 0:
        return Sand(pixelpos)
    elif stone_de-1<y < 0:
        return Sand(pixelpos)
    elif y < stone_de:
        return Stone(pixelpos)
    else:
        return Air(pixelpos)

def polar(x,y, pixelpos):
    if y == 0:
        return Ice(pixelpos)
    elif stone_de-1< y < 0:
        return Water(pixelpos)
    elif y < stone_de:
        return Stone(pixelpos)
    else:
        return Air(pixelpos)

def mountains(x,y, pixelpos):    
    if y <= 0:
        return Stone(pixelpos)
    else:
        mountain_height = (sin(lerp(0, pi, x/(16*(biome_spacing+1))))**2)*20
        snow_height = (sin(lerp(0, pi, (x/(16*(biome_spacing+1)))))**4)*28
        if y < mountain_height:
            return Stone(pixelpos)
        if mountain_height <= y <= snow_height:
            return Snow(pixelpos)
        return Air(pixelpos)

biome_count = 4

def test_render(x,y, chunk: Chunk):
    coordinates_glob = chunk.get_chunk_coordinates(vec2d(x,y))
    coordinates = vec2d(x= (coordinates_glob.x*BLOCK_DIMENSIONS[0]), y= (coordinates_glob.y*BLOCK_DIMENSIONS[1]))
    chunk_coords = chunk.position

    match floor(chunk_coords.x*(1/(biome_spacing+1)) % biome_count):
        case 0: return mountains(coordinates_glob.x, coordinates_glob.y, coordinates)
        case 1: return grassland(coordinates_glob.x, coordinates_glob.y, coordinates)
        case 2: return desert(coordinates_glob.x, coordinates_glob.y, coordinates)
        case 3: return polar(coordinates_glob.x, coordinates_glob.y, coordinates)

    return Air(coordinates)


    # return grassland(chunk_coords.x, chunk_coords.y, coordinates)


terrain_gen = test_render