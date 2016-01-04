import os, sys, inspect
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe()))[0], "../../..")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)
from jmoo_core import *
problem = dtlz1(7, 3)



def read_file(filename):
    population = []
    for line in open(filename, "r").readlines():
        if line == "\n": continue
        decision = 7
        objectives = 3
        line = [float(a) for a in line.split()]
        population.append(jmoo_individual(problem, line[:decision], line[decision:]))
    return population


def read_normalized(filename):
    population = []
    for line in open(filename, "r").readlines():
        if line == "\n": continue
        population.append([float(l) for l in line.split()])
    return population

def read_reference(filename):
    population = []
    for line in open(filename, "r").readlines():
        if line == "\n": continue
        population.append([float(l) for l in line.split()])
    return population

def read_associated(filename):
    population = []
    for line in open(filename, "r").readlines():
        if line == "\n": continue
        population.append([float(l) for l in line.split()])
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


population = read_file("population.txt")
for pop in population:
    pop.front_no = 0
last_front = read_file("lastfront.txt")
for lf in last_front:
    lf.front_no = -1


print "length of the front -1 : ", len(population)
print "length of the last front : ", len(last_front)

from Algorithms.NSGAIII.nsgaiii_components import compute_ideal_points, compute_max_points, compute_extreme_points

ideal_point = compute_ideal_points(problem, population+last_front)
print "Ideal point: ", ideal_point

max_point = compute_max_points(problem, population+last_front)
print "Max point: ", max_point

extreme_points = compute_extreme_points(problem, population+last_front, ideal_point)
print "Extreme Points: ", extreme_points

from Algorithms.NSGAIII.nsgaiii_components import compute_intercept_points
intercept_point = compute_intercept_points(problem, extreme_points, ideal_point, max_point)
print "Intercept points: ", intercept_point

from Algorithms.NSGAIII.nsgaiii_components import normalization
normalized_population = normalization(problem, population+last_front, intercept_point, ideal_point)
normal_values = [pop.normalized for pop in normalized_population]
jmetal_population = read_normalized("normalized_result.txt")

compare = lambda a,b: len(a)==len(b) and len(a)==sum([1 for i,j in zip(a,b) if round(i, 5) == round(j,5)])
for op in normal_values:
    test_value = False
    for jp in jmetal_population:
        assert(len(op) == len(jp)), "Something is wrong"
        if compare(op, jp) is True:
            test_value = True
            break
    if test_value is False:
        print op
    assert(test_value is True), "Something is wrong"

print "Normalized Values are the same"

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


population = associate(problem, normalized_population, reference_points)


associated_values = []
for pop in population:
    from copy import copy
    temp = copy(pop.fitness.fitness)
    temp.append(pop.perpendicular_distance)
    associated_values.append(temp)
jmetal_association = read_associated("associated.txt")

for original_ass1 in associated_values:
    original_ass = original_ass1[:3]
    test_value = False
    for jmetal_ass1 in jmetal_association:
        jmetal_ass = jmetal_ass1[:3]
        assert(len(original_ass) == len(jmetal_ass)), "Something is wrong"
        if compare(original_ass, jmetal_ass) is True:
            test_value = True
            assert(round(original_ass1[-1], 5) == round(jmetal_ass1[-1], 5)), "perpendicular distance"
            break

    if test_value is False:
        print original_ass
    assert(test_value is True), "Something is wrong"

print "Association works well"


population = assignment(problem, population,  reference_points)



final_scores = [pop.fitness.fitness for pop in population]
jmetal_final_scores = read_associated("assignment.txt")


for i in xrange(len(problem.objectives)):
    print i, np.median([pop.fitness.fitness[i] for pop in population]), np.median([jfs[i] for jfs in jmetal_final_scores])


# for fs in final_scores:
#     test_value = False
#     for jfs in jmetal_final_scores:
#         if compare(fs, jfs) is True:
#             test_value = True
#             break
#
#     if test_value is False:
#         print fs
#         raw_input()
#     # assert(test_value is True), "Something is wrong"