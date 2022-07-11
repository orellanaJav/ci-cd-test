import os
import sys
import unittest
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)


class ExampleTestCase(unittest.TestCase):
    """
    This is only an example of Unittest. You must develop your own.
    """

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FoxxzO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())


if __name__ == '__main__':
    unittest.main()
