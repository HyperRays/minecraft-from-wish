import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),'../game-logic'))
sys.path.append(os.path.join(os.path.dirname(__file__),'../graphics'))
from prelude import *

import timeit


shape1 = Simplex2d(a=vec2d(3.89262, 4.55136),b=vec2d(2.79635, 1.67626),c=vec2d(7.45029, 1.90378))
shape2 = Simplex2d(a=vec2d(6.74703, 5.23394),b=vec2d(4.57519, 2.60705),c=vec2d(7.94671, 3.51715))

assert(intersect(shape1, shape2))

shape1 = Simplex2d(a=vec2d(3.89262, 4.55136),b=vec2d(2.79635, 1.67626),c=vec2d(7.45029, 1.90378))
shape2 = Simplex2d(a=vec2d(6.74703, 5.23394),b=vec2d(1.56227, 6.82946),c=vec2d(7.94671, 3.51715))

assert(not intersect(shape1, shape2))

shape1 = Simplex2d(a=vec2d(-16.72515, -19.45256),b=vec2d(1.67862, 25.78305),c=vec2d(-13.16747, -22.10014))
shape2 = Simplex2d(a=vec2d(6.74703, 5.23394),b=vec2d(-15, 20),c=vec2d(7.94671, 3.51715))

assert(intersect(shape1, shape2))

shape1 = Quad(a=vec2d(0,10),b=vec2d(27.35223, 28.67227),c=vec2d(30,20), d=vec2d(-7.76959, -24.18785))
shape2 = Simplex2d(a=vec2d(-16.81612, 0.11362),b=vec2d(31.43204, -26.31644), c=vec2d(2.51862, 52.44158))

assert(intersect(shape1,shape2))

#test for accuracy with larger values

increment = vec2d(0,0)
increment_step = vec2d(10,10)

for x in range(10000):

    shape1 = Simplex2d(a=vec2d(3.89262, 4.55136)+increment,b=vec2d(2.79635, 1.67626)+increment,c=vec2d(7.45029, 1.90378)+increment)
    shape2 = Simplex2d(a=vec2d(6.74703, 5.23394)+increment,b=vec2d(4.57519, 2.60705)+increment,c=vec2d(7.94671, 3.51715)+increment)

    assert(intersect(shape1, shape2))

    shape1 = Simplex2d(a=vec2d(3.89262, 4.55136)+increment,b=vec2d(2.79635, 1.67626)+increment,c=vec2d(7.45029, 1.90378)+increment)
    shape2 = Simplex2d(a=vec2d(6.74703, 5.23394)+increment,b=vec2d(1.56227, 6.82946)+increment,c=vec2d(7.94671, 3.51715)+increment)

    assert(not intersect(shape1, shape2))

    increment += increment_step

def test_intersection():
    shape1 = Simplex2d(a=vec2d(3.89262, 4.55136),b=vec2d(2.79635, 1.67626),c=vec2d(7.45029, 1.90378))
    shape2 = Simplex2d(a=vec2d(6.74703, 5.23394),b=vec2d(4.57519, 2.60705),c=vec2d(7.94671, 3.51715))

    assert(intersect(shape1, shape2))


#https://pynative.com/python-get-execution-time-of-program/
# run same code many times to get measurable data
n = 100000

# calculate total execution time
result = timeit.timeit(stmt='test_intersection()', globals=globals(), number=n)

# calculate the execution time
print(f"Execution time is {(result / n) * 10**9} Nanoseconds")
print(f"Theoretical FPS possible with 1 check: {(1/(result/n))}")