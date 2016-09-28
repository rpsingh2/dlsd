from Osyczka2 import Osyczka2
from random import *
import copy

model = Osyczka2()

trials = 100000
p = 0.5

best_model = copy.deepcopy(model)

for x in range(trials):
    #model = Osyczka2()

    #print str(model.energy()) + " " + str(best_model.energy())
    if model.energy() < best_model.energy():
        best_model = copy.deepcopy(model)
        print "be: " + str(best_model.energy())
        if best_model.energy() == 0.0: break
    if p < random():
        model.mutate_rand_x()
        print "jump " + str(model.energy())
    else:
        model = model.roll()
        print "roll " + str(model.energy())

print "trials " + str(x)
print best_model.energy()
print best_model.to_str()
