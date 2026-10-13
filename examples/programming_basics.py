#!/usr/bin/env python3
"""Read, validate, join and summarize two artificial teaching tables by sample ID."""
import argparse
import csv
import json
import math
from pathlib import Path
import statistics
import sys

PROJECT=Path(__file__).resolve().parents[1]


def read_unique(path,columns):
    with Path(path).open(newline='',encoding='utf-8') as stream:
        reader=csv.DictReader(stream)
        if not set(columns)<=set(reader.fieldnames or []):raise ValueError(f'Missing required columns: {path}')
        rows=list(reader)
    identifiers=[row['sample_id'] for row in rows]
    if any(not value for value in identifiers) or len(set(identifiers))!=len(identifiers):
        raise ValueError(f'Empty or duplicate sample ID: {path}')
    return rows


def join_and_summarize(measurements,metadata):
    measured=[row['sample_id'] for row in measurements];indexed={row['sample_id']:row for row in metadata}
    if len(set(measured))!=len(measured) or len(indexed)!=len(metadata):raise ValueError('Duplicate sample ID')
    if set(measured)!=set(indexed):raise ValueError('Sample ID sets do not match')
    joined=[]
    for row in measurements:
        text=row['value'];value=None if text in {'','NA'} else float(text)
        if value is not None and not math.isfinite(value):
            raise ValueError(f"Non-finite value for sample {row['sample_id']}; use NA for missing values")
        joined.append(dict(sample_id=row['sample_id'],value=value,
                           condition=indexed[row['sample_id']]['condition'],batch=indexed[row['sample_id']]['batch']))
    groups={}
    for condition in sorted({row['condition'] for row in joined}):
        values=[row['value'] for row in joined if row['condition']==condition and row['value'] is not None]
        groups[condition]=dict(n=len(values),mean=statistics.mean(values) if values else None)
    return joined,dict(rows=len(joined),missing=sum(row['value'] is None for row in joined),groups=groups)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=PROJECT/'examples/output/programming/python')
    parser.add_argument('--plot',action='store_true')
    args=parser.parse_args()
    measurements=read_unique(PROJECT/'examples/data/programming_measurements.csv',['sample_id','value'])
    metadata=read_unique(PROJECT/'examples/data/programming_metadata.csv',['sample_id','condition','batch'])
    joined,summary=join_and_summarize(measurements,metadata)
    summary['python_version']=sys.version.split()[0]
    summary['scope']='Eight artificial samples; descriptive learning example, no biological inference'
    args.output.mkdir(parents=True,exist_ok=True)
    with (args.output/'joined.csv').open('w',newline='',encoding='utf-8') as stream:
        writer=csv.DictWriter(stream,fieldnames=['sample_id','value','condition','batch']);writer.writeheader()
        writer.writerows({**row,'value':'NA' if row['value'] is None else row['value']} for row in joined)
    (args.output/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
    if args.plot:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        fig,ax=plt.subplots(figsize=(5,3.5),constrained_layout=True)
        for i,condition in enumerate(summary['groups']):
            values=[row['value'] for row in joined if row['condition']==condition and row['value'] is not None]
            ax.scatter([i]*len(values),values,label=condition)
        ax.set(xticks=[0,1],xticklabels=['A','B'],xlabel='Artificial condition',ylabel='Artificial value',title='Seven observed values; one missing sample retained')
        fig.savefig(args.output/'values.png',dpi=160,facecolor='white');plt.close(fig)
    print(json.dumps(summary,ensure_ascii=False,allow_nan=False))


if __name__=='__main__':main()
