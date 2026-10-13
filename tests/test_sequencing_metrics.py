import importlib.util
from pathlib import Path
import unittest

spec=importlib.util.spec_from_file_location('sequencing_metrics',Path(__file__).resolve().parents[1]/'examples/sequencing_metrics_demo.py')
metrics=importlib.util.module_from_spec(spec);spec.loader.exec_module(metrics)


class SequencingMetricsTest(unittest.TestCase):
    def test_overlap_is_counted_once_within_a_molecule_only(self):
        self.assertEqual(metrics.coverage([[(0,3),(2,5)]],6),[1,1,1,1,1,0])
        self.assertEqual(metrics.coverage([[(0,3)],[(2,5)]],6),[1,1,2,1,1,0])

    def test_interval_union_preserves_unsequenced_gaps(self):
        self.assertEqual(metrics.merged_intervals([(5,8),(0,2)]),[(0,2),(5,8)])
        self.assertEqual(metrics.coverage([[(0,2),(5,8)]],8),[1,1,0,0,0,1,1,1])
        with self.assertRaises(ValueError):metrics.coverage([[(0,9)]],8)
        with self.assertRaises(ValueError):metrics.merged_intervals([(-1,2)])

    def test_n50_weighting_reference_and_unreachable_threshold(self):
        lengths=[500,100,100,100,100,100]
        self.assertEqual(metrics.n50(lengths),500)
        self.assertEqual(metrics.n50(lengths,1200),100)
        self.assertIsNone(metrics.n50(lengths,3000))
        with self.assertRaises(ValueError):metrics.n50([])
        with self.assertRaises(ValueError):metrics.n50([1,0])

    def test_quality_average_uses_error_probability(self):
        self.assertAlmostEqual(metrics.effective_phred([30,30]),30)
        self.assertAlmostEqual(metrics.effective_phred([20,40]),22.967086218813385)
        self.assertLess(metrics.effective_phred([20,40]),30)
        with self.assertRaises(ValueError):metrics.effective_phred([])


if __name__=='__main__':unittest.main()
