#!/usr/bin/env python3
"""Real SnpEff/bedtools execution on artificial genes, not functional validation."""
import argparse
from collections import Counter
import csv
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
from urllib.parse import unquote

PROJECT=Path(__file__).resolve().parents[1]
REQUIRED=['genome.fa','genes.gff3','cds.fa','protein.fa','variants.vcf','boundaries.bed']


def read_fasta(path):
    records={};current=None
    for line in Path(path).read_text().splitlines():
        if line.startswith('>'):
            current=line[1:].split()[0]
            if current in records:raise ValueError('Duplicate FASTA ID')
            records[current]=''
        elif line:
            if current is None:raise ValueError('FASTA sequence before header')
            records[current]+=line.strip().upper()
    return records


def read_gff(path,reference):
    """Read the controlled GFF3 fixture; not a complete GFF/GTF validator."""
    rows=[]
    for line in Path(path).read_text().splitlines():
        if not line or line.startswith('#'):continue
        f=line.split('\t')
        if len(f)!=9:raise ValueError('GFF3 needs nine tab-separated columns')
        start,end=int(f[3]),int(f[4])
        if f[0] not in reference or not 1<=start<=end<=len(reference[f[0]]):
            raise ValueError('GFF3 range is outside the reference')
        if f[2]=='CDS' and f[7] not in {'0','1','2'}:raise ValueError('CDS phase must be 0, 1 or 2')
        attrs={key:unquote(value) for key,value in (part.split('=',1) for part in f[8].split(';') if part)}
        rows.append(dict(chrom=f[0],type=f[2],start=start,end=end,strand=f[6],phase=f[7],attrs=attrs))
    return rows


def bed_row(feature):
    return [feature['chrom'],feature['start']-1,feature['end'],feature['attrs']['ID'],0,feature['strand']]


def ann_rows(path):
    """Exact ALT association for this small SNV/indel fixture and SnpEff ANN schema."""
    result=[];schema=None
    for line in Path(path).read_text().splitlines():
        if line.startswith('##INFO=<ID=ANN,'):
            quoted=re.search(r"'([^']+)'",line)
            if not quoted:raise ValueError('ANN header has no readable schema')
            schema=[part.strip() for part in quoted[1].split('|')]
        if line.startswith('#'):continue
        f=line.split('\t');info=dict(x.split('=',1) if '=' in x else (x,'') for x in f[7].split(';'))
        if not schema or schema[:3]!=['Allele','Annotation','Annotation_Impact']:
            raise ValueError('Unexpected ANN schema; check the actual tool header')
        for item in info.get('ANN','').split(','):
            if not item:continue
            values=item.split('|')
            if len(values)!=len(schema):raise ValueError('ANN length does not match its header')
            entry=dict(zip(schema,values));alt=entry['Allele']
            if alt not in f[4].split(','):
                raise ValueError('This teaching extractor requires an exact original ALT match')
            result.append(dict(chrom=f[0],pos=int(f[1]),record_id=f[2],ref=f[3],alt=alt,
                gene=entry['Gene_ID'],transcript=entry['Feature_ID'],effect=entry['Annotation'],
                impact=entry['Annotation_Impact'],hgvs_c=entry['HGVS.c'],hgvs_p=entry['HGVS.p'],
                warnings=values[-1]))
    return result


def write_tsv(path,rows,fields):
    with Path(path).open('w',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=fields,delimiter='\t',lineterminator='\n')
        writer.writeheader();writer.writerows(rows)


def resolve_tool(value):
    found=shutil.which(str(value))
    if not found:raise ValueError(f'Tool not found: {value}')
    return str(Path(found).resolve())


