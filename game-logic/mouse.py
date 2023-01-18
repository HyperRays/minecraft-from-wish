from startup import *
from blocks import *
from player import Player
class Mouse(GraphicsObject):

    graphics.create_layer("mouse_layer")
    mouse_layer = graphics.layers["mouse_layer"]

    graphics.create_layer("mouse_debug_layer")
    mouse_debug_layer = graphics.layers["mouse_debug_layer"]


    def __init__(self) -> None:
        super().__init__()
        self.collider = Point(vec2d(0,0))
        for obj in self.objects:
            if type(obj) == Player:
                self.player = obj

        self.current_mat = None

        #hide the cursor
        #https://stackoverflow.com/a/40628090
        pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))

    def save(self) -> bytes:
        return bytes(0)

    @classmethod
    def load(cls, _: bytes):
        
        self = cls.__new__(cls)
        self.collider = Point(vec2d(0,0))

        self.current_mat = Material.AIR

        for obj in self.objects:
            if type(obj) == Player:
                self.player = obj


        #hide the cursor
        #https://stackoverflow.com/a/40628090
        pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
        return self

    async def render(self):
        #draw in the mouse pointer (we can change this)
        pygame.draw.circle(self.mouse_layer, (100,200,100), (self.pos.x,-self.pos.y), 5)

        glob_coord = vec2d(self.chunk.position.x * CHUNK_DIMENSIONS[0] * BLOCK_DIMENSIONS[0], self.chunk.position.y * CHUNK_DIMENSIONS[1] * BLOCK_DIMENSIONS[1] - BLOCK_DIMENSIONS[1])
        # create the chunk outline (for debugging purposes only)
        tmp_outline = create_collider(glob_coord, CHUNK_DIMENSIONS[0] * BLOCK_DIMENSIONS[0], CHUNK_DIMENSIONS[1] * BLOCK_DIMENSIONS[1])
        pygame.draw.polygon(self.mouse_debug_layer, (40,150,250) , [ camera.screen_position(tmp_outline.b).into_tuple(), camera.screen_position(tmp_outline.a).into_tuple(), camera.screen_position(tmp_outline.c).into_tuple(), camera.screen_position(tmp_outline.d).into_tuple()], width = 2)

    
    async def input(self, key):
        #update all the mouse events (update which keys have been pressed)
        pygame.event.get()
        #get the mouse position and set the pointer (dot) positon
        (x,y) = pygame.mouse.get_pos()
        self.pos = vec2d(x,-y)
        self.collider.a = self.pos + camera.get_position()

        #get if a mouse button has been pressed
        mouse_down_left = pygame.mouse.get_pressed()[0]
        mouse_down_right = pygame.mouse.get_pressed()[2]

        # get in which chunk the player is in
        true_chunksize_width = BLOCK_DIMENSIONS[0] * CHUNK_DIMENSIONS[0]
        true_chunksize_height = BLOCK_DIMENSIONS[1] * CHUNK_DIMENSIONS[1]
        chunk_coord: vec2d = chunk_manager.find_chunk_pos(self.collider.a + vec2d(0, CHUNK_DIMENSIONS[1]), vec2d(true_chunksize_width, true_chunksize_height))
        try:
            self.chunk: Chunk = chunk_manager.get_chunk(chunk_coord)
        except KeyError:
            pass

        if key[store.characters["1"]]:
            self.current_mat = Material.DIRT
        elif key[store.characters["2"]]:
            self.current_mat = Material.GRASS
        elif key[store.characters["3"]]:
            self.current_mat = Material.ICE
        elif key[store.characters["4"]]:
            self.current_mat = Material.SAND
        elif key[store.characters["5"]]:
            self.current_mat = Material.SNOW
        elif key[store.characters["6"]]:
            self.current_mat = Material.STONE
        elif key[store.characters["7"]]:
            self.current_mat = Material.WATER
        elif key[store.characters["escape"]]:
            self.current_mat = Material.AIR

        if not intersect(self.collider, self.player.collider):
            # go through every block in the chunk and find which one the mouse is on
            for x,obj_x in enumerate(self.chunk.internal_objects):
                for y,obj in enumerate(obj_x):
                    if obj != None:
                        if intersect(self.collider, obj.collider):
                            obj.render_collision_detected()
                            #set the block to something else if the mouse is pressed
                            if mouse_down_left:
                                # print(Material.map(self.current_mat), bin(self.current_mat))
                                if (mat := Material.map(self.current_mat)) != None:
                                    self.chunk.set(vec2d(x,y), mat(obj.position))
                            if mouse_down_right and obj.mineable:
                                self.chunk.set(vec2d(x,y), Air(obj.position))

                        obj.render_collider_bounds()
        
