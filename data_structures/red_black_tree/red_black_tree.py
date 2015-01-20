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
        '''
        Double rotation
        '''
        root.nodes[not dir] = self.rot_1(root.nodes[not dir], not dir)
        return self.rot_1(root, dir)

    def rb_assert(root):
        '''
        Print message in case there are some Red/Black violations
        '''
        lh, rh = 0

        if not root:
            return True
        else:
            ln, rn = root.nodes

            if root.is_red and (ln.is_red or rn.is_red):
                print 'Red violation'
                return False

            lh = self.rb_assert(ln)
            rh = self.rb_assert(rn)

            if (ln and ln.data >= root.data) or (rn and rn.data <= root.data):
                print 'Binary tree violation'
                return False

            if lh and rh and (lh != rh):
                print 'Black violation'
                return False

            if lh and rh:
                return lh if root.is_red else lh + 1
            else:
                return False

class RBNode(object):
    '''
    Red Black tree's node
    '''
    def __init__(self):
        self.is_red = False
        self.data = []
        self.nodes = [] # 2 nodes: left ([0]) & right ([1])

