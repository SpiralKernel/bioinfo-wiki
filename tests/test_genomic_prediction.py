import importlib.util
from pathlib import Path
import unittest
import numpy as np

spec=importlib.util.spec_from_file_location('gs_demo',Path(__file__).resolve().parents[1]/'examples/genomic_prediction_demo.py')
gs=importlib.util.module_from_spec(spec);spec.loader.exec_module(gs)


class GenomicPredictionTest(unittest.TestCase):
    def test_matching_marker_and_relationship_formulations(self):
        self.assertLess(gs.equivalence_check(),1e-10)

    def test_family_folds_never_share_family_ids(self):
        groups=np.repeat(np.arange(10),3)
        seen=[]
        for train,test in gs.folds(np.arange(30),groups,'family',5,42):
            self.assertFalse(set(groups[train]) & set(groups[test]))
            self.assertFalse(set(train) & set(test))
            seen.extend(test)
        self.assertEqual(sorted(seen),list(range(30)))

    def test_centering_uses_training_only_and_rejects_zero_variation(self):
        train=np.array([[0.,0.],[1.,0.],[2.,0.]])
        test=np.array([[2.,2.]])
        z,ztest,scale,keep=gs.preprocess(train,test)
        self.assertEqual(keep.tolist(),[True,False])
        np.testing.assert_allclose(z[:,0],[-1.,0.,1.])
        np.testing.assert_allclose(ztest,[[1.]])
        self.assertAlmostEqual(scale,.5)
        with self.assertRaises(ValueError):gs.preprocess(np.zeros((3,2)),test)


if __name__=='__main__':unittest.main()
