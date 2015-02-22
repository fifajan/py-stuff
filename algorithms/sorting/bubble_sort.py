#! /usr/bin/python

# to test it run:
# $ ./bubble_sort.py array.txt
# it will take a LONG time (because of O(n^2))

# tests:
#    Array state     Time     (array is 10^4 integers text file)
# ---------------------------
#         random   18.3 s
#       inverted   25.1 s

from sys import argv

def sort(array):
    '''
    Bubble Sort implementation.
    '''
    is_sorted = False
    array_len_r = range(len(array) - 1)
    if array_len_r:
        while not is_sorted:
            is_sorted = True
            for i in array_len_r:
                j = i + 1
                if array[i] > array[j]:
                    swap(i, j, array)
                    is_sorted = False
    return array

def swap(i, j, array):
    A = array
    A[i], A[j] = A[j], A[i]

array1 = [int(line) for line in file(argv[1])]
array2 = array1[::]

print '- Does this algorithm work correctly? (checking it now...)'
print '- ' + 'Yes!' if sort(array1) == sorted(array2) else 'Nope!'
