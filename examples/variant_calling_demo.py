#!/usr/bin/env python3
"""Actual callers on artificial DNA; tiny truth checks, not a real-data benchmark."""
import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
import random
import shutil
import subprocess
import pysam

PROJECT = Path(__file__).resolve().parents[1]


def fresh_output(path):
    path = Path(path).resolve()
    if path.exists() and (not path.is_dir() or any(path.iterdir())):
        raise ValueError('Use a new/empty output directory; existing results are preserved')
    path.mkdir(parents=True, exist_ok=True)
    return path


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_vcf(path):
    with pysam.VariantFile(path) as handle:
        return [dict(chrom=r.contig, pos=r.pos, id=r.id, ref=r.ref, alt=list(r.alts or []),
                     svtype=r.info['SVTYPE'] if 'SVTYPE' in r.info else None, stop=r.stop, filters=list(r.filter),
                     samples={s:dict(gt=list(r.samples[s].get('GT') or []),
                                     support=r.samples[s].get('DV'),reference_support=r.samples[s].get('DR'),gq=r.samples[s].get('GQ')) for s in r.samples}) for r in handle]


def force_ps_compatibility(raw, derived, expected_sample=None):
    """Narrow, recorded workaround for observed Sniffles2.8.1 force FORMAT/PS defect."""
    raw,derived=Path(raw),Path(derived)
    if raw.resolve()==derived.resolve() or derived.exists():
        raise ValueError('Preserve raw output and use a new derived file')
    lines=raw.read_text().splitlines();known_source='##genotypeSource=Sniffles2_2.8.1' in lines
    has_ps=any(x.startswith('##FORMAT=<ID=PS,') for x in lines)
    changed=0;result=[];original_sample=None
    for line in lines:
        if line.startswith('#CHROM'):
            fields=line.split('\t')
            if len(fields)!=10:raise ValueError('Expected one-sample header')
            original_sample=fields[-1]
            if expected_sample:fields[-1]=expected_sample
            result.append('\t'.join(fields));continue
        if line.startswith('#'):result.append(line);continue
        fields=line.split('\t')
        if len(fields)!=10:raise ValueError('Expected the one-sample force fixture')
        keys=fields[8].split(':');values=fields[9].split(':')
        if len(keys)==len(values):result.append(line);continue
        if not (known_source and has_ps and fields[8]=='GT:GQ:DR:DV' and len(values)==5 and values[-1]=='.'):
            raise ValueError('Unrecognized force FORMAT defect; no repair applied')
        fields[8]+=':PS';changed+=1;result.append('\t'.join(fields))
    derived.write_text('\n'.join(result)+'\n')
    # Do not label inherited INFO fields as this sample's force-call evidence.
    return dict(changed_records=changed,operation='Sniffles2.8.1 only: append PS for known 4-key/5-value trailing-dot fixture; correct inherited sample header after BAM RG check; raw retained',
                raw_sha256=sha(raw),derived_sha256=sha(derived),
                original_sample_header=original_sample,actual_input_sample=expected_sample or original_sample,
                evidence_note='Use current sample FORMAT DR/DV; INFO SUPPORT/VAF/COVERAGE can be inherited from candidate VCF')


class Commands:
    def __init__(self, output):
        self.output = output
        self.log = []
    def run(self, name, *args, stdout=None):
        executable = shutil.which(os.environ.get(name.upper()+'_BIN', name))
        if not executable:
            raise ValueError(f'{name} not found; set {name.upper()}_BIN')
        result = subprocess.run([executable, *map(str,args)], cwd=self.output,
                                capture_output=True, text=True, check=True)
        self.log.append(dict(command=[name,*map(str,args)],stderr=result.stderr))
        if stdout:
            target=self.output/stdout;temporary=target.with_name(target.name+'.tmp')
            temporary.write_text(result.stdout);temporary.replace(target)
        return result.stdout
    def save(self):
        (self.output/'commands.json').write_text(json.dumps(self.log,indent=2)+'\n')


