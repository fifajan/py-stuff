#! /usr/bin/python

# to test it run:
# $ ./insertion_sort.py array.txt
# it will take a LONG time (because of O(n^2))

# tests:
#    Array state     Time     (array is 10^4 integers text file)
# ---------------------------
#         random    6.4 s
#       inverted   13.3 s

from sys import argv

def sort(array):
    '''
    Insertion Sort implementation.
    '''
    array_len_r = range(1, len(array))
    for i in array_len_r:
        prev_i = i - 1
        current = array[i]
        while prev_i >= 0 and array[prev_i] > current:
            array[prev_i + 1] = array[prev_i]
            array[prev_i] = current
            prev_i -= 1
    return array

array1 = [int(line) for line in file(argv[1])]
array2 = array1[:]

print '- Does this algorithm work correctly? (checking it now...)'
print '- ' + 'Yes!' if sort(array1) == sorted(array2) else 'Nope!'
