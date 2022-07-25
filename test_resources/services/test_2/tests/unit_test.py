import os
import sys
import unittest

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

# Agregar los imports de las funciones acá


class ExampleTestCase(unittest.TestCase):
    """
    Esto es solo un ejemplo de como debes realizar test unitarios a tus
    funciones.
    """

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())


if __name__ == '__main__':
    unittest.main()
