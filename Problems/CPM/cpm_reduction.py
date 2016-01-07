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
    assert (len(lista) == len(listb)), "Not a valid comparison"
    for i, j in zip(lista, listb):
        if i == j:
            pass
        else:
            return False
    return True


def WHEREDataTransformation(filename):
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


def east_west_where(filename):
    def furthest(one, all_members):
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
    cluster_table = WHEREDataTransformation(filename)

    ret = []
    for cluster in cluster_table:
        cluster[-1] = [c[:-1] for c in cluster[-1]]
        one = choice(cluster[-1])
        east = furthest(one, cluster[-1])
        west = furthest(east, cluster[-1])
        ret.append(east)
        ret.append(west)

    return ret


#
def exemplar_where(filename):
    cluster_table = WHEREDataTransformation(filename)

    ret = []
    for cluster in cluster_table:
        cluster[-1] = [c[:-1] for c in cluster[-1]]
        ret.append(sorted(cluster[-1], key=lambda x: x[-1])[0])
    return ret


def random_where(filename):
    cluster_table = WHEREDataTransformation(filename)

    ret = []
    for cluster in cluster_table:
        cluster[-1] = [c[:-1] for c in cluster[-1]]
        from random import choice
        ret.append(choice(cluster[-1]))
    return ret


def base_line(filename="./Data/Apache_AllMeasurements.csv"):
    cluster_table = WHEREDataTransformation(filename)

    ret = []
    for cluster in cluster_table:
        cluster[-1] = [c[:-1] for c in cluster[-1]]
        ret.extend(cluster[-1])
    return ret


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


testing_percent = 0
training_percent = 40


class cpm_reduction(jmoo_problem):
    def get_training_data(self, method=base_line):
        global testing_percent, training_percent
        from copy import deepcopy
        transformed_data = deepcopy(self.data)
        random_selection = self.get_testing_data(transformed_data, testing_percent)

        temp_file_generation(self.header, random_selection)
        training = method(temp_file_name)
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
        for i, j in zip(self.testing_dependent, prediction):
            mre.append(abs(i - j) / float(i))
        return sum(mre) / len(mre)

    def print_data(self):
        print len(self.data)

    def evaluate(self, input=None):
        if input:
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

    def evalConstraints(prob, input=None):
        return False


class cpm_apache_training_reduction(cpm_reduction):
    def __init__(self, treatment, number=50, requirements=9, name="CPM_APACHE",
                 filename="./Problems/CPM/Data/Apache_AllMeasurements.csv"):

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

    def generate_decision_tree(self):
        #TODO: build it

    def validate(self, tsolution):
        solution = [int(round(i, 0)) for i in tsolution]
        if sum(solution) == 0: return False
        if solution[0] != 1:
            return False
        if solution[7] == 1 and solution[8] != 0:
            return False
        return True


class cpm_BDBC(cpm_reduction):
    def __init__(self, treatment, number=50, requirements=18, name="CPM_BDBC",
                 filename="./Problems/CPM//Data/BDBC_AllMeasurements.csv"):

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


class cpm_BDBJ(cpm_reduction):
    def __init__(self, treatment, number=50, requirements=26, name="CPM_BDBJ",
                 filename="./Problems/CPM/Data/BDBJ_AllMeasurements.csv"):

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


class cpm_LLVM(cpm_reduction):
    def __init__(self, treatment, number=50, requirements=11, name="CPM_LLVM",
                 filename="./Problems/CPM/Data/LLVM_AllMeasurements.csv"):

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

    def validate(self, tsolution):
        solution = [int(round(i, 0)) for i in tsolution]
        if sum(solution) == 0: return False
        if solution[0] != 1: return False
        return True


class cpm_SQL(cpm_reduction):
    def __init__(self, treatment, number=50, requirements=39, name="CPM_SQL",
                 filename="./Problems/CPM/Data/SQL_AllMeasurements.csv"):

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


class cpm_X264(cpm_reduction):
    def __init__(self, treatment, number=50, requirements=16, fraction=0.5, name="cpm_X264",
                 filename="./Problems/CPM/Data/X264_AllMeasurements.csv"):

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
    def __init__(self, fraction, value):
        self.fraction = fraction
        self.value = value


def performance_test(dataset, treatment):
    repeats = 20
    scores = []
    print "Dataset: ", dataset.__name__, " Repeats: ", repeats, " Treatment: ", treatment.__name__, training_percent
    temp_store = []
    for repeat in xrange(repeats):
        print repeat, " ",
        p = dataset(treatment=treatment)
        temp_store.append(p.test_data())
    scores.append(data_container(training_percent, temp_store))
    return scores
    # draw([x.fraction for x in scores], [x.value for x in scores], problem.name)

