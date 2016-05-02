from __future__ import division
import sys, os, inspect

parentdir = os.path.realpath(
    os.path.abspath(os.path.join(os.path.split(inspect.getfile(inspect.currentframe()))[0], "../../")))
if parentdir not in sys.path:
    sys.path.insert(0, parentdir)
from jmoo_objective import *
from jmoo_decision import *
from jmoo_problem import jmoo_problem
from Techniques.euclidean_distance import euclidean_distance
from Problems.CPM.utilities.csv_utilities import read_csv
from sklearn import tree
import itertools


def equal_list(lista, listb):
    """Checks whether two list are same"""
    assert (len(lista) == len(listb)), "Not a valid comparison"
    for i, j in zip(lista, listb):
        if i == j:
            pass
        else:
            return False
    return True

class data_container:
    def __init__(self, fraction, value, saved_time, total_time, evaluations):
        self.fraction = fraction
        self.value = value
        self.saved_times = saved_time
        self.total_times = total_time
        self.evaluations = evaluations

    def __str__(self):
        return str(self.fraction) + str(self.value) + str(self.saved_times) + "\n"


def where_clusterer(filename):
    """
    This is function accepts a file with rows(=records) and clusters it. This is FASTNAP + PCA
    :param filename: Pass in the filename with rows as valid configurations
    :return: List of Cluster. Each cluster has a [[cluster_number], [list of members]]
    """
    from utilities.Tools.methods1 import wrapper_createTbl
    # The Data has to be access using this attribute table._rows.cells
    transformed_table = [[int(z) for z in x.cells[:-1]] + x.cells[-1:] for x in wrapper_createTbl(filename)._rows]
    cluster_numbers = set(map(lambda x: x[-1], transformed_table))

    # separating clusters
    # the element looks like [clusterno, rows]
    cluster_table = []
    for number in cluster_numbers:
        cluster_table.append([number] + [filter(lambda x: x[-1] == number, transformed_table)])
    return cluster_table


def random_where(filename):
    """
    Exemplar Sampling as described in the paper (S_1)
    :param filename: Name of the file containing records which needs to be clustered and sampled
    :return: samples from the population
    """
    cluster_table = where_clusterer(filename)
    ret = []
    for cluster in cluster_table:
        # Remove the cluster label from the cluster[-1]: members of the population
        cluster[-1] = [c[:-1] for c in cluster[-1]]
        from random import choice
        ret.append(choice(cluster[-1]))
    print "Length of Random Where: ", len(ret)
    return ret, len(cluster_table)


def east_west_where(filename):
    """
    This is the East-West sampling as described in the paper (S_2)
    :param filename: Name of the file containing records which needs to be clustered and sampled
    :return: samples of the population
    """

    def furthest(one, all_members):
        """Find the distant point (from the population) from one (point)"""
        ret = None
        ret_distance = -1 * 1e10
        for member in all_members:
            if equal_list(one, member) is True:
                continue
            else:
                temp = euclidean_distance(one, member)
                if temp > ret_distance:
                    ret = member
                    ret_distance = temp
        return ret

    from random import choice
    cluster_table = where_clusterer(filename)

    ret = []
    for cluster in cluster_table:
        # Remove the cluster label from the cluster[-1]: members of the population
        cluster[-1] = [c[:-1] for c in cluster[-1]]
        # Randomly select one of the members of the cluster
        one = choice(cluster[-1])
        east = furthest(one, cluster[-1])
        west = furthest(east, cluster[-1])
        ret.append(east)
        ret.append(west)

    # print len(ret), 2*len(cluster_table)
    assert(len(ret) == 2*len(cluster_table)), "Something's wrong"
    return ret, len(ret)


