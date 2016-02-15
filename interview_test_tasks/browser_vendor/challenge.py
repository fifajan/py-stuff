#! /usr/bin/python

# Answered by Alexey Ivchenko (yanepman@gmail.com)
# It took 1 hour 50 minutes to write, format and spell-check this document.
# Finished around 23:05 (GMT+2)
# P.S. i tried not to Google anything so it would be a fair interview :)

#  '###' is question
#  '#' is answer comments



### 1. Write a function to reverse elements inside passed list 
###      (without using any built-in functions).

def reversed(l):
    return l[::-1] # hope wou will not consider l[x:y:z] operation
                   # as a built-in function.

### 2. What is the result of running following code:

### >>> filter(lambda n: n % 2 == 0, range(10))
### ?

# if will filter out all 0-9 integers which have remainder if divided by 2
# so:
[0, 2, 4, 6, 8]


### 3. What is the result of second call to |f|?

### >>> def f(acc=[]):
### ...     acc.append(1)
### ...     return len(acc)
### ... 
### >>> f()
### 1
### >>> f()
### ?

# CPython will use same list for default acc value in both calls
# so:
2

### 4. Write generator for returning odd numbers

# infinite odd generator (because you did not told me when to stop :) )
def odds():
    i = 1
    while True:
        if i % 2:
            yield i
        i += 1

# usage :
odd_gen = odds()
next(odd_gen)
next(odd_gen)
# or (infinite loop):
#   for i in odd_gen:
#       print i


### 5. What is the result of running the following code:

### >>> t = (1,2,3)
### >>> t[1] = 4
### ?

TypeError

# it will raise TypeError exception because tuple is immutable type in Python.
# things could go better if we used t = [1,2,3] (list) here.

### 6. Write decorator defined as follows:

### * if 1st passed argument is equal to string 'foo' throws an exception
### * otherwise calls decorated function and returns its result

def dec(f): # decorator 
    def raiser(*args):
        try:
            if args[0] == 'foo':
                raise Exception
        except IndexError:
            pass
        f(*args)
    return raiser

@dec
def concat_strings(*args): # decorated function
    print ('%s' * len(args)) % args

### 7. Compare |range| and |xrange|

# In Python 2:
#  * range returns a list from 0 to <param_0> - 1 if <param_0> is an integer;
#  * xrange return iterable generator-like object 'xrange' which can save
#    memory and start actual iteration faster in case of large <param_0>.
# In Python 3:
#  * range behaves just like xrange from Python 2;
#  * there is no xrange.

### 8. Compare |set|, |tuple| and |dict| types.

# set:
#  Unordered container of unique hashable keys.
#  Optimized Hash Map stands behind set actually (in CPython) which means:
#   * constant time search [O(1)] so 'key in some_set' goes very fast
#   * constant time insertion [O(1)] of new element
#   * provides useful 'set operations' in linear time [O(n)] including:
#     common in 2 sets (intersection), different in 2 sets (difference) etc.
#   * not memory efficient because hash map requires about 1/3
#     additional memory to perform fast (to overcome collisions with open
#     addressing)
#   * can't store duplicates and not hashable types (lists, dicts, sets)
#   When to use set:
#    - if you need and can take benefit from fast 'set operations'
#    - if you constantly querying 'something in some_set'
#    - if you need to store unique values
#    - if you are not very concerned with memory usage
#
# tuple:
#  Immutable version of Python list (which is actually array in CPython).
#  Ordered sequence of values of any type which means:
#   * constant time access by index [O(1)] because tuple is actually
#     implemented as array in CPython
#   * provides great slicing operation (t[x:y:z])
#   * no modifications. This is read-only data type in Python.
#   * memory efficient as array should be. No additional memory is wasted.
#   * can store anything including duplicates and not hashable types.
#   When to use tuple:
#    - if you need constant sequenced data with fast iteration
#    - if you want a guarantee that no one will edit your container
#    - if you need sequenced container and you are concerned about memory
#
# dict:
#  Unordered container of unique hashable keys with value attached to each key.
#  Implements associative array in Python. Basically same as set but with
#  value for each key.
#   * same pros and cons as with set but no 'set operations'
#   * everything could be a value but only hashable types for keys
#   When to use dict:
#    - if you need to have an efficient key-value storage
#    - if are frequently inserting and searching for keys
#    - if you need associative container and you are not very concerned by
#      extra memory usage
#
# Resume: all 3 are great but should be used smartly
# 

### 9. Write a class for tree nodes:

### * node holds integer value
### * node has optional reference to left child
### * node has optional reference to right child

class TreeNode(object):
    L, R = 0, 1
    def __init__(self, value):
        self.value = int(value)
	self.children = [None, None]

### 10. Write a function which checks if in passed BST tree exists
###     specified number.

### def find_in_bst_tree(tree, number):
###     # TODO
### Use class from 9.

L, R = TreeNode.L, TreeNode.R
def find_in_bst_tree(tree, number):
    if tree.value == number:
        return True
    ch = tree.children
    if ch[L] and number < tree.value:
	return find_in_bst_tree(ch[L], number)
    elif ch[R] and number > tree.value:
        return find_in_bst_tree(ch[R], number)
    return False
