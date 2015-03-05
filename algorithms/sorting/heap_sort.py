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
        self.heap = [None, None]
        self.size = 0
        # defines if it will be max or min heap:
        self.min_root = True

    def build_heap(self):
        for k in reversed(range(1, (self.size // 2) + 1)):
            self.percolate_down(k)

    def double_size(self):
        old_heap = self.heap
        self.heap = [None] * (2 * self.size)
        self.heap[1:self.size] = old_heap[1:]

    def insert(self, value):
        if self.size == len(self.heap) - 1:
            self.double_size()

        self.size += 1
        pos = self.size
        while pos > 1 and self.heap[pos // 2] > value:
            self.heap[pos] = self.heap[pos // 2]
            pos = pos // 2

        self.heap[pos] = value

    def percolate_down(self, k):
        tmp = self.heap[k]
        child = 0

        while 2 * k <= self.size:
            child = 2 * k
            child += 1 if child != self.size and (
                            self.heap[child + 1] < self.heap[child]) else 0
            if self.heap[child] < tmp:
                self.heap[k] = self.heap[child]
            else:
                break
            k = child

        self.heap[k] = tmp

    def pop_min(self):
        if self.size == 0:
            return None
        else:
            min = self.heap[1]
            self.heap[1] = self.heap[self.size]
            self.size -= 1
            self.percolate_down(1)
            return min 

    def __len__(self):
        return self.size

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return str(self.heap)

# print '- Does this algorithm work correctly? (checking it now...)'
# print '- ' + 'Yes!' if sort(array1) == sorted(array2) else 'Nope!'
