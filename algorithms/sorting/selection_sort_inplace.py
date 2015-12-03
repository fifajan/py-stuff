#! /usr/bin/python

# to test it run:
# $ ./selection_sort_inplace.py array.txt

# tests:
#    Array state     Time     (array is 10^4 integers text file)
# ---------------------------
#         random   2.9 s
#       inverted   4.8 s

from sys import argv

def swap(i, j, array):
        A = array
        A[i], A[j] = A[j], A[i]

def sort(A):
    n = len(A)
    for sorted_i in range(n):
        min_i = sorted_i
        for i in range(sorted_i + 1, n):
            if A[i] < A[min_i]:
                min_i = i
        if min_i != sorted_i:
            swap(min_i, sorted_i, A)

    return A

if __name__ == '__main__':
    array1 = [int(line) for line in file(argv[1])]
    array2 = array1[:] # copy array

    print '- Does this algorithm work correctly? (checking it now...)'
    print '- ' + ('Yes!' if sort(array1) == sorted(array2) else 'Nope!')
