from Model import Model
import random

class Schafer(Model):    
    decisions = [0]
    energy = 0

    def ok(self):
        return True

    def calcEnergy(self):
        f1 = self.decisions[0]['value'] ** 2
        f2 = (self.decisions[0]['value'] - 2) ** 2
        self.energy = f1 + f2

    def getEnergy(self):
        self.calcEnergy()
        return self.energy

    def neighbor(self):
        current_position = self.decisions[0]['value']
        new_position = current_position + random.randint(-100, 100)
        while new_position < self.decisions[0]['min'] and new_position > self.decisions[0]['max']:
             new_position = current_position + random.randint(-1000, 1000)
        self.decisions[0]['value'] = new_position
        self.calcEnergy()

    def getRandomDecisions(self):
        self.decisions[0] = {'min': -10000, 'max': 10000, 'value': random.randint(-10000, 10000)}
        self.calcEnergy()

    def __init__(self):
        self.getRandomDecisions()

Schafer()
