import math
from pathlib import Path
import sys
import unittest
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from volume_statistics import summarize
from validation_metrics import metrics, analyze


class AnalysisTests(unittest.TestCase):
    def test_metrics_signed_bias(self):
        m = metrics([-2,1,1])
        self.assertEqual(m['bias'],0)
        self.assertAlmostEqual(m['mae'],4/3)
        self.assertAlmostEqual(m['rmse'],math.sqrt(2))

    def test_block_sem_and_discard(self):
        m = summarize([999,8,8,10,10,12,12,999],1,1,2)
        self.assertEqual(m['volume_mean_A3'],10)
        self.assertEqual(m['n_tail_excluded'],1)
        self.assertAlmostEqual(m['volume_block_SEM_A3'],2/math.sqrt(3))
        self.assertAlmostEqual(m['a_pc_from_mean_volume_A'],10**(1/3))

    def test_invalid_inputs(self):
        for volumes,n,skip,block in [([8,8],1,0,2),([8]*8,0,0,2),([8]*8,1,-1,2),([8]*8,1,0,1),([float('nan')]*8,1,0,2),([-1]*8,1,0,2)]:
            with self.assertRaises(ValueError): summarize(volumes,n,skip,block)

    def test_final_validation_regression(self):
        m = analyze(ROOT/'data/lafeo3_validation')
        self.assertEqual(m['energy_meV_atom']['n'],100)
        self.assertEqual(m['force_components_eV_A']['n'],48000)
        self.assertEqual(m['stress_six_components_GPa']['n'],600)
        self.assertAlmostEqual(m['energy_meV_atom']['mae'],0.2465296087500377,places=7)
        self.assertAlmostEqual(m['force_components_eV_A']['mae'],0.013784362780833333,places=9)
        self.assertAlmostEqual(m['stress_six_components_GPa']['rmse'],0.029029876353060965,places=9)


if __name__ == '__main__': unittest.main()