def make_long_inputs(output, seed=20261015):
    rng=random.Random(seed)
    reference=''.join(rng.choices('ACGT',k=100000));insertion=''.join(rng.choices('ACGT',k=300))
    haplotype=reference[:30000]+reference[30500:70000]+insertion+reference[70000:]
    (output/'reference.fa').write_text('>chrToySV\n'+reference+'\n')
    for sample in ['V01','R01']:
        with (output/(sample+'.fastq')).open('w') as handle:
            for i in range(160):
                seq=haplotype if sample=='V01' and i%2 else reference
                start=rng.randrange(len(seq)-16000+1);read=seq[start:start+16000]
                handle.write(f'@{sample}_{i:03d}\n{read}\n+\n'+ 'I'*len(read)+'\n')
    header='##fileformat=VCFv4.2\n##contig=<ID=chrToySV,length=100000>\n'
    header+='##INFO=<ID=SVTYPE,Number=1,Type=String,Description="Event type">\n'
    header+='##INFO=<ID=SVLEN,Number=1,Type=Integer,Description="Length change">\n'
    header+='##INFO=<ID=END,Number=1,Type=Integer,Description="End coordinate">\n'
    header+='##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">\n'
    body='#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tV01\n'
    body+=f'chrToySV\t30000\ttruth_del\t{reference[29999:30500]}\t{reference[29999]}\t60\tPASS\tSVTYPE=DEL;SVLEN=-500;END=30500\tGT\t0/1\n'
    body+=f'chrToySV\t70000\ttruth_ins\t{reference[69999]}\t{reference[69999]}{insertion}\t60\tPASS\tSVTYPE=INS;SVLEN=300;END=70000\tGT\t0/1\n'
    (output/'truth.vcf').write_text(header+body)
    (output/'callable.bed').write_text('chrToySV\t10000\t90000\n')
    return dict(seed=seed,reference_length=100000,read_length=16000,reads_per_sample=160,
                expected_events=[dict(type='DEL',anchor=30000,length=500),dict(type='INS',anchor=70000,length=300)],
                truth_sha256=sha(output/'truth.vcf'),
                input_sha256={name:sha(output/name) for name in ['reference.fa','V01.fastq','R01.fastq','truth.vcf','callable.bed']})


def compress_vcf(path):
    target=str(path)+'.gz';pysam.tabix_compress(str(path),target,force=True)
    pysam.tabix_index(target,preset='vcf',force=True)
    return target


