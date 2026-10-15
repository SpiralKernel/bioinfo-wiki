"""Actual caller boundaries: missing headers, constrained repair and tiny known inputs."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

PROJECT=Path(__file__).resolve().parents[1]
try:
    import pysam
except ImportError:
    pysam=None
if pysam is not None:
    sys.path.insert(0,str(PROJECT/'examples'))
    import variant_calling_demo as calling
    import trgt_official_demo as trgt_demo

def available(name):return shutil.which(os.environ.get(name.upper()+'_BIN',name))
CALLING_TOOLS=all(available(n) for n in ['minimap2','samtools','sniffles','truvari','freebayes'])
TRGT=available('trgt');FIXTURE=os.environ.get('TRGT_TEST_INPUT')

@unittest.skipUnless(pysam,'caller parsing tests require pysam')
class CallingBoundariesTest(unittest.TestCase):
    def test_small_variant_vcf_does_not_require_svtype_header(self):
        text='##fileformat=VCFv4.2\n##contig=<ID=toy,length=10>\n##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">\n#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\ts\ntoy\t2\t.\tC\tT\t50\tPASS\t.\tGT\t0/1\n'
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)/'small.vcf';p.write_text(text)
            rows=calling.read_vcf(p)
            self.assertIsNone(rows[0]['svtype']);self.assertEqual(rows[0]['samples']['s']['gt'],[0,1])

    def test_force_compatibility_preserves_values_and_rejects_unrecognized_changes(self):
        header='##fileformat=VCFv4.2\n##genotypeSource=Sniffles2_2.8.1\n##FORMAT=<ID=PS,Number=1,Type=Integer,Description="Phase block">\n#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tV01\n'
        row='toy\t100\tknown\tAC\tA\t60\tPASS\t.\tGT:GQ:DR:DV\t0/0:0:31:0:.\n'
        with tempfile.TemporaryDirectory() as temp:
            raw=Path(temp)/'raw.vcf';derived=Path(temp)/'derived.vcf';raw.write_text(header+row)
            before=raw.read_bytes();record=calling.force_ps_compatibility(raw,derived,'R01')
            self.assertEqual(raw.read_bytes(),before)
            self.assertEqual(derived.read_text().splitlines()[-1].split('\t')[:8],row.strip().split('\t')[:8])
            self.assertEqual(derived.read_text().splitlines()[-1].split('\t')[-1],'0/0:0:31:0:.')
            self.assertEqual(record['original_sample_header'],'V01')
            self.assertIn('\tR01\n',derived.read_text())
            for bad in [(header+row).replace('2.8.1','2.9.0'),header+row.replace('31:0:.','31:0:9'),header+row.replace('GT:GQ:DR:DV','GT:DR')]:
                raw.write_text(bad);target=Path(temp)/'rejected.vcf'
                with self.assertRaises(ValueError):calling.force_ps_compatibility(raw,target)
                self.assertFalse(target.exists())

    def test_existing_output_is_never_removed(self):
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)/'keep.txt';p.write_text('keep')
            with self.assertRaises(ValueError):calling.fresh_output(temp)
            self.assertEqual(p.read_text(),'keep')

@unittest.skipUnless(pysam and CALLING_TOOLS,'professional tiny integration requires calling tools and pysam')
class CallingToolsTest(unittest.TestCase):
    def test_actual_sv_chain_keeps_missing_cohort_gt_and_low_quality_force(self):
        with tempfile.TemporaryDirectory() as temp:
            result=calling.run_sv(Path(temp)/'sv')
            self.assertEqual(result['benchmark']['TP-base'],2)
            self.assertEqual(result['benchmark']['TP-comp_TP-gt'],2)
            for row in result['cohort']:self.assertEqual(row['samples']['R01']['gt'],[None,None])
            for row in result['forced_reference']:
                self.assertEqual(row['samples']['R01']['gq'],0)
                self.assertEqual(row['samples']['R01']['support'],0)
            self.assertEqual(result['force_format_compatibility']['changed_records'],2)

    def test_actual_freebayes_known_heterozygous_snv(self):
        with tempfile.TemporaryDirectory() as temp:
            result=calling.run_small(Path(temp)/'small')
            self.assertEqual(result['variants'][0]['samples']['toySample']['gt'],[0,1])

@unittest.skipUnless(pysam and TRGT and FIXTURE,'TRGT integration requires official local fixture and binary')
class TRGTOfficialTest(unittest.TestCase):
    def test_actual_official_repeat_allele_units(self):
        with tempfile.TemporaryDirectory() as temp:
            result=trgt_demo.run(Path(temp)/'trgt',TRGT,FIXTURE)
            sample=next(iter(result['variants'][0]['samples'].values()))
            self.assertEqual(sample['AL'],[33,33]);self.assertEqual(sample['MC'],['11','11'])
            self.assertEqual(sample['GT'],[1,1])

    def test_changed_official_reference_is_rejected_before_calling(self):
        with tempfile.TemporaryDirectory() as temp:
            source=Path(temp)/'input';shutil.copytree(FIXTURE,source)
            path=source/'reference.fasta';path.write_bytes(path.read_bytes()+b'A')
            with self.assertRaisesRegex(ValueError,'checksum mismatch'):
                trgt_demo.run(Path(temp)/'output',TRGT,source)
            self.assertFalse((Path(temp)/'output/calls.vcf.gz').exists())
