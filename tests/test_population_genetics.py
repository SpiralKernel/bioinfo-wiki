import importlib.util
from itertools import combinations
from pathlib import Path
import unittest
import numpy as np

spec = importlib.util.spec_from_file_location('population_genetics', Path(__file__).resolve().parents[1]/'examples/population_genetics_demo.py')
demo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(demo)


class PopulationGeneticsTest(unittest.TestCase):
    def test_pi_matches_direct_sequence_pairs_and_callable_denominator(self):
        x = np.array([[0,0], [0,1], [1,1], [1,0]])
        direct = np.mean([np.count_nonzero(a != b) for a,b in combinations(x,2)])
        original = demo.diversity(x)
        extended = demo.diversity(np.pad(x, ((0,0),(0,2))))
        self.assertAlmostEqual(original['pi_total'], direct)
        self.assertAlmostEqual(extended['pi_per_site'], original['pi_per_site']/2)
        self.assertEqual(extended['segregating_sites'], original['segregating_sites'])
        self.assertAlmostEqual(extended['Tajima_D'], original['Tajima_D'])

    def test_ld_pairing_allele_flip_and_monomorphic_boundary(self):
        x = np.array([0,0,1,1])
        self.assertAlmostEqual(demo.ld(x,x)['r2'], 1)
        self.assertAlmostEqual(demo.ld(x,1-x)['r2'], 1)
        self.assertIsNone(demo.ld(x,np.ones(4))['r2'])
        for invalid in [x[:,None], x[:-1], np.array([0,0,np.nan,1]), np.array([0,0,2,1])]:
            with self.subTest(shape=invalid.shape), self.assertRaises(ValueError):
                demo.ld(x,invalid)

    def test_descriptive_differentiation_boundaries_and_input_validation(self):
        a = np.zeros((4,2)); b = np.ones((3,2))
        self.assertAlmostEqual(demo.descriptive_fst(a,b)['FST'], 1)
        self.assertAlmostEqual(demo.descriptive_fst([[0],[1]],[[0],[1]])['FST'], 0)
        self.assertIsNone(demo.descriptive_fst(a,a)['FST'])
        for bad in [np.ones((4,1)), np.full((4,2), np.nan), np.ones(2)]:
            with self.assertRaises(ValueError):
                demo.descriptive_fst(a,bad)
