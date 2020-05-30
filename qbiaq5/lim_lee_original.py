import math
import sys
import random
import time
from fastecdsa.curve import P521

G = P521.G


alpha = 1  # this value is used in Cubaleska et al.

# From Cubaleska et al.:
# An exponentiation with 160 bit exponent can
# be performed with only 19.96 multiplications in average if 2299 intermediate
# values from the precomputation are stored. If only 10 values can be stored, the
# same exponentiation requires 82 multiplications.

# From our tests:
# find_optimal(160, 2299) -> 19.9609375 (18, 4)
# find_optimal(160, 10) -> 82.0 (64, 32)


def find_optimal(l=160, S=10):
    if l < 3:
        raise TypeError

    minCost = sys.maxsize
    parameters = None
    for a in range(1, l):
        for b in range(1, a):
            h = math.ceil(l/a)
            al = l - a*(h-1)
            v = math.ceil(a/b)
            vl = math.ceil(al/b)
            storage = ((2**h)-1)*vl + (2**(h-1)-1)*(v-vl)
            if storage <= S:
                cost = ((2**(h-1))-1)/(2**(h-1)) * (a-al) + \
                    (((2**h)-1)/(2**h))*al-1 + alpha * (b-1)
                if cost < minCost:
                    minCost = cost
                    parameters = (a, b)
                    break

    return minCost, parameters


def get_block(n, blockSize, i):
    binary = bin(n)[2:]
    binary = binary[::-1][i*blockSize:(i+1)*blockSize][::-1]

    try:
        return int(binary, 2)
    except:
        return 0

def precompute(l, S, a, b):
    t0 = time.perf_counter()
    h = math.ceil(l/a)
    v = math.ceil(a/b)

    res = [[0*G for u in range(2**h)] for j in range(v)]

    for u in range(1, 2**h):
        res[0][u] = 0*G

        btmp = [int(char) for char in bin(u)[2:]]
        
        l = h - len(btmp)
        binary = [0] * (h)
        binary[l:] = btmp
        
        for i in range(0, h):
            exponent = pow(2, i*a)
            r = G * exponent
            res[0][u] += r*binary[-(i+1)]

        for j in range(1, v):
            res[j][u]= res[0][u]*(pow(2,j*b))
    

    t1 = time.perf_counter()
    print("Time elapsed for precomputation:", t1 - t0)
    return res

def findValue(e, res, a, b, l):
    h = math.ceil(l/a)
    v = math.ceil(a/b)
    R=G*0
    for k in range(b-1,-1,-1):
        R+=R
        for j in range(v-1,-1,-1):
            I=0
            for i in range(0,h):
                e_i = get_block(e, a, i)  # i-th block of e, each block is of size a
                e_ij = get_block(e_i, b, j)  # j-th block of e_i, each block of size b 
                e_ijk = get_block(e_ij, 1, k)
                I += e_ijk * 2**i
            R+=res[j][I]
    return R


if __name__ == '__main__':
    l = 521
    S = [100, 5000]
    for s in S:
        cost, (a, b) = find_optimal(l, s)
        res = precompute(l, S, a, b)
        tests = 50
        t0 = time.perf_counter()
        for _ in range(tests):
            e = random.randint(2**(l-1), 2**l-1)
            val = findValue(e, res, a, b, l)
            assert(e*G == val)

        t1 = time.perf_counter()
        print(f"S: {s}; (a, b) = {(a, b)}; avg-op: {cost}; time elapsed: {t1 - t0}")
        