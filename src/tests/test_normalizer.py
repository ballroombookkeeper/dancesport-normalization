import os
import unittest

from dancesport_normalization.normalizer import getDances
from dancesport_normalization.enums import Dance, Style

ALL_EVENT_FILE = os.path.join(os.path.dirname(__file__), 'event_names.txt')

class TestNormalizer(unittest.TestCase):
    
    def test_getDance_waltz(self):
        waltzStrings = [
            'Waltz',
            ' Waltz',
            'waltz'
        ]

        notWaltzStrings = [
            'Viennese Waltz',
            'V. Waltz',
            'V Waltz'
        ]

        for waltzStr in waltzStrings:
            dances = getDances(waltzStr)
            self.assertIsNotNone(dances, waltzStr)
            self.assertEqual(dances[0], Dance.Waltz)

        for notWaltzStr in notWaltzStrings:
            dances = getDances(notWaltzStr)
            if dances is not None and len(dances) > 0:
                self.assertNotEqual(dances[0], Dance.Waltz)

    def test_getDance_allEventSetNoneNone(self):
        print(ALL_EVENT_FILE)
        with open(ALL_EVENT_FILE, 'r') as allEvents:
            for line in allEvents:
                self.assertIsNotNone(getDances(line), line)

if __name__ == '__main__':
    unittest.main()