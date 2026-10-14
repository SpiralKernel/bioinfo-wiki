#!/usr/bin/env python3
"""Plot record counts from the actual artificial bcftools extraction results."""
import argparse
import json
from pathlib import Path


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=Path(__file__).resolve().parent/'output/variants')
    args=parser.parse_args()
    counts=json.loads((args.output/'summary.json').read_text())['counts']
    labels=['SNV','Small indel','MNV','SV DEL','INV','DUP','BND','CNV','STR','TE insertion']
    keys=['snps','indels','mnps','symbolic_del','inv','dup','bnd','cnv','str','te']
    values=[counts[k] for k in keys]
    assert sum(values)==17
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none'})
    fig,ax=plt.subplots(figsize=(10,4),constrained_layout=True)
    bars=ax.bar(labels,values,color=['#0072b2']*3+['#d55e00']*7)
    ax.bar_label(bars,padding=3)
    ax.set(ylabel='VCF records',ylim=(0,6),title='Artificial normalized VCF: 17 records; the BND pair represents one event')
    ax.tick_params(axis='x',labelrotation=30)
    fig.savefig(args.output/'variant-records.png',dpi=180,facecolor='white')
    path=args.output/'variant-records.svg';fig.savefig(path,facecolor='white')
    path.write_text('\n'.join(line.rstrip() for line in path.read_text().splitlines())+'\n')
    plt.close(fig)


if __name__=='__main__':main()
