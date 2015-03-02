#! /usr/bin/python

# to test it run:
# $ ./heap_sort.py array.txt

# tests:
#    Array state     Time     (array is 10^4 integers text file)
# ---------------------------
#         random    ? s
#       inverted    ? s

from sys import argv

print '- Does this algorithm work correctly? (checking it now...)'
print '- ' + 'Yes!' if sort(array1) == sorted(array2) else 'Nope!'

