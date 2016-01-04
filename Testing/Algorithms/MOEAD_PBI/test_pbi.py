# def pbi(individual_fitness, weight_vector):
#     def normalized_vector(weight_array):
#         div = norm_vector(weight_array)
#         return [x/div for x in weight_array]
#
#     def norm_vector(weight_array):
#         from math import sqrt
#         return sqrt(sum([wa * wa for wa in weight_array]))
#
#     def inner_product(vector1, vector2):
#         assert(len(vector1) == len(vector2)), "Length of the vectors should be the same"
#         return sum([v1*v2 for v1, v2 in zip(vector1, vector2)])
#
#     # ideal_point = values_to_be_passed["ideal_point"]
#     # normalized_weight_vector = normalized_vector(weight_vector)  # namda after normalization
#     ideal_point = [0.85108, 1.40106, 10.1426 ]
#
#     realB = [0 for _ in xrange(3)]
#
#     # difference between current point and reference point
#     assert(len(individual_fitness) == len(ideal_point)), "Something is wrong"
#     realA = [ifv - ipv for ifv, ipv in zip(individual_fitness, ideal_point)]
#
#     # distance along the line segment
#     from math import fabs
#     d1 = fabs(inner_product(realA, weight_vector))
#
#     # distance to the line segment
#     for n in xrange(3):
#         realB[n] = individual_fitness[n] - (ideal_point[n] + (d1 * weight_vector[n]))
#     d2 = norm_vector(realB)
#     print "d1: ", d1, " d2: ", d2
#     return d1 + (5 * d2)


def pbi( individual_fitness, weight_vector):
    def normalized_vector(weight_array):
        div = norm_vector(weight_array)
        return [x/div for x in weight_array]

    def norm_vector(weight_array):
        from math import sqrt
        return sqrt(sum([wa * wa for wa in weight_array]))

    def inner_product(vector1, vector2):
        assert(len(vector1) == len(vector2)), "Length of the vectors should be the same"
        return sum([v1*v2 for v1, v2 in zip(vector1, vector2)])

    # ideal_point = values_to_be_passed["ideal_point"]
    normalized_weight_vector = normalized_vector(weight_vector)  # namda after normalization
    ideal_point = [0.85108, 1.40106, 10.1426 ]
    realB = [0 for _ in xrange(3)]

    # difference between current point and reference point
    assert(len(individual_fitness) == len(ideal_point)), "Something is wrong"
    realA = [ifv - ipv for ifv, ipv in zip(individual_fitness, ideal_point)]

    # distance along the line segment
    from math import fabs
    d1 = fabs(inner_product(realA, weight_vector))

    # distance to the line segment
    for n in xrange((3)):
        realB[n] = individual_fitness[n] - (ideal_point[n] + (d1 * weight_vector[n]))
    d2 = norm_vector(realB)
    print d1, d2
    return d1 + (5 * d2)


fitness = [88.3352, 212.104, 345.626]
weight = [0,0.0905357,0.995893 ]

print sum(weight)
pbi(fitness, weight)
