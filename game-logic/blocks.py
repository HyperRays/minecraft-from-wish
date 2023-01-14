from startup import *
from load_properties_config import load_block_properties

# stored values in variable to reduce typo errors
material_n = "material"
position_n = "position"
collider_n = "collider"

class Material:

    # remains for backward compatibility
    compat_AIR = "Air"
    compat_ICE = "Ice"
    compat_SAND = "Sand"
    compat_GRASS = "Grass"
    compat_DIRT = "Dirt"
    compat_WATER = "Water"
    compat_STONE = "Stone"
    compat_SNOW = "Snow"
    # ---
    
    AIR = 1 << 0
    ICE = 1 << 1
    SAND = 1 << 2
    GRASS = 1 << 3
    DIRT = 1 << 4
    WATER = 1 << 5
    STONE = 1 << 6
    SNOW = 1 << 7

    @staticmethod
    def map(material):
        match material:
            case Material.AIR: return Air
            case Material.ICE: return Ice
            case Material.SAND: return Sand
            case Material.GRASS: return Grass
            case Material.WATER: return Water
            case Material.STONE: return Stone
            case Material.SNOW: return Snow
    
    @staticmethod
    def __compat_map(material):
        match material:
            case Material.compat_AIR: return Air
            case Material.compat_ICE: return Ice
            case Material.compat_SAND: return Sand
            case Material.compat_GRASS: return Grass
            case Material.compat_WATER: return Water
            case Material.compat_STONE: return Stone
            case Material.compat_SNOW: return Snow
            
    
    @staticmethod
    def return_material(b: bytes):
        
        if (cls := Material.map(mat := pickle.loads(b)[material_n])) != None:
            return cls.load(b)
        else:
            if (cls := Material.__compat_map(mat := pickle.loads(b)[material_n])) != None:
                return cls.load(b)
            else:
                pass
            raise TypeError(f"No material called {mat}")

# square helper class, so that the collider creation and image (texture) loading is handled and 
class Square(GraphicsObject):
    # with slots, the object doesn't need to make a new dict for every instance
    # works like a named tuple
    # https://stackoverflow.com/a/1336890
    __slots__ = ("position", "texture", "collider","_render_collider_bounds","_render_collision_detected","_first")
    def __init__(self, position: vec2d) -> None:
        self.position = position
        self.texture = texture_handler.get_texture(self.tex_name)
        self.collider = create_collider(self.position, BLOCK_DIMENSIONS[0], -BLOCK_DIMENSIONS[1])
        self._render_collider_bounds = False
        self._render_collision_detected = False

        # only render once on the intermediate chunk texture for performance reasons (pygame)
        self._first = True
        if self.backend == "pygame":
            self.render = self.pygame_render
    
    def render_collider_bounds(self) -> None:
        self._render_collider_bounds = True
    
    def render_collision_detected(self) -> None:
        self._render_collision_detected = True

    async def pygame_render(self, x, y, chunk_intermediate_layer: pygame.Surface):
        if self._first:
            self._first = False
            chunk_intermediate_layer.blit(self.texture, (x*BLOCK_DIMENSIONS[0], y*BLOCK_DIMENSIONS[1]))

        if self._render_collider_bounds and not self._render_collision_detected:
            pygame.draw.polygon(chunk_manager.get_debug_layer(), (100,100,100) , [ camera.screen_position(self.collider.b).into_tuple(), camera.screen_position(self.collider.a).into_tuple(), camera.screen_position(self.collider.c).into_tuple(), camera.screen_position(self.collider.d).into_tuple()], width=1)
        elif self._render_collision_detected:
            pygame.draw.polygon(chunk_manager.get_debug_layer(), (200,100,120) , [ camera.screen_position(self.collider.b).into_tuple(), camera.screen_position(self.collider.a).into_tuple(), camera.screen_position(self.collider.c).into_tuple(), camera.screen_position(self.collider.d).into_tuple()] , width=2)
        
        self._render_collider_bounds = False
        self._render_collision_detected = False

    async def update(self):
        pass

    def save(self) -> bytes:
        save_dict = {
            material_n: self.material,
            position_n: self.position,
            collider_n: self.collider
        }

        return pickle.dumps(save_dict)
    
    @classmethod
    def load(cls, b: bytes):
        self = cls.__new__(cls)
        save_dict = pickle.loads(b)
        self.position = save_dict[position_n]
        self.texture = texture_handler.get_texture(cls.tex_name)
        self.collider = save_dict[collider_n]
        self._render_collider_bounds = False
        self._render_collision_detected = False

        self._first = True
        if self.backend == "pygame":
            self.render = self.pygame_render

        return self

