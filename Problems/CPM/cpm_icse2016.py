from __future__ import division
import sys, os, inspect
parentdir = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe()))[0],"../../")))
if parentdir not in sys.path:
    sys.path.insert(0, parentdir)

parentdir = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe()))[0],"../../Techniques")))
if parentdir not in sys.path:
    sys.path.insert(0, parentdir)
from jmoo_objective import *
from jmoo_decision import *
from jmoo_problem import jmoo_problem
from euclidean_distance import euclidean_distance
from Problems.CPM.utilities.csv_utilities import read_csv

from sklearn import tree
import itertools


testing_percent = 0
training_percent = 0
problem_name = ""
percent_name = -1
repeat_name = -1

def equal_list(lista, listb):
    assert(len(lista) == len(listb)), "Not a valid comparison"
    for i, j in zip(lista, listb):
        if i == j: pass
        else: return False
    return True

def WHEREDataTransformation(filename):
    global problem_name, percent_name, repeat_name
    cluster_file_name = "./Cluster_Data/" + str(problem_name) + "_" + str(percent_name) + "_" + str(repeat_name) + ".txt"
    # import pdb
    # pdb.set_trace()

    if os.path.isfile(cluster_file_name) is True:
        print "LOADED FROM THE FILE: ", cluster_file_name
        import pickle
        cluster_table = pickle.load(open(cluster_file_name, "rb"))
        return cluster_table


    from utilities.Tools.methods1 import wrapper_createTbl
    # The Data has to be access using this attribute table._rows.cells
    transformed_table = [[int(z) for z in x.cells[:-1]] + x.cells[-1:] for x in wrapper_createTbl(filename)._rows]
    cluster_numbers = set(map(lambda x: x[-1], transformed_table))

    #debug
    dict = {}
    for line in transformed_table:
        if line[-1] in dict.keys(): dict[line[-1]] += 1
        else: dict[line[-1]] = 1

    # separating clusters
    # the element looks like [clusterno, rows]
    cluster_table = []
    for number in cluster_numbers:
        cluster_table.append([number]+ [filter(lambda x: x[-1] == number, transformed_table)])

    import pickle
    pickle.dump(cluster_table, open(cluster_file_name, "wb"))

    return cluster_table

def east_west_where(filename):
    def furthest(one, all_members):
        ret = None
        ret_distance = -1 * 1e10
        for member in all_members:
            if equal_list(one, member) is True: continue
            else:
                temp = euclidean_distance(one, member)
                if temp > ret_distance:
                    ret = member
                    ret_distance = temp
        return ret
    from random import choice
    cluster_table = WHEREDataTransformation(filename)

    ret = []
    print ">>>>>>Length of cluster table: ", len(cluster_table)
    for cluster in cluster_table:
        cluster[-1] = [c[:-1] for c in cluster[-1]]
        one = choice(cluster[-1])
        east = furthest(one, cluster[-1])
        west = furthest(east, cluster[-1])
        ret.append(east)
        ret.append(west)

    # print len(ret), 2*len(cluster_table)
    assert(len(ret) == 2*len(cluster_table)), "Something's wrong"
    return ret, len(ret)


def exemplar_where(filename):
    cluster_table = WHEREDataTransformation(filename)

    ret = []
    print "Length of cluster table: ", len(cluster_table)
    for cluster in cluster_table:
        cluster[-1] = [c[:-1] for c in cluster[-1]]
        ret.append(sorted(cluster[-1], key=lambda x: x[-1])[0])
        # ret.append(sorted(cluster[-1], key=lambda x: x[-1])[int(len(cluster[-1])/2)])

    return ret, len(cluster_table)


def exemplar_where_median(filename):
    cluster_table = WHEREDataTransformation(filename)

    ret = []
    print "Length of cluster table: ", len(cluster_table)
    for cluster in cluster_table:
        cluster[-1] = [c[:-1] for c in cluster[-1]]
        ret.append(sorted(cluster[-1], key=lambda x: x[-1])[int(len(cluster[-1])/2)])

    return ret, len(cluster_table)

def random_where(filename):
    cluster_table = WHEREDataTransformation(filename)

    ret = []
    print "Length of cluster table: ", len(cluster_table)
    for cluster in cluster_table:
        cluster[-1] = [c[:-1] for c in cluster[-1]]
        from random import choice
        ret.append(choice(cluster[-1]))
    return ret, len(cluster_table)


