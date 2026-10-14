#!/usr/bin/env python3
"""Format already assessed artificial PAV evidence; does not discover PAVs."""
import argparse
import csv
import json
from pathlib import Path

PROJECT=Path(__file__).resolve().parents[1]


def build_matrix(rows):
    states={'present':'1','absent':'0','unknown':'NA'}
    indexed={}
    for row in rows:
        if not row['locus_id'] or not row['sample_id'] or row['status'] not in states:
            raise ValueError('Need locus ID, sample ID and present/absent/unknown status')
        key=(row['locus_id'],row['sample_id'])
        if key in indexed:raise ValueError('Duplicate locus/sample evidence')
        indexed[key]=states[row['status']]
    loci=sorted({key[0] for key in indexed});samples=sorted({key[1] for key in indexed})
    return samples,[{'locus_id':locus,**{sample:indexed.get((locus,sample),'NA') for sample in samples}} for locus in loci]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',type=Path,default=PROJECT/'examples/data/variants/pav_evidence.tsv')
    parser.add_argument('--output',type=Path,default=PROJECT/'examples/output/pav-matrix')
    args=parser.parse_args()
    source=args.input.resolve();output=args.output.resolve()
    if source==output/'matrix.tsv' or source==output/'summary.json':raise ValueError('Input would be overwritten')
    with source.open(newline='') as stream:rows=list(csv.DictReader(stream,delimiter='\t'))
    samples,matrix=build_matrix(rows);output.mkdir(parents=True,exist_ok=True)
    with (output/'matrix.tsv').open('w',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=['locus_id',*samples],delimiter='\t',lineterminator='\n');writer.writeheader();writer.writerows(matrix)
    counts={value:sum(row[sample]==value for row in matrix for sample in samples) for value in ['1','0','NA']}
    summary=dict(scope='Already assessed artificial evidence only; formatting, not genomic PAV discovery',loci=len(matrix),samples=samples,cells=counts)
    (output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary))


if __name__=='__main__':main()
