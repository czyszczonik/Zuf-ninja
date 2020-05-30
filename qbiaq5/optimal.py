import math
import sys
from qbiaq5.decorators import benchmark

_DEFAULT_ALPHA = 1
h = lambda l, a: math.ceil(l / a)
al = lambda l, a: l - a * (h(l, a) - 1)
v = lambda a, b: math.ceil(a / b)
vl = lambda a, b, l: math.ceil(al(l, a) / b)
computeStorage = lambda a, b, l: ((2 ** h(l, a)) - 1) * vl(a, b, l) + (2 ** (h(l, a) - 1) - 1) * (v(a, b) - vl(a, b, l))
computeCost = lambda a, b, l, alpha=_DEFAULT_ALPHA: ((2 ** (h(l, a) - 1)) - 1) / (2 ** (h(l, a) - 1)) * (a - al(l, a)) \
                                                    + (((2 ** h(l, a)) - 1) / (2 ** h(l, a))) * al(l, a) - 1 + alpha * (b - 1)


@benchmark
def find_optimal(length=160, storage=10):
    if length < 3:
        raise TypeError
    minCost = sys.maxsize
    parameters = None
    for blockSize in range(1, length):
        for subBlockSize in range(1, blockSize):
            currentStorage = computeStorage(blockSize, subBlockSize, length)
            if currentStorage <= storage:
                currentCost = computeCost(blockSize, subBlockSize, length)
                if currentCost < minCost:
                    minCost = currentCost
                    parameters = (blockSize, subBlockSize)
                    break
                elif minCost != sys.maxsize:
                    return minCost, parameters
    return minCost, parameters