#Air tile
class Air(Square, load_block_properties("air.toml")):

    material = Material.AIR

    #Air is transparent so has to have some custom parts defined

    def __init__(self, position: vec2d) -> None:
        self.position = position
        self.collider = create_collider(self.position, BLOCK_DIMENSIONS[0], BLOCK_DIMENSIONS[1])
        self._render_collider_bounds = False
        self._render_collision_detected = False
    
    async def update(self):
        self.collider = create_collider(self.position, BLOCK_DIMENSIONS[0], -BLOCK_DIMENSIONS[1], collider=self.collider)
        if self._render_collider_bounds and not self._render_collision_detected:
            pygame.draw.polygon(chunk_manager.get_debug_layer(), (100,100,100) , [ camera.screen_position(self.collider.b).into_tuple(), camera.screen_position(self.collider.a).into_tuple(), camera.screen_position(self.collider.c).into_tuple(), camera.screen_position(self.collider.d).into_tuple()], width=1)
        if self._render_collision_detected:
            pygame.draw.polygon(chunk_manager.get_debug_layer(), (200,100,120) , [ camera.screen_position(self.collider.b).into_tuple(), camera.screen_position(self.collider.a).into_tuple(), camera.screen_position(self.collider.c).into_tuple(), camera.screen_position(self.collider.d).into_tuple()] , width=2)
        self._render_collider_bounds = False
        self._render_collision_detected = False
    
    async def render(self, x,y,chunk_intermediate_layer: pygame.Surface):
        chunk_intermediate_layer.fill((0,0,0,0), Rect(x*BLOCK_DIMENSIONS[0], y*BLOCK_DIMENSIONS[1], BLOCK_DIMENSIONS[0], BLOCK_DIMENSIONS[1]))

    @classmethod
    def load(cls, b: bytes):
        self = cls.__new__(cls)
        save_dict = pickle.loads(b)
        self.position = save_dict[position_n]
        self.collider = save_dict[collider_n]
        self._render_collider_bounds = False
        self._render_collision_detected = False

        return self

#other tiles
class Ice(Square, load_block_properties("ice.toml")):
    material = Material.ICE
    tex_name = "Ice" 
    texture_handler.load_texture(tex_name, "ice_block.png")   
    texture_handler.rescale_image(tex_name, height=BLOCK_DIMENSIONS[0], width=BLOCK_DIMENSIONS[1])

class Sand(Square, load_block_properties("sand.toml")):
    material = Material.SAND
    tex_name = "Sand" 
    texture_handler.load_texture(tex_name, "sand_block.png")   
    texture_handler.rescale_image(tex_name, height=BLOCK_DIMENSIONS[0], width=BLOCK_DIMENSIONS[1])
    
class Grass(Square, load_block_properties("grass.toml")):
    material = Material.GRASS
    tex_name = "Grass" 
    texture_handler.load_texture(tex_name, "grass_block.png")   
    texture_handler.rescale_image(tex_name, height=BLOCK_DIMENSIONS[0], width=BLOCK_DIMENSIONS[1])

    graphics.create_layer("grass_layer")

    # grass should be in front of the player
    async def pygame_render(self, *_):
        graphics.layers["grass_layer"].blit(self.texture, camera.screen_position(self.position).into_tuple())

