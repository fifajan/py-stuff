"""Non recursive approach to get path from one vertext to other
using BFS (breadth first search).
Returns None if path does not exist in a given graph.
"""

from collections import deque as queue

def find_path_bfs(adj_list, from_v, to_v):
    path = []
    vertices_queue = queue((from_v,))
    visited = set()
    while vertices_queue:
        vertex = vertices_queue.pop()
        if vertex not in visited:
            visited.add(vertex)
            path = fix_path(adj_list, path, vertex) + [vertex]
            if vertex == to_v:
                return path
            vertices_queue.extendleft(adj_list[vertex])

# Wrong. TODO: fix it for BFS case
def fix_path(adj_list, path, vertex):
    print vertex, path
    if path:
        path_copy = path[:]
        for v in reversed(path_copy):
            if vertex not in adj_list[v]:
                path.pop()
            else:
                break
    return path
