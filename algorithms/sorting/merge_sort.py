#! /usr/bin/python

# to test it run:
# $ ./merge_sort.py array.txt

# tests:
#    Array state     Time     (array is 10^4 integers text file)
# ---------------------------
#         random    0.2 s
#       inverted    0.1 s

from sys import argv
from collections import deque

def sort(arr):
    '''
    Merge Sort implementation.
    '''
    mid = len(arr) / 2
    if not mid:
        return arr
    l, r = arr[:mid], arr[mid:]
    l, r = sort(l), sort(r)
    return merge(l, r)

def merge(l, r):
    '''
    This merge func works exactly as it should.
    '''
    res = []
    i = j = 0
    l_l = len(l)
    r_l = len(r)
    while i < l_l and j < r_l:
        if l[i] < r[j]:
            res.append(l[i])
            i += 1
        else:
            res.append(r[j])
            j += 1
    return res + l[i:] + r[j:]

def merge_list_pop(l, r):
    '''
    This merge func looks good but works significantly slower than it should.
    10 time slower than merge on only 200K int sorting.
    '''
    res = []
    lr_min = lambda: l.pop(0) if l[0] < r[0] else r.pop(0)
    while l and r:
        res.append(lr_min())
    return res + l + r


def merge_deque_pop(l, r):
    '''
    Looks quite good too and uses deque but works a bit slower than it should.
    1.5 time slower than merge on 2M int sorting.
    '''
    l_q, r_q = deque(l), deque(r)
    res = []
    lr_min = lambda: l_q.popleft() if l_q[0] < r_q[0] else r_q.popleft()
    while l_q and r_q:
        res.append(lr_min())
    return res + list(l_q) + list(r_q)

if __name__ == '__main__':
    array1 = [int(line) for line in file(argv[1])]
    array2 = array1[:]

    print '- Does this algorithm work correctly? (checking it now...)'
    print '- ' + ('Yes!' if sort(array1) == sorted(array2) else 'Nope!')

