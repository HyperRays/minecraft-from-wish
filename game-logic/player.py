from startup import *
from blocks import *
from terrain_generation import *
from load_properties_config import load_player_properties

# the Directions are actually just vectors, so they have to be turned into names
def _repr_Directions(dir: Directions) -> str:
    match dir:
        case Directions.up: return "up"
        case Directions.down: return "down"
        case Directions.left: return "left"
        case Directions.right: return "right"

input_timer = Timed(30_000_000_0)

class Player(GraphicsObject, load_player_properties()):

    graphics.create_layer("player_layer")
    player_layer = graphics.layers["player_layer"]

    graphics.create_layer("player_debug_layer")
    player_debug_layer = graphics.layers["player_debug_layer"]

    tex_name = "Player" 
    texture_handler.load_texture(tex_name, "test_images/batman.png")   
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

        # in which direction the player is colliding (needs to be improved)
        self.collided_dir = {
            Directions.up: False,
            Directions.down: False,
            Directions.left: False,
            Directions.right: False
        }
        
        self.furthest_dist: dict[Directions, vec2d] = {
            Directions.up: vec2d(0,0),
            Directions.down: vec2d(0,0),
            Directions.left: vec2d(0,0),
            Directions.right: vec2d(0,0)
        }

        self.debug_mode = False

        # create window boundaries (so that the chunks can get loaded in and out dynamically)
        self.window_quad = create_collider(camera.get_position() + vec2d(window.size[0]/2,window.size[1]/2), window.size[0], window.size[1])
        
        # internal refrence to chunk manager
        self.chunk_mgr = chunk_manager

    def save(self) -> bytes:
        save_dict = {
            "position": self.position,
            "collider": self.collider
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
        
        # create window boundaries (so that the chunks can get loaded in and out dynamically)
        self.window_quad = create_collider(camera.get_position(), window.size[0], window.size[1])
    
        # the forces that are applied to the player
        self.force = vec2d(0,0)

        # in which direction the player is colliding (bad)
        self.collided_dir = {
            Directions.up: False,
            Directions.down: False,
            Directions.left: False,
            Directions.right: False
        }

        self.furthest_dist = {
            Directions.up: vec2d(0,0),
            Directions.down: vec2d(0,0),
            Directions.left: vec2d(0,0),
            Directions.right: vec2d(0,0)
        }

        self.debug_mode = False

        return self

    async def render(self):
        # render the image of the player to the screen accoring to the camera
        self.player_layer.blit(self.texture, camera.screen_position(self.position).into_tuple())

        # draws a outline around the chunk (for debugging purposes only)
        for chunk in self.chunks:
            pygame.draw.polygon(self.player_debug_layer, (40,150,250) , [ camera.screen_position(chunk.collider.b).into_tuple(), camera.screen_position(chunk.collider.a).into_tuple(), camera.screen_position(chunk.collider.c).into_tuple(), camera.screen_position(chunk.collider.d).into_tuple()], width = 2)
        
        # draws the collider around the player (for debugging purposes only)
        pygame.draw.polygon(self.player_debug_layer, (100,200,140) , [ camera.screen_position(self.collider.b).into_tuple(), camera.screen_position(self.collider.a).into_tuple(), camera.screen_position(self.collider.c).into_tuple(), camera.screen_position(self.collider.d).into_tuple()], width=1)


    async def update(self):

        # "continuous collision detection" kind of
        # displacement = vec2d(0,0)
        # tmp_displacement = sum(self.furthest_dist.values(), start= vec2d(0,0))
        # print(tmp_displacement, self.furthest_dist.values())

        # checks in which direction the player is colliding and sets the force in that axis to 0 (bad)
        if self.collided_dir[Directions.down]:
            if self.force.y < 0:
                # displacement.y += (tmp_displacement.y > 0) * tmp_displacement.y
                self.force.y = 0
        if self.collided_dir[Directions.up]:
            if self.force.y > 0:
                # displacement.y += (tmp_displacement.y < 0) * tmp_displacement.y
                self.force.y = 0
        if self.collided_dir[Directions.right]:
            if self.force.x > 0:
                # displacement.x += tmp_displacement.x
                self.force.x = 0
        if self.collided_dir[Directions.left]:
            if self.force.x < 0:
                # displacement.x += tmp_displacement.x
                self.force.x = 0

        self.force.x = self.force.x * self.speed_multiplier

        # adds force to player 
        
        self.position += self.force

        #finds in which chunk the player is in through the chunk manager
        true_chunksize_width = BLOCK_DIMENSIONS[0] * CHUNK_DIMENSIONS[0]
        true_chunksize_height = BLOCK_DIMENSIONS[1] * CHUNK_DIMENSIONS[1]

        # renews collider and updates rendered/updated chunks only on movement
        if self.force != vec2d(0,0):
            self.collider = create_collider(self.position, self.w, -self.h, collider=self.collider)

            # use the window boundaries to find sout which chunks to update
            self.window_quad = create_collider(camera.get_position(), window.size[0], -window.size[1], collider= self.window_quad)
                    
            render_boundaries =     (chunk_manager.find_chunk_pos(self.window_quad.a + vec2d(0, CHUNK_DIMENSIONS[1]), vec2d(true_chunksize_width, true_chunksize_height)),
                                    chunk_manager.find_chunk_pos(self.window_quad.b + vec2d(0, CHUNK_DIMENSIONS[1]), vec2d(true_chunksize_width, true_chunksize_height)),
                                    chunk_manager.find_chunk_pos(self.window_quad.c + vec2d(0, CHUNK_DIMENSIONS[1]), vec2d(true_chunksize_width, true_chunksize_height)),
                                    chunk_manager.find_chunk_pos(self.window_quad.d + vec2d(0, CHUNK_DIMENSIONS[1]), vec2d(true_chunksize_width, true_chunksize_height)),
                                    )
            
            # one chunk margin to have smooth transition
            x_upper_bound = render_boundaries[1].x+1
            x_lower_bound = render_boundaries[0].x-1
        
            y_upper_bound = render_boundaries[0].y+1
            y_lower_bound = render_boundaries[2].y-1

            bounds_min = vec2d(x_lower_bound, y_lower_bound)
            bounds_max = vec2d(x_upper_bound,y_upper_bound)

            chunk_manager.set_renderables(bounds_max, bounds_min, terrain_gen)
            chunk_manager.set_updateables(bounds_max, bounds_min, terrain_gen)

        chunks_coords: set[vec2d] = set(
            (chunk_manager.find_chunk_pos(self.collider.a + vec2d(0, CHUNK_DIMENSIONS[1]), vec2d(true_chunksize_width, true_chunksize_height)),
            chunk_manager.find_chunk_pos(self.collider.b + vec2d(0, CHUNK_DIMENSIONS[1]), vec2d(true_chunksize_width, true_chunksize_height)),
            chunk_manager.find_chunk_pos(self.collider.c + vec2d(0, CHUNK_DIMENSIONS[1]), vec2d(true_chunksize_width, true_chunksize_height)),
            chunk_manager.find_chunk_pos(self.collider.d + vec2d(0, CHUNK_DIMENSIONS[1]), vec2d(true_chunksize_width, true_chunksize_height)),
            )
        )

        self.chunks: list[Chunk] = []
        for chunk_pos in chunks_coords:
            self.chunks += [chunk_manager.get_chunk(chunk_pos)]

        #resets all the forces
        self.force = vec2d(0,0)
        self.collided_dir = {
            Directions.up: False,
            Directions.down: False,
            Directions.left: False,
            Directions.right: False
        }
        
        # go though all objects in the chunks in which the player is in and find out with which one it is colliding with
        for chunk in self.chunks:
            for x,obj_x in enumerate(chunk.internal_objects):
                for y,obj in enumerate(obj_x):
                        obj.render_collider_bounds()
                        if obj != None and obj.collision:
                            if intersect(self.collider, obj.collider):

                                obj.render_collision_detected()

                                self.speed_multiplier = obj.speed_multiplier

                                b = adjacency_bytes(chunk, vec2d(x,y), chunk_manager)
                                poss = collision_possibile_dir(b)
                                if len(poss) == 0:
                                    self.force.y += 100
                                    self.collided_dir[Directions.down] = True
                                    continue
                                dir = -relative_position(obj.collider, self.collider, list(poss))

                                # _c = (_a := self.collider.furthest_in_dir(dir)).dot(_a) - (_b := obj.collider.furthest_in_dir(-dir)).dot(_b)
                                # if _c > self.furthest_dist[dir].dot(self.furthest_dist[dir]):
                                #     self.furthest_dist[dir] = _c

                                self.collided_dir[dir] = True


        #adds the gravity force
        self.force += vec2d(0,-GRAVITY_ACCEL)

    async def input(self, keys):
        # adds to force and controlls in which direction the player moves
        if keys[store.characters["s"]]:
                self.force.y -= PLAYER_SPEED

        # elif keys[self.characters["w"]]:
        #     self.force.y += PLAYER_SPEED
        
        if keys[store.characters["d"]]:
            self.force.x += PLAYER_SPEED

        elif keys[store.characters["a"]]:
            self.force.x -= PLAYER_SPEED
        
        if keys[store.characters["space"]] and self.collided_dir[Directions.down]:
            self.force.y += BLOCK_DIMENSIONS[0]*1.25

        #closes the programm (for debugging purposes only)
        if keys[store.characters["e"]]:
            sys.exit()

        if keys[store.characters["v"]]:
            print("saving")
            self.chunk_mgr.save(input("path to file: "))

        if keys[store.characters["t"]]:
            # test saving/loading texture handler
            print(TextureHandler.load( texture_handler.save() ))

        if keys[store.characters["p"]]:
            # test saving/loading player
            print(Player.load( self.save() ))
        
        if keys[store.characters["l"]]:
            print("loading")
            chunk_manager.redefine(ChunkManager.load(input("path to file: ")))

            #finds in which chunk the player is in through the cunk manager
            true_chunksize_width = BLOCK_DIMENSIONS[0] * CHUNK_DIMENSIONS[0]
            true_chunksize_height = BLOCK_DIMENSIONS[1] * CHUNK_DIMENSIONS[1]

            render_boundaries =     (chunk_manager.find_chunk_pos(self.window_quad.a + vec2d(0, CHUNK_DIMENSIONS[1]), vec2d(true_chunksize_width, true_chunksize_height)),
                        chunk_manager.find_chunk_pos(self.window_quad.b + vec2d(0, CHUNK_DIMENSIONS[1]), vec2d(true_chunksize_width, true_chunksize_height)),
                        chunk_manager.find_chunk_pos(self.window_quad.c + vec2d(0, CHUNK_DIMENSIONS[1]), vec2d(true_chunksize_width, true_chunksize_height)),
                        chunk_manager.find_chunk_pos(self.window_quad.d + vec2d(0, CHUNK_DIMENSIONS[1]), vec2d(true_chunksize_width, true_chunksize_height)),
                        )
        
            margin = 1
        
            x_upper_bound = render_boundaries[1].x+margin
            x_lower_bound = render_boundaries[0].x-margin
        
            y_upper_bound = render_boundaries[0].y+margin
            y_lower_bound = render_boundaries[2].y-margin

            bounds_min = vec2d(x_lower_bound, y_lower_bound)
            bounds_max = vec2d(x_upper_bound,y_upper_bound)

            chunk_manager.set_renderables(bounds_max, bounds_min, terrain_gen)
            chunk_manager.set_updateables(bounds_max, bounds_min, terrain_gen)
        
        input_timer.poll()
        if input_timer.reached():
            if keys[store.characters["F3"]]:
                input_timer.reset()
                if self.debug_mode:
                    self.debug_mode = not self.debug_mode
                    graphics.set_render_layers(["bg","chunks_layer", "player_layer", "grass_layer", "day-night-overlay", "mouse_layer"])
                else:
                    self.debug_mode = not self.debug_mode
                    graphics.set_render_layers(["bg", "chunks_layer",  "player_layer", "grass_layer", "day-night-overlay", "mouse_layer", "chunks_debug", "player_debug_layer", "mouse_debug_layer"])
            
            input_timer.reset()

        #TODO - https://www.gamedeveloper.com/programming/improved-lerp-smoothing-
        #updates the camera position, so that the player stays in the center
        camera.update_position(self.position - vec2d(window.size[0]/2,-window.size[1]/2))
