from Model import Model
import random
import math

class Kursawe(Model):    
    decisions = [None, None, None]
    energy = 0
    a = b = 1
    def ok(self):
        return True

    def f1(self):
        rv = 0
        for i in range(len(self.decisions) -1):
            exponent = (-0.2) * math.sqrt(self.decisions[i]['value'] ** 2 + self.decisions[i+1]['value'] ** 2)
            rv += -10 * math.exp(exponent)
        return rv

    def f2(self):
        sum = 0
        for i in range(len(self.decisions)):
            sum += math.fabs(self.decisions[i]['value']**self.a + 5 * math.sin(self.decisions[i]['value']**self.b))
        #f = lambda x: (math.fabs(x)**self.a) + (5 * math.sin(x)**self.b)
        #return sum(f(x) for x in xs) 
        return sum

    def calcEnergy(self):
        self.energy = self.f1() + self.f2()

    def neighbor(self):
        for dec in self.decisions:
            current_position = dec['value']
            new_position = current_position + random.randint(-1, 1)
            while new_position < dec['min'] and new_position > dec['max']:
                new_position = current_position + random.randint(-1, 1)
            dec['value'] = new_position
        self.calcEnergy()

    def getRandomDecisions(self):
        self.decisions[0] = {'min': -5, 'max': 5, 'value': random.randint(-5, 5)}
        self.decisions[1] = {'min': -5, 'max': 5, 'value': random.randint(-5, 5)}
        self.decisions[2] = {'min': -5, 'max': 5, 'value': random.randint(-5, 5)}
        self.calcEnergy()

    def __init__(self):
        self.getRandomDecisions()

