class Individual(object):
    def __init__(self):
        self.rank = None
        self.dominated_solutions = set()
        self.features = None
        self.decisions = None
        self.dominates = None