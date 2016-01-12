#! /usr/bin/python

'''
Approach to print out randomly generated RB tree to
visualize if it is balanced.
'''

from random import choice
from red_black_tree import RBTree

c_range = range(40, 121)
rc = lambda : chr(choice(c_range))
rand_4_chars = lambda: rc() + rc() + rc() + rc()

print_t = lambda t : 'Tree:\n%s' % t

print '#### Only insertions:'
t = RBTree()
for i in range(1000):
    s = rand_4_chars()
    t.insert(s)

print print_t(t) + '\n#### 4/4 insertions then 3/4 removal:'

# test deletion
t = RBTree()
values = set()
for i in range(4000):
    s = rand_4_chars()
    if i > 999:
        values.add(s)
    t.insert(s)

for v in values:
    t.remove(v)

print print_t(t)
