import math
import time
from fastecdsa.point import Point

h = lambda a, l: math.ceil(l / a)
v = lambda a, b: math.ceil(a / b)

# formula for array size is over (13) equation
createPrecomputationArray = lambda G, a, b, l: [[Point.IDENTITY_ELEMENT for _ in range(2 ** h(a, l))] for _ in
                                                range(v(a, b))]
getBinaryArray = lambda number: [int(entity) for entity in bin(number)[2:]]
getEmptyArray = lambda size: [0 for _ in range(size)]


def precompute(G, l, S, a, b):
    t0 = time.perf_counter()

    array = createPrecomputationArray(G, a, b, l)

    for row in range(1, 2 ** h(a, l)):
        array[0][row] = 0 * G  # POI
        binaryArray = getBinaryArray(row)
        l = h(a, l) - len(binaryArray)
        binary = getEmptyArray(h(a, l))
        binary[l:] = binaryArray

        array = performSquarting(G, a, l, array, row, binary)
        array = performMultiplying(a, b, row, array)

    t1 = time.perf_counter()
    print("Time elapsed for precomputation:", t1 - t0)

    return array


def performSquarting(G, a, l, array, row, binary):
    for iterator in range(h(a, l)):
        exponent = pow(2, iterator * a)
        r = G * exponent
        array[0][row] += r * binary[-(iterator + 1)]
    return array


def performMultiplying(a, b, row, array):
    for iterator in range(1, v(a, b)):
        array[iterator][row] = array[0][row] * (pow(2, iterator * b))
    return array