def run_step(step,input_dir,output,jar=None,bedtools='bedtools',java='java',core_config=None):
    source=Path(input_dir).resolve();output=Path(output).resolve()
    if source==output or source in output.parents or output in source.parents:
        raise ValueError('Keep input and output separate and non-nested')
    for name in REQUIRED:
        if not (source/name).is_file():raise ValueError(f'Missing input: {name}')
    reference=read_fasta(source/'genome.fa');features=read_gff(source/'genes.gff3',reference)
    output.mkdir(parents=True,exist_ok=True)
    log=[]

    def run(command,cwd,save=None):
        result=subprocess.run(list(map(str,command)),cwd=cwd,text=True,capture_output=True,check=True)
        display=[str(x).replace(str(output),'<output>') for x in command]
        display=[Path(x).name if str(source) in x or '/.local-tools/' in x else x for x in display]
        log.append(dict(command=display,stderr=result.stderr.replace(str(output),'<output>')))
        if save:
            target=Path(cwd)/save;temp=target.with_name(target.name+'.tmp');temp.write_text(result.stdout);temp.replace(target)
        return result

    if step=='build':
        if not jar:raise ValueError('Set SNPEFF_JAR or pass --snpeff-jar')
        jar=Path(jar).resolve();java=resolve_tool(java)
        core=Path(core_config).resolve() if core_config else jar.parent/'snpEff.config'
        database=output/'database';data=database/'data/toy';data.mkdir(parents=True,exist_ok=True)
        for src,dst in [('genome.fa','sequences.fa'),('genes.gff3','genes.gff'),('cds.fa','cds.fa'),('protein.fa','protein.fa')]:
            shutil.copy2(source/src,data/dst)
        config=core.read_text()+'\n# Local artificial genome for this teaching run\ndata.dir = ./data\ntoy.genome = ArtificialTeachingGenome\n'
        (database/'snpeff.config').write_text(config)
        version=run([java,'-jar',jar,'-version'],database).stdout.strip()
        result=run([java,'-Xmx512m','-jar',jar,'build','-c','snpeff.config','-gff3','-v','-noLog','toy'],database)
        (database/'build.log').write_text(result.stdout+result.stderr)
        checks=[line for line in (result.stdout+result.stderr).splitlines() if any(word in line for word in ['CDS check','Protein check','Checked','Errors','OK:'])]
        counts={}
        for label in ['CDS','Protein']:
            match=re.search(label+r' check:\s*toy\s*OK:\s*(\d+).*?Errors:\s*(\d+)',result.stdout+result.stderr)
            if not match:raise ValueError(f'No readable {label} validation result')
            counts[label]=dict(ok=int(match[1]),errors=int(match[2]))
            if counts[label]!=dict(ok=3,errors=0):raise ValueError(f'{label} validation did not pass all three artificial transcripts')
        (output/'build-verification.json').write_text(json.dumps(dict(snpeff_version=version,jar_sha256=hashlib.sha256(jar.read_bytes()).hexdigest(),checks=checks,sequence_checks=counts,
            input_sha256={name:hashlib.sha256((source/name).read_bytes()).hexdigest() for name in ['genome.fa','genes.gff3','cds.fa','protein.fa']}),indent=2)+'\n')
    elif step=='annotate':
        if not jar:raise ValueError('Set SNPEFF_JAR or pass --snpeff-jar')
        jar=Path(jar).resolve();java=resolve_tool(java)
        folder=output/'annotation';folder.mkdir(exist_ok=True)
        shutil.copy2(source/'variants.vcf',folder/'variants.vcf')
        run([java,'-Xmx512m','-jar',jar,'ann','-c','../database/snpeff.config',
             '-nodownload','-noLog','-noStats','-ud','0','toy','variants.vcf'],folder,'annotated.vcf')
        rows=ann_rows(folder/'annotated.vcf');fields=['chrom','pos','record_id','ref','alt','gene','transcript','effect','impact','hgvs_c','hgvs_p','warnings']
        write_tsv(folder/'consequences.tsv',rows,fields)
        write_tsv(folder/'selected-high.tsv',[row for row in rows if row['impact']=='HIGH'],fields)
        (output/'annotation-verification.json').write_text(json.dumps(dict(input_vcf_sha256=hashlib.sha256((source/'variants.vcf').read_bytes()).hexdigest(),database_sha256=hashlib.sha256((output/'database/data/toy/snpEffectPredictor.bin').read_bytes()).hexdigest()),indent=2)+'\n')
    elif step=='intervals':
        bedtools=resolve_tool(bedtools);folder=output/'intervals';folder.mkdir(exist_ok=True)
        for src in ['genome.fa','boundaries.bed']:shutil.copy2(source/src,folder/src)
        for kind,name in [('gene','genes.bed'),('exon','exons.bed')]:
            rows=sorted((bed_row(f) for f in features if f['type']==kind),key=lambda r:(r[0],r[1],r[2],r[3]))
            (folder/name).write_text(''.join('\t'.join(map(str,row))+'\n' for row in rows))
        variants=[]
        for line in (source/'variants.vcf').read_text().splitlines():
            if line.startswith('#'):continue
            f=line.split('\t');pos=int(f[1])
            # Local record REF span; not a generic SV/BND affected-base conversion.
            variants.append([f[0],pos-1,pos-1+len(f[3]),f[2],0,'.'])
        (folder/'variants.bed').write_text(''.join('\t'.join(map(str,row))+'\n' for row in variants))
        version=run([bedtools,'--version'],folder).stdout.strip()
        run([bedtools,'intersect','-a','variants.bed','-b','genes.bed','-wa','-wb'],folder,'gene-overlaps.tsv')
        run([bedtools,'intersect','-a','variants.bed','-b','exons.bed','-wa','-wb'],folder,'exon-overlaps.tsv')
        run([bedtools,'intersect','-a','boundaries.bed','-b','genes.bed','-wao'],folder,'boundary-overlaps.tsv')
        run([bedtools,'closest','-a','boundaries.bed','-b','genes.bed','-d','-t','all'],folder,'closest.tsv')
        run([bedtools,'getfasta','-fi','genome.fa','-bed','exons.bed','-s','-name'],folder,'exon-sequences.fa')
        load=lambda name:[line.split('\t') for line in (folder/name).read_text().splitlines()]
        genes=load('gene-overlaps.tsv');exons=load('exon-overlaps.tsv');closest=load('closest.tsv')
        summary=dict(bedtools_version=version,vcf_records=len(variants),gene_overlap_pairs=len(genes),gene_overlap_unique_records=len({r[3] for r in genes}),exon_overlap_pairs=len(exons),exon_overlap_unique_records=len({r[3] for r in exons}),tie_window=[dict(gene=r[7],distance=int(r[-1])) for r in closest if r[3]=='tie_window'],
            input_sha256={name:hashlib.sha256((source/name).read_bytes()).hexdigest() for name in ['genome.fa','genes.gff3','variants.vcf','boundaries.bed']})
        (output/'interval-verification.json').write_text(json.dumps(summary,indent=2)+'\n')
    elif step=='report':
        build=json.loads((output/'build-verification.json').read_text())
        intervals=json.loads((output/'interval-verification.json').read_text())
        annotation=json.loads((output/'annotation-verification.json').read_text())
        for record in [build,intervals]:
            for name,expected_hash in record['input_sha256'].items():
                if hashlib.sha256((source/name).read_bytes()).hexdigest()!=expected_hash:
                    raise ValueError(f'Stale stage result: input {name} changed; rerun upstream steps')
        if annotation['input_vcf_sha256']!=hashlib.sha256((source/'variants.vcf').read_bytes()).hexdigest():
            raise ValueError('Stale annotation: variants.vcf changed')
        if annotation['database_sha256']!=hashlib.sha256((output/'database/data/toy/snpEffectPredictor.bin').read_bytes()).hexdigest():
            raise ValueError('Stale annotation: database changed')
        rows=ann_rows(output/'annotation/annotated.vcf')
        expected={'plus_synonymous':'synonymous_variant','plus_missense':'missense_variant','frameshift':'frameshift_variant','splice_donor':'splice_donor_variant','intron':'intron_variant','minus_synonymous':'synonymous_variant','minus_missense':'missense_variant'}
        for record,effect in expected.items():
            assert any(row['record_id']==record and effect in row['effect'].split('&') for row in rows),(record,effect)
        assert any(row['record_id']=='transcript_specific' and row['transcript']=='txPlus1' and 'missense_variant' in row['effect'] for row in rows)
        assert any(row['record_id']=='transcript_specific' and row['transcript']=='txPlus2' and 'intron_variant' in row['effect'] for row in rows)
        high=[row for row in rows if row['impact']=='HIGH']
        assert {r['alt'] for r in high if r['record_id']=='multi'}=={'T'}
        minus=next(row for row in rows if row['record_id']=='minus_missense' and row['transcript']=='txMinus')
        assert minus['ref']=='G' and minus['alt']=='A' and minus['hgvs_c']=='c.5C>T',minus
        assert intervals['gene_overlap_pairs']==9 and intervals['exon_overlap_pairs']==11 and intervals['exon_overlap_unique_records']==7
        assert intervals['tie_window']==[dict(gene='gPlus',distance=120),dict(gene='gMinus',distance=120)]
        summary=dict(scope='Artificial genome and variants; actual local SnpEff database checks and annotation, bedtools intervals; not gene-function validation or a real-organism benchmark',
            build=build,intervals=intervals,
            annotation_rows=len(rows),high_annotation_rows=len(high),high_record_alleles=sorted({r['record_id']+':'+r['alt'] for r in high}),
            impact_annotation_row_counts=dict(Counter(row['impact'] for row in rows)),negative_strand_example=minus,
            transcript_specific=[r for r in rows if r['record_id']=='transcript_specific'],
            input_sha256={name:hashlib.sha256((source/name).read_bytes()).hexdigest() for name in REQUIRED})
        (output/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
        print(json.dumps({key:summary[key] for key in ['annotation_rows','high_record_alleles','intervals','negative_strand_example']},ensure_ascii=False,indent=2))
    else:raise ValueError('Unknown step')
    (output/(step+'.commands.json')).write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--step',choices=['all','build','annotate','intervals','report'],default='all')
    parser.add_argument('--input-dir',type=Path,default=PROJECT/'examples/data/annotation')
    parser.add_argument('--output',type=Path,default=PROJECT/'examples/output/annotation')
    parser.add_argument('--snpeff-jar',default=os.environ.get('SNPEFF_JAR'))
    parser.add_argument('--snpeff-config',default=os.environ.get('SNPEFF_CONFIG'))
    parser.add_argument('--bedtools',default=os.environ.get('BEDTOOLS_BIN','bedtools'))
    parser.add_argument('--java',default=os.environ.get('JAVA_BIN','java'))
    args=parser.parse_args()
    try:
        for step in ['build','annotate','intervals','report'] if args.step=='all' else [args.step]:
            run_step(step,args.input_dir,args.output,args.snpeff_jar,args.bedtools,args.java,args.snpeff_config)
    except subprocess.CalledProcessError as error:parser.exit(1,f'Tool failed (exit {error.returncode}):\n{error.stderr}\n')
    except ValueError as error:parser.exit(1,f'{error}\n')


if __name__=='__main__':main()
