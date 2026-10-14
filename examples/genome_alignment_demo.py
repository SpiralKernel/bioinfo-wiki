#!/usr/bin/env python3
"""Actually align artificial FASTQ, check BAM and call one known heterozygous SNV."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess

PROJECT=Path(__file__).resolve().parents[1]


def run_demo(source,output,minimap2,samtools,bcftools):
    source,output=Path(source).resolve(),Path(output).resolve()
    if source==output or source in output.parents or output in source.parents:raise ValueError('Keep input and output separate')
    tools={}
    for key,value in [('minimap2',minimap2),('samtools',samtools),('bcftools',bcftools)]:
        found=shutil.which(str(value))
        if not found:raise ValueError(f'{key} not found')
        tools[key]=str(Path(found).resolve())
    output.mkdir(parents=True,exist_ok=True)
    for name in ['genome.fa','reads.fastq']:shutil.copy2(source/name,output/name)
    log=[]
    def run(tool,*args,save=None):
        result=subprocess.run([tools[tool],*map(str,args)],cwd=output,capture_output=True,text=True,check=True)
        log.append(dict(command=[tool,*map(str,args)],stderr=result.stderr))
        if save:
            path=output/save;temp=path.with_name(path.name+'.tmp');temp.write_text(result.stdout);temp.replace(path)
        return result.stdout
    versions={name:run(name,'--version').splitlines()[:2] for name in tools}
    run('minimap2','-ax','sr','-t','1','-R',r'@RG\tID:toy\tSM:toySample','genome.fa','reads.fastq',save='alignments.sam')
    run('samtools','sort','-o','alignments.bam','alignments.sam')
    run('samtools','quickcheck','-v','alignments.bam')
    run('samtools','index','alignments.bam')
    run('samtools','faidx','genome.fa')
    run('samtools','flagstat','-O','json','alignments.bam',save='flagstat.json')
    run('samtools','coverage','-o','coverage.tsv','alignments.bam')
    run('bcftools','mpileup','-f','genome.fa','-Ob','-o','pileup.bcf','alignments.bam')
    run('bcftools','call','--no-version','-m','-v','-Ov','-o','called.vcf','pileup.bcf')
    calls=[line.split('\t') for line in (output/'called.vcf').read_text().splitlines() if not line.startswith('#')]
    assert len(calls)==1 and calls[0][1:2]==['105'] and calls[0][3:5]==['C','T'],calls
    gt=dict(zip(calls[0][8].split(':'),calls[0][9].split(':')))['GT'];assert gt=='0/1',gt
    stats=json.loads((output/'flagstat.json').read_text())
    assert stats['QC-passed reads']['total']==40 and stats['QC-passed reads']['primary mapped']==40,stats
    summary=dict(scope='Artificial 40 single-end 150 bp reads, 1.6 kb reference; real mapping/BAM checks/calling; no real-sample accuracy benchmark',
        versions=versions,primary_mapped=stats['QC-passed reads']['primary mapped'],input_reads=40,
        call=dict(chrom=calls[0][0],pos=105,ref='C',alt='T',gt=gt),
        coverage=(output/'coverage.tsv').read_text().splitlines(),
        input_sha256={name:hashlib.sha256((source/name).read_bytes()).hexdigest() for name in ['genome.fa','reads.fastq']})
    (output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    (output/'commands.json').write_text(json.dumps(log,indent=2)+'\n')
    print(json.dumps(summary,indent=2));return summary


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input-dir',type=Path,default=PROJECT/'examples/data/annotation')
    parser.add_argument('--output',type=Path,default=PROJECT/'examples/output/alignment-chain')
    parser.add_argument('--minimap2',default=os.environ.get('MINIMAP2_BIN','minimap2'))
    parser.add_argument('--samtools',default=os.environ.get('SAMTOOLS_BIN','samtools'))
    parser.add_argument('--bcftools',default=os.environ.get('BCFTOOLS_BIN','bcftools'))
    args=parser.parse_args()
    try:run_demo(args.input_dir,args.output,args.minimap2,args.samtools,args.bcftools)
    except subprocess.CalledProcessError as error:parser.exit(1,f'Tool failed:\n{error.stderr}\n')
    except ValueError as error:parser.exit(1,f'{error}\n')
