import pyglet
import os

window = pyglet.window.Window(700,700)
path = "sand_block.png"
fullname = os.path.join("../assets/images", path)
image = pyglet.image.load(fullname)

@window.event
def on_draw():
    window.clear()
    image.blit(0, 0)

pyglet.app.run()