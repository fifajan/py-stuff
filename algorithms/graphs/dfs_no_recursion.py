"""Non recursive approach to get path from one vertext to other
using DFS (depth first search).
Returns None if path does not exist in a given graph.
"""

stack = list # standard list should do well as a stack

def find_path_dfs(adj_list, from_v, to_v):
    path = []
    vertices_stack = stack((from_v,))
    while vertices_stack:
        vertex = vertices_stack.pop()
        path = fix_path(adj_list, path, vertex) + [vertex]
        if vertex == to_v:
            return path
        vertices_stack.extend(adj_list[vertex])

def fix_path(adj_list, path, vertex):
    if path:
        path_copy = path[:]
        for v in reversed(path_copy):
            if vertex not in adj_list[v]:
                path.pop()
            else:
                break
    return path
            
    
    


