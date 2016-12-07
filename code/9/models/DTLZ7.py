from math import *

class DTLZ7():
    def name(self):
        return "DTLZ7"

    def g(self, individual, objs):
        return (1 + ((9 / len(individual.features)) * sum(individual.features)))

    def h(self, individual, objs):
        import math
        sum = 0
        count = 0
        while count <= objs - 1:
            sum += (individual.features[0]/(1 + self.g(individual, objs))) * (1 + math.sin(3 * math.pi * individual.features[0]))
            count += 1
        return objs - sum

    def calc_objectives(self, individual, objs):
        import math
        m = objs
        n = len(individual.features)
        multiplier = 1 / floor(n / m)

        g_val = self.g(individual, objs)
        h_val = self.h(individual, objs)

        f = []
        f = individual.features[: objs -1]
        f.append(1 + g_val * h_val)

        #point.objectives = [self.igd(f)]
        return f