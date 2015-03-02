#! /usr/bin/python

# to test it run:
# $ ./merge_sort.py array.txt

# tests:
#    Array state     Time     (array is 10^4 integers text file)
# ---------------------------
#         random    0.2 s
#       inverted    0.1 s

from sys import argv

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
    ll = len(l)
    lr = len(r)
    while i < ll and j < lr:
        if l[i] < r[j]:
            res.append(l[i])
            i += 1
        else:
            res.append(r[j])
            j += 1
    return res + l[i:] + r[j:]

def merge_pretty(l, r):
    '''
    This merge func looks good but works slower than it should.
    '''
    res = []
    lr_min = lambda: l.pop(0) if l[0] < r[0] else r.pop(0)
    while l and r:
        res += [lr_min()]
    return res + l + r

array1 = [int(line) for line in file(argv[1])]
array2 = array1[:]

print '- Does this algorithm work correctly? (checking it now...)'
print '- ' + 'Yes!' if sort(array1) == sorted(array2) else 'Nope!'