def exemplar_where(filename):
    """
    Exemplar Sampling as described in the paper (S_3)
    :param filename: Name of the file containing records which needs to be clustered and sampled
    :return: samples from the population
    """
    cluster_table = where_clusterer(filename)
    ret = []
    for cluster in cluster_table:
        # Remove the cluster label from the cluster[-1]: members of the population
        cluster[-1] = [c[:-1] for c in cluster[-1]]
        ret.append(sorted(cluster[-1], key=lambda x: x[-1])[0])
    return ret, sum(len(c) for c in cluster_table)


def base_line(filename="./Data/Apache_AllMeasurements.csv"):
    """
    Baseline Sampling as described in the paper (Baseline)
    :param filename: Name of the file containing records which needs to be clustered and sampled
    :return: Consists of all the members of the population
    """
    content = [map(int, map(float, c.strip().split(","))) for c in open(filename, "r").readlines()[1:]]
    return content, len(content)


""" + Used to handle temporary file generation and deletion"""
# filename used for temporary file generation
temp_file_name = "temp_file.csv"


def temp_file_generation(header, listoflist):
    import csv
    with open(temp_file_name, 'wb') as fwrite:
        writer = csv.writer(fwrite, delimiter=',')
        writer.writerow(header)
        for l in listoflist:
            writer.writerow(l[1:])
    fwrite.close()


def temp_file_removal():
    os.remove(temp_file_name)


""" - Used to handle temporary file generation and deletion"""

""" + Global Variables to handle the fixed value experiments for research question 3"""
testing_percent = 0
training_percent = 40
""" + Global Variables to handle the fixed value experiments for research question 3"""


class CPMReduction(jmoo_problem):
    """BaseClass to handle data"""

    def get_training_data(self, method=base_line):
        global testing_percent, training_percent
        from copy import deepcopy
        transformed_data = deepcopy(self.data)
        random_selection = self.get_testing_data(transformed_data, testing_percent)

        temp_file_generation(self.header, random_selection)
        training, self.no_of_clusters = method(temp_file_name)
        temp_file_removal()

        return [row[:-1] for row in training], [row[-1] for row in training]

    def get_testing_data(self, data, testing_perc):
        from random import shuffle
        shuffle(data)
        testing_data = data[:int(testing_perc * len(data))]
        self.testing_independent = [row[1:-1] for row in testing_data]
        self.testing_dependent = [float(row[-1]) for row in testing_data]

        # This makes sure that the training and testing doesn't overlap
        return data[int(testing_perc * len(data)):]

    def test_data(self):
        prediction = [float(x) for x in self.CART.predict(self.testing_independent)]
        mre = []
        # sum of absolute error
        sae = []
        for i, j in zip(self.testing_dependent, prediction):
            mre.append(abs(i - j) / float(i))
            sae.append(abs(i - j))
        # return sum(mre) / len(mre)
        return sum(sae)

    def print_data(self):
        print len(self.data)

    def evaluate(self, input=None):
        if input:
            import time
            start = time.time()
            for i, decision in enumerate(self.decisions):
                decision.value = input[i]

            input = [round(decision.value, 0) for decision in self.decisions]
            assert (len(input) == len(self.decisions)), "Something's wrong"
            if self.validate(input) is False: return [10 ** 10]

            prediction = self.CART.predict(input)
            # print "Evaluation Time: ", time.time() - start
            return [p / float(10 ** 4) for p in prediction]
        else:
            assert (False), "BOOM"
            exit()

    def find_total_time(self):
        return sum([d[-1] for d in self.data])

    def evalConstraints(prob, input=None):
        return False


