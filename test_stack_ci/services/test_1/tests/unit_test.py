import os
import sys
import unittest

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

# Agregar los imports de las funciones acá
from core.test_1 import lambda_handler


class ExampleTestCase(unittest.TestCase):
    """
    Esto es solo un ejemplo de como debes realizar test unitarios a tus
    funciones.
    """

    def test_lambda_handler(self):
        handler = lambda_handler({}, {})
        self.assertEqual(handler, {'status': 'status'})

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())


if __name__ == '__main__':
    unittest.main()
