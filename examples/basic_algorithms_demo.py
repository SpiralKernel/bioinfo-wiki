#!/usr/bin/env python3
"""Transparent toy implementations of search, counting, graphs, alignment, clustering and optimization."""
import argparse
from collections import Counter, deque
import json
from pathlib import Path
import numpy as np

PROJECT=Path(__file__).resolve().parents[1]


def lower_bound(values, target):
    """First index with value >= target in an already sorted sequence."""
    lo,hi=0,len(values)
    while lo<hi:
        mid=(lo+hi)//2
        if values[mid]<target:lo=mid+1
        else:hi=mid
    return lo


def kmer_counts(sequence, k):
    if k<=0:raise ValueError('k must be positive')
    return Counter(sequence[i:i+k] for i in range(max(0,len(sequence)-k+1)))


def bfs_distances(graph, start):
    distance={start:0};pending=deque([start])
    while pending:
        node=pending.popleft()
        for neighbor in graph.get(node,[]):
            if neighbor not in distance:
                distance[neighbor]=distance[node]+1;pending.append(neighbor)
    return distance


def global_alignment(a,b,match=2,mismatch=-1,gap=-2):
    """Needleman-Wunsch with linear gap costs; no affine gaps or local resets."""
    score=np.zeros((len(a)+1,len(b)+1),dtype=int)
    score[:,0]=np.arange(len(a)+1)*gap
    score[0,:]=np.arange(len(b)+1)*gap
    for i in range(1,len(a)+1):
        for j in range(1,len(b)+1):
            score[i,j]=max(score[i-1,j-1]+(match if a[i-1]==b[j-1] else mismatch),
                           score[i-1,j]+gap,score[i,j-1]+gap)
    i,j=len(a),len(b);left=[];right=[]
    while i or j:
        if i and j and score[i,j]==score[i-1,j-1]+(match if a[i-1]==b[j-1] else mismatch):
            left.append(a[i-1]);right.append(b[j-1]);i-=1;j-=1
        elif i and score[i,j]==score[i-1,j]+gap:
            left.append(a[i-1]);right.append('-');i-=1
        else:
            left.append('-');right.append(b[j-1]);j-=1
    return int(score[-1,-1]),''.join(reversed(left)),''.join(reversed(right))


def kmeans(points,k,seed=20261013,max_iter=100):
    points=np.asarray(points,float)
    if points.ndim!=2 or not np.isfinite(points).all() or not 1<=k<=len(points):
        raise ValueError('Need finite n by p points and 1 <= k <= n')
    centers=points[np.random.default_rng(seed).choice(len(points),k,replace=False)].copy()
    objective=[]
    for iteration in range(max_iter):
        labels=np.argmin(((points[:,None,:]-centers[None,:,:])**2).sum(axis=2),axis=1)
        updated=centers.copy()
        for label in range(k):
            if (labels==label).any():updated[label]=points[labels==label].mean(axis=0)
        objective.append(float(((points-updated[labels])**2).sum()))
        converged=np.allclose(updated,centers,rtol=0,atol=1e-12)
        centers=updated
        if converged:break
    labels=np.argmin(((points[:,None,:]-centers[None,:,:])**2).sum(axis=2),axis=1)
    objective.append(float(((points-centers[labels])**2).sum()))
    return centers,labels,objective


def gradient_least_squares(x,y,max_iter=10000,tolerance=1e-10):
    x,y=np.asarray(x,float),np.asarray(y,float)
    lipschitz=np.linalg.norm(x,2)**2/len(y)
    if lipschitz<=0:raise ValueError('No usable design')
    step=1/lipschitz
    coefficients=np.zeros(x.shape[1]);loss=[]
    for iteration in range(max_iter):
        residual=x@coefficients-y
        loss.append(float(residual@residual/(2*len(y))))
        gradient=x.T@residual/len(y)
        if np.linalg.norm(gradient)<tolerance:break
        coefficients-=step*gradient
    return coefficients,loss,step


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=PROJECT/'examples/output/basic-algorithms')
    args=parser.parse_args();out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
    rng=np.random.default_rng(20261013)
    raw=rng.normal(size=(120,2));raw[:,1]=.8*raw[:,0]+.4*raw[:,1]
    means,scales=raw.mean(axis=0),raw.std(axis=0)
    standardized=(raw-means)/scales
    x=np.column_stack([np.ones(len(raw)),standardized])
    y=1+2*standardized[:,0]-.7*standardized[:,1]+rng.normal(0,.2,len(raw))
    coefficients,loss,step=gradient_least_squares(x,y)
    reference=np.linalg.lstsq(x,y,rcond=None)[0]
    np.testing.assert_allclose(coefficients,reference,atol=1e-8,rtol=0)
    points=np.vstack([rng.normal([-2,-1],.5,(50,2)),rng.normal([2,1],.5,(50,2))])
    centers,labels,inertia=kmeans(points,2)
    if (np.diff(inertia)>1e-9).any():raise ValueError('K-means objective increased')
    alignment=global_alignment('ACGT','AGT')
    graph={'reads':['QC'],'QC':['alignment'],'alignment':['counts'],'counts':['differential'],'differential':[],'isolated':[]}
    summary=dict(seed=20261013,numpy_version=np.__version__,scope='Artificial toy implementations, not production tools',
        search=dict(sorted_values=[1,3,3,8],target=3,first_index=lower_bound([1,3,3,8],3),index_base=0),
        overlapping_kmers=dict(sequence='ATATAT',k=2,counts=dict(kmer_counts('ATATAT',2))),
        graph=dict(unweighted_distances=bfs_distances(graph,'reads'),unreachable=['isolated']),
        global_alignment=dict(a='ACGT',b='AGT',match=2,mismatch=-1,gap=-2,score=alignment[0],alignment=list(alignment[1:])),
        kmeans=dict(individuals=100,k=2,cluster_sizes=np.bincount(labels,minlength=2).tolist(),
                    centers=centers.tolist(),SSE=inertia[-1],objective_history=inertia),
        gradient_descent=dict(observations=120,columns=3,loss_definition='mean squared residual / 2',
                    iterations=len(loss),step=step,coefficients=coefficients.tolist(),
                    reference_lstsq=reference.tolist(),max_abs_coefficient_error=float(abs(coefficients-reference).max()),
                    initial_loss=loss[0],final_loss=loss[-1]))
    (out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none'})
    fig,axes=plt.subplots(1,3,figsize=(12,3.5),constrained_layout=True)
    axes[0].scatter(points[:,0],points[:,1],c=labels,cmap='viridis',s=20)
    axes[0].scatter(centers[:,0],centers[:,1],marker='x',c='red',s=100)
    axes[0].set(title='K-means on 100 artificial points',xlabel='Feature 1',ylabel='Feature 2')
    axes[1].plot(np.arange(len(inertia)),inertia,marker='o',color='#0072b2')
    axes[1].set(title='Lloyd updates reduce within-cluster SSE',xlabel='Update',ylabel='Sum of squared distances')
    axes[2].semilogy(np.arange(len(loss)),np.maximum(np.asarray(loss)-loss[-1],1e-16),color='#d55e00')
    axes[2].set(title='Gradient descent toward least squares',xlabel='Iteration',ylabel='Loss minus final loss (floor 1e-16)')
    fig.savefig(out/'clustering-and-optimization.png',dpi=180,bbox_inches='tight',facecolor='white')
    svg=out/'clustering-and-optimization.svg';fig.savefig(svg,bbox_inches='tight',facecolor='white')
    svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines())+'\n');plt.close(fig)
    print(json.dumps(summary,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
