#! /usr/bin/python

# to test it run:
# $ ./merge_sort_mp.py large.txt

# tests:
#    Num of concurrent processes     Time  (array is 3*10^6 integers text file)
# ------------------------------------------
#                              1     21 s
#                              2     15 s

from sys import argv
from math import floor
from multiprocessing import Process, Manager

PROC_N = 2 # number of processes

def sort_mp(responses, arr):
    responses.append(sort(arr))

def merge_mp(responses, l_arr, r_arr):
    responses.append(merge(l_arr, r_arr))

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

array1 = [int(line) for line in file(argv[1])]
array2 = array1[::]

manager = Manager() 
responses = manager.list()

l = len(array1)
step = int(floor(l / PROC_N))

p = []
for n in range(PROC_N):
    if n < PROC_N - 1:
        proc = Process(target=sort_mp,
                        args=(responses, array1[n * step : (n + 1) * step],))
    else:
        proc = Process(target=sort_mp, args=(responses, array1[n * step :],))
    p.append(proc)

for proc in p:
    proc.start()

for proc in p:
    proc.join()

array1 = merge(*responses[:2])

print '- Does this algorithm work correctly? (checking it now...)'
print '- ' + 'Yes!' if array1 == sorted(array2) else 'Nope!'

