from startup import *
from load_block_config import *

#stored values in variable to reduce typo errors
material_n = "material"
position_n = "position"
collider_n = "collider"

class Material:
    
    AIR = "Air"
    ICE = "Ice"
    SAND = "Sand"
    GRASS = "Grass"
    DIRT = "Dirt"
    WATER = "Water"

    @staticmethod
    def map(material):
        match material:
            case Material.AIR: return Air
            case Material.ICE: return Ice
            case Material.SAND: return Sand
            case Material.GRASS: return Grass
            case Material.WATER: return Water
    
    @staticmethod
    def return_material(b: bytes):
        
        if (cls := Material.map(mat := pickle.loads(b)[material_n])) != None:
            return cls.load(b)
        else:
            raise TypeError(f"No material called {mat}")

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
        self.render_collider_bounds = False
        self.render_collision_detected = False

        return self

#Air tile
class Air(Square, load_block_properties("air.toml")):

    #Air is transparent so has to have some custom parts defined

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
    
    async def render(self):
        pass

    @classmethod
    def load(cls, b: bytes):
        self = cls.__new__(cls)
        save_dict = pickle.loads(b)
        self.position = save_dict[position_n]
        self.collider = save_dict[collider_n]
        self.render_collider_bounds = False
        self.render_collision_detected = False

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

class Dirt(Square, load_block_properties("grass.toml")):
    material = Material.DIRT
    tex_name = "Dirt" 
    texture_handler.load_texture(tex_name, "dirt_block.png")   
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
        self.render_collider_bounds = False
        self.render_collision_detected = False

        if self.current_tex == 0:
            self.texture = self.texture1
        else:
            self.texture = self.texture2

        return self