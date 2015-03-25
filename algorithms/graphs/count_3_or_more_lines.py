#! /usr/bin/python

x = v = lambda v: v[0]
y = d = lambda v: v[1]

def lines_of_3_or_more_count(vertices):
    edges = all_possible_edges(vertices)
    counts = vertex_counts(edges)
    return sum([1 for count in counts.values() if count >= 3])
    
def vertex_counts(edges):
    vertex_counts = dict()
    for edge in edges:
        a, b = edge
        dx = x(a) - x(b)
        dy = y(a) - y(b)
        new_vector = (a, (dx, dy))
        merged = False
        for vector in vertex_counts:
            if in_same_line(a, vector) and in_same_line(b, vector):
                vertex_counts[vector] += 1
                merged = True
                break
        if not merged:
            vertex_counts[new_vector] = 2
    return vertex_counts

def in_same_line(vertex, vector):
    (xv, yv), (dx, dy) = vector
    if dx == 0:
        return xv == x(vertex)
    elif dy == 0:
        return yv == y(vertex)
    else:
        return (xv - x(vertex))/float(dx) == (yv - y(vertex))/float(dy)

def all_possible_edges(vertices):
    return {frozenset([tuple(u), 
                       tuple(v)]) for v in vertices for u in vertices if (
                        u != v)}


if __name__ == '__main__':
    # Complex 4x4 square:
    assert 10 == lines_of_3_or_more_count([[0, 0], [3, 0], [6, 0], [9, 0],
                                           [0, 3], [2, 3], [5, 3], [9, 3],
                                           [0, 6], [4, 6], [9, 6], [0, 9],
                                           [3, 9], [6, 9], [9,9]])
