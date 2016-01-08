#! /usr/bin/python

# to test it run:
# $ ./quick_sort.py array.txt

# tests:
#    Array state     Time     (array is 10^4 integers text file)
# ---------------------------
#         random    0.2 s
#       inverted    3.3 s


from sys import argv, setrecursionlimit

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

if __name__ == '__main__':
    A = [int(line) for line in file(argv[1])]

    setrecursionlimit(2**16) # got 'RuntimeError maximum recursion depth' 
                             # otherwise

    print 'Input read finished.'
                             
    B = A[:]
    sort((0, len(A) - 1))

    print '- Does this algorithm work correctly? (checking it now...)'
    print '- ' + ('Yes!' if A == sorted(B) else 'Nope!')
