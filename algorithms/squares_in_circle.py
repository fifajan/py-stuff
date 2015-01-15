from math import hypot, ceil

def rel_to_circ(r, sqare_SW):
    x, y = sqare_SW
    square = ((x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1))
    outer_vertexes = [v for v in square if hypot(*v) > r]
    inner_vertexes = [v for v in square if hypot(*v) <= r]
    if outer_vertexes and inner_vertexes:
        return 'INTERSECTS'
    elif inner_vertexes:
        return 'INNER'
    else:
        return 'OUTER'

def inner_edge_squares_count(radius):
    range_N = range(int(ceil(radius)))
    squares = {'INTERSECTS' : 0, 'INNER' : 0, 'OUTER' : 0}
    squares_SW = [(x, y) for x in range_N for y in range_N]
    for square in squares_SW:
        squares[rel_to_circ(radius, square)] += 1

    return [squares['INNER'] * 4, squares['INTERSECTS'] * 4]

#These "asserts" using only for self-checking and not necessary for auto-testing
if __name__ == '__main__':
    assert inner_edge_squares_count(2) == [4, 12], "N=2"
    assert inner_edge_squares_count(3) == [16, 20], "N=3"
    assert inner_edge_squares_count(2.1) == [4, 20], "N=2.1"
    assert inner_edge_squares_count(2.5) == [12, 20], "N=2.5"