class cpm_apache_training_reduction(CPMReduction):
    def __init__(self, treatment, requirements=9, name="CPM_APACHE", filename="./Data/Apache_AllMeasurements.csv"):
        self.name = name
        self.filename = filename

        if treatment is None:
            treatment = random_where
        elif treatment == 0:
            treatment = base_line

        # Setting up to create decisions (This is something specific from the JMOO framework
        names = ["x" + str(i + 1) for i in xrange(requirements)]
        lows = [0 for _ in xrange(requirements)]
        ups = [1 for _ in xrange(requirements)]

        # Generating decisions
        self.decisions = [jmoo_decision(names[i], lows[i], ups[i]) for i in range(requirements)]
        # Generating Objectives (this is single objective)
        self.objectives = [jmoo_objective("f1", True)]

        # Read Data
        self.header, self.data = read_csv(self.filename, header=True)

        self.training_independent, self.training_dependent = self.get_training_data(method=treatment)
        self.CART = tree.DecisionTreeRegressor()
        self.CART = self.CART.fit(self.training_independent, self.training_dependent)
        self.saved_time = (self.find_total_time() - sum(self.training_dependent))/10**4

    def validate(self, tsolution):
        solution = [int(round(i, 0)) for i in tsolution]
        if sum(solution) == 0: return False
        if solution[0] != 1:
            return False
        if solution[7] == 1 and solution[8] != 0:
            return False
        return True


class cpm_BDBC(CPMReduction):
    def __init__(self, treatment, number=50, requirements=18, name="CPM_BDBC", filename="./Data/BDBC_AllMeasurements.csv"):

        self.name = name
        self.filename = filename
        if treatment is None:
            treatment = random_where
        elif treatment == 0:
            treatment = base_line
        names = ["x" + str(i + 1) for i in xrange(requirements)]
        lows = [0 for _ in xrange(requirements)]
        ups = [1 for _ in xrange(requirements)]
        self.decisions = [jmoo_decision(names[i], lows[i], ups[i]) for i in range(requirements)]
        self.objectives = [jmoo_objective("f1", True)]
        self.header, self.data = read_csv(self.filename, header=True)

        self.training_independent, self.training_dependent = self.get_training_data(method=treatment)
        self.CART = tree.DecisionTreeRegressor()
        self.CART = self.CART.fit(self.training_independent, self.training_dependent)
        self.saved_time = (self.find_total_time() - sum(self.training_dependent))/10**4

    def validate(self, tsolution):
        solution = [int(round(i, 0)) for i in tsolution]
        if sum(solution) == 0: return False
        page_size_index = 7
        cache_size_index = 13
        pages_indexes = [8, 9, 10, 11, 12]
        caches_indexes = [14, 15, 16, 17]
        if solution[page_size_index] != 1: return False
        if solution[cache_size_index] != 1: return False
        if sum([solution[i] for i in pages_indexes]) != 1: return False
        if sum([solution[i] for i in caches_indexes]) != 1: return False
        return True


class cpm_BDBJ(CPMReduction):
    def __init__(self, treatment, number=50, requirements=26, name="CPM_BDBJ", filename="./Data/BDBJ_AllMeasurements.csv"):
        self.name = name
        self.filename = filename
        if treatment is None:
            treatment = random_where
        elif treatment == 0:
            treatment = base_line
        # Setting up to create decisions
        names = ["x" + str(i + 1) for i in xrange(requirements)]
        lows = [0 for _ in xrange(requirements)]
        ups = [1 for _ in xrange(requirements)]
        # Generating decisions
        self.decisions = [jmoo_decision(names[i], lows[i], ups[i]) for i in range(requirements)]
        # Generating Objectives (this is single objective)
        self.objectives = [jmoo_objective("f1", True)]
        # Read Data
        self.header, self.data = read_csv(self.filename, header=True)
        self.training_independent, self.training_dependent = self.get_training_data(method=treatment)
        self.CART = tree.DecisionTreeRegressor()
        self.CART = self.CART.fit(self.training_independent, self.training_dependent)
        self.saved_time = (self.find_total_time() - sum(self.training_dependent))/10**4

    def validate(self, tsolution):
        solution = [int(round(i, 0)) for i in tsolution]
        if sum(solution) == 0: return False
        if solution[0] != 1: return False
        if solution[1] != 1: return False
        if solution[2] != 1: return False
        if sum([solution[3], solution[4]]) != 1: return False
        if solution[4] == 1 and solution[5] != 1: return False
        if solution[4] == 1 and solution[6] != 1: return False
        if solution[6] == 1 and sum([solution[7], solution[8]]) != 1: return False
        if solution[10] != 1: return False
        if solution[10] == 1 and sum([solution[11], solution[12]]) != 1: return False
        if solution[13] != 1: return False
        if solution[14] != 1: return False
        if solution[19] == 1 and solution[15] != 1: return False
        if solution[16] != 1: return False
        if solution[16] == 1 and solution[17] != 1: return False
        if solution[16] == 1 and solution[18] != 1: return False
        if solution[20] == 1 and solution[21] != 1: return False
        if solution[20] == 1 and solution[22] != 1: return False
        if solution[22] == 1 and sum([solution[23], solution[24]]) != 1: return False
        if solution[20] == 0 and sum(solution[21:25]) != 0: return False
        return True


