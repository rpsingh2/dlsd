import random
import math

from abc import ABCMeta, abstractmethod
class Model:
    __metaclass__ = ABCMeta

    @abstractmethod
    def getRandomDecisions(self):
        pass
    
    @abstractmethod
    def __init__(self):
        pass