def base_line(filename="./Data/Apache_AllMeasurements.csv"):
    # cluster_table = WHEREDataTransformation(filename)
    ret0 = open(filename, "r").readlines()[1:]
    ret0 = [x.replace("\r", "").replace("\n", "") for x in ret0]
    ret = []
    for r in ret0:
        ret.append([int(float(x)) for x in r.split(",")])

    print "Length of cluster table: ", len(ret)
    return ret, len(ret)

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




class cpm_apache_data_frame:
    newid = itertools.count().next
    def __init__(self, list):
        self.id = cpm_apache_data_frame.newid()
        self.Base = list[0]
        self.HostnameLookups = list[1]
        self.KeepAlive = list[2]
        self.EnableSendfile = list[3]
        self.FollowSymLinks = list[4]
        self.AccessLog = list[5]
        self.ExtendedStatus = list[6]
        self.InMemory = list[7]
        self.Handle = list[8]
        self.Performance = list[9]


class cpm_reduction(jmoo_problem):
    def get_training_data(self, method=base_line):
        # print method.__name__
        global testing_percent, training_percent
        from copy import deepcopy
        transformed_data = deepcopy(self.data)
        random_selection = self.get_testing_data(transformed_data, testing_percent)
        # print "Length of the $$training set: ", len(random_selection)

        temp_file_generation(self.header, random_selection)
        training, self.no_of_clusters = method(temp_file_name)
        temp_file_removal()

        #
        # print "Length of training set: ", len(training),
        # print "Length of testing set: ", len(self.testing_dependent)

        return [row[:-1] for row in training], [row[-1] for row in training]

    def get_testing_data(self, data, testing_perc):
        # print "testing_percent: ", testing_percent
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
            mre.append(abs(i - j)/float(i))
        return sum(mre)/len(mre)

    def print_data(self):
        print len(self.data)

    def evaluate(self, input = None):
        print "This needs to be changed"
        exit()
        if input:
            for i,decision in enumerate(self.decisions):
                decision.value = input[i]
            input = [round(decision.value, 1) for decision in self.decisions]
            # print "Input: ", input
            assert(len(input) == len(self.decisions)), "Something's wrong"
            prediction = self.CART.predict(input)
            return prediction
        else:
            assert(False), "BOOM"
            exit()


    def evalConstraints(prob,input = None):
        return False

    def find_total_time(self):
        return sum([d[-1] for d in self.data])


class cpm_apache_training_reduction(cpm_reduction):
    def __init__(self, treatment, requirements=9, name="CPM_APACHE", filename="./Data/Apache_AllMeasurements.csv"):
    # def __init__(self, treatment, number=50, requirements=9, name="CPM_APACHE", filename="./Problems/CPM/Data/Apache_AllMeasurements.csv"):

        self.name = name
        self.filename = filename
        self.no_of_clusters = 0
        # Setting up to create decisions
        names = ["x"+str(i+1) for i in xrange(requirements)]
        lows = [0 for _ in xrange(requirements)]
        ups = [1 for _ in xrange(requirements)]
        # Generating decisions
        self.decisions = [jmoo_decision(names[i], lows[i], ups[i]) for i in range(requirements)]
        # Generating Objectives (this is single objective)
        self.objectives = [jmoo_objective("f1", True)]
        # Read Data
        self.header, self.data = read_csv(self.filename, header=True)

        self.training_independent, self.training_dependent,  = self.get_training_data(method=treatment)
        global training_percent
        from math import log, ceil
        # # print training_percent,
        # print "=" * 20
        # print "Reduced Data: ", self.training_dependent
        # print "total run time: ", sum(self.training_dependent)
        # print "totol total run time: ", self.find_total_time()
        # print "sadsadsa time: ", self.find_total_time() - sum(self.training_dependent)
        # print "Saving Percentage: ", (sum(self.training_dependent)/self.find_total_time()) *100
        # print "Length of self.Data: ", len(self.Data)
        # print treatment.__name__


        print "Length of training dataset: ", len(self.training_dependent), len(self.data), (2*log(len(self.data) * training_percent, 2))
        self.CART = tree.DecisionTreeRegressor()
        self.CART = self.CART.fit(self.training_independent, self.training_dependent)
        self.saved_time = (self.find_total_time() - sum(self.training_dependent))/10**4
        # print "Saved_time: ", self.saved_time
        # print "asdasdas Saving : ", ((self.find_total_time() - self.saved_time)/self.find_total_time()) * 100
        # raw_input()

