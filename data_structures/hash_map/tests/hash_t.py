#! /usr/bin/python

'''
real    0m26.026s
user    0m10.089s
sys     0m2.800s

3.411 times slower than standart library dict on this test
'''

from random import choice
from hash_map import HashMap

c_range = range(40, 121)
rc = lambda : chr(choice(c_range))

for i in range(5000):
    d = HashMap() # table_size = 100
    for j in range(70):
        s = rc() + rc() + rc()
        d.add((s, s.upper()))
    for k in d:
        v = d.get(k)
        print v
        d.remove(k)
        d.add((k, v))
