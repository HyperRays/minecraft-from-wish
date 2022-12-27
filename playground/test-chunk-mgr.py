from multiprocessing import freeze_support
import os
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

def create_collider(position, w, h) -> Quad:
    return Quad(position, position + vec2d(w, 0), position + vec2d(0,h), position + vec2d(w,h))

camera = Camera()

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

timer = Timed(1_000_000)

class Square(GraphicsObject):

    def __init__(self, position: vec2d) -> None:
        self.position = position
        self.texture = self.textures[self.texture].copy()
        self.collider = create_collider(self.position, block_dimensions[0], block_dimensions[1])
        self.render_collider_bounds = False
        self.render_collision_detected = False
    
    def render(self):
        self.screen.blit(self.texture.image, camera.screen_position(self.position).into_tuple())
    
    async def update(self):
        self.collider = create_collider(self.position, block_dimensions[0], -block_dimensions[1])
        self.render()
        if self.render_collider_bounds and not self.render_collision_detected:
            pygame.draw.polygon(self.screen, (100,100,100) , [ camera.screen_position(self.collider.b).into_tuple(), camera.screen_position(self.collider.a).into_tuple(), camera.screen_position(self.collider.c).into_tuple(), camera.screen_position(self.collider.d).into_tuple()], width=1)
        if self.render_collision_detected:
            pygame.draw.polygon(self.screen, (200,100,120) , [ camera.screen_position(self.collider.b).into_tuple(), camera.screen_position(self.collider.a).into_tuple(), camera.screen_position(self.collider.c).into_tuple(), camera.screen_position(self.collider.d).into_tuple()] , width=2)
        self.render_collider_bounds = False
        self.render_collision_detected = False

class Air(GraphicsObject):

    def __init__(self, position: vec2d) -> None:
        self.position = position
        self.collider = create_collider(self.position, block_dimensions[0], block_dimensions[1])
        self.render_collider_bounds = False
        self.render_collision_detected = False
    
    async def update(self):
        self.collider = create_collider(self.position, block_dimensions[0], -block_dimensions[1])
        if self.render_collider_bounds and not self.render_collision_detected:
            pygame.draw.polygon(self.screen, (100,100,100) , [ camera.screen_position(self.collider.b).into_tuple(), camera.screen_position(self.collider.a).into_tuple(), camera.screen_position(self.collider.c).into_tuple(), camera.screen_position(self.collider.d).into_tuple()], width=1)
        if self.render_collision_detected:
            pygame.draw.polygon(self.screen, (200,100,120) , [ camera.screen_position(self.collider.b).into_tuple(), camera.screen_position(self.collider.a).into_tuple(), camera.screen_position(self.collider.c).into_tuple(), camera.screen_position(self.collider.d).into_tuple()] , width=2)
        self.render_collider_bounds = False
        self.render_collision_detected = False

class Ice(Square):
    texture = GraphicsObject.add_texture("ice_block.png") 
    rescale_image(texture, height=block_dimensions[0], width=block_dimensions[1])

class Sand(Square):
    texture = GraphicsObject.add_texture("sand_block.png") 
    rescale_image(texture, height=block_dimensions[0], width=block_dimensions[1])

    

class Grass(Square):
    texture = GraphicsObject.add_texture("grass_block.png") 
    rescale_image(texture, height=block_dimensions[0], width=block_dimensions[1])


class Dirt(Square):
    texture = GraphicsObject.add_texture("dirt_block.png") 
    rescale_image(texture, height=block_dimensions[0], width=block_dimensions[1])

