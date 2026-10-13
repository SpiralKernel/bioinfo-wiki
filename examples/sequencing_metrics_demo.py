#!/usr/bin/env python3
"""Artificial interval and quality metrics; no wet-lab, alignment or deduplication run."""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import random

PROJECT=Path(__file__).resolve().parents[1]
SEED=20261013


def n50(lengths, reference_length=None):
    lengths=list(lengths)
    if not lengths or any(not isinstance(x,int) or x<=0 for x in lengths):
        raise ValueError('Need positive integer lengths')
    target=sum(lengths) if reference_length is None else reference_length
    if target<=0:raise ValueError('Reference length must be positive')
    cumulative=0
    for length in sorted(lengths,reverse=True):
        cumulative+=length
        if 2*cumulative>=target:return length
    return None


def effective_phred(scores):
    scores=list(scores)
    if not scores or any(not math.isfinite(q) or q<0 for q in scores):
        raise ValueError('Need finite nonnegative Phred scores')
    probability=sum(10**(-q/10) for q in scores)/len(scores)
    if probability<=0:raise ValueError('Probability underflow')
    return -10*math.log10(probability)


def merged_intervals(intervals):
    result=[]
    for start,end in sorted(intervals):
        if start<0 or end<=start:raise ValueError('Need valid half-open intervals')
        if result and start<=result[-1][1]:result[-1]=(result[-1][0],max(result[-1][1],end))
        else:result.append((start,end))
    return result


def coverage(groups, reference_length):
    """Each group contributes at most once per position after interval union."""
    if reference_length<=0:raise ValueError('Reference length must be positive')
    depth=[0]*reference_length
    for intervals in groups:
        for start,end in merged_intervals(intervals):
            if end>reference_length:raise ValueError('Interval exceeds reference')
            for i in range(start,end):depth[i]+=1
    return depth


def depth_summary(depth):
    return dict(mean_depth=sum(depth)/len(depth),
                breadth_at_least_1=sum(x>=1 for x in depth)/len(depth),
                breadth_at_least_5=sum(x>=5 for x in depth)/len(depth),
                uncovered_positions=sum(x==0 for x in depth))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=PROJECT/'examples/output/sequencing')
    args=parser.parse_args();out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
    rng=random.Random(SEED)
    reference_length=1000;fragment_length=120;read_length=75
    starts=[rng.randrange(reference_length-fragment_length+1) for _ in range(40)]
    origins=list(range(40))+list(range(10))
    raw_groups=[];pair_groups=[];unique_groups={};records=[]
    for pair,origin in enumerate(origins):
        start=starts[origin];end=start+fragment_length
        intervals=[(start,start+read_length),(end-read_length,end)]
        raw_groups.extend([[intervals[0]],[intervals[1]]])
        pair_groups.append(intervals);unique_groups[origin]=intervals
        records.append([f'PAIR{pair:04}',f'MOLECULE{origin:03}',start,end])
    depths={'raw_read_bases':coverage(raw_groups,reference_length),
            'per_pair_union':coverage(pair_groups,reference_length),
            'known_unique_molecule_read_bases':coverage([[i] for group in unique_groups.values() for i in group],reference_length),
            'known_unique_molecule_union':coverage(unique_groups.values(),reference_length)}
    assert sum(depths['raw_read_bases'])==50*2*75
    assert sum(depths['per_pair_union'])==50*120
    assert sum(depths['known_unique_molecule_read_bases'])==40*2*75
    assert sum(depths['known_unique_molecule_union'])==40*120
    lengths=[500,100,100,100,100,100]
    summary=dict(seed=SEED,scope='Artificial intervals and known molecule IDs; no reads, aligner, deduplicator, platform or wet-lab run',
        library=dict(reference_bp=reference_length,original_molecules=40,read_pairs=len(origins),reads=len(origins)*2,
                read_bp=read_length,fragment_bp=fragment_length,overlap_bp=2*read_length-fragment_length,
                introduced_extra_copies=10,extra_copies_fraction_of_observed_pairs=10/len(origins)),
        coverage={name:depth_summary(depth) for name,depth in depths.items()},
        quality=dict(example_scores=[20,40],arithmetic_mean_Q=30,
                effective_Q_of_mean_error=effective_phred([20,40]),
                Q30_error_probability=10**(-30/10),expected_errors_per_1000_Q30_bases=1),
        continuity=dict(lengths=lengths,total_bp=sum(lengths),N50=n50(lengths),median_length=100,
                reference_for_NG50_bp=1200,NG50=n50(lengths,1200),NG50_if_reference_3000bp=n50(lengths,3000)))
    with (out/'simulation-truth.tsv').open('w') as stream:
        writer=csv.writer(stream,delimiter='\t');writer.writerow(['pair_id','molecule_simulation_only','start_0based','end_exclusive']);writer.writerows(records)
    with (out/'coverage.tsv').open('w') as stream:
        writer=csv.writer(stream,delimiter='\t');writer.writerow(['position_0based']+list(depths))
        writer.writerows(zip(range(reference_length),*depths.values()))
    summary['file_sha256']={name:hashlib.sha256((out/name).read_bytes()).hexdigest() for name in ['simulation-truth.tsv','coverage.tsv']}
    (out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
    print(json.dumps(summary,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
