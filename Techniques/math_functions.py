def combination(n, r):
    from math import factorial
    return factorial(n) / factorial(r) / factorial(n - r)