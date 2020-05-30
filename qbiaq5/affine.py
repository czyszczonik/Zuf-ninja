from random import randint

O = 'Point at infinity'  # cannot be represented normally


class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if not isinstance(other, Point):
            return False
        elif (self.x == other.x and self.y == other.y):
            return True
        return False

    def __repr__(self):
        return f"({self.x},{self.y})"


def invertPoint(P, p):
    if P == O:
        return P
    return Point(P.x, (-P.y) % p)


def extendedGCD(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = extendedGCD(b % a, a)
        return g, x - (b // a) * y, y


def invertMod(a, m):
    a = a % m
    g, x, _ = extendedGCD(a, m)
    assert g == 1, 'EGCD error, g should be 1'
    return x % m


def add(P, Q, p, a):
    if P == O:
        return Q
    elif Q == O:
        return P
    elif Q == invertPoint(P, p):
        return O
    elif P == Q:
        return double(P, p, a)
    else:
        return addition(P, Q, p, a)


def addition(P, Q, p, a):
    m = (P.y - Q.y) * invertMod((P.x - Q.x), p)
    x = (m ** 2 - P.x - Q.x) % p
    y = (P.y + m * (x - P.x)) % p
    R = Point(x, y)
    return invertPoint(R, p)


def double(P, p, a):
    m = (3 * P.x ** 2 + a) * invertMod((2 * P.y), p)
    x = (m ** 2 - 2 * P.x) % p
    y = (P.y + m * (x - P.x)) % p
    R = Point(x, y)
    return invertPoint(R, p)


def multiply(n, P, p, a):
    result = O
    accumulator = P
    bits = reversed(bin(n)[2:])
    for bit in bits:
        if bit == '1':
            result = add(result, accumulator, p, a)
        accumulator = double(accumulator, p, a)
    return result
