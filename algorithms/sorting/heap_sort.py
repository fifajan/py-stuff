#! /usr/bin/python

# to test it run:
# $ ./heap_sort.py array.txt

# tests:
#    Array state     Time     (array is 10^4 integers text file)
# ---------------------------
#         random    ? s
#       inverted    ? s

from sys import argv

class PriorityQueue(object):
    """My attempt to implement a priority queue.
    
    http://www.cs.cmu.edu/~adamchik/15-121/lectures/Binary%20Heaps/heaps.html
    resource was used for heap implementation details reference.
    """

    def __init__(self):
        self.heap = []
        self.size = 0
        # defines if it will be max or min heap:
        self.min_root = True

    def double_size(self):
        old_heap = self.heap
        self.heap = [None] * (2 * self.size)
        self.heap[1:self.size] = old_heap[1:]

    def insert(self, value):
        if self.size == len(self.heap - 1):
            self.double_size()

        self.size += 1
        pos = self.size
        while pos > 1 and XXXX: # TODO
            self.heap[pos] = self.heap[pos // 2]

        self.heap[pos] = value

# print '- Does this algorithm work correctly? (checking it now...)'
# print '- ' + 'Yes!' if sort(array1) == sorted(array2) else 'Nope!'

