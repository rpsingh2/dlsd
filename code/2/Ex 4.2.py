from swampy.TurtleWorld import *
import sys,math
world = TurtleWorld()
#sq = Turtle()
#poly = Turtle()
pattern = Turtle()
pattern.delay = 0.000000001
def square(t,len):
	for x in xrange(0,4):
		fd(t,len)
		lt(t)

def polygon(t,len,n):
	angle = 360/n
	for x in xrange(0,n):
		fd(t,len)
		lt(t,angle)

def polyline(t, n, length, angle):
	for x in xrange(0,n):
		fd(t,length)
		lt(t,angle)

def circle (t,r):
	circumeference = 2 * math.pi * r
	n = 50
	length = circumeference/n
	polygon(t, length, n)

def move(t,len):
	pu(t)
	fd(t, len)
	pd(t)


def polyline(t, n, len, angle):
    for i in range(n):
        fd(t, len)
        lt(t, angle)


def arc(t, r, angle):
    arc_length = 2 * math.pi * r * angle / 360
    n = int(arc_length / 3) + 1
    step_length = arc_length / n
    step_angle = float(angle) / n
    polyline(t, n, step_length, step_angle)
    lt(t, 180-angle)		
    polyline(t, n, step_length, step_angle)

def petal(t, n, clock, aclock):
	angle = 360/n
	for i in xrange(0,n):
		arc(pattern,60, clock*angle)
		lt(pattern, aclock*angle)
		print pattern

set_pen_color(pattern,"#FF0000")
move(pattern, -150)
petal(pattern, 7, 1, 1.5)
set_pen_color(pattern,"#008000")
move(pattern, 200)
petal(pattern, 10, 3, 3)
set_pen_color(pattern,"#00FFFF")
move(pattern, 150)
petal(pattern, 20, 1, 2)

wait_for_user()
