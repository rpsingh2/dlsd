import random
import math

from abc import ABCMeta, abstractmethod
class Optimizer:
    __metaclass__ = ABCMeta

    @abstractmethod
    def mainLoop(self, model):
        pass

    @abstractmethod
    def __init__(self, model):
        pass
