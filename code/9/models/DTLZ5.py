import math

class DTLZ5():
    def name(self):
        return "DTLZ5"

    def calc_objectives(self, individual, objs):
        return1 = []
        g = 0
        for x in individual.features[objs - 1:]:
            g = g + (x - 0.5) ** 2
        theta = [math.pi * individual.features[0] / 2]
        for x in individual.features[1:objs - 1]:
            theta.append((1 + 2 * g * x) * math.pi / (4 * (1 + g)))
        for i in xrange(objs):
            tmp = 1 + g
            for x in theta[:objs - 1 - i]:
                tmp = tmp * math.cos(x * math.pi / 2)
            if not i == 0:
                tmp = tmp * math.sin(theta[objs - i - 1] * math.pi / 2)
            return1.append(tmp)
        return return1