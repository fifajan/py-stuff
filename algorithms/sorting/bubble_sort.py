#! /usr/bin/python

# to test it run:
# $ ./bubble_sort.py array.txt
# it will take a LONG time (because of O(n^2))

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

array = [int(line) for line in file(argv[1])]

print '- Does this algorithm work correctly? (checking it now...)'
print '- ' + 'Yes!' if sort(array) == sorted(array) else 'Nope!'
