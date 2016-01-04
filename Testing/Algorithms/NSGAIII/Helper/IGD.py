import os
os.chdir("../")
print os.getcwd()


def euclidean_distance(list1, list2):
    assert(len(list1) == len(list2)), "The points don't have the same dimension"
    distance = sum([(i - j) ** 2 for i, j in zip(list1, list2)]) ** 0.5
    assert(distance >= 0), "Distance can't be less than 0"
    return distance


def IGD(approximation_points, original_points):
    summ = 0
    for o in original_points:
        min_distance = 1e32
        for a in approximation_points:
            min_distance = min(min_distance, euclidean_distance(o, a))
        summ += min_distance
    return summ/len(original_points)



def readpf():
    filename = "./Helper/originalpf.txt"
    content = []
    for line in open(filename, "r").readlines():
        content.append([float(l) for l in line.split()])
    return content

def read_file(filename):
    population = []
    for line in open(filename, "r").readlines():
        if line == "\n": continue
        decision = 7
        objectives = 3
        line = [float(a) for a in line.split()]
        population.append(line[len(line) - objectives:])
    return population

result = []
for file in sorted(os.listdir("./Results/")):
    filename = "./Results/" + file
    print filename
    number = filename.split("/")[-1].split(".")[0]
    result.append([int(number), IGD(read_file(filename), readpf())])

for i, j in sorted(result, key=lambda x:x[0]):
    print i, j