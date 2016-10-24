from Schafer import Schafer
from SA import SA
from MWS import MWS
from Kursawe import Kursawe
from Osyczka2 import Osyczka2

for model in [Schafer, Kursawe, Osyczka2]:
    for optimizer in [SA, MWS]:  
        optimizer(model())
