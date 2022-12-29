from blocks import *
from player import *
from mouse import *
from terrain_generation import *

# sets the chunks with chunk positions 
for a in range(-3,3):
    for b in range(-3,3):
        chunk_manager.add_chunk(Chunk(vec2d(a,b), test_render))

cpos = camera.get_position()
chunk_manager.set_all()
camera.update_position(-vec2d(window.size[0]/2,window.size[1]/2))
Player(vec2d(0,100))
Mouse()
# graphics.set_render_layers(["chunks_layer",  "player_layer", "mouse_layer", "player_debug_layer", "chunks_debug", "mouse_debug_layer"])
graphics.set_render_layers(["chunks_layer", "player_layer", "mouse_layer"])
window.run()