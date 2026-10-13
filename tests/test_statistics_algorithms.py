import bisect
import importlib.util
from pathlib import Path
import unittest
import numpy as np
from scipy import stats

EXAMPLES=Path(__file__).resolve().parents[1]/'examples'

def load(name):
    spec=importlib.util.spec_from_file_location(name,EXAMPLES/(name+'.py'))
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module

inference=load('statistics_demo')
algorithms=load('basic_algorithms_demo')


class StatisticsAlgorithmsTest(unittest.TestCase):
    def test_welch_direction_interval_and_independent_reference(self):
        a=np.array([0.,1.,2.,4.]);b=np.array([3.,4.,8.,9.,11.])
        forward=inference.welch_summary(a,b);reverse=inference.welch_summary(b,a)
        reference=stats.ttest_ind(b,a,equal_var=False)
        np.testing.assert_allclose([forward['t'],forward['p']],[reference.statistic,reference.pvalue],rtol=1e-12)
        np.testing.assert_allclose(reverse['CI'],[-forward['CI'][1],-forward['CI'][0]])
        self.assertAlmostEqual(forward['effect_B_minus_A'],-reverse['effect_B_minus_A'])

    def test_bh_ties_reordering_and_invalid_values(self):
        p=np.array([.2,.01,.04,.01])
        np.testing.assert_allclose(inference.adjust_bh(p),[.2,.02,.16/3,.02])
        np.testing.assert_allclose(inference.adjust_bh(p),stats.false_discovery_control(p))
        for bad in [[],[np.nan],[1.01],[-.01]]:
            with self.assertRaises(ValueError):inference.adjust_bh(bad)

    def test_binary_search_matches_standard_library_at_boundaries(self):
        for values in [[],[3],[1,3,3,8]]:
            for target in [-1,0,1,2,3,8,9]:
                self.assertEqual(algorithms.lower_bound(values,target),bisect.bisect_left(values,target))
        self.assertEqual(dict(algorithms.kmer_counts('ATATAT',2)),{'AT':3,'TA':2})

    def test_alignment_traceback_restores_inputs_and_score(self):
        for a,b in [('', 'AGT'),('ACGT',''),('ACGT','AGT'),('AC','GT')]:
            score,left,right=algorithms.global_alignment(a,b)
            self.assertEqual(left.replace('-',''),a);self.assertEqual(right.replace('-',''),b)
            self.assertEqual(len(left),len(right))
            rescored=sum(-2 if '-' in (x,y) else (2 if x==y else -1) for x,y in zip(left,right))
            self.assertEqual(score,rescored)
        self.assertEqual(algorithms.global_alignment('ACGT','AGT')[0],4)

    def test_graph_cycles_and_unreachable_nodes(self):
        graph={'a':['b','c'],'b':['a','d'],'c':['d'],'d':[],'z':[]}
        self.assertEqual(algorithms.bfs_distances(graph,'a'),{'a':0,'b':1,'c':1,'d':2})

    def test_kmeans_objective_and_final_assignment(self):
        points=np.array([[-2.,-1.],[-2.,0.],[-1.,-1.],[2.,1.],[2.,2.],[3.,1.]])
        centers,labels,history=algorithms.kmeans(points,2)
        self.assertTrue((np.diff(history)<=1e-10).all())
        distances=((points[:,None,:]-centers[None,:,:])**2).sum(axis=2)
        np.testing.assert_array_equal(labels,distances.argmin(axis=1))
        for cluster in np.unique(labels):np.testing.assert_allclose(centers[cluster],points[labels==cluster].mean(axis=0))

    def test_gradient_descent_matches_full_rank_solver(self):
        x=np.column_stack([np.ones(6),np.arange(6.)]);y=np.array([1.,3.,4.,7.,8.,11.])
        result,loss,_=algorithms.gradient_least_squares(x,y)
        reference=np.linalg.lstsq(x,y,rcond=None)[0]
        np.testing.assert_allclose(result,reference,atol=1e-8,rtol=0)
        self.assertTrue((np.diff(loss)<=1e-12).all())


if __name__=='__main__':unittest.main()
