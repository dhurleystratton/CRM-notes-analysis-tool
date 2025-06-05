import os
import unittest

import analyze_crm_threads as analyzer

DATA_PATH = os.path.join(os.path.dirname(__file__), 'sample_notes.csv')


class TestAnalyzer(unittest.TestCase):
    def test_parse_notes(self):
        notes = analyzer.parse_notes(DATA_PATH)
        self.assertEqual(len(notes), 3)
        self.assertEqual(notes[0]['Item ID'], '1')
        self.assertEqual(notes[1]['User'], 'Bob')

    def test_analyze_notes(self):
        notes = analyzer.parse_notes(DATA_PATH)
        analysis = analyzer.analyze_notes(notes)
        self.assertEqual(set(analysis.keys()), {'1', '2'})
        self.assertEqual(analysis['1']['last_user'], 'Bob')


if __name__ == '__main__':
    unittest.main()
