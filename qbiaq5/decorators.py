import time


def benchmark(method):
    def timed(*args, **kwargs):
        ts = time.perf_counter()
        result = method(*args, **kwargs)
        te = time.perf_counter()
        print(f'Running {method.__name__}, time elapsed: {te - ts}s')
        return result

    return timed
