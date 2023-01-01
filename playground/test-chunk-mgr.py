"""
this file has been used to test the following systems:
-Chunk Manager
-Render Layers
-Physics
(-World Loading/Saving)
"""

import os
import pickle
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),'../game-logic'))

# import all the nessesary modules
sys.path.append(os.path.join(os.path.dirname(__file__),'../graphics'))
from prelude import *
from chunks_module import Chunk
from chunk_manager import ChunkManager
import itertools
from random import randint


# initialize the window
window.init((700,700),"test chunk mgr")

texture_handler = TextureHandler()

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

# create a camera
camera = Camera()

# rescale the image to required size
def rescale_image(texture, height = None, width = None, factor = None, direct = None) -> tuple[int, int]: 
    if direct != None:
        texture.get_size()
    else:
        (a,b) = store.textures[texture].image.get_size()

    ratio = a/b
    if height != None and width != None:
        (w,h) = width, height
    if height != None:
        (w,h) = (height,height/ratio)
    elif width != None:
        (w,h) = (width*ratio,width)
    elif factor != None:
        (w,h) = (a*factor,b*factor)
    
    if direct != None:
        del ratio
        return pygame.transform.scale(texture, (w,h))
    else:
        store.textures[texture].image = pygame.transform.scale(store.textures[texture].image, (w,h))
        del ratio
        return w,h

#square helper class, so that the collider creation and image (texture) loading is handled and 
class Square(GraphicsObject):

    def __init__(self, position: vec2d) -> None:
        self.position = position
        self.texture = texture_handler.get_texture(self.tex_name)
        self.collider = create_collider(self.position, BLOCK_DIMENSIONS[0], BLOCK_DIMENSIONS[1])
        self.render_collider_bounds = False
        self.render_collision_detected = False
    
    async def render(self):
        chunk_manager.get_layer().blit(self.texture, camera.screen_position(self.position).into_tuple())
    
    async def update(self):
        self.collider = create_collider(self.position, BLOCK_DIMENSIONS[0], -BLOCK_DIMENSIONS[1], collider=self.collider)
        # self.render()
        if self.render_collider_bounds and not self.render_collision_detected:
            pygame.draw.polygon(chunk_manager.get_debug_layer(), (100,100,100) , [ camera.screen_position(self.collider.b).into_tuple(), camera.screen_position(self.collider.a).into_tuple(), camera.screen_position(self.collider.c).into_tuple(), camera.screen_position(self.collider.d).into_tuple()], width=1)
        if self.render_collision_detected:
            pygame.draw.polygon(chunk_manager.get_debug_layer(), (200,100,120) , [ camera.screen_position(self.collider.b).into_tuple(), camera.screen_position(self.collider.a).into_tuple(), camera.screen_position(self.collider.c).into_tuple(), camera.screen_position(self.collider.d).into_tuple()] , width=2)
        self.render_collider_bounds = False
        self.render_collision_detected = False

    def save(self) -> bytes:
        save_dict = {
            "position": pickle.dumps(self.position),
            "collider": pickle.dumps(self.collider)
        }

        return pickle.dumps(save_dict)
    
    @classmethod
    def load(cls, b: bytes):
        self = cls.__new__(cls)
        save_dict = pickle.loads(b)
        self.position = save_dict["position"]
        self.texture = texture_handler.get_texture(cls.tex_name)
        self.collider = save_dict["collider"]
        self.render_collider_bounds = False
        self.render_collision_detected = False

        return self


#Air tile
class Air(GraphicsObject):

    def __init__(self, position: vec2d) -> None:
        self.position = position
        self.collider = create_collider(self.position, BLOCK_DIMENSIONS[0], BLOCK_DIMENSIONS[1])
        self.render_collider_bounds = False
        self.render_collision_detected = False
    
    async def update(self):
        self.collider = create_collider(self.position, BLOCK_DIMENSIONS[0], -BLOCK_DIMENSIONS[1], collider=self.collider)
        if self.render_collider_bounds and not self.render_collision_detected:
            pygame.draw.polygon(chunk_manager.get_debug_layer(), (100,100,100) , [ camera.screen_position(self.collider.b).into_tuple(), camera.screen_position(self.collider.a).into_tuple(), camera.screen_position(self.collider.c).into_tuple(), camera.screen_position(self.collider.d).into_tuple()], width=1)
        if self.render_collision_detected:
            pygame.draw.polygon(chunk_manager.get_debug_layer(), (200,100,120) , [ camera.screen_position(self.collider.b).into_tuple(), camera.screen_position(self.collider.a).into_tuple(), camera.screen_position(self.collider.c).into_tuple(), camera.screen_position(self.collider.d).into_tuple()] , width=2)
        self.render_collider_bounds = False
        self.render_collision_detected = False
    
    def save(self) -> bytes:
        save_dict = {
            "position": pickle.dumps(self.position),
            "collider": pickle.dumps(self.collider)
        }

        return pickle.dumps(save_dict)
    
    @classmethod
    def load(cls, b: bytes):
        self = cls.__new__(cls)
        save_dict = pickle.loads(b)
        self.position = save_dict["position"]
        self.collider = save_dict["collider"]
        self.render_collider_bounds = False
        self.render_collision_detected = False

        return self


