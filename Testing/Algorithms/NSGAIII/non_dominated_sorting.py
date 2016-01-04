import os, sys, inspect
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe()))[0], "../../..")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)
from jmoo_core import *
problem = dtlz1(7, 3)
def read_file():

    population = []
    for line in open("test_non_dominated_sorting.txt", "r").readlines():
        decision = 7
        objectives = 3
        line = [float(a) for a in line.split()[1:]]
        population.append(jmoo_individual(problem, line[:decision], line[decision:]))
    return population

def convert_jmoo(pareto_fronts, front_no_d=0):
    tpopulation = []
    for front_no, front in enumerate(pareto_fronts):
        for i, dIndividual in enumerate(front):
            cells = []
            for j in xrange(len(dIndividual)):
                cells.append(dIndividual[j])
            tpopulation.append(jmoo_individual(problem, cells, dIndividual.fitness.values))
            tpopulation[-1].front_no = front_no_d
    return tpopulation



population = read_file()
os.chdir("../../..")  # Since the this file is nested so the working directory has to be changed
from Algorithms.DEAP.tools.emo import sortNondominated
Individuals = jmoo_algorithms.deap_format(problem, population)
pareto_fronts = sortNondominated(Individuals, jmoo_properties.MU)
population = convert_jmoo(pareto_fronts[:-1])
last_front = convert_jmoo(pareto_fronts[-1:])

print "Length of population: ", len(population)
print "Front: ", len(last_front)
print "Remain: ", jmoo_properties.MU - len(population)