from Model import Model
import random

class Osyczka2(Model):    
    decisions = [None,None,None,None,None,None]
    energy = 0

    def ok(self):
        d1 = 0 <= self.decisions[0]['value'] + self.decisions[1]['value'] - 2
        d2 = 0 <= 6 - self.decisions[0]['value'] - self.decisions[1]['value']
        d3 = 0 <= 2 - self.decisions[1]['value'] + self.decisions[0]['value']
        d4 = 0 <= 2 - self.decisions[0]['value'] + 3 * self.decisions[1]['value']
        d5 = 0 <= 4 - (self.decisions[4]['value'] - 3) ** 2 - self.decisions[3]['value']
        d6 = 0 <= (self.decisions[4]['value'] - 3) ** 3 + self.decisions[5]['value'] - 4
        return (d1 and d2 and d3 and d4 and d5 and d6)  
 
    def f1(self):
        return -(25 * (self.decisions[0]['value'] - 2) ** 2 + (self.decisions[1]['value'] - 2) ** 2 + ((self.decisions[2]['value'] - 1) ** 2) * ((self.decisions[3]['value'] - 4) ** 2) + (self.decisions[4]['value'] - 1) ** 2)


    def f2(self):
        return self.decisions[0]['value'] ** 2 + self.decisions[1]['value'] ** 2 + self.decisions[2]['value'] ** 2 + self.decisions[3]['value'] ** 2 + self.decisions[4]['value'] ** 2 + self.decisions[5]['value'] ** 2
    
    def calcEnergy(self):
        self.energy = self.f1() + self.f2()

    def neighbor(self):
        r_dec = random.randint(0,5)
        current_position = self.decisions[r_dec]['value']
        new_position = current_position + random.randint(-10, 10)
        while new_position < self.decisions[r_dec]['min'] and new_position > self.decisions[r_dec]['max'] and (False == self.ok()):
             new_position = current_position + random.randint(-10, 10)
             self.decisions[0]['value'] = new_position
        self.calcEnergy()

    def getRandomDecisions(self):
        while True:
            self.decisions[0] = {'min': 0, 'max': 10, 'value': random.randint(0, 10)}
            self.decisions[1] = {'min': 0, 'max': 10, 'value': random.randint(0, 10)}
            self.decisions[2] = {'min': 1, 'max': 5, 'value': random.randint(1, 5)}
            self.decisions[3] = {'min': 0, 'max': 6, 'value': random.randint(0, 6)}
            self.decisions[4] = {'min': 1, 'max': 5, 'value': random.randint(1, 5)}
            self.decisions[5] = {'min': 0, 'max': 10, 'value': random.randint(0, 10)}
            if self.ok(): break
        self.calcEnergy()

    def __init__(self):
        self.getRandomDecisions()