class cpm_LLVM(CPMReduction):
    def __init__(self, treatment, number=50, requirements=11, fraction=0.5, name="CPM_LLVM", filename="./Data/LLVM_AllMeasurements.csv"):

        self.name = name
        self.filename = filename
        if treatment is None:
            treatment = random_where
        elif treatment == 0:
            treatment = base_line
        # Setting up to create decisions
        names = ["x" + str(i + 1) for i in xrange(requirements)]
        lows = [0 for _ in xrange(requirements)]
        ups = [1 for _ in xrange(requirements)]
        # Generating decisions
        self.decisions = [jmoo_decision(names[i], lows[i], ups[i]) for i in range(requirements)]
        # Generating Objectives (this is single objective)
        self.objectives = [jmoo_objective("f1", True)]
        # Read Data
        self.header, self.data = read_csv(self.filename, header=True)
        self.training_independent, self.training_dependent = self.get_training_data(method=treatment)
        self.CART = tree.DecisionTreeRegressor()
        self.CART = self.CART.fit(self.training_independent, self.training_dependent)
        self.saved_time = (self.find_total_time() - sum(self.training_dependent))/10**4

    def validate(self, tsolution):
        solution = [int(round(i, 0)) for i in tsolution]
        if sum(solution) == 0: return False
        if solution[0] != 1: return False
        return True


class cpm_SQL(CPMReduction):
    def __init__(self, treatment, number=50, requirements=39, fraction=0.5, name="CPM_SQL", filename="./Data/SQL_AllMeasurements.csv"):

        self.name = name
        self.filename = filename
        if treatment is None:
            treatment = random_where
        elif treatment == 0:
            treatment = base_line
        # Setting up to create decisions
        names = ["x" + str(i + 1) for i in xrange(requirements)]
        lows = [0 for _ in xrange(requirements)]
        ups = [1 for _ in xrange(requirements)]
        # Generating decisions
        self.decisions = [jmoo_decision(names[i], lows[i], ups[i]) for i in range(requirements)]
        # Generating Objectives (this is single objective)
        self.objectives = [jmoo_objective("f1", True)]
        # Read Data
        self.header, self.data = read_csv(self.filename, header=True)

        self.training_independent, self.training_dependent = self.get_training_data(method=treatment)
        self.CART = tree.DecisionTreeRegressor()
        self.CART = self.CART.fit(self.training_independent, self.training_dependent)
        self.saved_time = (self.find_total_time() - sum(self.training_dependent))/10**4

    def validate(self, tsolution):
        solution = [int(round(i, 0)) for i in tsolution]

        indexes1 = [3, 4, 5, 6]
        if solution[2] == 1 and sum([solution[i] for i in indexes1]) != 1: return False
        indexes2 = [25, 26]
        if solution[24] == 1 and sum([solution[i] for i in indexes2]) != 1: return False
        indexes3 = [28, 29, 30]
        if solution[27] == 1 and sum(solution[i] for i in indexes3) != 1: return False
        indexes4 = [32, 33]
        if solution[31] == 1 and sum(solution[i] for i in indexes4) != 1: return False
        indexes5 = [35, 36, 37, 38]
        if solution[34] == 1 and sum(solution[i] for i in indexes5) != 1: return False
        return True