class Dirt(Square, load_block_properties("dirt.toml")):
    material = Material.DIRT
    tex_name = "Dirt" 
    texture_handler.load_texture(tex_name, "dirt_block.png")   
    texture_handler.rescale_image(tex_name, height=BLOCK_DIMENSIONS[0], width=BLOCK_DIMENSIONS[1])

class Stone(Square, load_block_properties("stone.toml")):
    material = Material.STONE
    tex_name = "Stone" 
    texture_handler.load_texture(tex_name, "stone_block.png")   
    texture_handler.rescale_image(tex_name, height=BLOCK_DIMENSIONS[0], width=BLOCK_DIMENSIONS[1])

class Snow(Square, load_block_properties("snow.toml")):
    material = Material.SNOW
    tex_name = "Snow" 
    texture_handler.load_texture(tex_name, "snow_block.png")   
    texture_handler.rescale_image(tex_name, height=BLOCK_DIMENSIONS[0], width=BLOCK_DIMENSIONS[1])

#Water is special, because it is animated
class Water(Square, load_block_properties("water.toml")):

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
        self.collider = create_collider(self.position, BLOCK_DIMENSIONS[0], -BLOCK_DIMENSIONS[1])

        #set the debugging outlines of the collider
        self._render_collider_bounds = False
        self._render_collision_detected = False

        self._updated = True
        if self.backend == "pygame":
            self.render = self.pygame_render
    
    async def pygame_render(self, x,y,chunk_intermediate_layer: pygame.Surface):

        if self._updated:
            self._updated = False
            chunk_intermediate_layer.blit(self.texture, (x*BLOCK_DIMENSIONS[0], y*BLOCK_DIMENSIONS[1]))

        #setting the collider outlines and collision boundaries
        if self._render_collider_bounds and not self._render_collision_detected:
            pygame.draw.polygon(chunk_manager.get_debug_layer(), (100,100,100) , [ camera.screen_position(self.collider.b).into_tuple(), camera.screen_position(self.collider.a).into_tuple(), camera.screen_position(self.collider.c).into_tuple(), camera.screen_position(self.collider.d).into_tuple()], width=1)
        if self._render_collision_detected:
            pygame.draw.polygon(chunk_manager.get_debug_layer(), (200,100,120) , [ camera.screen_position(self.collider.b).into_tuple(), camera.screen_position(self.collider.a).into_tuple(), camera.screen_position(self.collider.c).into_tuple(), camera.screen_position(self.collider.d).into_tuple()] , width=2)
        
        self._render_collider_bounds = False
        self._render_collision_detected = False
    

    async def update(self):
        #renew the collider and render the image
        # self.collider = create_collider(self.position, BLOCK_DIMENSIONS[0], -BLOCK_DIMENSIONS[1], collider=self.collider)
        # self.render()

        #after certain time switch the textures
        self.timer.poll()
        if self.timer.reached():
            self._updated = True
            if self.current_tex == 0:
                self.current_tex = 1
                self.texture = self.texture2
            else:
                self.current_tex = 0
                self.texture = self.texture1
            
            self.timer.reset()

    
    def save(self) -> bytes:
        save_dict = {
            material_n: Material.WATER,
            position_n: self.position,
            "current_tex": self.current_tex,
            collider_n: self.collider
        }

        return pickle.dumps(save_dict)

    @classmethod
    def load(cls, b: bytes):
        self = cls.__new__(cls)
        save_dict = pickle.loads(b)
        self.timer = Timed(7_000_000_00)
        self.position = save_dict[position_n]
        self.current_tex = save_dict["current_tex"]
        self.texture1 = texture_handler.get_texture(cls.tex_name1)
        self.texture2 = texture_handler.get_texture(cls.tex_name2)
        self.collider = save_dict[collider_n]
        self._render_collider_bounds = False
        self._render_collision_detected = False

        if self.current_tex == 0:
            self.texture = self.texture1
        else:
            self.texture = self.texture2
        
        self._updated = True
        if self.backend == "pygame":
            self.render = self.pygame_render

        return self