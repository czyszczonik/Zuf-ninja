import sys

from qbiaq5.decorators import benchmark
from qbiaq5.math_commons import computeStorage, computeCost


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
    return minCost, parameters
