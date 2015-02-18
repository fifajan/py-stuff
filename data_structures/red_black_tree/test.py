#! /usr/bin/python

'''
Approach to print out randomly generated RB tree to
visualize if it is balanced.
'''

from random import choice
from red_black_tree import RBTree

c_range = range(40, 121)
rc = lambda : chr(choice(c_range))

t = RBTree()
for i in range(100):
    s = rc() + rc() + rc()
    t.insert(s)

print 'Tree:\n%s' % t
