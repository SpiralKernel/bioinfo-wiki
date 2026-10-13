#!/usr/bin/env python3
"""Artificial haplotypes and neutral drift; not demographic or selection inference."""
import argparse
import json
import math
from pathlib import Path
import numpy as np

PROJECT=Path(__file__).resolve().parents[1]


def diversity(haplotypes):
    x=np.asarray(haplotypes)
    if x.ndim!=2 or x.shape[0]<2 or x.shape[1]<1 or not np.isin(x,[0,1]).all():
        raise ValueError('Need complete binary haplotypes, n >= 2 and L >= 1')
    n,length=x.shape
    counts=x.sum(axis=0);p=counts/n
    segregating=int(((counts>0)&(counts<n)).sum())
    pi_total=float((2*p*(1-p)*n/(n-1)).sum())
    a1=sum(1/i for i in range(1,n));a2=sum(1/i**2 for i in range(1,n))
    theta=segregating/a1
    b1=(n+1)/(3*(n-1));b2=2*(n*n+n+3)/(9*n*(n-1))
    c1=b1-1/a1;c2=b2-(n+2)/(a1*n)+a2/(a1*a1)
    e1=c1/a1;e2=c2/(a1*a1+a2)
    variance=e1*segregating+e2*segregating*(segregating-1)
    tajima=(pi_total-theta)/math.sqrt(variance) if variance>0 else None
    return dict(haplotypes=n,callable_sites=length,segregating_sites=segregating,
                pi_total=pi_total,pi_per_site=pi_total/length,
                theta_W_total=theta,theta_W_per_site=theta/length,Tajima_D=tajima)


def descriptive_fst(a,b):
    """Equal-population-weight heterozygosity contrast, NOT WC or Hudson estimator."""
    a,b=np.asarray(a,float),np.asarray(b,float)
    if (a.ndim!=2 or b.ndim!=2 or min(a.shape)<1 or min(b.shape)<1
            or a.shape[1]!=b.shape[1] or not np.isin(a,[0,1]).all() or not np.isin(b,[0,1]).all()):
        raise ValueError('Need complete binary matrices with matching site columns')
    pa=a.mean(axis=0);pb=b.mean(axis=0)
    pooled=(pa+pb)/2
    ht=2*pooled*(1-pooled);hs=(2*pa*(1-pa)+2*pb*(1-pb))/2
    denominator=float(ht.sum())
    return dict(estimator='Descriptive equal-population-weight (sum HT - sum HS) / sum HT; no finite-sample correction',
                FST=(float((ht-hs).sum())/denominator if denominator>0 else None),
                sum_HT=float(ht.sum()),sum_HS=float(hs.sum()))


def ld(x,y):
    x,y=np.asarray(x,float),np.asarray(y,float)
    if (x.ndim!=1 or y.ndim!=1 or x.size==0 or x.shape!=y.shape
            or not np.isin(x,[0,1]).all() or not np.isin(y,[0,1]).all()):
        raise ValueError('Need matching nonempty one-dimensional binary haplotypes')
    p,q=float(x.mean()),float(y.mean())
    d=float((x*y).mean()-p*q)
    denominator=p*(1-p)*q*(1-q)
    return dict(p=p,q=q,D=d,r2=d*d/denominator if denominator>0 else None)


def drift(ne,generations=40,replicates=500,seed=20261013):
    rng=np.random.default_rng(seed);p=np.full(replicates,.5);history=[]
    for generation in range(generations+1):
        history.append(dict(generation=generation,mean_frequency=float(p.mean()),
                variance_frequency=float(p.var(ddof=0)),
                theoretical_variance=.25*(1-(1-1/(2*ne))**generation)))
        if generation<generations:p=rng.binomial(2*ne,p)/(2*ne)
    return history


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=PROJECT/'examples/output/population-genetics')
    args=parser.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    x=np.array([[0,0,0,0,0,0,0,0,0,0,0,0],
                [0,1,0,0,1,0,0,0,0,0,0,0],
                [0,0,0,1,0,1,0,0,0,0,0,0],
                [1,1,0,0,0,0,0,0,0,0,0,0],
                [1,1,0,1,1,1,0,0,0,0,0,0],
                [1,0,0,1,0,1,0,0,0,0,0,0],
                [1,1,0,1,1,0,0,0,0,0,0,0],
                [1,1,0,0,0,1,0,0,0,0,0,0]])
    results={str(ne):drift(ne,seed=20261013+ne) for ne in [50,500]}
    summary=dict(seed=20261013,numpy_version=np.__version__,
        scope='Complete artificial phased binary haplotypes; no VCF, ancestry, ROH, selection or demographic software run',
        all=diversity(x),A=diversity(x[:4]),B=diversity(x[4:]),
        descriptive_differentiation=descriptive_fst(x[:4],x[4:]),
        LD_all_first_two_sites=ld(x[:,0],x[:,1]),
        LD_B_first_two_sites=ld(x[4:,0],x[4:,1]),
        drift_model='Neutral diploid Wright-Fisher, fixed Ne, no mutation/migration/selection, p0=0.5; 500 independent simulated populations',
        drift=results)
    (args.output/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
    np.savetxt(args.output/'artificial-haplotypes.tsv',x,fmt='%d',delimiter='\t')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none'})
    fig,axes=plt.subplots(1,2,figsize=(10,3.8),constrained_layout=True)
    for ne,color in [('50','#d55e00'),('500','#0072b2')]:
        history=results[ne]
        axes[0].plot([r['generation'] for r in history],[r['variance_frequency'] for r in history],label=f'Simulation Ne={ne}',color=color)
        axes[0].plot([r['generation'] for r in history],[r['theoretical_variance'] for r in history],ls='--',color=color,alpha=.6)
    axes[0].set(xlabel='Generation',ylabel='Variance across simulated populations',title='Neutral drift: dashed lines are model expectations')
    axes[0].legend(fontsize=8)
    groups=['A','B','all'];offset=np.arange(3)
    axes[1].bar(offset-.17,[summary[g]['pi_per_site'] for g in groups],width=.34,label='Pairwise diversity pi')
    axes[1].bar(offset+.17,[summary[g]['theta_W_per_site'] for g in groups],width=.34,label='Watterson theta')
    axes[1].set(xticks=offset,xticklabels=groups,ylabel='Per callable artificial site',title='Pooling structured groups changes summaries')
    axes[1].legend(fontsize=8)
    fig.savefig(args.output/'diversity-and-drift.png',dpi=180,bbox_inches='tight',facecolor='white')
    p=args.output/'diversity-and-drift.svg';fig.savefig(p,bbox_inches='tight',facecolor='white')
    p.write_text('\n'.join(line.rstrip() for line in p.read_text().splitlines())+'\n')
    print(json.dumps({k:v for k,v in summary.items() if k!='drift'},ensure_ascii=False,indent=2))
    print('drift_final',json.dumps({k:v[-1] for k,v in results.items()}))


if __name__=='__main__':main()