class Water(Square):
    texture1 = GraphicsObject.add_texture("water_block1.png") 
    rescale_image(texture1, height=block_dimensions[0], width=block_dimensions[1])
    texture2 = GraphicsObject.add_texture("test_images/test_water_block2.png") 
    rescale_image(texture2, height=block_dimensions[0], width=block_dimensions[1])


    def __init__(self, position: vec2d) -> None:
        self.timer = Timed(randint(1_000_000_0, 1_000_000_000_0))
        self.position = position
        self.current_tex = 0
        self.texture1 = self.textures[self.texture1].copy()
        self.texture2 = self.textures[self.texture2].copy()
        self.texture = self.texture1
        self.collider = create_collider(self.position, block_dimensions[0], block_dimensions[1])
        self.render_collider_bounds = False
        self.render_collision_detected = False
    
    def render(self):
        self.timer.poll()
        if self.timer.reached():
            if self.current_tex == 0:
                self.current_tex = 1
                self.texture = self.texture2
            else:
                self.current_tex = 0
                self.texture = self.texture1
            
            self.timer.reset(new_target_ns=randint(1_000_000_0, 1_000_000_000_0))

        
        self.screen.blit(self.texture.image, camera.screen_position(self.position).into_tuple())

    async def update(self):
        self.collider = create_collider(self.position, block_dimensions[0], -block_dimensions[1])
        self.render()
        if self.render_collider_bounds and not self.render_collision_detected:
            pygame.draw.polygon(self.screen, (100,100,100) , [ camera.screen_position(self.collider.b).into_tuple(), camera.screen_position(self.collider.a).into_tuple(), camera.screen_position(self.collider.c).into_tuple(), camera.screen_position(self.collider.d).into_tuple()], width=1)
        if self.render_collision_detected:
            pygame.draw.polygon(self.screen, (200,100,120) , [ camera.screen_position(self.collider.b).into_tuple(), camera.screen_position(self.collider.a).into_tuple(), camera.screen_position(self.collider.c).into_tuple(), camera.screen_position(self.collider.d).into_tuple()] , width=2)
        self.render_collider_bounds = False
        self.render_collision_detected = False




chunk_manager = ChunkManager()


def test_render(x,y, chunk):
    coordinates_glob = chunk.get_chunk_coordinates(vec2d(x,y))
    coordinates = vec2d(x= (coordinates_glob.x*block_dimensions[0]), y= (coordinates_glob.y*block_dimensions[1]))

    if (coordinates_glob.x < -3 or coordinates_glob.x > 5) and 3 < coordinates_glob.y > -1 and coordinates_glob.y < 7 :
        return Ice(coordinates)

    if coordinates_glob.y < 0:
        return Water(coordinates)
    elif coordinates_glob.y == 0:
        return Ice(coordinates)
    else:
        return Air(coordinates)


for a in range(-3,3):
    for b in range(-3,3):
        chunk_manager.add_chunk(Chunk(vec2d(a,b), test_render))

def _repr_Directions(dir: Directions) -> str:
    match dir:
        case Directions.up: return "up"
        case Directions.down: return "down"
        case Directions.left: return "left"
        case Directions.right: return "right"

