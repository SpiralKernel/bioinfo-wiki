import csv
import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('programming_basics', ROOT/'examples/programming_basics.py')
demo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(demo)


class ProgrammingBasicsTest(unittest.TestCase):
    def setUp(self):
        self.measured = demo.read_unique(ROOT/'examples/data/programming_measurements.csv', ['sample_id', 'value'])
        self.metadata = demo.read_unique(ROOT/'examples/data/programming_metadata.csv', ['sample_id', 'condition', 'batch'])

    def test_shuffled_metadata_preserves_ids_missing_and_known_means(self):
        joined, summary = demo.join_and_summarize(self.measured, self.metadata[::-1])
        self.assertEqual([r['sample_id'] for r in joined], [r['sample_id'] for r in self.measured])
        self.assertIsNone(joined[3]['value'])
        self.assertEqual(summary, {'rows': 8, 'missing': 1, 'groups': {'A': {'n': 3, 'mean': 2}, 'B': {'n': 4, 'mean': 5.5}}})

    def test_duplicate_and_unmatched_ids_stop_before_join(self):
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            demo.join_and_summarize(self.measured + self.measured[:1], self.metadata)
        with self.assertRaisesRegex(ValueError, 'sets do not match'):
            demo.join_and_summarize(self.measured, self.metadata[1:])

    def test_non_finite_numbers_are_rejected_not_counted_as_observations(self):
        for bad in ['NaN', 'Infinity', '-inf']:
            rows = [dict(r) for r in self.measured]
            rows[0]['value'] = bad
            with self.subTest(value=bad), self.assertRaisesRegex(ValueError, 'Non-finite'):
                demo.join_and_summarize(rows, self.metadata)

    def test_csv_ids_keep_leading_zeros_and_duplicates_are_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)/'input.csv'
            path.write_text('sample_id,value\n001,1\n010,2\n', encoding='utf-8')
            self.assertEqual([r['sample_id'] for r in demo.read_unique(path, ['sample_id', 'value'])], ['001', '010'])
            path.write_text('sample_id,value\n001,1\n001,2\n', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'duplicate'):
                demo.read_unique(path, ['sample_id', 'value'])
