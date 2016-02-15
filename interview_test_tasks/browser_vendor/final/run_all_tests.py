#! /usr/bin/python
"""Runs all unit-tests for all tasks."""

import unittest
import sys

from common.custom_test_case import TestNothing

if __name__ == '__main__':
    loader = unittest.TestLoader()
    cases = loader.discover('.', pattern='test.py')
    verb = 0 if len(sys.argv) < 2 else sys.argv[1]
    unittest.TextTestRunner(verbosity=verb).run(cases)
