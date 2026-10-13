#!/usr/bin/env python3
"""Plot the artificial GS validation example; no real individual records."""
import argparse
import csv
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

PROJECT=Path(__file__).resolve().parents[1]

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',type=Path,default=PROJECT/'examples/output/gs')
    parser.add_argument('--output',type=Path,default=PROJECT/'examples/output/gs/figures')
    args=parser.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    summary=json.loads((args.input/'summary.json').read_text())
    with (args.input/'predictions.tsv').open() as f:rows=list(csv.DictReader(f,delimiter='\t'))
    with (args.input/'candidate-predictions.tsv').open() as f:candidates=list(csv.DictReader(f,delimiter='\t'))
    plt.rcParams.update({'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none'})
    fig,axes=plt.subplots(2,2,figsize=(11,7.5),constrained_layout=True)
    colors={'random':'#0072b2','family':'#d55e00'}
    labels={'random':'Random individuals','family':'Held-out families'}
    for index,mode in enumerate(['random','family']):
        folds=summary['validation'][mode]['outer_folds']
        for ax,key in [(axes[0,0],'corr_observed_y'),(axes[0,1],'corr_true_g_simulation_only')]:
            values=[fold[key] for fold in folds]
            ax.scatter(np.full(len(values),index)+np.linspace(-.07,.07,len(values)),values,color=colors[mode],s=45,alpha=.8)
            ax.plot([index-.2,index+.2],[np.mean(values)]*2,color=colors[mode],linewidth=3)
    for ax in axes[0,:]:
        ax.axhline(0,color='#888888',linestyle='--',linewidth=1)
        ax.set(xticks=[0,1],xticklabels=list(labels.values()),ylim=(-.45,1.0),ylabel='Outer-fold Pearson correlation')
    axes[0,0].set_title('Predictive ability: observed phenotype')
    axes[0,1].set_title('Accuracy: true breeding value known in simulation')
    observed=[float(row['observed_y']) for row in rows]
    predicted=[float(row['prediction_family']) for row in rows]
    axes[1,0].scatter(predicted,observed,s=16,alpha=.5,color=colors['family'])
    axes[1,0].set(title='Family-held-out predictions have weak transfer here',xlabel='Out-of-fold predicted phenotype',ylabel='Observed phenotype')
    axes[1,1].hist([float(row['GEBV_training_reference']) for row in candidates],bins=15,color='#009e73',edgecolor='white')
    axes[1,1].set(title='60 unphenotyped artificial candidates',xlabel='Predicted GEBV relative to training reference',ylabel='Candidates')
    fig.savefig(args.output/'validation-and-candidates.png',dpi=180,bbox_inches='tight',facecolor='white')
    path=args.output/'validation-and-candidates.svg';fig.savefig(path,bbox_inches='tight',facecolor='white')
    path.write_text('\n'.join(line.rstrip() for line in path.read_text().splitlines())+'\n')
    print(args.output/'validation-and-candidates.png')

if __name__=='__main__':main()
