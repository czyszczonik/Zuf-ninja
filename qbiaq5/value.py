from qbiaq5.math_commons import h, v


def get_block(n, blockSize, i):
    try:
        return int(bin(n)[2:][::-1][i * blockSize:(i + 1) * blockSize][::-1], 2)
    except:
        return 0


def get_elementIJK(e, a, b, i, j, k):
    return get_block(get_block(get_block(e, a, i), b, j), 1, k)


def findValue(G, e, precomputed, a, b, l):
    hc = h(l, a)
    vc = v(a, b)
    result = G * 0
    for k in reversed(range(b)):
        result += result
        for j in reversed(range(vc)):
            I = 0
            for i in range(0, hc):
                I += get_elementIJK(e, a, b, i, j, k) * 2 ** i
            result += precomputed[j][I]
    return result
