#! /usr/bin/python

import unittest
from os import remove as rm

from sort_sorted_streams import merge_streams, MyStream
from gen_int_arrays import write_int_array_to_text_file


class TestBigData(unittest.TestCase):
    """Here we are going to test our algorithm with 100 [k] streams (read 
    from 100 files) with 4,000 [m] integers in each.

    So total n is 4,000,000 here.

    With this input algorithm performs about (compared to my implemenations):
        3 times slower than mergesort;
      2.5 times slower than quicksort;
          about the same speed as heapsort;
      BUT requires only k memory (for the minimum heap).

      SO:
          time complexity is O(m*log(k));
          space complexity is O(k);
    """

    name_pat = 'i%04i.txt'
    n_files = 100
    n_ints_in_file = 40000

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
            pass
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
                prev_int = curr_int
        if curr_int is not None:
            print '*** Sorted! (algorithm is fine) ***'

        self.assertIsNotNone(curr_int)

if __name__ == '__main__':
    unittest.main()
