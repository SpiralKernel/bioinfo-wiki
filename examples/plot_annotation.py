#!/usr/bin/env python3
"""Plot the fixed artificial gene model and actual annotation-row counts."""
import argparse
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from annotation_demo import read_fasta,read_gff

ROOT=Path(__file__).resolve().parents[1]
def main(summary_path,output):
    summary=json.loads(summary_path.read_text())
    features=read_gff(ROOT/'examples/data/annotation/genes.gff3',read_fasta(ROOT/'examples/data/annotation/genome.fa'))
    output.mkdir(parents=True,exist_ok=True)
    fig,(ax,bars)=plt.subplots(2,1,figsize=(10,6),gridspec_kw={'height_ratios':[2,1.2]},layout='constrained')
    for y,tx in [(3,'txPlus1'),(2,'txPlus2'),(1,'txMinus')]:
        parts=[f for f in features if f['type']=='CDS' and f['attrs']['Parent']==tx]
        lo=min(f['start'] for f in parts);hi=max(f['end'] for f in parts)
        ax.plot([lo,hi],[y,y],color='#536471',lw=1.5)
        for f in parts:ax.add_patch(Rectangle((f['start'],y-.13),f['end']-f['start']+1,.26,color='#187ca8' if f['strand']=='+' else '#d87530'))
        a,b=(lo,hi) if parts[0]['strand']=='+' else (hi,lo)
        ax.annotate('',xy=(b,y+.27),xytext=(a,y+.27),arrowprops={'arrowstyle':'->','color':'#536471'})
    for pos,label in [(325,'325: transcript-dependent'),(996,'996: G>A / c.5C>T')]:
        ax.axvline(pos,color='#a63254',ls='--',lw=1);ax.text(pos,3.65,label,ha='center',fontsize=9,color='#a63254')
    ax.set(yticks=[1,2,3],yticklabels=['txMinus (-)','txPlus2 (+)','txPlus1 (+)'],xlim=(50,1070),ylim=(.5,4),xlabel='chrToy coordinate (1-based, inclusive CDS)',title='Artificial gene models: 2 genes, 3 coding transcripts')
    ax.spines[['top','right','left']].set_visible(False)
    counts=summary['impact_annotation_row_counts'];labels=['HIGH','MODERATE','LOW','MODIFIER'];values=[counts[k] for k in labels]
    bars.bar(labels,values,color=['#a63254','#d87530','#187ca8','#6c7a89'],width=.6)
    for i,v in enumerate(values):bars.text(i,v+.1,str(v),ha='center')
    bars.set(ylim=(0,max(values)+1.5),ylabel='Annotation rows',title='12 VCF records / 13 ALT alleles -> 21 annotation rows')
    bars.spines[['top','right']].set_visible(False)
    fig.savefig(output/'gene-models.png',dpi=180);fig.savefig(output/'gene-models.svg');plt.close(fig)
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--summary',type=Path,default=ROOT/'examples/output/annotation/summary.json')
    p.add_argument('--output',type=Path,default=ROOT/'examples/output/annotation-plots')
    args=p.parse_args();main(args.summary,args.output)
