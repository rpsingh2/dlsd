from Optimizer import Optimizer
import random
import math
import copy
class MWS(Optimizer):

    def mainLoop(self, model):
        t = 1
        t_max = 10000
        new_model = copy.deepcopy(model)
        current_model = copy.deepcopy(model)
        best_model = copy.deepcopy(model)
        while t < t_max:
            new_model.neighbor()
            if best_model.energy > new_model.energy:
                best_model = copy.deepcopy(new_model)
                best_model.decisions = copy.deepcopy(new_model.decisions)
            if random.random() < 0.5:
                current_model = copy.deepcopy(new_model)
                current_model.decisions = copy.deepcopy(new_model.decisions)
            else:
                dec_num = random.randint(0, len(current_model.decisions) - 1)
                dec_min = new_model.decisions[dec_num]['min']
                dec_max = new_model.decisions[dec_num]['max']
                
                for x in xrange(dec_min, dec_max):
                    current_model.decisions[dec_num]['value'] = x
                    if not current_model.ok(): continue
                    if best_model.energy > new_model.energy:
                        best_model = copy.deepcopy(new_model)
                        best_model.decisions = copy.deepcopy(new_model.decisions)
            t += 1
        print best_model.decisions
        print best_model.energy

    def __init__(self, model):
        self.mainLoop(model)