def run_sv(output):
    output=fresh_output(output);info=make_long_inputs(output);commands=Commands(output)
    commands.run('samtools','faidx','reference.fa')
    for sample in ['V01','R01']:
        commands.run('minimap2','-ax','map-hifi','-t','1','-R',fr'@RG\tID:{sample}\tSM:{sample}',
                     'reference.fa',sample+'.fastq',stdout=sample+'.sam')
        commands.run('samtools','sort','-o',sample+'.bam',sample+'.sam')
        commands.run('samtools','quickcheck','-v',sample+'.bam')
        commands.run('samtools','index',sample+'.bam')
        commands.run('sniffles','--input',sample+'.bam','--reference','reference.fa','--vcf',sample+'.vcf',
                     '--snf',sample+'.snf','--sample-id',sample,'--threads','1','--all-contigs','--minsvlen','50')
    commands.run('sniffles','--input','V01.snf','R01.snf','--vcf','cohort.vcf','--reference','reference.fa','--threads','1','--all-contigs')
    commands.run('sniffles','--input','R01.bam','--reference','reference.fa','--genotype-vcf','V01.vcf',
                 '--vcf','R01.force.vcf','--sample-id','R01','--threads','1','--all-contigs')
    truth=compress_vcf(output/'truth.vcf');calls=compress_vcf(output/'V01.vcf')
    commands.run('truvari','bench','-b',Path(truth).name,'-c',Path(calls).name,'-o','bench',
                 '-f','reference.fa','--includebed','callable.bed','--passonly','-s','50','-S','50',
                 '-r','100','-p','0.7','-P','0.7','--pick','single')
    bench=json.loads((output/'bench/summary.json').read_text())
    rows=read_vcf(output/'V01.vcf');control=read_vcf(output/'R01.vcf')
    with pysam.AlignmentFile(output/'R01.bam') as bam:
        assert {r['SM'] for r in bam.header.to_dict()['RG']}=={'R01'}
    force_check=force_ps_compatibility(output/'R01.force.vcf',output/'R01.force.compat.vcf',expected_sample='R01')
    forced=read_vcf(output/'R01.force.compat.vcf');cohort=read_vcf(output/'cohort.vcf')
    assert len(rows)==2 and {r['svtype'] for r in rows}=={'DEL','INS'},rows
    assert not control,control
    assert bench['TP-base']==2 and bench['TP-comp']==2 and bench['FP']==0 and bench['FN']==0,bench
    assert len(forced)==2 and all(list(r['samples'].values())[0]['gt']==[0,0] for r in forced),forced
    assert len(cohort)==2 and all(set(r['samples'])=={'V01','R01'} for r in cohort),cohort
    summary=dict(scope='Fully artificial reference and perfect DNA reads; actual mapping, Sniffles discovery/SNF/force and Truvari matching; not a real-data accuracy estimate',
                 inputs=info,versions=dict(sniffles=commands.run('sniffles','--version').strip(),
                    truvari=commands.run('truvari','version').strip(),minimap2=commands.run('minimap2','--version').strip(),
                    samtools=commands.run('samtools','--version').splitlines()[0]),
                 variants=rows,reference_control_calls=len(control),forced_reference=forced,force_format_compatibility=force_check,cohort=cohort,
                 benchmark={key:bench[key] for key in ['TP-base','TP-comp','FP','FN','precision','recall','f1','gt_concordance','TP-comp_TP-gt','TP-comp_FP-gt']},
                 evaluation=dict(region='chrToySV:10000-90000 BED',refdist=100,pctseq=.7,pctsize=.7,pick='single',passonly=True))
    (output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');commands.save();return summary


def run_small(output):
    output=fresh_output(output);commands=Commands(output)
    for name in ['genome.fa','reads.fastq']:shutil.copy2(PROJECT/'examples/data/annotation'/name,output/name)
    commands.run('samtools','faidx','genome.fa')
    commands.run('minimap2','-ax','sr','-t','1','-R',r'@RG\tID:toy\tSM:toySample','genome.fa','reads.fastq',stdout='aligned.sam')
    commands.run('samtools','sort','-o','aligned.bam','aligned.sam');commands.run('samtools','index','aligned.bam')
    commands.run('freebayes','-f','genome.fa','-p','2','aligned.bam',stdout='calls.vcf')
    rows=read_vcf(output/'calls.vcf')
    assert len(rows)==1 and rows[0]['pos']==105 and rows[0]['ref']=='C' and rows[0]['alt']==['T'],rows
    assert list(rows[0]['samples'].values())[0]['gt']==[0,1],rows
    result=dict(scope='Artificial 40 short reads; actual FreeBayes diploid call; no polyploid accuracy benchmark',
                freebayes_version=commands.run('freebayes','--version').strip(),variants=rows,
                input_sha256={name:sha(output/name) for name in ['genome.fa','reads.fastq']})
    (output/'summary.json').write_text(json.dumps(result,indent=2)+'\n');commands.save();return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case',choices=['sv','small'],default='sv');parser.add_argument('--output',type=Path)
    args=parser.parse_args();output=args.output or PROJECT/('examples/output/calling-'+args.case)
    try:result=run_sv(output) if args.case=='sv' else run_small(output)
    except (ValueError,subprocess.CalledProcessError) as error:
        parser.exit(1,str(error)+'\n'+getattr(error,'stderr',''))
    print(json.dumps(result,indent=2))
