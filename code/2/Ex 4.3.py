from swampy.TurtleWorld import *
import math, sys

def triangle(pen, arc, size):
    arc = arc/2
    base_len = 2 * (size * math.sin(arc * math.pi / 180))
    
    fd(pen, size)
    lt(pen, arc + 90)
    fd(pen, base_len)
    lt(pen, arc + 90)
    fd(pen, size)
    lt(pen, 180)

def draw_shape(pen, n, size):
    pd(pen)
    arc = 360.0 / n
    print arc
    for x in xrange(n):
        triangle(pen, arc, size)
    pu(pen)
    fd(pen, size + 50)

#world and pen setup
world = TurtleWorld()
pen = Turtle()
pen.delay = 0.1

pu(pen)
bk(pen, 130)
pd(pen)

# draw polypies with various number of sides
size = 40
draw_shape(pen, 5, size)
draw_shape(pen, 6, size)
draw_shape(pen, 7, size)
draw_shape(pen, 8, size)

die(pen)

wait_for_user()
