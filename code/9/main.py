from DE import de
from nsgaii import NSGAII

from models import MODEL
from models.DTLZ1 import *
from models.DTLZ3 import *
from models.DTLZ5 import *
from models.DTLZ7 import *

decs = [10, 20, 40]
objs = [2, 4, 6, 8]
model = [DTLZ1, DTLZ3, DTLZ5, DTLZ7]
model_name = ["dtlz1", "dtlz3", "dtlz5", "dtlz7"]
for name, mod in zip(model_name, model):
    for dec in decs:
        for obj in objs:
            print name, dec, obj
            prob = NSGAII_PROBLEM(name, dec, obj)
            fin = de(prob, gens =  5, pop_size = 10)
            print fin