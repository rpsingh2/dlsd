from util import *
from GA_MODEL import *

prob = GA_PROBLEM(DTLZ1())
fin = ga(prob, 2, 2, 0.3)

print fin