class cpm_BDBC(cpm_reduction):
    def __init__(self, treatment, number=50, requirements=18, name="CPM_BDBC", filename="./Data/BDBC_AllMeasurements.csv"):
    # def __init__(self, treatment, number=50, requirements=18, name="CPM_BDBC", filename="./Problems/CPM//Data/BDBC_AllMeasurements.csv"):

        self.name = name
        self.filename = filename
        if treatment is None: treatment = east_west_where
        elif treatment == 0: treatment = base_line
        names = ["x"+str(i+1) for i in xrange(requirements)]
        lows = [0 for _ in xrange(requirements)]
        ups = [1 for _ in xrange(requirements)]
        self.decisions = [jmoo_decision(names[i], lows[i], ups[i]) for i in range(requirements)]
        self.objectives = [jmoo_objective("f1", True)]
        self.header, self.data = read_csv(self.filename, header=True)

        self.training_independent, self.training_dependent = self.get_training_data(method=treatment)
        global training_percent
        # print "inside: ", training_percent
        from math import log
        # print "Length of training dataset: ", len(self.training_dependent), len(self.Data), (2*log(len(self.Data) * training_percent, 2))

        self.CART = tree.DecisionTreeRegressor()
        self.CART = self.CART.fit(self.training_independent, self.training_dependent)

        self.saved_time = (self.find_total_time() - sum(self.training_dependent))/10**4

class cpm_BDBJ(cpm_reduction):
    def __init__(self, treatment, number=50, requirements=26, name="CPM_BDBJ", filename="./Data/BDBJ_AllMeasurements.csv"):
    # def __init__(self, treatment, number=50, requirements=26, name="CPM_BDBJ", filename="./Problems/CPM/Data/BDBJ_AllMeasurements.csv"):

        self.name = name
        self.filename = filename
        # Setting up to create decisions
        names = ["x"+str(i+1) for i in xrange(requirements)]
        lows = [0 for _ in xrange(requirements)]
        ups = [1 for _ in xrange(requirements)]
        # Generating decisions
        self.decisions = [jmoo_decision(names[i], lows[i], ups[i]) for i in range(requirements)]
        # Generating Objectives (this is single objective)
        self.objectives = [jmoo_objective("f1", True)]
        # Read Data
        self.header, self.data = read_csv(self.filename, header=True)



        self.training_independent, self.training_dependent = self.get_training_data(method=treatment)
        global training_percent
        # print training_percent,
        from math import log
        # print "Length of training dataset: ", len(self.training_dependent), len(self.Data), (2*log(len(self.Data) * training_percent, 2))

        self.CART = tree.DecisionTreeRegressor()
        self.CART = self.CART.fit(self.training_independent, self.training_dependent)



        self.saved_time = (self.find_total_time() - sum(self.training_dependent))/10**4

class cpm_LLVM(cpm_reduction):
    def __init__(self, treatment, number=50, requirements=11, fraction=0.5, name="CPM_LLVM", filename="./Data/LLVM_AllMeasurements.csv"):
    # def __init__(self, treatment, number=50, requirements=11, name="CPM_LLVM", filename="./Problems/CPM/Data/LLVM_AllMeasurements.csv"):

        self.name = name
        self.filename = filename
        # Setting up to create decisions
        names = ["x"+str(i+1) for i in xrange(requirements)]
        lows = [0 for _ in xrange(requirements)]
        ups = [1 for _ in xrange(requirements)]
        # Generating decisions
        self.decisions = [jmoo_decision(names[i], lows[i], ups[i]) for i in range(requirements)]
        # Generating Objectives (this is single objective)
        self.objectives = [jmoo_objective("f1", True)]
        # Read Data
        self.header, self.data = read_csv(self.filename, header=True)



        self.training_independent, self.training_dependent = self.get_training_data(method=treatment)
        global training_percent
        # print training_percent,
        from math import log
        # print "Length of training dataset: ", len(self.training_dependent), len(self.Data), (2*log(len(self.Data) * training_percent, 2))

        self.CART = tree.DecisionTreeRegressor()
        self.CART = self.CART.fit(self.training_independent, self.training_dependent)

        self.saved_time = (self.find_total_time() - sum(self.training_dependent))/10**4

