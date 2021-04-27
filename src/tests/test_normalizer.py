import unittest

from dancesport_normalization.normalizer import getDance
from dancesport_normalization.enums import Dance, Style

class TestNormalizer(unittest.TestCase):
    
    def test_getDance_waltz(self):
        self.assertEqual(getDance('Waltz'), Dance.Waltz)
        self.assertEqual(getDance(' Waltz'), Dance.Waltz)
        self.assertEqual(getDance('waltz'), Dance.Waltz)
        # self.assertEqual(getDance('W'), Dance.Waltz)
        self.assertNotEqual(getDance('Viennese Waltz'), Dance.Waltz)

if __name__ == '__main__':
    unittest.main()