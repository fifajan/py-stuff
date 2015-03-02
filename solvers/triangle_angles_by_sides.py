from math import acos, degrees

def angles(a, b, c):
    sides = ((a, b, c), (b, c, a), (c, a, b))
    if not all([a + b > c for a, b, c in sides]):
        return [0, 0, 0]
    angle = lambda t: round(
        degrees(acos(float(t[1]**2 + t[2]**2 - t[0]**2) / (2 * t[1] * t[2]))))
    return sorted(map(angle, sides))

#These "asserts" using only for self-checking and not necessary for auto-testing
if __name__ == '__main__':
    assert angles(4, 4, 4) == [60, 60, 60], "All sides are equal"
    assert angles(3, 4, 5) == [37, 53, 90], "Egyptian triangle"
    assert angles(2, 2, 5) == [0, 0, 0], "It's can not be a triangle"
