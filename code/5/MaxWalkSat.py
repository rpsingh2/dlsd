from Osyczka2 import Osyczka2
from random import *
import copy
import sys

"""

How to read output:
. = iteration complete
! = new best entropy found
r = rolling (probably not the technical term (local search?))
j = jumping to random location

float at end of the line is the current best entropy

"""

model = Osyczka2()

trials = 100000
p = 0.5

best_model = copy.deepcopy(model)

def say(x):
    sys.stdout.write(str(x)); sys.stdout.flush()

for x in range(trials):
    if model.energy() < best_model.energy():
        best_model = copy.deepcopy(model)
        say("!")
        if best_model.energy() == 0.0: break
    if p < random():
        model.mutate_rand_x()
        say("j")
    else:
        model = model.roll()
        say("r")
    say(".")
    if x % 50 == 0: say("|" + str(best_model.energy()) + "\n")
    #print str(model.f1()) + "," + str(model.f2())
print
print
print "number of trials:" + str(x)
print "best entropy: " + str(best_model.energy())
print "best x vals: " + str(best_model.to_str())
