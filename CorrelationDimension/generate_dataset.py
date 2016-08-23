import pandas as pd
from random import random

number_of_points = 10000
number_of_dimension = 512

content = [[random() for _ in xrange(number_of_dimension)] for _ in xrange(number_of_points)]

import csv

with open("./Data/" + str(number_of_dimension) + "_dimension.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(content)