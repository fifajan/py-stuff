#! /usr/bin/python
'''
    we have a directed graph:

    (1) <-> (2) -> (3) -> (4)
             |      |
             v      v
            (5) -> (6)
           
    you should implement a function (and some classes or
    data structures if it is necessary) to return a path
    from any node to any other. It thould return None if
    there is no such path in a graph.
'''

from bfs_no_recursion import find_path_bfs as bfs
from dfs_no_recursion import find_path_dfs as dfs

adj_list = dict()

adj_list[1] = [2]
adj_list[2] = [1, 3, 5]
adj_list[3] = [4, 6]
adj_list[4] = []
adj_list[5] = [6]
adj_list[6] = []

g = adj_list

# TODO: fix bfs path
assert dfs(g, 1, 4) == [1, 2, 3, 4]
assert dfs(g, 2, 2) == [2]
assert dfs(g, 2, 5) == [2, 5]
assert dfs(g, 5, 4) == None

