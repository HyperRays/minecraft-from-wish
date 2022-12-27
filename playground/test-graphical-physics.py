import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),'../game-logic'))
sys.path.append(os.path.join(os.path.dirname(__file__),'../graphics'))
from prelude import *

camera = Camera()
camera.update_position(vec2d(0,0))
window.init((500,500), "test physics")
other = None


class static_shape(GraphicsObject):
    def __init__(self, shape) -> None:
        self.shape = shape
        super().__init__()
    
    def render(self):
        if (result := intersect(self.shape, other.shape, points=True))[0]:
            pygame.draw.polygon(self.screen, (100,100,100) , [ 
                camera.screen_position(self.shape.b).into_tuple(), 
                camera.screen_position(self.shape.a).into_tuple(), 
                camera.screen_position(self.shape.c).into_tuple()
                ])
        else:
            pygame.draw.polygon(self.screen, (100,200,200) , [ 
                camera.screen_position(self.shape.b).into_tuple(), 
                camera.screen_position(self.shape.a).into_tuple(), 
                camera.screen_position(self.shape.c).into_tuple()
                ])

        points = result[2]
        pygame.draw.line(window.screen, (255, 50, 255), camera.screen_position(points[0]).into_tuple(), camera.screen_position(points[1]).into_tuple())

    async def update(self):
        self.render()

class static_quad(static_shape):
    def render(self):
        if (result := intersect(self.shape, other.shape, points=True))[0]:
            pygame.draw.polygon(self.screen, (100,100,100) , [ 
                camera.screen_position(self.shape.b).into_tuple(), 
                camera.screen_position(self.shape.a).into_tuple(), 
                camera.screen_position(self.shape.c).into_tuple(), 
                camera.screen_position(self.shape.d).into_tuple()
                ])
        else:
            pygame.draw.polygon(self.screen, (100,200,200) , [ 
                camera.screen_position(self.shape.b).into_tuple(), 
                camera.screen_position(self.shape.a).into_tuple(), 
                camera.screen_position(self.shape.c).into_tuple(), 
                camera.screen_position(self.shape.d).into_tuple()
                ])

        points = result[2]
        pygame.draw.line(window.screen, (255, 50, 255), camera.screen_position(points[0]).into_tuple(), camera.screen_position(points[1]).into_tuple())

class moveable_shape(static_shape):
    def __init__(self, shape) -> None:
        super().__init__(shape)
    
    def render(self):
        pygame.draw.polygon(self.screen, (100,100,100) , [ camera.screen_position(self.shape.b).into_tuple(), camera.screen_position(self.shape.a).into_tuple(), camera.screen_position(self.shape.c).into_tuple()], width = 2)

    async def input(self, keys):
        self.shape.a += vec2d(0,0)
        self.shape.b += vec2d(0,0)
        self.shape.c += vec2d(0,0)

        speed = 2
        if keys[store.characters["w"]]:
            self.shape.a += vec2d(0,speed)
            self.shape.b += vec2d(0,speed)
            self.shape.c += vec2d(0,speed)

        elif keys[store.characters["s"]]:
            self.shape.a += vec2d(0,-speed)
            self.shape.b += vec2d(0,-speed)
            self.shape.c += vec2d(0,-speed)
        
        if keys[store.characters["a"]]:
            self.shape.a += vec2d(-speed,0)
            self.shape.b += vec2d(-speed,0)
            self.shape.c += vec2d(-speed,0)

        elif keys[store.characters["d"]]:
            self.shape.a += vec2d(speed,0)
            self.shape.b += vec2d(speed,0)
            self.shape.c += vec2d(speed,0)

class mouse(static_shape):
    def __init__(self, shape) -> None:
        super().__init__(shape)

    def render(self):
        pass
    
    async def input(self, _):
        (x,y) = pygame.mouse.get_pos()
        pos = vec2d(x,-y)
        self.shape.a = pos

#from dist test ./test-physics.py
shape1 = Simplex2d(a=vec2d(0,0), b=vec2d(0,100), c=vec2d(100,0))
shape1q = Quad(a=vec2d(0,0), b=vec2d(0,100), c=vec2d(100,0), d=vec2d(100,100))
shape2 = Simplex2d(a=vec2d(300,100), b=vec2d(200,0), c=vec2d(300,0))

shift = vec2d(100,-200)
shape1.a += shift
shape1.b += shift
shape1.c += shift

shape2.a += shift
shape2.b += shift
shape2.c += shift

shape1q.a += shift
shape1q.b += shift
shape1q.c += shift
shape1q.d += shift


dpos = vec2d(50,-50)
static_quad(shape1q)
# other = moveable_shape(shape2)
other = mouse(Point(vec2d(0,0)))



window.run()