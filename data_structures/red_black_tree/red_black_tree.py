#! /usr/bin/python

class RBTree(object):
    '''
    My attempt to implement Red Black Tree.
    Implementation follows this great tutorial:
    http://www.eternallyconfuzzled.com/tuts/datastructures/jsw_tut_rbtree.aspx
    '''
    root = None

class RBNode(object):
    '''
    Red Black tree's node
    '''
    def __init__(self):
        self.is_red = False
        self.data = []
        self.nodes = []

