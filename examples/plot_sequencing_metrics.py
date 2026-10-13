#!/usr/bin/env python3
"""Plot coverage definitions using known artificial molecule identities."""
import argparse
import csv
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

PROJECT=Path(__file__).resolve().parents[1]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',type=Path,default=PROJECT/'examples/output/sequencing')
    parser.add_argument('--output',type=Path,default=PROJECT/'examples/output/sequencing/figures')
    args=parser.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    summary=json.loads((args.input/'summary.json').read_text())
    with (args.input/'coverage.tsv').open() as stream:rows=list(csv.DictReader(stream,delimiter='\t'))
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none'})
    fig,axes=plt.subplots(1,2,figsize=(10.5,3.8),constrained_layout=True)
    positions=[int(r['position_0based']) for r in rows]
    for key,label,color in [('raw_read_bases','Raw reads: mean 7.5','#0072b2'),('known_unique_molecule_union','Known unique molecule union: mean 4.8','#d55e00')]:
        axes[0].plot(positions,[int(r[key]) for r in rows],label=label,color=color,lw=1.1)
    axes[0].set(xlabel='Position in artificial 1000-bp interval (0-based)',ylabel='Coverage contribution',title='Copies and overlap change depth, not original molecules')
    axes[0].legend(fontsize=8)
    keys=list(summary['coverage']);labels=['Raw reads','Pair union','Unique reads','Unique union']
    values=[summary['coverage'][k]['breadth_at_least_5'] for k in keys]
    axes[1].bar(labels,values,color=['#0072b2','#56b4e9','#e69f00','#d55e00'])
    for i,value in enumerate(values):axes[1].text(i,value+.015,f'{value:.3f}',ha='center')
    axes[1].set(ylim=(0,1),ylabel='Fraction of positions with depth >= 5',title='Equal mean depth can hide different coverage')
    fig.savefig(args.output/'coverage-definitions.png',dpi=180,bbox_inches='tight',facecolor='white')
    p=args.output/'coverage-definitions.svg';fig.savefig(p,bbox_inches='tight',facecolor='white')
    p.write_text('\n'.join(line.rstrip() for line in p.read_text().splitlines())+'\n')
    plt.close(fig)
    print(args.output/'coverage-definitions.png')


if __name__=='__main__':main()
