#! /usr/bin/python

'''
real    0m7.629s
user    0m1.788s
sys     0m1.348s
'''

from random import choice

c_range = range(40, 121)
rc = lambda : chr(choice(c_range))

for i in range(5000):
    d = {}
    for j in range(70):
        s = rc() + rc() + rc()
        d[s] = s.upper()
    for k in d:
        print d[k]
        del d[k]
        d[k] = k
