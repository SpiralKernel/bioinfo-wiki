import contextlib
import importlib.util
import io
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'examples/data/annotation'
def load(name):
    spec=importlib.util.spec_from_file_location(name,ROOT/'examples'/(name+'.py'))
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
ann=load('annotation_demo');alignment=load('genome_alignment_demo')
JAR=os.environ.get('SNPEFF_JAR')
BEDTOOLS=shutil.which(os.environ.get('BEDTOOLS_BIN','bedtools'))
JAVA=shutil.which(os.environ.get('JAVA_BIN','java'))
SAMTOOLS=shutil.which(os.environ.get('SAMTOOLS_BIN','samtools'))
MINIMAP2=shutil.which(os.environ.get('MINIMAP2_BIN','minimap2'))
BCFTOOLS=shutil.which(os.environ.get('BCFTOOLS_BIN','bcftools'))


class AnnotationInputTest(unittest.TestCase):
    def test_single_base_bed_conversion_and_invalid_gff_range(self):
        row=dict(chrom='chrToy',start=101,end=101,strand='+',attrs={'ID':'one'})
        self.assertEqual(ann.bed_row(row),['chrToy',100,101,'one',0,'+'])
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'bad.gff3';path.write_text('chrToy\ttest\tgene\t0\t1\t.\t+\t.\tID=bad\n')
            with self.assertRaisesRegex(ValueError,'outside'):ann.read_gff(path,{'chrToy':'ACGT'})

    def test_cds_sequences_match_both_strands_after_transcription_order(self):
        reference=ann.read_fasta(SOURCE/'genome.fa');expected=ann.read_fasta(SOURCE/'cds.fa')
        features=ann.read_gff(SOURCE/'genes.gff3',reference)
        complement=str.maketrans('ACGT','TGCA')
        for tx,sequence in expected.items():
            parts=[f for f in features if f['type']=='CDS' and f['attrs']['Parent']==tx]
            minus=parts[0]['strand']=='-';parts.sort(key=lambda f:f['start'],reverse=minus)
            reconstructed=''
            for part in parts:
                block=reference[part['chrom']][part['start']-1:part['end']]
                reconstructed+=block.translate(complement)[::-1] if minus else block
            self.assertEqual(reconstructed,sequence,tx)

    def test_multiallelic_ann_keeps_consequence_attached_to_its_allele(self):
        header="##INFO=<ID=ANN,Number=.,Type=String,Description=\"'Allele | Annotation | Annotation_Impact | Gene_Name | Gene_ID | Feature_Type | Feature_ID | HGVS.c | HGVS.p | WARNINGS'\">\n"
        body='chrToy\t107\tmulti\tC\tT,A\t60\tPASS\tANN=T|stop_gained|HIGH|gene|g|transcript|tx|c.7C>T|p.Gln3*|,A|missense_variant|MODERATE|gene|g|transcript|tx|c.7C>A|p.Gln3Lys|\n'
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'ann.vcf';path.write_text(header+body)
            rows=ann.ann_rows(path)
            self.assertEqual([(r['alt'],r['effect']) for r in rows],[('T','stop_gained'),('A','missense_variant')])
            self.assertEqual([r['alt'] for r in rows if r['impact']=='HIGH'],['T'])


@unittest.skipUnless(JAR and BEDTOOLS and JAVA,'SnpEff/bedtools integration requires matching environment variables')
class AnnotationToolsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory();cls.source=Path(cls.temp.name)/'input';cls.output=Path(cls.temp.name)/'output'
        shutil.copytree(SOURCE,cls.source)
        with contextlib.redirect_stdout(io.StringIO()):
            for step in ['build','annotate','intervals','report']:ann.run_step(step,cls.source,cls.output,JAR,BEDTOOLS,JAVA)
    @classmethod
    def tearDownClass(cls):cls.temp.cleanup()

    def test_half_open_gene_boundaries_and_negative_transcription_start(self):
        rows=[line.split('\t') for line in (self.output/'intervals/boundary-overlaps.tsv').read_text().splitlines()]
        by_id={r[3]:int(r[-1]) for r in rows}
        self.assertEqual(by_id,dict(before_plus=0,first_plus=1,last_plus=1,after_plus=0,tie_window=0,first_minus=1,before_minus=0))

    def test_report_rejects_stale_input_even_when_result_files_exist(self):
        copied=Path(self.temp.name)/'changed';shutil.copytree(self.source,copied)
        path=copied/'boundaries.bed';path.write_text(path.read_text().replace('99\t100','98\t100'))
        with self.assertRaisesRegex(ValueError,'Stale'):
            ann.run_step('report',copied,self.output)

    def test_wrong_protein_reference_does_not_save_a_validated_database(self):
        copied=Path(self.temp.name)/'bad-protein';shutil.copytree(self.source,copied)
        path=copied/'protein.fa';path.write_text(path.read_text().replace('MAQ','WWQ'))
        output=Path(self.temp.name)/'rejected'
        with self.assertRaises((ValueError,subprocess.CalledProcessError)):
            ann.run_step('build',copied,output,JAR,BEDTOOLS,JAVA)
        self.assertFalse((output/'database/data/toy/snpEffectPredictor.bin').exists())


@unittest.skipUnless(SAMTOOLS and MINIMAP2 and BCFTOOLS,'Alignment integration requires matching tool paths')
class AlignmentChainTest(unittest.TestCase):
    def test_real_alignment_chain_and_truncated_bam_detection(self):
        with tempfile.TemporaryDirectory() as tmp,contextlib.redirect_stdout(io.StringIO()):
            output=Path(tmp)/'output';alignment.run_demo(SOURCE,output,MINIMAP2,SAMTOOLS,BCFTOOLS)
            truncated=output/'truncated.bam';truncated.write_bytes((output/'alignments.bam').read_bytes()[:-28])
            result=subprocess.run([SAMTOOLS,'quickcheck','-v',str(truncated)],capture_output=True,text=True)
            self.assertNotEqual(result.returncode,0)
            self.assertIn('EOF',result.stderr)
