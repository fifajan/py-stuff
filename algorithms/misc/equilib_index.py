#! /usr/bin/python

def eq_index(array):
    '''
    Finds equilibrium index in linear time [O(n)].
    '''
    ls = 0 # l sum
    rs = sum(array) # r sum
    for i in range(len(array)):
        if i: ls += array[i - 1]
        rs -= array[i]
    
        if rs == ls:
            return i

    return -1

test_array = [1, 0, 0, -1, 2, -1, -1, 3, 123456, 0, 0, 0, 1, 10, -10, 2]

assert eq_index(test_array) == 8
