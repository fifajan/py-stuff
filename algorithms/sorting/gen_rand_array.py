#! /usr/bin/python

from random import shuffle
from sys import argv

try:
    n = int(argv[1])
except Exception as e:
    print "Can't read array size (agrument #1): %s" % e
else:
    try:
        arr_f = argv[2]
    except Exception as e:
        print "Can't read array filename (agrument #2): %s" % e
    else:
        rand_i_list = range(n)
        shuffle(rand_i_list)

        with open(arr_f, 'w') as f:
            for i in rand_i_list:
                f.write(str(i) + '\n')





