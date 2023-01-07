from blocks import *
from player import *
from mouse import *
from terrain_generation import *

# sets the chunks with chunk positions 
for a in range(-3,3):
    for b in range(-3,3):
        chunk_manager.add_chunk(Chunk(vec2d(a,b), terrain_gen))

cpos = camera.get_position()
chunk_manager.set_all()
camera.update_position(-vec2d(window.size[0]/2,window.size[1]/2))
Background()
player = Player(vec2d(0,100))
mouse = Mouse()
graphics.set_render_layers(["bg", "chunks_layer",  "player_layer", "grass_layer", "mouse_layer", "player_debug_layer", "chunks_debug", "mouse_debug_layer"])
# graphics.set_render_layers(["bg","chunks_layer", "player_layer", "grass_layer", "mouse_layer"])
graphics.create_layer("bg")
graphics.layers["bg"].fill((0,0,100))
window.run()