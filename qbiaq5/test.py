import sys, time, math
start = time.time()
alpha = 1 
data = {}

def benchmark(method):
    def timed(*args, **kwargs):
        ts = time.perf_counter()
        result = method(*args, **kwargs)
        te = time.perf_counter()      
        print(f'Running {method.__name__}, time elapsed: {te-ts}s')
        return result    
    return timed

@benchmark
def find_optimal(l=160, S=10):
    if l < 3:
        raise TypeError

    minCost = sys.maxsize
    parameters = None
    for a in range(1, l):
        for b in range(1, a):
            h = math.ceil(l / a)
            al = l - a * (h - 1)
            v = math.ceil(a / b)
            vl = math.ceil(al / b)
            storage = ((2 ** h) - 1) * vl + (2 ** (h - 1) - 1) * (v - vl)
            if storage <= S:
                cost = ((2 ** (h - 1)) - 1) / (2 ** (h - 1)) * (a - al) + \
                       (((2 ** h) - 1) / (2 ** h)) * al - 1 + alpha * (b - 1)
                if cost < minCost:
                    minCost = cost
                    parameters = (a, b)
                    data[a] = (a,b,cost)
                    break

    return minCost, parameters, data

c, p, d = find_optimal()
print(c)
print(p)
print(d)