#other tiles
class Ice(Square):
    tex_name = "Ice" 
    texture_handler.load_texture(tex_name, "ice_block.png")   
    texture_handler.rescale_image(tex_name, height=BLOCK_DIMENSIONS[0], width=BLOCK_DIMENSIONS[1])

class JungleTreeLeaf(Square):
    texture = GraphicsObject.add_texture("leaf_jungle_block.png") 
    rescale_image(texture, height=block_dimensions[0], width=block_dimensions[1])

class JungleTreeBark(Square):
    texture = GraphicsObject.add_texture("bark_jungle_block.png") 
    rescale_image(texture, height=block_dimensions[0], width=block_dimensions[1])

class Sand(Square):
    tex_name = "Sand" 
    texture_handler.load_texture(tex_name, "sand_block.png")   
    texture_handler.rescale_image(tex_name, height=BLOCK_DIMENSIONS[0], width=BLOCK_DIMENSIONS[1])
    

class Grass(Square):
    tex_name = "Grass" 
    texture_handler.load_texture(tex_name, "grass_block.png")   
    texture_handler.rescale_image(tex_name, height=BLOCK_DIMENSIONS[0], width=BLOCK_DIMENSIONS[1])

class Dirt(Square):
    tex_name = "Dirt" 
    texture_handler.load_texture(tex_name, "dirt_block.png")   
    texture_handler.rescale_image(tex_name, height=BLOCK_DIMENSIONS[0], width=BLOCK_DIMENSIONS[1])


#Water is special, because it is animated
class Water(Square):

    tex_name1 = "Water1" 
    texture_handler.load_texture(tex_name1, "water_block1.png")   
    texture_handler.rescale_image(tex_name1, height=BLOCK_DIMENSIONS[0], width=BLOCK_DIMENSIONS[1])

    tex_name2 = "Water2" 
    texture_handler.load_texture(tex_name2, "test_images/test_water_block2.png")   
    texture_handler.rescale_image(tex_name2, height=BLOCK_DIMENSIONS[0], width=BLOCK_DIMENSIONS[1])


    def __init__(self, position: vec2d) -> None:
        # sets a random time after which it will change to the next tile (it cycles through two tile)
        self.timer = Timed(7_000_000_00)

        #set the starting position
        self.position = position

        #set which image number (texture) is currently set 
        self.current_tex = 0

        #the images that are loaded in 
        self.texture1 = texture_handler.get_texture(self.tex_name1)
        self.texture2 = texture_handler.get_texture(self.tex_name2)

        # set the texture to be rendered
        self.texture = self.texture1

        #create the collider
        self.collider = create_collider(self.position, BLOCK_DIMENSIONS[0], BLOCK_DIMENSIONS[1])

        #set the debugging outlines of the collider
        self.render_collider_bounds = False
        self.render_collision_detected = False
    
    async def render(self):

        #after certain time switch the textures
        self.timer.poll()
        if self.timer.reached():
            if self.current_tex == 0:
                self.current_tex = 1
                self.texture = self.texture2
            else:
                self.current_tex = 0
                self.texture = self.texture1
            
            self.timer.reset()

        chunk_manager.get_layer().blit(self.texture, camera.screen_position(self.position).into_tuple())
    

    async def update(self):
        #renew the collider and render the image
        self.collider = create_collider(self.position, BLOCK_DIMENSIONS[0], -BLOCK_DIMENSIONS[1], collider=self.collider)
        # self.render()

        #setting the collider outlines and collision boundaries
        if self.render_collider_bounds and not self.render_collision_detected:
            pygame.draw.polygon(chunk_manager.get_debug_layer(), (100,100,100) , [ camera.screen_position(self.collider.b).into_tuple(), camera.screen_position(self.collider.a).into_tuple(), camera.screen_position(self.collider.c).into_tuple(), camera.screen_position(self.collider.d).into_tuple()], width=1)
        if self.render_collision_detected:
            pygame.draw.polygon(chunk_manager.get_debug_layer(), (200,100,120) , [ camera.screen_position(self.collider.b).into_tuple(), camera.screen_position(self.collider.a).into_tuple(), camera.screen_position(self.collider.c).into_tuple(), camera.screen_position(self.collider.d).into_tuple()] , width=2)
        
        self.render_collider_bounds = False
        self.render_collision_detected = False
    
    def save(self) -> bytes:
        save_dict = {
            "position": pickle.dumps(self.position),
            "current_tex": pickle.dumps(self.current_tex),
            "collider": pickle.dumps(self.collider)
        }

        return pickle.dumps(save_dict)

    @classmethod
    def load(cls, b: bytes):
        self = cls.__new__(cls)
        save_dict = pickle.loads(b)
        self.position = save_dict["position"]
        self.current_tex = save_dict["current_tex"]
        self.texture1 = texture_handler.get_texture(cls.tex_name1)
        self.texture2 = texture_handler.get_texture(cls.tex_name2)
        self.collider = save_dict["collider"]
        self.render_collider_bounds = False
        self.render_collision_detected = False

        return self



