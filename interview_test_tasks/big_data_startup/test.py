#! /usr/bin/python

import unittest
from os import remove as rm

from sort_sorted_streams import merge_streams, MyStream
from gen_int_arrays import write_int_array_to_text_file


class TestBigData(unittest.TestCase):
    """Here we are going to test our algorithm with 1000 streams (read 
    from 1000 files) with 8,000 integers in each.

    So total n is 8,000,000 here.
    """
    name_pat = 'i%04i.txt'
    n_files = 1000
    n_ints_in_file = 8 * n_files

    def setUp(self):
        # create test files:
        print 'Started generation of test files (%s of %s integers)...' % (
                        TestBigData.n_files, TestBigData.n_ints_in_file)
        for i in range(TestBigData.n_files):
            write_int_array_to_text_file(TestBigData.name_pat % i, 
                                         TestBigData.n_ints_in_file)
        print 'Done!'

    def tearDown(self):
        print 'Started deletion of test files (%s)...' % TestBigData.n_files
        for i in range(TestBigData.n_files):
             rm(TestBigData.name_pat % i)
        print 'Done!'

    def test_sort(self):
        print 'Started creation of MyStream objects (%s)...' % (
                                                    TestBigData.n_files)
        streams = [MyStream(TestBigData.name_pat % i) for i in range(
                                                        TestBigData.n_files)]
        print 'Done!'
        sorted_generator = merge_streams(streams)
        try:
            prev_int = next(sorted_generator)
        except StopIteration:
            print 'Got empty streams.'
            curr_int = 1
        else:
            print 'Actual sorting is started...'
            for curr_int in sorted_generator:
                if curr_int < prev_int:
                    print '*** Not sorted! (algorithm is wrong) ***'
                    curr_int = None
                    break
        if curr_int is not None:
            print '*** Sorted! (algorithm is fine) ***'

if __name__ == '__main__':
    unittest.main()
