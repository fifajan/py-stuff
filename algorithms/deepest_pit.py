#! /usr/bin/python

def deepest_pit(A):
    '''
    Returns array's A deepest pit in linear time [O(n)].
    '''
    n = len(A)
 
    depth = 0
 
    P = 0
    Q = -1
    R = -1
 
    for i in range(1, n):
        if Q < 0 and A[i] >= A[i - 1]:
            Q = i - 1
 
        if Q >= 0 and R < 0 and (A[i] <= A[i - 1] or i + 1 == n):
            R = i - 1
            depth = max(depth, min(A[P] - A[Q], A[R] - A[Q]))
            P = i - 1
            Q = -1
            R = -1
 
    return depth if depth else -1

if __name__ == '__main__':
    assert deepest_pit([0, 1, 3, -2, 0, 1, 0, -3, 2, 3]) == 4
