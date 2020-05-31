import random
import time

from fastecdsa.curve import P521

from qbiaq5.optimal import find_optimal
from qbiaq5.precomputation import precompute
from qbiaq5.value import findValue

randomScalar = lambda l: random.randint(2 ** (l - 1), 2 ** l - 1)


def performTests(G, l, S, iterations):
    for storage in S:
        print("_" * 100)
        print("_" * 100)
        print(f"Performing benchmark for storage: {storage}")
        cost, (a, b) = find_optimal(l, storage)
        precomputed = precompute(G, l, storage, a, b)
        t0 = time.perf_counter()
        for _ in range(iterations):
            e = randomScalar(l)
            value = findValue(G, e, precomputed, a, b, l)
            assert (e * G == value)

        t1 = time.perf_counter()
        print("_" * 100)
        print("Summary:")
        print(f"Storage Size: {storage}\n "
              f"Optimal (a, b): {(a, b)}\n"
              f"Average operations: {cost}\n "
              f"Time elapsed: {t1 - t0}\n"
              f"Iterations: {iterations}\n"
              f"Average Time per test: {(t1 - t0) / iterations}")


if __name__ == '__main__':
    G = P521.G
    l = 521
    S = [100, 5000]
    performTests(G, l, S, 50)
