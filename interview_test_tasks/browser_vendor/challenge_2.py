#! /usr/bin/python

descr = '''
    (a) -> (b) ->(c) -> (d)
            |     |
            v     v
           (e) -> (f)

           a, b e, f
           a, b, c f

    (a) -> (b) -> (c)
        <-
'''

adj_list = dict()

adj_list['a'] = ['b']
adj_list['b'] = ['e', 'c']
adj_list['c'] = ['d', 'f']
adj_list['d'] = []
adj_list['e'] = ['f']
adj_list['f'] = []

paths = set()

def path(v, c, _path, visited):
    visited |= {c}
    if c == v:
        paths.add(_path + (c,))
    for node in adj_list[c]:
        if node in visited:
            pass
        else:
            return path(v, node, _path + (c,), visited)

    paths.add(_path + (c,))

visited = set()
u, v = 'a', 'c'
path(v, u, (), visited)

for p in paths:
    if p[0] == u and p[-1] == v:
        print p