class cpm_X264(CPMReduction):
    def __init__(self, treatment, number=50, requirements=16, fraction=0.5, name="cpm_X264", filename="./Data/X264_AllMeasurements.csv"):

        self.name = name
        self.filename = filename
        if treatment is None:
            treatment = random_where
        elif treatment == 0:
            treatment = base_line
        # Setting up to create decisions
        names = ["x" + str(i + 1) for i in xrange(requirements)]
        lows = [0 for _ in xrange(requirements)]
        ups = [1 for _ in xrange(requirements)]
        # Generating decisions
        self.decisions = [jmoo_decision(names[i], lows[i], ups[i]) for i in range(requirements)]
        # Generating Objectives (this is single objective)
        self.objectives = [jmoo_objective("f1", True)]
        # Read Data
        self.header, self.data = read_csv(self.filename, header=True)
        self.training_independent, self.training_dependent = self.get_training_data(method=treatment)
        self.CART = tree.DecisionTreeRegressor()
        self.CART = self.CART.fit(self.training_independent, self.training_dependent)
        self.saved_time = (self.find_total_time() - sum(self.training_dependent))/10**4

    def validate(self, tsolution):
        solution = [int(round(i, 0)) for i in tsolution]
        if sum(solution) == 0: return False
        if solution[0] != 1: return False
        if solution[8] != 1: return False
        if solution[8] == 1 and sum([solution[9], solution[10], solution[11]]) != 1: return False
        if solution[12] != 1: return False
        if solution[12] == 1 and sum([solution[13], solution[14], solution[15]]) != 1: return False
        return True


class data_container:
    def __init__(self, fraction, value, saved_time, total_time, evaluations):
        self.fraction = fraction
        self.value = value
        self.saved_times = saved_time
        self.total_times = total_time
        self.evaluations = evaluations

    def __str__(self):
        return str(self.fraction) + str(self.value) + str(self.saved_times) + "\n"


def performance_test(dataset, treatment):
    global repeat_name
    repeats = 20
    scores = []
    saved_times = []
    total_times = []
    evaluations = []
    # print dataset.__name__, treatment.__name__,
    temp_store = []
    for repeat in xrange(repeats):
        repeat_name = repeat
        # print repeat, " ",
        # print "Dataset: ", dataset.__name__, " Repeats: ", repeats,
        # print " Treatment: ", treatment.__name__, "Training Percent: ", training_percent,
        # print ".",
        p = dataset(treatment=treatment)
        saved_times.append(p.saved_time)
        total_times.append(p.find_total_time())
        temp_store.append(p.test_data())
        evaluations.append(p.no_of_clusters)

    # import pdb
    # pdb.set_trace()
    assert(int(sum(total_times)/len(total_times)) == int(total_times[0])), "Something's wrong"
    scores.append(data_container(training_percent, temp_store, sum(saved_times)/len(saved_times), sum(total_times)/len(total_times), sum(evaluations)/len(evaluations)))
    return scores
    #draw([x.fraction for x in scores], [x.value for x in scores], problem.name)