# the chunk_manager stores all of the chunks
chunk_manager = ChunkManager()


#the chunk manager takes in a function which return a block
def test_render(x,y, chunk):
    coordinates_glob = chunk.get_chunk_coordinates(vec2d(x,y))
    coordinates = vec2d(x= (coordinates_glob.x*BLOCK_DIMENSIONS[0]), y= (coordinates_glob.y*BLOCK_DIMENSIONS[1]))

    if (coordinates_glob.x < -3 or coordinates_glob.x > 5) and 3 < coordinates_glob.y > -1 and coordinates_glob.y < 7 :
        return Ice(coordinates)

    if coordinates_glob.y < 0:
        return Water(coordinates)
    elif coordinates_glob.y == 0:
        return Ice(coordinates)
    else:
        return Air(coordinates)


# sets the chunks with chunk positions 
for a in range(-3,3):
    for b in range(-3,3):
        chunk_manager.add_chunk(Chunk(vec2d(a,b), test_render))

# the Directions are actually just vectors, so they have to be turned into names
def _repr_Directions(dir: Directions) -> str:
    match dir:
        case Directions.up: return "up"
        case Directions.down: return "down"
        case Directions.left: return "left"
        case Directions.right: return "right"

class Player(GraphicsObject):

    graphics.create_layer("player_layer")
    player_layer = graphics.layers["player_layer"]

    graphics.create_layer("player_debug_layer")
    player_debug_layer = graphics.layers["player_debug_layer"]

    tex_name = "Player" 
    texture_handler.load_texture(tex_name, "test_images/hi-res-stickman.png")   
    (w,h) = texture_handler.rescale_image(tex_name, height=PLAYER_HEIGHT, width=PLAYER_WIDTH)

    def __init__(self, position: vec2d) -> None:
        #make sure that the player gets directly called
        super().__init__()

        #set the starting position
        self.position = position
        self.texture = texture_handler.get_texture(self.tex_name)

        #create the collider
        self.collider = create_collider(self.position, self.w, -self.h)
    
        # the forces that are applied to the player
        self.force = vec2d(0,0)

        # in which direction the player is colliding (bad)
        self.collided_dir = {
            Directions.up: False,
            Directions.down: False,
            Directions.left: False,
            Directions.right: False
        }
    
    def save(self) -> bytes:
        save_dict = {
            "position": pickle.dumps(self.position),
            "collider": pickle.dumps(self.collider)
        }

        return pickle.dumps(save_dict)
    
    @classmethod
    def load(cls, b: bytes):
        self = cls.__new__(cls)
        save_dict = pickle.loads(b)
        self.position = save_dict["position"]
        self.collider = save_dict["collider"]

        #create the collider
        self.collider = create_collider(self.position, self.w, -self.h)
    
        # the forces that are applied to the player
        self.force = vec2d(0,0)

        # in which direction the player is colliding (bad)
        self.collided_dir = {
            Directions.up: False,
            Directions.down: False,
            Directions.left: False,
            Directions.right: False
        }

        return self


    async def render(self):
        # render the image of the player to the screen accoring to the camera
        self.player_layer.blit(self.texture, camera.screen_position(self.position).into_tuple())
    
    async def update(self):
        # checks in which direction the player is colliding and sets the force in that axis to 0 (bad)
        if self.collided_dir[Directions.down]:
            if self.force.y < 0:
                self.force.y = 0
        if self.collided_dir[Directions.up]:
            if self.force.y > 0:
                self.force.y = 0
        if self.collided_dir[Directions.right]:
            if self.force.x > 0:
                self.force.x = 0
        if self.collided_dir[Directions.left]:
            if self.force.x < 0:
                self.force.x = 0

        # adds force to player
        self.position += self.force
        # renews collider
        self.collider = create_collider(self.position, self.w, -self.h, collider=self.collider)

        #finds in which chunk the player is in through the cunk manager
        true_chunksize_width = BLOCK_DIMENSIONS[0] * CHUNK_DIMENSIONS[0]
        true_chunksize_height = BLOCK_DIMENSIONS[1] * CHUNK_DIMENSIONS[1]
        chunks_coords: set[Chunk] = set(
            (chunk_manager.find_chunk_pos(self.collider.a + vec2d(0, CHUNK_DIMENSIONS[1]), vec2d(true_chunksize_width, true_chunksize_height)),
            chunk_manager.find_chunk_pos(self.collider.b + vec2d(0, CHUNK_DIMENSIONS[1]), vec2d(true_chunksize_width, true_chunksize_height)),
            chunk_manager.find_chunk_pos(self.collider.c + vec2d(0, CHUNK_DIMENSIONS[1]), vec2d(true_chunksize_width, true_chunksize_height)),
            chunk_manager.find_chunk_pos(self.collider.d + vec2d(0, CHUNK_DIMENSIONS[1]), vec2d(true_chunksize_width, true_chunksize_height)),
            )
        )

        chunks: list[Chunk] = []
        for chunk_pos in chunks_coords:
            chunks += [chunk_manager.get_chunk(chunk_pos)]
       
        # draws a outline around the chunk (for debugging purposes only)
        for chunk in chunks:
            glob_coord = vec2d(chunk.position.x * CHUNK_DIMENSIONS[0] * BLOCK_DIMENSIONS[0], chunk.position.y * CHUNK_DIMENSIONS[1] * BLOCK_DIMENSIONS[1] - BLOCK_DIMENSIONS[1])
            tmp_outline = create_collider(glob_coord, CHUNK_DIMENSIONS[0] * BLOCK_DIMENSIONS[0], CHUNK_DIMENSIONS[1] * BLOCK_DIMENSIONS[1])
            pygame.draw.polygon(self.player_debug_layer, (40,150,250) , [ camera.screen_position(tmp_outline.b).into_tuple(), camera.screen_position(tmp_outline.a).into_tuple(), camera.screen_position(tmp_outline.c).into_tuple(), camera.screen_position(tmp_outline.d).into_tuple()], width = 2)

        # #renders the player itself
        # self.render()

        # draws the collider around the player (for debugging purposes only)
        pygame.draw.polygon(self.player_debug_layer, (100,200,140) , [ camera.screen_position(self.collider.b).into_tuple(), camera.screen_position(self.collider.a).into_tuple(), camera.screen_position(self.collider.c).into_tuple(), camera.screen_position(self.collider.d).into_tuple()], width=1)

        #resets all the forces
        self.force = vec2d(0,0)
        self.collided_dir = {
            Directions.up: False,
            Directions.down: False,
            Directions.left: False,
            Directions.right: False
        }

        # goes through every block in the chunk to find out with which block the player is colliding with
        for chunk in chunks:
            for obj in itertools.chain(*chunk.internal_objects):
                if obj != None and type(obj) != Air and type(obj) != Water:
                    if intersect(self.collider, obj.collider):
                        dir = -relative_position(obj.collider, self.collider)
                        self.collided_dir[dir] = True
                        obj.render_collision_detected = True

                    obj.render_collider_bounds = True

        #adds the gravity force
        self.force += vec2d(0,-GRAVITY_ACCEL)

    async def input(self, keys):

        # adds to force and controlls in which direction the player moves
        if keys[self.characters["s"]]:
                self.force.y -= PLAYER_SPEED

        # elif keys[self.characters["w"]]:
        #     self.force.y += PLAYER_SPEED
        
        if keys[self.characters["d"]]:
            self.force.x += PLAYER_SPEED

        elif keys[self.characters["a"]]:
            self.force.x -= PLAYER_SPEED
        
        if keys[self.characters["space"]] and self.collided_dir[Directions.down]:
            self.force.y += BLOCK_DIMENSIONS[0]+10

        #updates the camera position, so that the player stays in the center
        camera.update_position(self.position - vec2d(window.size[0]/2,-window.size[1]/2))

        #closes the programm (for debugging purposes only)
        if keys[self.characters["e"]]:
            os.abort()

        if keys[self.characters["v"]]:
            print("saving")
            chunk_manager.save()
        
        if keys[self.characters["l"]]:
            print("loading")
            chunk_manager = ChunkManager.load()

