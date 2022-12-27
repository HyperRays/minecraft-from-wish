import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),'../game-logic'))
sys.path.append(os.path.join(os.path.dirname(__file__),'../graphics'))
from prelude import *

import timeit

print(f"\n{bcolors.BOLD}{bcolors.OKBLUE}Physics Test{bcolors.ENDC}{bcolors.ENDC}\n")

print(f"\nStarting simple Tests")

try:
    shape1 = Simplex2d(a=vec2d(3.89262, 4.55136),b=vec2d(2.79635, 1.67626),c=vec2d(7.45029, 1.90378))
    shape2 = Simplex2d(a=vec2d(6.74703, 5.23394),b=vec2d(4.57519, 2.60705),c=vec2d(7.94671, 3.51715))

    assert intersect(shape1, shape2), "simple intersect" 

    shape1 = Simplex2d(a=vec2d(3.89262, 4.55136),b=vec2d(2.79635, 1.67626),c=vec2d(7.45029, 1.90378))
    shape2 = Simplex2d(a=vec2d(6.74703, 5.23394),b=vec2d(1.56227, 6.82946),c=vec2d(7.94671, 3.51715))

    assert not intersect(shape1, shape2), "simple not intersect"

    shape1 = Simplex2d(a=vec2d(-16.72515, -19.45256),b=vec2d(1.67862, 25.78305),c=vec2d(-13.16747, -22.10014))
    shape2 = Simplex2d(a=vec2d(6.74703, 5.23394),b=vec2d(-15, 20),c=vec2d(7.94671, 3.51715))

    assert intersect(shape1, shape2), "simple cover" 

    shape1 = Quad(a=vec2d(0,10),b=vec2d(27.35223, 28.67227),c=vec2d(30,20), d=vec2d(-7.76959, -24.18785))
    shape2 = Simplex2d(a=vec2d(-16.81612, 0.11362),b=vec2d(31.43204, -26.31644), c=vec2d(2.51862, 52.44158))

    assert intersect(shape1,shape2), "Quad-Simplex2d intersect"
    print(f"{bcolors.OKGREEN}Passed{bcolors.ENDC}\n")

except Exception as e:
    print(f"{bcolors.FAIL}Failed{bcolors.ENDC} with error at {e}\n")


#test for accuracy with larger values


print(f"\nStarting Tests for shapes far from origin")
increment = vec2d(10000000,10000000)
increment_step = vec2d(10,10)

try:
    for x in range(10000):

        shape1 = Simplex2d(a=vec2d(3.89262, 4.55136)+increment,b=vec2d(2.79635, 1.67626)+increment,c=vec2d(7.45029, 1.90378)+increment)
        shape2 = Simplex2d(a=vec2d(6.74703, 5.23394)+increment,b=vec2d(4.57519, 2.60705)+increment,c=vec2d(7.94671, 3.51715)+increment)

        assert intersect(shape1, shape2), "intersect large values"

        shape1 = Simplex2d(a=vec2d(3.89262, 4.55136)+increment,b=vec2d(2.79635, 1.67626)+increment,c=vec2d(7.45029, 1.90378)+increment)
        shape2 = Simplex2d(a=vec2d(6.74703, 5.23394)+increment,b=vec2d(1.56227, 6.82946)+increment,c=vec2d(7.94671, 3.51715)+increment)

        assert not intersect(shape1, shape2), "not intersect large values"

        increment += increment_step

    
    print(f"{bcolors.OKGREEN}Passed{bcolors.ENDC}\n")

except Exception as e:
    print(f"{bcolors.FAIL}Failed{bcolors.ENDC} with error at {e}\n")

print(f"\nStarting Test for distance")

try:

    shape1 = Simplex2d(a=vec2d(0,0), b=vec2d(0,1), c=vec2d(1,0))
    shape2 = Simplex2d(a=vec2d(3,1), b=vec2d(2,0), c=vec2d(3,0))

    (intersects, dist) = intersect(shape1, shape2, dist=True)

    assert (intersects, dist) == (False, 1), f"distance check expected {(False, 1)}, got {(intersects, dist)}"

    print(f"{bcolors.OKGREEN}Passed{bcolors.ENDC}\n")

except Exception as e:
    print(f"{bcolors.FAIL}Failed{bcolors.ENDC} with error at {e}\n")


def test_intersection():
    shape1 = Simplex2d(a=vec2d(3.89262, 4.55136),b=vec2d(2.79635, 1.67626),c=vec2d(7.45029, 1.90378))
    shape2 = Simplex2d(a=vec2d(6.74703, 5.23394),b=vec2d(4.57519, 2.60705),c=vec2d(7.94671, 3.51715))

    assert intersect(shape1, shape2)

def test_intersection_dist():
    shape1 = Simplex2d(a=vec2d(3.89262, 4.55136),b=vec2d(2.79635, 1.67626),c=vec2d(7.45029, 1.90378))
    shape2 = Simplex2d(a=vec2d(6.74703, 5.23394),b=vec2d(4.57519, 2.60705),c=vec2d(7.94671, 3.51715))

    assert intersect(shape1, shape2, dist=True)[0]

def test_intersection_points():
    shape1 = Simplex2d(a=vec2d(3.89262, 4.55136),b=vec2d(2.79635, 1.67626),c=vec2d(7.45029, 1.90378))
    shape2 = Simplex2d(a=vec2d(6.74703, 5.23394),b=vec2d(4.57519, 2.60705),c=vec2d(7.94671, 3.51715))

    assert intersect(shape1, shape2, points=True)[0]

#https://pynative.com/python-get-execution-time-of-program/
# run same code many times to get measurable data
n = 1000000
print(f"{bcolors.BOLD}test_intersection(){bcolors.ENDC}")

# calculate total execution time
result = timeit.timeit(stmt='test_intersection()', globals=globals(), number=n)

# calculate the execution time
print(f"Execution time is {(result / n) * 10**9} Nanoseconds")
print(f"Theoretical FPS possible with 1 check: {(1/(result/n))}")

print()
print(f"{bcolors.BOLD}test_intersection_dist(){bcolors.ENDC}")

# calculate total execution time
result = timeit.timeit(stmt='test_intersection_dist()', globals=globals(), number=n)

# calculate the execution time
print(f"Execution time is {(result / n) * 10**9} Nanoseconds")
print(f"Theoretical FPS possible with 1 check: {(1/(result/n))}")
print()

print(f"{bcolors.BOLD}test_intersection_points(){bcolors.ENDC}")

# calculate total execution time
result = timeit.timeit(stmt='test_intersection_points()', globals=globals(), number=n)

# calculate the execution time
print(f"Execution time is {(result / n) * 10**9} Nanoseconds")
print(f"Theoretical FPS possible with 1 check: {(1/(result/n))}")
print()