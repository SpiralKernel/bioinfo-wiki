#!/usr/bin/env python3
"""Generate independent synthetic diploid genotypes and a quantitative trait."""
import argparse
import csv
from pathlib import Path
import random


def generate(output, samples=120, variants=600):
    output.mkdir(parents=True, exist_ok=True)
    rng = random.Random(20261013)
    identifiers = [f'S{i:03}' for i in range(samples)]
    genotype = []
    for v in range(variants):
        frequency = rng.uniform(0.2, 0.8)
        genotype.append([int(rng.random() < frequency) + int(rng.random() < frequency)
                         for _ in identifiers])
    with (output/'toy.vcf').open('w') as stream:
        stream.write('##fileformat=VCFv4.2\n##contig=<ID=1,length=1000000>\n')
        stream.write('##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">\n')
        stream.write('\t'.join(['#CHROM','POS','ID','REF','ALT','QUAL','FILTER','INFO','FORMAT'] + identifiers)+'\n')
        for v, row in enumerate(genotype):
            fields=['1',str((v+1)*1000),f'v{v+1}','A','G','.','PASS','.','GT']
            fields += [('0/0','0/1','1/1')[g] for g in row]
            stream.write('\t'.join(fields)+'\n')
    with (output/'phenotype.tsv').open('w') as stream:
        writer=csv.writer(stream, delimiter='\t')
        writer.writerow(['#FID','IID','trait'])
        for i, identifier in enumerate(identifiers):
            value=2.0*genotype[0][i]+rng.gauss(0,1)
            writer.writerow(['0',identifier,f'{value:.6f}'])
    print(f'Generated {samples} samples, {variants} variants; v1 affects the simulated trait.')

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,default=Path(__file__).parent/'output/population')
    args=parser.parse_args()
    generate(args.output)
