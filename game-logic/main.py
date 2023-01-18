
# you need this here, or otherwise the multiprocessing library spawns a new window
if __name__ == "__main__":

    from basic_units import bcolors
    import sys,os

    os.chdir(os.path.dirname(__file__))

    path = os.path.join(os.getcwd() , os.path.basename(__file__))
    print(path, os.path.join("minecraft-from-wish","game-logic","main.py"))
    if not path.endswith(os.path.join("minecraft-from-wish","game-logic","main.py")):
        sys.exit(f"please run this file from the {bcolors.BOLD}{bcolors.OKCYAN}minecraft-from-wish/game-logic/main.py{bcolors.ENDC}{bcolors.ENDC} folder")

    from blocks import *
    from player import *
    from mouse import *
    from background import *
    from sound_manager import SoundManager
    from terrain_generation import *
    from random import randint



    # sets the chunks with chunk positions 
    for a in range(-3,3):
        for b in range(-3,3):
            chunk_manager.add_chunk(Chunk(vec2d(a,b), terrain_gen))

    cpos = camera.get_position()
    chunk_manager.set_all()
    camera.update_position(-vec2d(window.size[0]/2,window.size[1]/2))


    s_mgr = SoundManager()
    Background()
    DayCycle()
    player = Player(vec2d(0,100))
    mouse = Mouse()

    s_mgr.load_sound("../assets/audio/Track_1.1.wav", "track1")
    s_mgr.load_sound("../assets/audio/Track_1.2.wav", "track2")
    match randint(0,1):
        case 0: s_mgr.play_sound("track1")
        case 1: s_mgr.play_sound("track2")

    graphics.set_render_layers(["bg", "chunks_layer",  "player_layer", "grass_layer", "day-night-overlay", "mouse_layer", "chunks_debug", "player_debug_layer", "mouse_debug_layer"])
    # graphics.set_render_layers(["bg","chunks_layer", "player_layer", "grass_layer", "day-night-overlay", "mouse_layer"])
    graphics.create_layer("day-night-overlay")
    graphics.create_layer("bg")
    window.run()
