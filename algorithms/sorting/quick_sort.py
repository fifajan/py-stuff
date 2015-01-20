#! /usr/bin/python

from sys import argv

A = [int(line) for line in file(argv[1])]

def sort(r):
    '''
    Quick Sort implementation.
    '''
    fi, li = r
    if li > fi:
        pi = choose_pi(r)
        swap(fi, pi)
        pi = partition(r)
        sort((fi, pi - 1))
        sort((pi + 1, li))

def partition(r):
    fi, li = r
    i = fi + 1
    for j in range(i, li + 1):
        if A[j] < A[fi]:
            swap(i, j)
            i = i + 1
    swap(fi, i - 1)
    return i - 1

def swap(i, j):
    A[i], A[j] = A[j], A[i]

def choose_pi(r):
    fi, li = r
    mi = fi + (li - fi) / 2

    pis = sorted([fi, mi, li], key = lambda x: A[x])
    return pis[len(pis)/2]

sort((0, len(A) - 1))

print '- Does this algorithm work correctly? (checking it now...)'
print '- ' + 'Yes!' if A == sorted(A) else 'Nope!'
