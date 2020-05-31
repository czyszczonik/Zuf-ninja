import math
from fastecdsa.point import Point

_DEFAULT_ALPHA = 1
computeStorage = lambda a, b, l: ((2 ** h(l, a)) - 1) * vl(a, b, l) + (2 ** (h(l, a) - 1) - 1) * (v(a, b) - vl(a, b, l))
computeCost = lambda a, b, l, alpha=_DEFAULT_ALPHA: ((2 ** (h(l, a) - 1)) - 1) / (2 ** (h(l, a) - 1)) * (a - al(l, a)) \
                                                    + (((2 ** h(l, a)) - 1) / (2 ** h(l, a))) * al(l, a) - 1 + alpha * (
                                                            b - 1)
# formula for array size is over (13) equation
createPrecomputationArray = lambda G, a, b, l: [[Point.IDENTITY_ELEMENT for _ in range(2 ** h(l, a))] for _ in
                                                range(v(a, b))]
getBinaryArray = lambda number: [int(entity) for entity in bin(number)[2:]]
getEmptyArray = lambda size: [0 for _ in range(size)]

h = lambda l, a: math.ceil(l / a)
al = lambda l, a: l - a * (h(l, a) - 1)
v = lambda a, b: math.ceil(a / b)
vl = lambda a, b, l: math.ceil(al(l, a) / b)
