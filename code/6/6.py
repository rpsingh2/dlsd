from Schafer import Schafer
from SA import SA
from MWS import MWS
from Kursawe import Kursawe

for model in [Schafer, Kursawe]:
    for optimizer in [SA, MWS]:  
        optimizer(model())
