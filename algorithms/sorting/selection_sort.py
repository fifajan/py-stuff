#! /usr/bin/python

# to test it run:
# $ ./selection_sort.py array.txt

# tests:
#    Array state     Time     (array is 10^4 integers text file)
# ---------------------------
#         random   2.3 s
#       inverted   4.2 s

from sys import argv

def pos_min(A):
    min_i = 0
    min_v = A[min_i]
    for i in range(min_i + 1, len(A)):
        if A[i] < min_v:
            min_v = A[i]
            min_i = i
    return (min_i, min_v)

def sort(A):
    n = len(A)
    sorted_A = [None] * n
    for i in range(n):
        pos, val = pos_min(A)
        sorted_A[i] = val
        del A[pos]
    return sorted_A
        

array1 = [int(line) for line in file(argv[1])]
array2 = array1[:] # copy array

print '- Does this algorithm work correctly? (checking it now...)'
print '- ' + ('Yes!' if sort(array1) == sorted(array2) else 'Nope!')

