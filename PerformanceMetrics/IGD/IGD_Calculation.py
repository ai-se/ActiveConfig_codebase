# IGD(inverse generational distance) metric which as a single metric which can provide a combined information about
#  the convergence and diversity of the obtained solutions.


from __future__ import division
from Techniques.euclidean_distance import euclidean_distance


def IGD(approximation_points, original_points):

    summ = 0
    for o in original_points:
        min_distance = 1e32
        for a in approximation_points:
            min_distance = min(min_distance, euclidean_distance(o, a))
        summ += min_distance
    return summ/len(original_points)