class Mouse(GraphicsObject):

    graphics.create_layer("mouse_layer")
    mouse_layer = graphics.layers["mouse_layer"]

    graphics.create_layer("mouse_debug_layer")
    mouse_debug_layer = graphics.layers["mouse_debug_layer"]


    def __init__(self) -> None:
        super().__init__()
        self.collider = Point(vec2d(0,0))

        #hide the cursor
        #https://stackoverflow.com/a/40628090
        pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))

    def save(self) -> bytes:
        return bytes(0)

    @classmethod
    def loads(cls, _: bytes):
        
        self = cls.__new__(cls)
        self.collider = Point(vec2d(0,0))

        #hide the cursor
        #https://stackoverflow.com/a/40628090
        pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
        return self

    async def render(self):
        pass
    
    async def input(self, _):
        #update all the mouse events (update which keys have been pressed)
        pygame.event.get()
        #get the mouse position and set the pointer (dot) positon
        (x,y) = pygame.mouse.get_pos()
        pos = vec2d(x,-y)
        self.collider.a = pos + camera.get_position()

        #get if a mouse button has been pressed
        mouse_down_left = pygame.mouse.get_pressed()[0]
        mouse_down_right = pygame.mouse.get_pressed()[2]

        # get in which chunk the player is in
        true_chunksize_width = BLOCK_DIMENSIONS[0] * CHUNK_DIMENSIONS[0]
        true_chunksize_height = BLOCK_DIMENSIONS[1] * CHUNK_DIMENSIONS[1]
        chunk_coord: vec2d = chunk_manager.find_chunk_pos(self.collider.a + vec2d(0, CHUNK_DIMENSIONS[1]), vec2d(true_chunksize_width, true_chunksize_height))
        chunk: Chunk = chunk_manager.get_chunk(chunk_coord)
        glob_coord = vec2d(chunk.position.x * CHUNK_DIMENSIONS[0] * BLOCK_DIMENSIONS[0], chunk.position.y * CHUNK_DIMENSIONS[1] * BLOCK_DIMENSIONS[1] - BLOCK_DIMENSIONS[1])
        
        #draw in the mouse pointer (we can change this)
        pygame.draw.circle(self.mouse_layer, (100,200,100), (x,y), 5)

        # create the chunk outline (for debugging purposes only)
        tmp_outline = create_collider(glob_coord, CHUNK_DIMENSIONS[0] * BLOCK_DIMENSIONS[0], CHUNK_DIMENSIONS[1] * BLOCK_DIMENSIONS[1])
        pygame.draw.polygon(self.mouse_debug_layer, (40,150,250) , [ camera.screen_position(tmp_outline.b).into_tuple(), camera.screen_position(tmp_outline.a).into_tuple(), camera.screen_position(tmp_outline.c).into_tuple(), camera.screen_position(tmp_outline.d).into_tuple()], width = 2)

        
        # go through every block in the chunk and find which one the mouse is on
        for x,obj_x in enumerate(chunk.internal_objects):
            for y,obj in enumerate(obj_x):
                if obj != None:
                    if intersect(self.collider, obj.collider):
                        obj.render_collision_detected = True

                        #set the block to something else if the mouse is pressed
                        if mouse_down_left:
                            chunk.set(vec2d(x,y), JungleTreeLeaf(obj.position))
                        if mouse_down_right:
                            chunk.set(vec2d(x,y), JungleTreeBark(obj.position))

                    obj.render_collider_bounds = True



        

cpos = camera.get_position()
chunk_manager.set_all()
camera.update_position(-vec2d(window.size[0]/2,window.size[1]/2))
Player(vec2d(0,100))
Mouse()
graphics.set_render_layers(["chunks_layer",  "player_layer", "mouse_layer", "player_debug_layer", "chunks_debug", "mouse_debug_layer"])
# graphics.set_render_layers(["chunks_layer", "player_layer", "mouse_layer"])
window.run()