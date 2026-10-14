import contextlib
import hashlib
import importlib.util
import io
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT/'examples/data/variants'
spec = importlib.util.spec_from_file_location('variant_extraction', ROOT/'examples/variant_extraction_demo.py')
demo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(demo)
BCFTOOLS = shutil.which(os.environ.get('BCFTOOLS_BIN', 'bcftools'))
spec_pav = importlib.util.spec_from_file_location('pav_matrix', ROOT/'examples/pav_matrix_demo.py')
pav = importlib.util.module_from_spec(spec_pav)
spec_pav.loader.exec_module(pav)


class VariantInputTest(unittest.TestCase):
    def test_pav_unknown_and_absent_stay_distinct_after_shuffling(self):
        rows=[dict(locus_id='gene2',sample_id='S02',status='present'),
              dict(locus_id='gene1',sample_id='S01',status='absent'),
              dict(locus_id='gene1',sample_id='S02',status='unknown')]
        samples,matrix=pav.build_matrix(rows[::-1])
        self.assertEqual(samples,['S01','S02'])
        self.assertEqual(matrix,[{'locus_id':'gene1','S01':'0','S02':'NA'},
                                 {'locus_id':'gene2','S01':'NA','S02':'1'}])

    def test_duplicate_pav_evidence_stops_instead_of_overwriting(self):
        row=dict(locus_id='gene1',sample_id='S01',status='absent')
        with self.assertRaisesRegex(ValueError,'Duplicate'):
            pav.build_matrix([row,{**row,'status':'present'}])

    def test_output_cannot_overwrite_or_enclose_inputs(self):
        for target in [FIXTURE, FIXTURE/'output', FIXTURE.parent]:
            with self.subTest(target=target), self.assertRaises(ValueError):
                demo.validate_paths(FIXTURE, target)

    def test_fasta_index_offsets_match_contigs_and_record_reference_alleles(self):
        raw = (FIXTURE/'toy.fa').read_bytes()
        sequences = {}
        for line in (FIXTURE/'toy.fa.fai').read_text().splitlines():
            name, length, offset, line_bases, line_width = line.split('\t')
            self.assertEqual(int(line_width), int(line_bases)+1)
            sequence = raw[int(offset):int(offset)+int(length)].decode()
            self.assertEqual(len(sequence), int(length))
            self.assertTrue(set(sequence) <= set('ACGT'))
            sequences[name] = sequence
        for record in demo.read_records(FIXTURE/'calls.vcf'):
            start = record['pos']-1
            self.assertEqual(sequences[record['chrom']][start:start+len(record['ref'])], record['ref'])


@unittest.skipUnless(BCFTOOLS, 'bcftools integration requires BCFTOOLS_BIN or bcftools on PATH')
class VariantBcftoolsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.output = Path(cls.temp.name)/'output'
        cls.before = {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in FIXTURE.iterdir() if p.is_file()}
        with contextlib.redirect_stdout(io.StringIO()):
            cls.summary = demo.run_demo(BCFTOOLS, FIXTURE, cls.output)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_split_genotypes_keep_the_correct_alt_and_inputs_are_unchanged(self):
        records = [r for r in demo.read_records(self.output/'normalized.vcf') if r['id']=='mixed']
        by_alt = {r['alt']:[s['GT'] for s in r['samples']] for r in records}
        # Original S01=1/2, S02=0/2: alt 1 and alt 2 are different alleles.
        self.assertEqual(by_alt, {'G':['1/0','0/0','./.'], 'CA':['0/1','0/1','./.']})
        self.assertEqual(self.before, {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in FIXTURE.iterdir() if p.is_file()})

    def test_wrong_reference_stops_instead_of_silently_repairing_it(self):
        source = Path(self.temp.name)/'wrong-reference'
        shutil.copytree(FIXTURE, source)
        path = source/'calls.vcf'
        lines = path.read_text().splitlines()
        for i, line in enumerate(lines):
            if '\tsnv\t' in line:
                fields = line.split('\t'); fields[3] = 'T'; lines[i] = '\t'.join(fields)
        path.write_text('\n'.join(lines)+'\n')
        with self.assertRaises(subprocess.CalledProcessError) as caught:
            demo.run_demo(BCFTOOLS, source, Path(self.temp.name)/'rejected')
        self.assertIn('Reference allele mismatch', caught.exception.stderr)

    def test_bnd_mate_links_are_reciprocal_not_two_independent_events(self):
        rows = demo.read_records(self.output/'bnd.vcf')
        by_id = {r['id']:r for r in rows}
        self.assertEqual(len(rows), 2)
        self.assertEqual(len({r['info']['EVENT'] for r in rows}), 1)
        for row in rows:
            self.assertEqual(by_id[row['info']['MATEID']]['info']['MATEID'], row['id'])
