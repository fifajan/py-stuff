#! /usr/bin/python

L, R = 0, 1

class RBTree(object):
    '''
    My attempt to implement Red Black Tree.
    Implementation follows this great tutorial:
    http://www.eternallyconfuzzled.com/tuts/datastructures/jsw_tut_rbtree.aspx
    '''
    def __init__(self):
        self.root = None

    def __repr__(self):
        return repr(self.root)

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

    def rot_2(self, root, dir):
        '''
        Double rotation
        '''
        root.nodes[not dir] = self.rot_1(root.nodes[not dir], not dir)
        return self.rot_1(root, dir)

    def rb_assert(self, root):
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

    def make_red_node(self, data):
        rn = RBNode(data)
        rn.is_red = True
        rn.nodes = [None, None]
        return rn

    def insert_red_node(self, root, data): # TODO: rename to recoursive
        if not root:
            root = self.make_red_node(data)
        elif data != root.data:
            dir = root.data < data
            root.nodes[dir] = self.insert_red_node(root.nodes[dir], data)

            # rebalancing:
            if root.nodes[dir].is_red:
                if root.nodes[not dir].is_red:
                    # case 1:
                    root.is_red = True
                    root.nodes[L].is_red = False
                    root.nodes[R].is_red = False
                else:
                    # cases 2, 3:
                    if root.nodes[dir].nodes[dir].is_red:
                        root = self.rot_1(root, not dir)
                    elif root.nodes[dir].nodes[not dir].is_red:
                        root = self.rot_2(root, not dir)

        return root

    def insert(self, data):
        self.root = self.insert_red_node(self.root, data)
        self.root.is_red = False
        return True

    def remove_red_node(self, root, data, done): # TODO: rename to recoursive
        if not root:
            done = [1]
        else:
            if root.data == data:
                if None in root.nodes:
                    save = root.nodes[not root.nodes[L]]

                    # case 0:
                    if root.is_red:
                        done = [1]
                    elif save.is_red:
                        save.is_red = False
                        done = [1]

                    return save
                else:
                    heir = root.nodes[L]

                    while heil.nodes[R]:
                        heir = heir.nodes[R]

                    root.data = heir.data
                    data = heir.data

                dir = root.data < data
                root.nodes[dir] = self.remove_red_node( # TODO: rename
                                        root.nodes[dir], data, done)
                if not done:
                    root = self.remove_balance(root, dir, done)

        return root

    def remove(self, data):
        done = []
        self.root = remove_red_node(self.root, data, done) # TODO: rename
        if self.root:
            self.root.is_red = False

        return True


class RBNode(object):
    '''
    Red Black tree's node
    '''
    def __init__(self, data=None):
        self.is_red = False
        self.data = data
        self.nodes = [] # 2 nodes: left ([L=0]) & right ([R=1])

    def __repr__(self):
        pat = '(%s) = %s'
        pat = '%s\n - %s\n - %s' % ((pat,) * 3)
        l, r = self.nodes
        lc, ld = l.color() if l else 'X', l.data if l else 'None'
        rc, rd = r.color() if r else 'X', r.data if r else 'None'
        return pat % (self.color(), str(self.data), lc, ld, rc, rd)

    def color(self):
        return 'R' if self.is_red else 'B'
