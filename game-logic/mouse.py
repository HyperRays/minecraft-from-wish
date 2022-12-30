from startup import *
from blocks import *
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
                        print(chunk.collision_possiblites(vec2d(x,y)),end="\r")
                        #set the block to something else if the mouse is pressed
                        if mouse_down_left:
                            chunk.set(vec2d(x,y), Ice(obj.position))
                        if mouse_down_right:
                            chunk.set(vec2d(x,y), Air(obj.position))

                    obj.render_collider_bounds = True

        
