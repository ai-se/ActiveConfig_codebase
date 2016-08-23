from __future__ import division
import sys, os, inspect

parentdir = os.path.realpath(
    os.path.abspath(os.path.join(os.path.split(inspect.getfile(inspect.currentframe()))[0], "../")))
if parentdir not in sys.path:
    sys.path.insert(0, parentdir)

import pandas as pd
import numpy as np
from Techniques.euclidean_distance import euclidean_distance

distance_matrix = []


def get_c_r(content, r):
    global distance_matrix
    lines = len(content)
    sum_value = 0
    for i in xrange(lines):
        for j in xrange(i, lines):
            if distance_matrix[i][j] < r:
                sum_value += 1
            else:
                sum_value += 0
    print '#',
    sys.stdout.flush()
    return np.log((2/lines * (lines-1)) * sum_value)


def highest_r():
    global distance_matrix
    max_value = -1e20
    for d in distance_matrix:
            max_value = max(max_value, max(d))
    return max_value

def generate_distance_matrix(content):
    lines = len(content)
    global distance_matrix
    for i in xrange(lines):
        temp = []
        for j in xrange(lines):
            temp.append(euclidean_distance(content.iloc[i], content.iloc[j]))
        distance_matrix.append(temp)

def generate_distance_matrix2(X):
    global distance_matrix
    from scipy.spatial.distance import pdist, squareform
    distance_matrix = squareform(pdist(X,'euclidean'))

def run(cont, size):
    print size,
    content = cont[:size]
    high_r = highest_r()
    values_r = [i*0.05*high_r for i in xrange(1, 20)]
    log_c_r = [get_c_r(content, r) for r in values_r]
    log_r = map(lambda x:np.log(x), values_r)
    slopes = []
    for i in xrange(len(log_r)-1):
        slopes.append((log_c_r[i+1]-log_c_r[i])/(log_r[i+1]-log_r[i]))
    return max(slopes)

def wrapper_function(filename):
    content = pd.read_csv("./data/" + filename + ".csv")
    generate_distance_matrix2(content)
    sizes = [100, 500, 1000, 2000, 3000, 4000, 8000, 10000]

    dimensions = []
    for size in sizes:
        dimensions.append(run(content, size))
        print "."
    import pickle
    pickle.dump(dimensions, open("./Results/" + filename + ".p", "wb"))
    import matplotlib.pyplot as plt
    plt.plot(sizes, dimensions)
    plt.xlabel("Number of points")
    plt.ylabel("Fractal Dimensions")
    plt.savefig("./Figs/" + filename + ".png")
    plt.clf()

files = ["1_dimension", "2_dimension", "3_dimension", "5_dimension", "8_dimension", "16_dimension", "32_dimension", "64_dimension", "128_dimension"]
for file in files:
    print file
    wrapper_function(file)