class Player(GraphicsObject):

    texture = GraphicsObject.add_texture("test_images/hi-res-stickman.png") 
    (w,h) = rescale_image(texture, height=PLAYER_HEIGHT, width=PLAYER_WIDTH)
    def __init__(self, position: vec2d) -> None:
        super().__init__()
        self.position = position
        self.texture = self.textures[self.texture].copy()
        self.chunk_mgr: ChunkManager = chunk_manager
        self.collider = create_collider(self.position, self.w, -self.h)
        self.should_update_chunks = False
        self.force = vec2d(0,0)
        self.collided_dir = {
            Directions.up: False,
            Directions.down: False,
            Directions.left: False,
            Directions.right: False
        }

    def render(self):
        self.screen.blit(self.texture.image, camera.screen_position(self.position).into_tuple())
    
    async def update(self):
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

        self.position += self.force
        self.collider = create_collider(self.position, self.w, -self.h)
        true_chunksize_width = block_dimensions[0] * CHUNK_DIMENSIONS[0]
        true_chunksize_height = block_dimensions[1] * CHUNK_DIMENSIONS[1]
        chunk: Chunk = self.chunk_mgr.find_chunk(self.position + vec2d(0, CHUNK_DIMENSIONS[1]), vec2d(true_chunksize_width, true_chunksize_height))
        glob_coord = vec2d(chunk.position.x * CHUNK_DIMENSIONS[0] * block_dimensions[0], chunk.position.y * CHUNK_DIMENSIONS[1] * block_dimensions[1] - block_dimensions[1])
        
        tmp_outline = create_collider(glob_coord, CHUNK_DIMENSIONS[0] * block_dimensions[0], CHUNK_DIMENSIONS[1] * block_dimensions[1])
        pygame.draw.polygon(self.screen, (40,150,250) , [ camera.screen_position(tmp_outline.b).into_tuple(), camera.screen_position(tmp_outline.a).into_tuple(), camera.screen_position(tmp_outline.c).into_tuple(), camera.screen_position(tmp_outline.d).into_tuple()], width = 2)
    
        self.render()
        self.force = vec2d(0,0)
        self.collided_dir = {
            Directions.up: False,
            Directions.down: False,
            Directions.left: False,
            Directions.right: False
        }
        pygame.draw.polygon(self.screen, (100,200,140) , [ camera.screen_position(self.collider.b).into_tuple(), camera.screen_position(self.collider.a).into_tuple(), camera.screen_position(self.collider.c).into_tuple(), camera.screen_position(self.collider.d).into_tuple()], width=1)
        for obj in itertools.chain(*chunk.internal_objects):
            if obj != None and type(obj) != Air:
                if intersect(self.collider, obj.collider):
                    dir = -relative_position(obj.collider, self.collider)
                    self.collided_dir[dir] = True
                    obj.render_collision_detected = True

                obj.render_collider_bounds = True

        self.force += vec2d(0,-GRAVITY_ACCEL)

    async def input(self, keys):


        timer.poll()

        if timer.reached():

            if keys[self.characters["s"]]:
                    self.force.y -= PLAYER_SPEED

            # elif keys[self.characters["w"]]:
            #     self.force.y += PLAYER_SPEED
            
            if keys[self.characters["d"]]:
                self.force.x += PLAYER_SPEED

            elif keys[self.characters["a"]]:
                self.force.x -= PLAYER_SPEED
            
            if keys[self.characters["space"]] and self.collided_dir[Directions.down]:
                self.force.y += block_dimensions[0]+10
            
            
            camera.update_position(self.position - vec2d(window.size[0]/2,-window.size[1]/2))

            if keys[self.characters["e"]]:
                os.abort()
                
            timer.reset()

class Mouse(GraphicsObject):
    def __init__(self) -> None:
        super().__init__()
        self.collider = Point(vec2d(0,0))
        self.chunk_mgr: ChunkManager = chunk_manager

    def render(self):
        pass
    
    async def input(self, _):
        pygame.event.get()
        (x,y) = pygame.mouse.get_pos()
        pos = vec2d(x,-y)
        self.collider.a = pos + camera.get_position()
        mouse_down = pygame.mouse.get_pressed()[0]

        true_chunksize_width = block_dimensions[0] * CHUNK_DIMENSIONS[0]
        true_chunksize_height = block_dimensions[1] * CHUNK_DIMENSIONS[1]
        chunk: Chunk = self.chunk_mgr.find_chunk(self.collider.a + vec2d(0, CHUNK_DIMENSIONS[1]), vec2d(true_chunksize_width, true_chunksize_height))
        pygame.draw.circle(window.screen, (100,200,100), (x-2.5,y-2.5), 5)
        glob_coord = vec2d(chunk.position.x * CHUNK_DIMENSIONS[0] * block_dimensions[0], chunk.position.y * CHUNK_DIMENSIONS[1] * block_dimensions[1] - block_dimensions[1])
          
        tmp_outline = create_collider(glob_coord, CHUNK_DIMENSIONS[0] * block_dimensions[0], CHUNK_DIMENSIONS[1] * block_dimensions[1])
        pygame.draw.polygon(self.screen, (40,150,250) , [ camera.screen_position(tmp_outline.b).into_tuple(), camera.screen_position(tmp_outline.a).into_tuple(), camera.screen_position(tmp_outline.c).into_tuple(), camera.screen_position(tmp_outline.d).into_tuple()], width = 2)

        
        for x,obj_x in enumerate(chunk.internal_objects):
            for y,obj in enumerate(obj_x):
                if obj != None:
                    if intersect(self.collider, obj.collider):
                        obj.render_collision_detected = True
                        if mouse_down:
                            chunk.set(vec2d(x,y), Ice(obj.position))

                    obj.render_collider_bounds = True



        

cpos = camera.get_position()
chunk_manager.set_all()
camera.update_position(-vec2d(window.size[0]/2,window.size[1]/2))
Player(vec2d(0,100))
Mouse()
window.run()