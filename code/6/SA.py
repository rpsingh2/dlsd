from Optimizer import Optimizer
import random
import math
import copy
class SA(Optimizer):

    def P(self, old, new, t):
        try:
            ans = math.exp((old-new)/t)
        except OverflowError:
            ans = 2
        return ans

    def mainLoop(self, model):
        t = 1
        t_max = 100000
        new_model = copy.deepcopy(model)
        current_model = copy.deepcopy(model)
        best_model = copy.deepcopy(model)
        while t < t_max:
            new_model.neighbor()
            if best_model.energy > new_model.energy:
                best_model = copy.deepcopy(new_model)
                best_model.decisions = copy.deepcopy(new_model.decisions)
            if current_model.energy > new_model.energy: 
                current_model = copy.deepcopy(new_model)
                current_model.decisions = copy.deepcopy(new_model.decisions)
            if self.P(current_model.energy, new_model.energy, float(t)/t_max) <  random.random():
                current_model = copy.deepcopy(new_model)
                current_model.decisions = copy.deepcopy(new_model.decisions)
            t += 1
        print best_model.decisions
        print best_model.energy
    def __init__(self, model):
        self.mainLoop(model)    
