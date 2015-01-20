#! /usr/bin/python

class RBTree(object):
    '''
    My attempt to implement Red Black Tree.
    Implementation follows this great tutorial:
    http://www.eternallyconfuzzled.com/tuts/datastructures/jsw_tut_rbtree.aspx
    '''
    def __init__(self):
        root = None

    def rot_1(self, root, dir):
        '''
        Single rotation
        '''
        save = root.nodes[not dir]

        root.nodes[not dir] = save.nodes[dir]
        save.nodes[dir] = root

        root.is_red = True
        save.is_red = False

        return save

    def rot_2(self, root, dir)
        root.nodes[not dir] = self.rot_1(root.nodes[not dir], not dir)
        return self.rot_1(root, dir)


class RBNode(object):
    '''
    Red Black tree's node
    '''
    def __init__(self):
        self.is_red = False
        self.data = []
        self.nodes = []

