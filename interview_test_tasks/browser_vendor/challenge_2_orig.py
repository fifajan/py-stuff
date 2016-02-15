'''
    we have a directed graph:

    (a) -> (b) ->(c) -> (d)
            |     |
            v     v
           (e) -> (f)

          or

      (loop)
    (a) -> (b) -> (c)
        <-

    you should implement a function (and some classes or
    data structures if it is necessary) to return a path
    from any node to any other. It thould return None if
    there is no such path in a graph
'''

adj_list = dict()

adj_list['a'] = ['b']
adj_list['b'] = ['e', 'c']
adj_list['c'] = ['d', 'f']
adj_list['d'] = []
adj_list['e'] = ['f']
adj_list['f'] = []

def path(v, c, path, visited):
    visited |= {c}
    if c == v:
        return path + (c,)
    for node in adj_list[c]:
        if node in visited:
            continue
        return path(v, node, (v,) + path, visited)

visited = set()
path('c', 'a', (), visited)
