"""
This code is to generate
i. random solutions
ii. use the data from the spl datasets
then plot the first and second eigen vectors
"""
import itertools
class SolutionContainer():
    newid = itertools.count().next

    def __init__(self, data, valid=False):
        self.id = -1 * (SolutionContainer.newid() + 1)
        self.data = data
        self.valid = valid
        self.x = None
        self.y = None

    def set_coordinates(self, x, y):
        self.x = x
        self.y = y


def one(lst):
    """Returns one item in a list, selected at random"""
    from random import uniform
    any = uniform
    return lst[int(any(0, len(lst)-1))]


def hamming_distance(list1, list2):
    return sum([1 if l1!=l2 else 0 for l1, l2 in zip(list1, list2)])


def euclidean_distance(list1, list2):
    assert(len(list1) == len(list2)), "The points don't have the same dimension"
    distance = sum([(i - j) ** 2 for i, j in zip(list1, list2)]) ** 0.5
    assert(distance >= 0), "Distance can't be less than 0"
    return distance


def furthest(point, rows, distance):
    max_distance = -1e32
    for row in rows:
        temp_distance = distance(point, row)
        if temp_distance > max_distance:
            max_distance = temp_distance
            from copy import copy
            maximum_dist_point = copy(row)
    return maximum_dist_point


def project(solutions, distance=hamming_distance):
    "Uses the O(2N) Fastmap heuristic."
    rows = [row.data for row in solutions]
    w = one(rows)  # any row, selected at random
    west = furthest(w, rows, distance)
    east = furthest(west, rows, distance)
    c = distance(east, west)
    for row in solutions:
        a = distance(west, row.data)
        b = distance(east, row.data)
        x = (a ** 2 + c ** 2 - b ** 2) / (2 * c + 0.00001)
        y = (a ** 2 - x ** 2)**0.5
        row.set_coordinates(x, y)
    return solutions


def generate_invalid_solutions(valid_solutions):
    return_solutions = []
    number_of_columns = len(valid_solutions[0].data)
    number_of_solutions = 100 * len(valid_solutions)
    for i in xrange(number_of_solutions):
        while True:
            from random import randint
            temp = [randint(0, 1) for _ in xrange(number_of_columns)]
            validity = True
            for vs in valid_solutions:
                # print vs.data, temp
                score = sum([0 if i == j else 1 for i, j in zip(vs.data, temp)])
                print score
                if score == 0:
                    print ".",
                    validity = False
                    break

            if validity is True: print ">> ";print temp;raw_input();break
        return_solutions.append(SolutionContainer(temp))
    return return_solutions


def generate_graphs(filename):
    content = open(filename).readlines()[1:]
    number_of_columns = len(content[0].split(",")) - 1  # substract 1 because the data also contains class variable

    valid_configurations = [SolutionContainer([1 if x == "Y" else 0 for x in c.split(",")[:-1]], True) for c in content]

    # invalid_configurations = generate_invalid_solutions(valid_configurations)

    from random import randint
    invalid_configurations = [SolutionContainer([randint(0, 1) for _ in xrange(number_of_columns)]) for _ in xrange(100 * len(content))]

    all_content = valid_configurations + invalid_configurations
    # all_content = valid_configurations + valid_configurations

    assert(len(valid_configurations) + len(invalid_configurations) == len(all_content)), "Something is wrong"

    all_content = project(all_content)

    lista = [[content.x, content.y] for content in all_content if content.valid is True]
    listb = [[content.x, content.y] for content in all_content if content.valid is False]

    from scatter import plot_scatter
    plot_scatter(lista, listb, filename.split("/")[-1].split("_")[0])


if __name__ == "__main__":
    filenames = ["Apache_AllMeasurements", "BDBC_AllMeasurements", "BDBJ_AllMeasurements", "LLVM_AllMeasurements",
                  "X264_AllMeasurements", "SQL_AllMeasurements"]
    # filenames = ["WebPortal"] # needs to be changed
    filepath = "../data/"
    extension = ".csv"
    for filename in filenames:
        generate_graphs(filepath+filename+extension)