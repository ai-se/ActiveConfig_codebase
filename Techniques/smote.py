from collections import defaultdict
from random import choice, random

# Flag:
SMOTE_BINARY_CLASSIFICATION = True

def euclidean(list1, list2, k=3):
    assert(len(list1) == len(list2)), "Length mismatch"
    dist = 0
    for a,b in zip(list1[k:], list2[k:]):
        dist += (float(a)-float(b))**2
    return dist**0.5

def nearest(one, data):
    dist = []
    for d in data:
        if one != d:
            dist.append([d, euclidean(one,d)])
    dist = sorted(dist, key=lambda x: x[-1])[:5]
    return [x[0] for x in dist]


def extrapolate(one, two, k=3):
    assert(len(one) == len(two)), "Length mismatch"
    if SMOTE_BINARY_CLASSIFICATION is True:
        assert(one[-1] >= 1 and two[-1] >= 1), "Class mismatch"
    else:
        assert(one[-1] == two[-1]), "Class mismatch"
    new = [0 for _ in xrange(len(one))]
    new[:k] = one[:k]
    for i, (a, b) in enumerate(zip(one[k:], two[k:])):
        a = float(a)
        b = float(b)
        new[k+1] = a + random() * (b - a)
        # new[k+i] = max(min(a, b), min(min(a, b) + random() * abs(a - b), max(a, b)))
    if SMOTE_BINARY_CLASSIFICATION is True:
        new[-1] = float(one[-1]) if random() > 0.5 else float(two[-1])
    else:
        new[-1] = float(one[-1])
    if SMOTE_BINARY_CLASSIFICATION is not True:
        assert(float(one[-1]) == float(two[-1]) == new[-1]), "Objective not correct"
    else:
        assert(float(one[-1]) == new[-1] or float(two[-1]) == new[-1]), "Objectives not correct"
    return new


def smote(reader, k=3):
    def shrink(data, new_size):
        new_data = []
        for _ in xrange(new_size):
            temp = choice(data)
            temp[-1] = float(temp[-1])
            new_data.append(temp[k:])
        return new_data

    def expand(data, new_size):

        new_data = []
        for d in data:
            new_data.append(d[k:])
            new_data[-1][-1] = float(d[-1])
        more = new_size - len(data)
        assert(more > 0), "Something is wrong"
        for _ in xrange(more):
            if len(data) == 1:
                import copy
                temp = copy.deepcopy(data[0])
                temp[-1] = float(temp[-1])
                new_data.append(temp[k:])
            else:
                one = choice(data)
                two = choice(nearest(one, data))
                new_data.append(extrapolate(one, two)[k:])
        assert(len(new_data) == new_size), "Expansion unsuccessful"
        return new_data

    classes = defaultdict(list)
    new_population = []
    for n, line in enumerate(reader):
        if n != 0:
            if SMOTE_BINARY_CLASSIFICATION is not True:
                if line[-1] not in classes.keys():
                    classes[line[-1]] = []
                    classes[line[-1]].append(line)
                else:
                    classes[line[-1]].append(line)
            else:
                    class_type = "True" if float(line[-1]) >= 1 else "False"
                    if class_type not in classes.keys():
                        classes[class_type] = []
                        classes[class_type].append(line)
                    else:
                        classes[class_type].append(line)

    new_class_size = sum([len(a) for a in classes.values()])/len(classes.keys())
    assert(new_class_size > 0), "new class size is 0 or a negative value"
    for i in classes.keys():
        if len(classes[i]) < new_class_size:
            new_population.extend(expand(classes[i], new_class_size))
        elif len(classes[i]) > new_class_size:
            new_population.extend(shrink(classes[i], new_class_size))
        else:
            new_population.extend(map(lambda x: x[k:], classes[i]))

    #---------------- Test----------------------#
    # cl = {}
    # for d in new_population:
    #     if d[-1] not in cl.keys():
    #         cl[d[-1]] = 1
    #     else:
    #         cl[d[-1]] += 1
    # print cl
    # exit()
    assert(len(new_population[0]) == len(line)-k), "Length mismatch"
    # print "OLD: ", len(new_population[0])
    # print new_population[0]
    # print "NEW: ", len(line)
    return new_population, line[:k]

if __name__ == "__main__":
    print euclidean([1,1,1], [2,2,2])