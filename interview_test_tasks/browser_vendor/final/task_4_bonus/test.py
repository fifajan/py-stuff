#! /usr/bin/python
"""Unit-tests for bonus task #4."""

import unittest

from common.custom_test_case import TestNothing
from common.tree import TreeStringNode as TreeNode

from tree_diameter import tree_diameter


class TestTreeDiameter(TestNothing):
    """Test for:
    [#4 bonus] Binary tree diameter.
    """
    def test_5_node_tree(self):
        r"""Input tree:
             X
             |\
             D C
            /|
           A B
        """
        # Initial liks:
        a = TreeNode('A')
        b = TreeNode('B')
        c = TreeNode('C')
        d = TreeNode('D', a, b)
        x = TreeNode('X', d, c)

        # Backward links (so DFS could go from f.e. leaf node):
        a.children.append(d)
        b.children.append(d)
        d.children.append(x)
        c.children.append(x)

        self.assertEqual(tree_diameter(x), 4)

    def test_12_node_tree(self):
        r"""Input tree:
                 1
                 |\
                 2 3
                 |
                 4
                /|
               6 5
              /  |
             7   8
             |   |
            11   9
             |   |
            12  10
                 |
                13
        """
        # Initial liks:
        n13 = TreeNode('13')
        n10 = TreeNode('10', n13)
        n9 = TreeNode('9', n10)
        n12 = TreeNode('12')
        n11 = TreeNode('11', n12)
        n7 = TreeNode('7', n11)
        n8 = TreeNode('8', n9)
        n5 = TreeNode('5', n8)
        n6 = TreeNode('6', n7)
        n4 = TreeNode('4', n6, n5)
        n3 = TreeNode('3')
        n2 = TreeNode('2', n4)
        n1 = TreeNode('1', n2, n3)

        # Backward links (so DFS could go from f.e. leaf node):
        n13.children.append(n10)
        n12.children.append(n11)
        n10.children.append(n9)
        n11.children.append(n7)
        n9.children.append(n8)
        n7.children.append(n6)
        n8.children.append(n5)
        n5.children.append(n4)
        n6.children.append(n4)
        n4.children.append(n2)
        n2.children.append(n1)
        n3.children.append(n1)

        self.assertEqual(tree_diameter(n1), 10)


if __name__ == '__main__':
    unittest.main()
