#! /usr/bin/python
"""Unit-tests for task #2."""

import unittest
from common.custom_test_case import TestNothing

from selprint import query_database


class TestDatabase(TestNothing):
    """Test for:
    [#2] Database selection.
    """
    def test_single_key(self):
        result = '34382SDF23'
        self.assertEqual(query_database('under_body'), result)
        self.assertEqual(query_database('under_body', engine='dict'), result)
        self.assertEqual(query_database('under_body', engine='tree'), result)

        result = 'AX65\nAAH\nGGH321D'
        self.assertEqual(query_database('bearing'), result)
        self.assertEqual(query_database('bearing', engine='dict'), result)
        self.assertEqual(query_database('bearing', engine='tree'), result)

    def test_muli_key(self):
        result = 'GGH321D'
        self.assertEqual(query_database('under_body bearing'), result)
        self.assertEqual(query_database('under_body bearing', engine='tree'),
                         result)
        self.assertEqual(query_database('under_body driving_system bearing'), 
                         result)
        self.assertEqual(query_database('under_body driving_system bearing',
                                        engine='tree'), result)

        result = 'AX65\nAAH'
        self.assertEqual(query_database('car_body bearing'), result)
        self.assertEqual(query_database('car_body bearing', engine='tree'),
                         result)


if __name__ == '__main__':
    unittest.main()