def draw(data, name):
    import pylab as pl

    """ + To generate logs of the experiments"""
    filename = "./NewLogs/" + name + ".txt"
    fdesc = open(filename, "w")
    fdesc.write("training_percent, mean, standard_deviation, saved_time, total_time, technique, evaluations \n")
    scores1 = []
    import numpy as np
    for row in data:
        scores = []
        for d in row:
            temp = []
            temp.append(d[0])
            temp.append(np.percentile(d[1], 50))
            temp.append(np.percentile(d[1], 75) - np.percentile(d[1], 25))
            temp.append(d[2])
            # temp_string = str(d[0][-1]) + "," + str(np.percentile(d[1], 50)) + "," + str(
            #     np.percentile(d[1], 75) - np.percentile(d[1], 25)) + "," + str(d[3][-1]) + "," + str(
            #     d[4][-1] // 10 ** 4) + "," + str(int(d[-1][-1])) + "," + str(d[2]) + "\n"

            temp_string = str(d[0][-1]) + "," + str(np.around(np.mean(d[1]), 3)) + "," + str(
                np.around(np.std(d[1]), 3)) + "," + str(d[3][-1]) + "," + str(d[4][-1] // 10 ** 4) + "," + str(
                int(d[-1][-1])) + "," + str(d[2]) + "\n"
            fdesc.write(temp_string)
            scores.append(temp)
        scores1.append(scores)
    fdesc.close()
    """ - To generate logs of the experiments"""


    """ + To generate graph of the experiments """
    for score in scores1:
        x_coordinates = [s[0] for s in score]
        y_coordinates = [s[1] for s in score]
        y_error = [s[2] for s in score]
        pl.errorbar(x_coordinates, y_coordinates, yerr=y_error, linestyle="-", label=score[-1][-1])

    pl.xlim(0.4, 1.2)
    # pl.ylim(min([min(s1[1]) for s1 in scores1]) * 0.9, max([max(s1[1]) for s1 in scores1]) * 1.4)
    pl.ylim(0, 1.0)
    pl.xlabel('Training Data (% of Data)')
    pl.ylabel('MRE variation over 20 repeats')
    pl.legend(loc='upper right')
    pl.title(name)
    pl.savefig("./figures/" + name + ".png")
    pl.close()

    """ - To generate graphs of the experiments """
    print "#" * 20, "END", "#" * 20


# This is a function that would help to generate numbers to compare the elbow (trade off between amount of training
# and accuracy)


def test_cpm_apache():
    problems = [cpm_apache_training_reduction]
    treatments = [random_where, east_west_where, exemplar_where, base_line]
    global training_percent, testing_percent
    percents = [10*i for i in xrange(1, 10)]
    scores = []
    for problem in problems:
        for treatment in treatments:
            treatscores = []
            for percent in percents:
                training_percent = percent / 100
                testing_percent = 1 - training_percent
                temp = performance_test(dataset=problem, treatment=treatment)
                treatscores.append([[x.fraction for x in temp], [x.value for x in temp], treatment.__name__,
                                    [x.saved_times for x in temp], [x.total_times for x in temp],
                                    [x.evaluations for x in temp]])
            scores.append(treatscores)
    draw(scores, problem.__name__)


def test_BDBJ():
    problems = [cpm_BDBJ]
    treatments = [random_where, east_west_where, exemplar_where, base_line]
    global training_percent, testing_percent
    percents = [10*i for i in xrange(1, 10)]
    scores = []
    for problem in problems:
        for treatment in treatments:
            treatscores = []
            for percent in percents:
                training_percent = percent / 100
                testing_percent = 1 - training_percent
                temp = performance_test(dataset=problem, treatment=treatment)
                treatscores.append([[x.fraction for x in temp], [x.value for x in temp], treatment.__name__,
                                    [x.saved_times for x in temp], [x.total_times for x in temp],
                                    [x.evaluations for x in temp]])
            scores.append(treatscores)
    draw(scores, problem.__name__)


def test_BDBC():
    problems = [cpm_BDBC]
    treatments = [random_where, east_west_where, exemplar_where, base_line]
    global training_percent, testing_percent
    percents = [10*i for i in xrange(1, 10)]
    scores = []
    for problem in problems:
        for treatment in treatments:
            treatscores = []
            for percent in percents:
                training_percent = percent / 100
                testing_percent = 1 - training_percent
                temp = performance_test(dataset=problem, treatment=treatment)
                treatscores.append([[x.fraction for x in temp], [x.value for x in temp], treatment.__name__,
                                    [x.saved_times for x in temp], [x.total_times for x in temp],
                                    [x.evaluations for x in temp]])
            scores.append(treatscores)
    draw(scores, problem.__name__)


