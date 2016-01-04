import os
import sys
import inspect

cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe()))[0], "../../..")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

from jmoo_core import *

def readpf(problem):
    filename = "./Testing/PF/" + problem.name.split("_")[0] + "(" + str(len(problem.objectives)) + ")-PF.txt"
    return [[float(num) for num in line.split()] for line in open(filename, "r").readlines()]

from PerformanceMetrics.IGD.IGD_Calculation import IGD
algorithms_TCH = [jmoo_MOEAD_TCH()]
Configurations = {
    "Universal": {
        "Repeats" : 5,
        "Population_Size" : 136,
        "No_of_Generations" : 1500
    },
    "MOEAD" : {
        "niche" : 20,  # Neighbourhood size
        "SBX_Probability": 1,
        "ETA_C_DEFAULT_" : 20,
        "ETA_M_DEFAULT_" : 20,
        "Theta" : 5
    },
}

def problems_runner(list_args):
    problems = [list_args[0]]
    Configurations["Universal"]["Population_Size"] = list_args[1]
    Configurations["Universal"]["No_of_Generations"] = list_args[2]



    # Wrap the tests in the jmoo core framework
    tests = jmoo_test(problems, algorithms_TCH)
    IGD_Results = []
    for problem in tests.problems:
        print problem.name, " ",
        for algorithm in tests.algorithms:
            for repeat in xrange(Configurations["Universal"]["Repeats"]):
                print repeat, " ",
                import sys
                sys.stdout.flush()
                initialPopulation(problem, Configurations["Universal"]["Population_Size"])
                statBox = jmoo_evo(problem, algorithm, Configurations)

                resulting_pf = [[float(f) for f in individual.fitness.fitness] for individual in statBox.box[-1].population]
                IGD_Results.append(IGD(resulting_pf, readpf(problem)))
                print IGD(resulting_pf, readpf(problem))
            IGD_Results = sorted(IGD_Results)

            results_string = ""
            results_string += "Problem Name: " + str(problem.name) + "\n"
            results_string += "Algorithm Name: "+ str(algorithm.name) + "\n"
            results_string += "- Generated New Population" + "\n"
            results_string += "- Ran the algorithm for "+ str(Configurations["Universal"]["Repeats"]) + "\n"
            results_string += "- The SBX crossover and mutation parameters are correct" + "\n"
            results_string += "Best: " + str(IGD_Results[0]) + "\n"
            results_string += "Median: " + str(IGD_Results[int(len(IGD_Results)/2)]) + "\n"
            results_string += "Worst: " + str(IGD_Results[-1]) + "\n"

            filename = "./Testing/Algorithms/MOEAD_TCH/Results/" + str(problem.name) + ".txt"
            f = open(filename, "w")
            f.write(results_string)
            f.close()


problems = [

    [dtlz1(7,3), 91, 400], [dtlz1(9, 5), 210, 600], [dtlz1(12, 8), 156, 750],
    [dtlz1(14, 10), 275, 1000], [dtlz1(19, 15), 135, 1500],
    [dtlz2(12, 3), 91, 250], [dtlz2(14, 5), 210, 350], [dtlz2(17, 8), 156, 500], [dtlz2(19, 10), 275, 750], [dtlz2(24, 15), 135, 1000],
    [dtlz3(12, 3), 91, 1000], [dtlz3(14, 5), 210, 1000], [dtlz3(17, 8), 156, 1000], [dtlz3(19, 10), 275, 1500], [dtlz3(24, 15), 135, 2000],
    [dtlz4(12, 3), 91, 600], [dtlz4(14, 5), 210, 1000], [dtlz4(17, 8), 156, 1250], [dtlz4(19, 10), 275, 2000], [dtlz4(24, 15), 135, 3000],
        ]

os.chdir("../../..")  # Since the this file is nested so the working directory has to be changed
for problem in problems:
    problems_runner(problem)
