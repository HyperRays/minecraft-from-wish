from startup import *
from blocks import *
from terrain_generation import *

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
        self.window_quad = create_collider(camera.get_position(), window.size[0], -window.size[1])
    
        # the forces that are applied to the player
        self.force = vec2d(0,0)

        # in which direction the player is colliding (bad)
        self.collided_dir = {
            Directions.up: False,
            Directions.down: False,
            Directions.left: False,
            Directions.right: False
        }

        self.window_quad = create_collider(camera.get_position() + vec2d(window.size[0]/2,window.size[1]/2), window.size[0], -window.size[1])
        
        self.chunk_mgr = chunk_manager
        self.speed_mult = 1

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

        self.window_quad = create_collider(camera.get_position(), window.size[0], -window.size[1])
    
        # the forces that are applied to the player
        self.force = vec2d(0,0)

        # in which direction the player is colliding (bad)
        self.collided_dir = {
            Directions.up: False,
            Directions.down: False,
            Directions.left: False,
            Directions.right: False
        }
        self.speed_mult = 1
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
        self.force.x = self.force.x * self.speed_mult
        self.position += self.force
        self.speed_mult = 1
        # renews collider
        self.collider = create_collider(self.position, self.w, -self.h, collider=self.collider)

        #finds in which chunk the player is in through the cunk manager
        true_chunksize_width = BLOCK_DIMENSIONS[0] * CHUNK_DIMENSIONS[0]
        true_chunksize_height = BLOCK_DIMENSIONS[1] * CHUNK_DIMENSIONS[1]

        self.window_quad = create_collider(camera.get_position(), window.size[0], -window.size[1], collider= self.window_quad)
                   
        render_boundaries =     (chunk_manager.find_chunk_pos(self.window_quad.a + vec2d(0, CHUNK_DIMENSIONS[1]), vec2d(true_chunksize_width, true_chunksize_height)),
                                chunk_manager.find_chunk_pos(self.window_quad.b + vec2d(0, CHUNK_DIMENSIONS[1]), vec2d(true_chunksize_width, true_chunksize_height)),
                                chunk_manager.find_chunk_pos(self.window_quad.c + vec2d(0, CHUNK_DIMENSIONS[1]), vec2d(true_chunksize_width, true_chunksize_height)),
                                chunk_manager.find_chunk_pos(self.window_quad.d + vec2d(0, CHUNK_DIMENSIONS[1]), vec2d(true_chunksize_width, true_chunksize_height)),
                                )
        
        x_upper_bound = render_boundaries[1].x+1
        x_lower_bound = render_boundaries[0].x-1
    
        y_upper_bound = render_boundaries[0].y+1
        y_lower_bound = render_boundaries[2].y-1

        bounds_min = vec2d(x_lower_bound, y_lower_bound)
        bounds_max = vec2d(x_upper_bound,y_upper_bound)

        chunk_manager.set_renderables(bounds_max, bounds_min, test_render)
                        
        chunks_coords: set[vec2d] = set(
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
                if obj != None and obj.collision:
                    if intersect(self.collider, obj.collider):
                        self.speed_mult = obj.speed_mutiplier
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
            self.chunk_mgr .save()
        
        if keys[self.characters["l"]]:
            print("loading")
            chunk_manager.redifine(ChunkManager.load())

            #finds in which chunk the player is in through the cunk manager
            true_chunksize_width = BLOCK_DIMENSIONS[0] * CHUNK_DIMENSIONS[0]
            true_chunksize_height = BLOCK_DIMENSIONS[1] * CHUNK_DIMENSIONS[1]

            render_boundaries =     (chunk_manager.find_chunk_pos(self.window_quad.a + vec2d(0, CHUNK_DIMENSIONS[1]), vec2d(true_chunksize_width, true_chunksize_height)),
                        chunk_manager.find_chunk_pos(self.window_quad.b + vec2d(0, CHUNK_DIMENSIONS[1]), vec2d(true_chunksize_width, true_chunksize_height)),
                        chunk_manager.find_chunk_pos(self.window_quad.c + vec2d(0, CHUNK_DIMENSIONS[1]), vec2d(true_chunksize_width, true_chunksize_height)),
                        chunk_manager.find_chunk_pos(self.window_quad.d + vec2d(0, CHUNK_DIMENSIONS[1]), vec2d(true_chunksize_width, true_chunksize_height)),
                        )
        
            x_upper_bound = render_boundaries[1].x+1
            x_lower_bound = render_boundaries[0].x-1
        
            y_upper_bound = render_boundaries[0].y+1
            y_lower_bound = render_boundaries[2].y-1

            bounds_min = vec2d(x_lower_bound, y_lower_bound)
            bounds_max = vec2d(x_upper_bound,y_upper_bound)

            chunk_manager.set_renderables(bounds_max, bounds_min, test_render)