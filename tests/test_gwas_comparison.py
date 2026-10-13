import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('gwas_comparison', Path(__file__).resolve().parents[1]/'examples/plot_gwas_comparison.py')
comparison = importlib.util.module_from_spec(spec)
spec.loader.exec_module(comparison)


class ComparisonTest(unittest.TestCase):
    def reference(self):
        return {'v1': {'ID':'v1', 'CHR':'1', 'POS':10, 'EA':'A', 'OA':'G', 'EAF':.2, 'BETA':.5,
                       'SE':.1, 'NEG_LOG10_P':5., 'N':100}}

    def test_swapping_alleles_changes_beta_and_frequency_only(self):
        reference = self.reference()
        incoming = {'v1': dict(reference['v1'], EA='G', OA='A', EAF=.8, BETA=-.5)}
        harmonized, flipped = comparison.harmonize(reference, incoming)
        self.assertEqual(flipped, 1)
        self.assertAlmostEqual(harmonized['v1']['EAF'], .2)
        self.assertEqual(harmonized['v1']['BETA'], .5)
        self.assertEqual(harmonized['v1']['NEG_LOG10_P'], 5.)
        self.assertEqual(incoming['v1']['EA'], 'G')

    def test_mismatched_strand_coordinates_or_samples_are_rejected(self):
        reference = self.reference()
        for changes in [{'EA':'T', 'OA':'C'}, {'POS':11}, {'N':99}]:
            with self.assertRaises(ValueError):
                comparison.harmonize(reference, {'v1':dict(reference['v1'], **changes)})
        with self.assertRaises(ValueError):
            comparison.harmonize(reference, {})

    def test_regenie_log10p_is_not_interpreted_as_raw_p(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'result.regenie'
            header='CHROM GENPOS ID ALLELE0 ALLELE1 A1FREQ N TEST BETA SE CHISQ LOG10P EXTRA\n'
            row='1 10 v1 G A 0.2 100 ADD 0.5 0.1 25 5 NA\n'
            path.write_text(header+row)
            result=comparison.normalize(path, 'regenie', 100)
            self.assertEqual(result['v1']['NEG_LOG10_P'], 5.)
            path.write_text(header+row+row)
            with self.assertRaisesRegex(ValueError, 'Duplicate'):
                comparison.normalize(path, 'regenie', 100)


if __name__ == '__main__':
    unittest.main()
