#! /usr/bin/python

from itertools import permutations
from operator import mul
from functools import reduce

def perm_parity(perm):
    parity = 1
    for i in range(0, len(perm) - 1):
        if perm[i] != i:
            parity *= -1
            mn = min(range(i, len(perm)), key = lambda i: perm[i])
            perm[i], perm[mn] = perm[mn], perm[i]

    return parity

def leibniz_det(data):
    '''
    Leibniz formula for determinants implementation.
    '''
    r_N = range(len(data))
    def perm_product(perm):
        indexes = zip(r_N, perm)
        return reduce(mul, [data[i][j] for (i, j) in indexes])

    return sum([perm_parity(list(p)) * perm_product(p) for p in (
                                                permutations(r_N))])

#These "asserts" using only for self-checking and not necessary for auto-testing
if __name__ == '__main__':
    assert leibniz_det([[4, 3], [6, 3]]) == -6, 'First example'

    assert leibniz_det([[1, 3, 2],
                    [1, 1, 4],
                    [2, 2, 1]]) == 14, 'Second example'

