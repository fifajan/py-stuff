"""
Task description:

Prepare a function that returns diameter of given binary tree.
Diameter is a length of longest possible path connecting some 2 nodes of
the tree. 
Describe your algorithms time complexity in terms of "Big O" notation.
"""


def dfs_paths(node, path, longest):
    """Recursive DFS will save longest path in longest list."""
    path += (node,)
    for child in node.children:
        if child not in path:
            path = dfs_paths(child, path, longest)
    if len(path) > len(longest[0]):
        longest[0] = path
    path = path[:-1]
    return path


def tree_diameter(node):
    """Standard 2 pass DFS diameter calculation approach.
    To be honest i googled this algorithm :) (but coded myself, ofcoure).

    Terms used:
        E - number of edges in tree;
        V - number of vertices (nodes) in tree.

    Algorithm summary:
        This is a classical DFS algorithm. Recursion approach was used.

    Complexity analysis (known for DFS):
        Time: O(E);
        Space: O(V).
    """
    for i in range(2): # 2 times.
        longest_path = [()] # Actual path will be saved instead of empty tuple.
        dfs_paths(node, (), longest_path)
        node = longest_path[0][-1]
    return len(longest_path[0])
