"""Unit-tests for some task."""

from unittest import TestCase


class TestNothing(TestCase):
    """Test for:
    [#?] <Description>.

    Should be subclassed.
    """
    def setUp(self):
        print '*** Testing %s task ***' % self.get_description()
        pass

    def tearDown(self):
        pass

    def get_description(self):
        return self.__class__.__doc__.split('\n')[1][:-1].strip()
