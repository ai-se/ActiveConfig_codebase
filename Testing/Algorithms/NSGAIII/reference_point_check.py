import os, sys, inspect
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe()))[0], "../../..")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)
from jmoo_core import *
problem = dtlz1(7, 3)



def read_reference(filename):
    population = []
    for line in open(filename, "r").readlines():
        if line == "\n": continue
        population.append([float(l) for l in line.split()])
    return population

def test():
    compare = lambda a,b: len(a)==len(b) and len(a)==sum([1 for i,j in zip(a,b) if round(i, 5) == round(j,5)])
    from Algorithms.NSGAIII.nsgaiii_components import associate
    reference_points = two_level_weight_vector_generator([12, 0], len(problem.objectives))
    jmetal_reference_points = read_reference("reference_point.txt")

    for org_rp in reference_points:
        for jmetal_rp in jmetal_reference_points:
            if compare(org_rp.coordinates, jmetal_rp) is True:
                test_value = True
                break
        if test_value is False:
            print org_rp
        assert(test_value is True), "Something is wrong"

    print "Reference Points are the same"


for i in xrange(100):
    test()