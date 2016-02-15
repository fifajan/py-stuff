#! /usr/bin/python
"""Unit-tests for task #3."""

import unittest
from common.custom_test_case import TestNothing
from print_tree import PrintableTreeNode as TreeNode


class TestTreePrinting(TestNothing):
    """Test for:
    [#3] Tree printing.
    """
    def test_3_layer_tree(self):
        """Given example 3-layer tree is used as input."""
        # leaf nodes:
        d = TreeNode('D')
        e = TreeNode('E')
        f = TreeNode('F')
        g = TreeNode('G')

        # middle nodes:
        b = TreeNode('B', d, e, f)
        c = TreeNode('C', g)

        # root node:
        a = TreeNode('A', b, c)

        # test:
        self.assertEqual(str(a), ('A\n'
                                  'B C\n'
                                  'D E F G'))

    def test_6_layer_tree(self):
        r"""Input tree:

        layer 1:             A
                            /|\
        layer 2:           B C D
                          / / \ \
                         /| | /\ \
        layer 3:        E F G H I J
                       /| | | | |\ \
        layer 4:      K L M N O P Q R
                     / \      |   |  \
        layer 5:    S   T     U   V   W
                       /|\           /|\
        layer 6:      X Y Z         1 2 3
        """
        # leaf nodes (layer 6):
        x = TreeNode('X')
        y = TreeNode('Y')
        z = TreeNode('Z')
        n1 = TreeNode('1')
        n2 = TreeNode('2')
        n3 = TreeNode('3')

        # middle nodes (layer 5):
        s = TreeNode('S')
        t = TreeNode('T', x, y, z)
        u = TreeNode('U')
        v = TreeNode('V')
        w = TreeNode('W', n1, n2, n3)

        # middle nodes (layer 4):
        k = TreeNode('K', s, t)
        l = TreeNode('L')
        m = TreeNode('M')
        n = TreeNode('N')
        o = TreeNode('O', u)
        p = TreeNode('P')
        q = TreeNode('Q', v)
        r = TreeNode('R', w)

        # middle nodes (layer 3):
        e = TreeNode('E', k, l)
        f = TreeNode('F', m)
        g = TreeNode('G', n)
        h = TreeNode('H', o)
        i = TreeNode('I', p, q)
        j = TreeNode('J', r)

        # middle nodes (layer 2):
        b = TreeNode('B', e, f)
        c = TreeNode('C', g, h, i)
        d = TreeNode('D', j)

        # root node (layer 1):
        a = TreeNode('A', b, c, d)

        # test:
        self.assertEqual(str(a), ('A\n'
                                  'B C D\n'
                                  'E F G H I J\n'
                                  'K L M N O P Q R\n'
                                  'S T U V W\n'
                                  'X Y Z 1 2 3'))


if __name__ == '__main__':
    unittest.main()
