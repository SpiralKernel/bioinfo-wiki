#!/usr/bin/env python3
"""Run TRGT only on the pinned PacBio-provided official tiny example."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import urllib.request
import pysam
from variant_calling_demo import fresh_output, sha

PROJECT=Path(__file__).resolve().parents[1]
MANIFEST=PROJECT/'examples/data/variant-detection/trgt-inputs.json'


def run(output,trgt,input_dir=None):
    executable=shutil.which(trgt)
    if not executable:raise ValueError('TRGT not found; set TRGT_BIN or --trgt')
    executable=str(Path(executable).resolve())
    output=fresh_output(output);inputs=output/'inputs';inputs.mkdir()
    manifest=json.loads(MANIFEST.read_text())
    for item in manifest['files']:
        if input_dir is not None:content=(Path(input_dir)/item['name']).read_bytes()
        else:
            with urllib.request.urlopen(item['url'],timeout=60) as response:content=response.read(item['bytes']+1)
        if len(content)!=item['bytes'] or hashlib.sha256(content).hexdigest()!=item['sha256']:
            raise ValueError('Official fixture checksum mismatch: '+item['name'])
        (inputs/item['name']).write_bytes(content)
    command=[executable,'genotype','--genome','inputs/reference.fasta','--reads','inputs/sample.bam',
             '--repeats','inputs/repeat.bed','--output-prefix','calls','--threads','1']
    result=subprocess.run(command,cwd=output,capture_output=True,text=True,check=True)
    (output/'run.log').write_text(result.stdout+result.stderr)
    pysam.tabix_index(str(output/'calls.vcf.gz'),preset='vcf',force=True)
    with pysam.VariantFile(output/'calls.vcf.gz') as handle:
        rows=[]
        for record in handle:
            rows.append(dict(chrom=record.contig,pos=record.pos,trid=record.info.get('TRID'),
                motif=list(record.info.get('MOTIFS') or []),
                samples={name:{key:list(value) if isinstance(value,tuple) else value
                               for key,value in record.samples[name].items()} for name in record.samples}))
    assert len(rows)==1 and rows[0]['trid']=='TR1',rows
    sample=list(rows[0]['samples'].values())[0]
    assert sample['AL']==[33,33] and sample['MC']==['11','11'],sample
    summary=dict(scope='Actual TRGT on fixed PacBio-provided chrA/TR1 example; not human/ONT/real-data performance',
        trgt_version=subprocess.check_output([executable,'--version'],text=True).strip(),
        source_commit=manifest['source_commit'],license=manifest['license'],
        input_sha256={item['name']:sha(inputs/item['name']) for item in manifest['files']},
        catalog=(inputs/'repeat.bed').read_text().strip(),variants=rows,
        checks=dict(official_inputs_SHA_verified=True,one_TR1=True,AL_bp_33_33=True,MC_counts_11_11=True))
    (output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');return summary


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--trgt',default=os.environ.get('TRGT_BIN','trgt'))
    parser.add_argument('--output',type=Path,default=PROJECT/'examples/output/trgt-official')
    parser.add_argument('--input-dir',type=Path,help='Existing pinned official fixture; same SHA checks apply')
    args=parser.parse_args()
    try:result=run(args.output,args.trgt,args.input_dir)
    except (ValueError,subprocess.CalledProcessError) as error:parser.exit(1,str(error)+'\n'+getattr(error,'stderr',''))
    print(json.dumps(result,indent=2))
