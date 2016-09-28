class Osyczka2:
    max_energy = 0
    min_energy = 0
    
    def min_max(self):
        for i in xrange(10000):
            self.new_vars()
            pure_energy = self.f1() + self.f2()
            #print str(self.to_str()) + " " + str(pure_energy)
            if i == 0: 
                self.max_energy = self.min_energy = pure_energy
            if pure_energy > self.max_energy: self.max_energy = pure_energy
            if pure_energy < self.min_energy: self.min_energy = pure_energy
        print self.max_energy
        print self.min_energy

    def ok(self):
        g1 = 0 <= self.x1 + self.x2 - 2
        g2 = 0 <= 6 - self.x1 - self.x2
        g3 = 0 <= 2 - self.x2 + self.x1
        g4 = 0 <= 2 - self.x1 + 3 * self.x2
        g5 = 0 <= 4 - (self.x3 - 3) ** 2 - self.x4
        g6 = 0 <= (self.x5 - 3) ** 3 + self.x6 - 4
        return (g1 and g2 and g3 and g4 and g5 and g6)

    def rand_vars(self):
        from random import randint
        self.x1 = randint(0, 10)
        self.x2 = randint(0, 10)
        self.x3 = randint(1, 5)
        self.x4 = randint(0, 6)
        self.x5 = randint(1, 5)
        self.x6 = randint(0, 10)

    def new_vars(self):
        while True:
            self.rand_vars()
            if self.ok(): 
                break

    def mutate_rand_x(self):
        while True:
            from random import randint
            c = randint(1, 6)
            if c == 1: self.x1 = randint(0, 10)
            elif c == 2: self.x2 = randint(0, 10)
            elif c == 3: self.x3 = randint(1, 5)
            elif c == 4: self.x4 = randint(0, 6)
            elif c == 5: self.x5 = randint(1, 5)
            elif c == 6: self.x6 = randint(0, 10)
            
            if self.ok(): break

    def roll(self):
        import copy
        from random import randint
        best_self = copy.deepcopy(self)
        c = randint(1, 6)
        def en(): self.energy() < best_self.energy()
        if c == 1: 
            for x in xrange(0, 10): 
                self.x1 = x
                if self.ok():
                    if en(): best_self = self    
        elif c == 2:
            for x in xrange(0, 10):
                self.x2 = x
                if self.ok():
                    if  en(): best_self = self    
        elif c == 3:
            for x in xrange(1, 5):
                self.x3 = x
                if self.ok():
                    if en(): best_self = self    
        elif c == 4: 
            for x in xrange(0, 6):
                self.x4 = x
                if self.ok():
                    if en(): best_self = self    
        elif c == 5:
            for x in xrange(1, 5):
                self.x5 = x
                if self.ok():
                    if en(): best_self = self    
        elif c == 6:
            for x in xrange(0, 10):
                self.x6 = x
                if self.ok():
                    if en(): best_self = self
        return best_self

    def energy(self):
        #if (self.f1() + self.f2()) < self.min_energy: 
        #if (self.f1() + self.f2()) > self.max_energy: 
        return float((self.f1() + self.f2()) - self.min_energy) / (self.max_energy - self.min_energy)

    def f1(self):
        return -(25 * (self.x1 - 2) ** 2 + (self.x2 - 2) ** 2 + ((self.x3 - 1) ** 2) * ((self.x4 - 4) ** 2) + (self.x5 - 1) ** 2)


    def f2(self):
        return self.x1 ** 2 + self.x2 ** 2 + self.x3 ** 2 + self.x4 ** 2 + self.x5 ** 2 + self.x6 ** 2

    def to_str(self):
        return str(self.x1) + " " + str(self.x2) + " " + str(self.x3) + " " + str(self.x4) + " " + str(self.x5) + " " + str(self.x6)

    def __init__(self):
        self.new_vars()
        self.min_max()
       
    """
    def __init__(self, x1, x2, x3, x4, x5, x6):
        self.x1 = x1
        self.x2 = x2
        self.x3 = x3
        self.x4 = x4
        self.x5 = x5
        self.x6 = x6
        self.min_max()
    """
