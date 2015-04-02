"""Non recursive approach to get path from one vertext to other
using BFS (breadth first search).
Returns None if path does not exist in a given graph.
"""

from collections import deque as queue

def find_path_bfs(adj_list, from_v, to_v):
    path = []
    vertices_queue = queue([(None, from_v)])
    visited = set()
    while vertices_queue:
        parrent, vertex = vertices_queue.pop()
        if vertex not in visited:
            visited.add(vertex)
            path += [(parrent, vertex)]
            if vertex == to_v:
                return fix_path(path)
            parrent_child_pairs = [(vertex, v) for v in adj_list[vertex]]
            vertices_queue.extendleft(parrent_child_pairs)

def fix_path(path):
    if path:
        parrent, vertix = path.pop()
        path_copy = path[:]
        path = ([parrent] if parrent else []) + [vertix]
        for p, v in reversed(path_copy):
            if v == parrent:
                if p:
                    path = [p] + path
                    parrent = p
                else:
                    break
    return path