class cpm_SQL(cpm_reduction):
    def __init__(self, treatment, number=50, requirements=39, fraction=0.5, name="CPM_SQL", filename="./Data/SQL_AllMeasurements.csv"):
    # def __init__(self, treatment, number=50, requirements=39, name="CPM_SQL", filename="./Problems/CPM/Data/SQL_AllMeasurements.csv"):

        self.name = name
        self.filename = filename
        # Setting up to create decisions
        names = ["x"+str(i+1) for i in xrange(requirements)]
        lows = [0 for _ in xrange(requirements)]
        ups = [1 for _ in xrange(requirements)]
        # Generating decisions
        self.decisions = [jmoo_decision(names[i], lows[i], ups[i]) for i in range(requirements)]
        # Generating Objectives (this is single objective)
        self.objectives = [jmoo_objective("f1", True)]
        # Read Data
        self.header, self.data = read_csv(self.filename, header=True)

        self.training_independent, self.training_dependent = self.get_training_data(method=treatment)
        global training_percent
        # print training_percent,
        from math import log
        # print "Length of training dataset: ", len(self.training_dependent), len(self.Data), (2*log(len(self.Data) * training_percent, 2))

        self.CART = tree.DecisionTreeRegressor()
        self.CART = self.CART.fit(self.training_independent, self.training_dependent)
        self.saved_time = (self.find_total_time() - sum(self.training_dependent))/10**4


