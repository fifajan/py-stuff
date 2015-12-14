#! /usr/bin/python

def distance(a, b):
    """Gets distance between 2 given x,y points."""
    ax, ay = a
    bx, by = b
    return ((ax - bx)**2 + (ay - by)**2)**.5

def radius(a, b, c):
    """Gets radius of circumscribed circle for abc triangle."""
    ab = distance(a, b)
    ac = distance(a, c)
    bc = distance(b, c)

    a, b, c = ab, ac, bc

    return (a * b * c) / (
                (a + b + c) * (-a + b + c) * (a - b + c) * (a + b - c))**.5


if __name__ == '__main__':
    assert abs(radius((0, 0), (1, 0), (0, 1)) - .5 * 2**.5) < 10**-10
