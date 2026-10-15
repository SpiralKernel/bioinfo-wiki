"""Native-R input semantics and preservation of existing teaching results."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

PROJECT = Path(__file__).resolve().parents[1]
RSCRIPT = shutil.which(os.environ.get('RSCRIPT_BIN', 'Rscript'))


@unittest.skipUnless(RSCRIPT, 'native R tests require RSCRIPT_BIN or Rscript on PATH')
class NativeRNAInputsTest(unittest.TestCase):
    def test_native_input_checks_reject_invalid_counts_and_unidentifiable_designs(self):
        result = subprocess.run([RSCRIPT, 'examples/test_rnaseq_inputs.R'], cwd=PROJECT,
                                capture_output=True, text=True, check=True)
        self.assertIn('PASS: 10 input/design assertions', result.stdout)

    def test_existing_results_are_preserved_before_analysis_starts(self):
        with tempfile.TemporaryDirectory() as folder:
            sentinel = Path(folder) / 'keep.txt'
            sentinel.write_text('existing result\n')
            result = subprocess.run([RSCRIPT, 'examples/rnaseq_airway_demo.R', folder], cwd=PROJECT,
                                    capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('existing results are preserved', result.stderr)
            self.assertEqual(sentinel.read_text(), 'existing result\n')
            self.assertEqual(list(Path(folder).iterdir()), [sentinel])