class cpm_X264(cpm_reduction):
    def __init__(self, treatment, number=50, requirements=16, fraction=0.5, name="cpm_X264", filename="./Data/X264_AllMeasurements.csv"):
    # def __init__(self, treatment, number=50, requirements=16, fraction=0.5, name="cpm_X264", filename="./Problems/CPM/Data/X264_AllMeasurements.csv"):

        self.name = name
        self.filename = filename
        # Setting up to create decisions
        names = ["x"+str(i+1) for i in xrange(requirements)]
        lows = [0 for _ in xrange(requirements)]
        ups = [1 for _ in xrange(requirements)]
        # Generating decisions
        self.decisions = [jmoo_decision(names[i], lows[i], ups[i]) for i in range(requirements)]
        # Generating Objectives (this is single objective)
        self.objectives = [jmoo_objective("f1", True)]
        # Read Data
        self.header, self.data = read_csv(self.filename, header=True)



        self.training_independent, self.training_dependent = self.get_training_data(method=treatment)
        global training_percent
        # print training_percent,
        from math import log
        # print "Length of training dataset: ", len(self.training_dependent), len(self.Data), (2*log(len(self.Data) * training_percent, 2))

        self.CART = tree.DecisionTreeRegressor()
        self.CART = self.CART.fit(self.training_independent, self.training_dependent)
        self.saved_time = (self.find_total_time() - sum(self.training_dependent))/10**4


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
    repeats = 5
    scores = []
    saved_times = []
    total_times = []
    evaluations = []
    print dataset.__name__, treatment.__name__,
    temp_store = []
    for repeat in xrange(repeats):
        repeat_name = repeat
        # print repeat, " ",
        # print "Dataset: ", dataset.__name__, " Repeats: ", repeats,
        # print " Treatment: ", treatment.__name__, "Training Percent: ", training_percent,
        print ".",
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
    filename = "./Logs/" + name + ".txt"
    fdesc = open(filename, "w")
    fdesc.write("training_percent, mean, standard_deviation, saved_time, total_time, technique, evaluations \n")
    scores1 = []
    import numpy as np
    for row in data:
        scores = []
        for d in row:
            print d[1]
            temp = []
            temp.append(d[0])
            temp.append(np.percentile(d[1], 50))
            temp.append(np.percentile(d[1], 75) - np.percentile(d[1], 25))
            temp.append(d[2])
            # temp_string = str(d[0][-1]) + "," + str(np.percentile(d[1], 50)) + "," + str(np.percentile(d[1], 75) -
            #                                         np.percentile(d[1], 25)) + "," + str(d[3][-1]) + "," + str(d[4][-1]//10**4) + "," + str(int(d[-1][-1])) + "," + str(d[2])+"\n"
            temp_string = str(d[0][-1]) + "," + str(np.around(np.mean(d[1]), 3)) + "," + str(np.around(np.std(d[1]), 3)) + "," + str(d[3][-1]) + "," + str(d[4][-1]//10**4) + "," + str(int(d[-1][-1])) + "," + str(d[2])+"\n"
            print temp_string
            fdesc.write(temp_string)
            scores.append(temp)
        scores1.append(scores)
    fdesc.close()


    for score in scores1:
        x_coordinates = [s[0] for s in score]
        y_coordinates = [s[1] for s in score]
        y_error = [s[2] for s in score]
        pl.errorbar(x_coordinates, y_coordinates, yerr=y_error, linestyle="-", label=score[-1][-1])

    pl.xlim(0.0, 1.2)
    # pl.ylim(min([min(s1[1]) for s1 in scores1]) * 0.9, max([max(s1[1]) for s1 in scores1]) * 1.4)
    pl.ylim(0, 1.0)
    pl.xlabel('Training Data (% of Data)')
    pl.ylabel('MRE variation over 20 repeats')
    pl.legend(loc='upper right')
    pl.title(name)
    pl.savefig("./figures/" + name + ".png")
    pl.close()

    print "#" * 20, "END", "#" * 20

# This is a function that would help to generate numbers to compare the elbow (trade off between amount of training
# and accuracy)


def test_cpm_apache():
    problems = [cpm_apache_training_reduction]
    treatments = [random_where, base_line, exemplar_where, east_west_where]
    global training_percent, testing_percent, problem_name, percent_name, problem_name, percent_name
    percents = [10,20,30,40, 50,60,70,80,90]
    scores = []
    for problem in problems:
        problem_name = problem.__name__
        for treatment in treatments:
            treatscores = []
            for percent in percents:
                percent_name = percent
                print percent,
                training_percent = percent/100
                # print "before performance test: ", training_percent
                testing_percent = 1 - training_percent
                temp = performance_test(dataset=problem, treatment=treatment)
                treatscores.append([[x.fraction for x in temp], [x.value for x in temp], treatment.__name__, [x.saved_times for x in temp], [x.total_times for x in temp], [x.evaluations for x in temp]])
            scores.append(treatscores)
    draw(scores, problem.__name__)

def test_BDBJ():
    problems = [cpm_BDBJ]
    treatments = [random_where, base_line, exemplar_where, east_west_where]
    # treatments = [exemplar_where_median, base_line, exemplar_where,]
    global training_percent, testing_percent, problem_name, percent_name
    percents = [10,20,30,40, 50,60,70,80,90]
    scores = []
    for problem in problems:
        problem_name = problem.__name__
        for treatment in treatments:
            treatscores = []
            for percent in percents:
                percent_name = percent
                print percent,
                training_percent = percent/100
                testing_percent = 1 - training_percent
                temp = performance_test(dataset=problem, treatment=treatment)
                treatscores.append([[x.fraction for x in temp], [x.value for x in temp], treatment.__name__, [x.saved_times for x in temp], [x.total_times for x in temp], [x.evaluations for x in temp]])
            scores.append(treatscores)
    draw(scores, problem.__name__)

def test_BDBC():
    problems = [cpm_BDBC]
    treatments = [random_where, base_line, exemplar_where, east_west_where]
    # treatments = [exemplar_where_median, base_line, exemplar_where,]
    global training_percent, testing_percent, problem_name, percent_name
    percents = [10,20,30,40, 50,60,70,80,90]
    scores = []
    for problem in problems:
        problem_name = problem.__name__
        for treatment in treatments:
            treatscores = []
            for percent in percents:
                percent_name = percent
                print percent,
                training_percent = percent/100
                testing_percent = 1 - training_percent
                temp = performance_test(dataset=problem, treatment=treatment)
                treatscores.append([[x.fraction for x in temp], [x.value for x in temp], treatment.__name__, [x.saved_times for x in temp], [x.total_times for x in temp], [x.evaluations for x in temp]])
            scores.append(treatscores)
    draw(scores, problem.__name__)


def test_SQL():
    problems = [cpm_SQL]
    treatments = [exemplar_where, random_where, base_line,  east_west_where]
    # treatments = [exemplar_where_median, base_line, exemplar_where,]
    global training_percent, testing_percent, problem_name, percent_name
    percents = [10,20,30,40, 50,60,70,80,90]
    scores = []
    for problem in problems:
        problem_name = problem.__name__
        for treatment in treatments:
            treatscores = []
            for percent in percents:
                percent_name = percent
                print percent,
                training_percent = percent/100
                testing_percent = 1 - training_percent
                temp = performance_test(dataset=problem, treatment=treatment)
                treatscores.append([[x.fraction for x in temp], [x.value for x in temp], treatment.__name__, [x.saved_times for x in temp], [x.total_times for x in temp], [x.evaluations for x in temp]])
            scores.append(treatscores)
    draw(scores, problem.__name__)


def test_x264():
    problems = [cpm_X264]
    treatments = [random_where, base_line, exemplar_where, east_west_where]
    # treatments = [random_where, base_line, exemplar_where, east_west_where]
    global training_percent, testing_percent, problem_name, percent_name
    percents = [10,20,30,40, 50,60,70,80,90]
    scores = []
    for problem in problems:
        problem_name = problem.__name__
        for treatment in treatments:
            treatscores = []
            for percent in percents:
                percent_name = percent
                print percent,
                training_percent = percent/100
                testing_percent = 1 - training_percent
                temp = performance_test(dataset=problem, treatment=treatment)
                treatscores.append([[x.fraction for x in temp], [x.value for x in temp], treatment.__name__, [x.saved_times for x in temp], [x.total_times for x in temp], [x.evaluations for x in temp]])
            scores.append(treatscores)
    draw(scores, problem.__name__)

def test_LLVM():
    problems = [cpm_LLVM]
    treatments = [random_where, base_line, exemplar_where, east_west_where]
    # treatments = [random_where, base_line, exemplar_where, east_west_where]
    global training_percent, testing_percent, problem_name, percent_name
    percents = [10,20,30,40, 50,60,70,80,90]
    scores = []
    for problem in problems:
        problem_name = problem.__name__
        for treatment in treatments:
            treatscores = []
            for percent in percents:
                percent_name = percent
                print percent,
                training_percent = percent/100
                testing_percent = 1 - training_percent
                # print "1 training_percent: ", training_percent
                temp = performance_test(dataset=problem, treatment=treatment)
                treatscores.append([[x.fraction for x in temp], [x.value for x in temp], treatment.__name__, [x.saved_times for x in temp], [x.total_times for x in temp], [x.evaluations for x in temp]])
            scores.append(treatscores)
    draw(scores, problem.__name__)


def start_test():
    test_cpm_apache()
    test_BDBJ()
    test_BDBC()
    test_SQL()
    test_x264()
    test_LLVM()


def offline_draw( name):
    from collections import defaultdict
    import pylab as pl
    filename = "./Logs/" + name + ".txt"
    fdesc = open(filename, "r")
    scores = defaultdict(list)
    for i, line in enumerate(fdesc):
        if i == 0: continue
        line_split = line.split(",")
        # print ">> ", line_split
        if line_split[-1] not in scores.keys():  scores[line_split[-1]] = []
        scores[line_split[-1]].append([float(xx) for xx in line_split[:-2]])


    ymin = 1e10
    ymax = -1e10
    for key in scores.keys():
        score = scores[key]
        # for score in score_temp:
        #     print score
        #     raw_input()
        # print score
        x_coordinates = [s[0] for s in score]
        y_coordinates = [s[1]*100 for s in score]
        # y_error = [s[2]*100 for s in score]
        y_error = [0 for s in score]
        ymin = min(min(y_coordinates), ymin)
        ymax = max(max(y_coordinates), ymax)
        # print x_coordinates
        # print y_coordinates
        # print y_error
        # print key
        # pl.errorbar(x_coordinates, y_coordinates, yerr=y_error, linestyle="-", label=key)
        pl.plot(x_coordinates, y_coordinates, label=key)

    print ymin
    print ymax
    pl.xlim(0.0, 1.2)
    pl.ylim(ymin * 0.9, ymax * 1.6)
    # pl.ylim(0, 1.0)
    pl.xlabel('Training Data (% of Data)')
    pl.ylabel('MRE variation over 20 repeats')
    pl.legend(loc='upper right')
    pl.title(name)
    pl.savefig("./figures/" + name + "1.png")

    pl.close()

def delete_file(filenames):
    for filename in filenames:
        os.remove(filename)

def delete_cluster_data():
    cluster_data_dir = "./Cluster_Data/"
    files = os.listdir(cluster_data_dir)
    files = [cluster_data_dir + f for f in files]
    delete_file(files)

# def clear_logging():


def start_drawing():
    problems = [ "cpm_BDBC", "cpm_BDBJ", "cpm_LLVM", "cpm_SQL", "cpm_X264"]
    for problem in problems:
        offline_draw(problem)

if __name__ == "__main__":
    # start_drawing()
    from random import seed
    seed(1)
    start_test()
    # delete_cluster_data()