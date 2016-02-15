r"""
Task description:

Prepare a function that displays nodes values of a tree passed to it as an
argument. The passed element is the root node of the tree. All values should
be displayed by tree levels (one tree level per line), i.e. root node in the
firs line, all nodes from the 2nd level in the second line, etc.
Below example presents the behaviour:

       A
      / \
     B   C
    /|\   \
   D E F   G

For the above tree, the following result should be displayed on the screen:
A
B C
D E F G

You are allowed to decide on the data structure of the tree in the program
memory.
"""


from common.tree import TreeStringNode
from collections import deque as queue


def print_tree(root_node): # Not used in tests. See TreeNode's __str__
    """Task function implementation."""
    print root_node


class PrintableTreeNode(TreeStringNode):
    """Tree node that could be printed in its layers.

    Terms used:
        E - number of edges in tree;
        V - number of vertices (nodes) in tree.

    Algorithm summary:
        This is a classical BFS algorithm. Iterative approach was used
        instead of recursion so it should perform quite fast.

    Complexity analysis (known for BFS):
        Time: O(E);
        Space: O(V).
    """
    def __repr__(self):
        str_repr_list = []
        nodes_queue = queue((self,))
        layer_len = len(nodes_queue)
        next_layer_len = 0
        while nodes_queue:
            node = nodes_queue.pop()
            next_layer_len += len(node.children)
            nodes_queue.extendleft(node.children)
            layer_len -= 1
            str_repr_list.append(node.value)
            if nodes_queue:
                if layer_len < 1:
                    str_repr_list.append('\n')
                    layer_len = next_layer_len
                    next_layer_len = 0
                else:
                    str_repr_list.append(' ')
        return ''.join(str_repr_list)