def test_SQL():
    problems = [cpm_SQL]
    treatments = [random_where, east_west_where, exemplar_where, base_line]
    global training_percent, testing_percent
    percents = [10*i for i in xrange(1, 10)]
    scores = []
    for problem in problems:
        for treatment in treatments:
            treatscores = []
            for percent in percents:
                training_percent = percent / 100
                testing_percent = 1 - training_percent
                temp = performance_test(dataset=problem, treatment=treatment)
                treatscores.append([[x.fraction for x in temp], [x.value for x in temp], treatment.__name__,
                                    [x.saved_times for x in temp], [x.total_times for x in temp],
                                    [x.evaluations for x in temp]])
            scores.append(treatscores)
    draw(scores, problem.__name__)


def test_x264():
    problems = [cpm_X264]
    treatments = [random_where, east_west_where, exemplar_where, base_line]
    global training_percent, testing_percent
    percents = [10*i for i in xrange(1, 10)]
    scores = []
    for problem in problems:
        for treatment in treatments:
            treatscores = []
            for percent in percents:
                training_percent = percent / 100
                testing_percent = 1 - training_percent
                temp = performance_test(dataset=problem, treatment=treatment)
                treatscores.append([[x.fraction for x in temp], [x.value for x in temp], treatment.__name__,
                                    [x.saved_times for x in temp], [x.total_times for x in temp],
                                    [x.evaluations for x in temp]])
            scores.append(treatscores)
    draw(scores, problem.__name__)


def test_LLVM():
    problems = [cpm_LLVM]
    treatments = [random_where, east_west_where, exemplar_where, base_line]
    global training_percent, testing_percent
    percents = [10*i for i in xrange(1, 10)]
    scores = []
    for problem in problems:
        for treatment in treatments:
            treatscores = []
            for percent in percents:
                training_percent = percent / 100
                testing_percent = 1 - training_percent
                temp = performance_test(dataset=problem, treatment=treatment)
                treatscores.append([[x.fraction for x in temp], [x.value for x in temp], treatment.__name__,
                                    [x.saved_times for x in temp], [x.total_times for x in temp],
                                    [x.evaluations for x in temp]])
            scores.append(treatscores)
    draw(scores, problem.__name__)



def median_where(filename):

    def furthest(one, all_members):
        """Find the distant point (from the population) from one (point)"""
        ret = None
        ret_distance = -1 * 1e10
        for member in all_members:
            if equal_list(one, member) is True:
                continue
            else:
                temp = euclidean_distance(one, member)
                if temp > ret_distance:
                    ret = member
                    ret_distance = temp
        return ret

    def find_x_cord(member, pole1, pole2):
        member_dec = member[:-1]
        pole1_dec = pole1[:-1]
        pole2_dec = pole2[:-1]

        a = euclidean_distance(member_dec, pole1_dec)
        b = euclidean_distance(member_dec, pole2_dec)
        c = euclidean_distance(pole1_dec, pole2_dec)

        return [member, (a**2 + c**2 - b**2)//(2*c)]

    from random import choice
    cluster_table = where_clusterer(filename)

    ret = []
    for cluster in cluster_table:
        # Remove the cluster label from the cluster[-1]: members of the population
        cluster[-1] = [c[:-1] for c in cluster[-1]]
        # Randomly select one of the members of the cluster
        one = choice(cluster[-1])
        east = furthest(one, cluster[-1])
        west = furthest(east, cluster[-1])

        t_store = []
        for member in cluster[-1]:
            t_store.append(find_x_cord(member, east, west))
        t_store = sorted(t_store, key=lambda x: x[-1])
        ret.append(t_store[int(len(t_store)/2)][0])

    # print len(ret), 2*len(cluster_table)
    assert(len(ret) == len(cluster_table)), "Something's wrong"
    return ret, len(ret)







def start_test():
    # test_cpm_apache()
    # test_BDBC()
    # test_BDBJ()
    # test_SQL()
    test_x264()
    test_LLVM()


if __name__ == "__main__":
    start_test()
