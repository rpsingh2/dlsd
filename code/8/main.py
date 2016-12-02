from nsgaii import NSGAII

from models.DTLZ1 import *
from models.DTLZ3 import *
from models.DTLZ5 import *
from models.DTLZ7 import *
from models import MODEL

from hypervolume import *
from stats import rdivDemo as sk

def print_generation(population, generation_num):
    print("Generation: {}".format(generation_num))

for dtlz_name, dtlz_definitions in zip(["dtlz1", "dtlz3", "dtlz5", "dtlz7"], [DTLZ1(), DTLZ3(), DTLZ5(), DTLZ7()]):
    for num_obj in [2, 4, 6, 8]:
        hv_stats = []
        run_stats = []
        for num_dec in [10, 20, 40]:
            for dom in ["bdom", "cdom"]:
                avg_vol = 0
                avg_runs = 0
                repeats = 20
                info_hv = [dtlz_name + " " + str(num_obj) + " " + str(num_dec) + " " + dom]
                info_runs = [dtlz_name + " " + str(num_obj) + " " + str(num_dec) + " " + dom]
                for x in range(repeats): #repeats
                    problem = MODEL(dtlz_definitions, num_dec, num_obj, dom)

                    #Evolution(problem, max_iterations, pop_size)
                    nsga = NSGAII(problem, 100, 100, dom)

                    hypervolume, runs = nsga.run()

                    info_hv.append(hypervolume)
                    info_runs.append(runs)

                    avg_runs += runs
                hv_stats.append(info_hv)
                run_stats.append(info_runs)

        sk(hv_stats)
        sk(run_stats)
        print