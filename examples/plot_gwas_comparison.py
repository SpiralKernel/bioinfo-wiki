#!/usr/bin/env python3
"""Normalize this demo's outputs and plot auditable scientific comparisons."""
import argparse
import csv
import json
import math
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]


def read_table(path):
    lines = path.read_text().splitlines()
    if not lines:
        raise ValueError(f'Empty result: {path}')
    header = lines[0].split()
    rows = []
    for line in lines[1:]:
        values = line.split()
        if len(values) != len(header):
            raise ValueError(f'Incorrect column count in {path}')
        rows.append(dict(zip(header, values)))
    return rows


def normalize(path, schema, sample_count):
    fields = {
        'plink': ('ID', '#CHROM', 'POS', 'A1', 'OMITTED', 'A1_FREQ', 'BETA', 'SE', 'P', 'OBS_CT'),
        'gemma': ('rs', 'chr', 'ps', 'allele1', 'allele0', 'af', 'beta', 'se', 'p_wald', 'n_obs'),
        'gcta': ('SNP', 'Chr', 'bp', 'A1', 'A2', 'Freq', 'b', 'se', 'p', None),
        'fastgwa': ('SNP', 'CHR', 'POS', 'A1', 'A2', 'AF1', 'BETA', 'SE', 'P', 'N'),
        'regenie': ('ID', 'CHROM', 'GENPOS', 'ALLELE1', 'ALLELE0', 'A1FREQ', 'BETA', 'SE', 'LOG10P', 'N'),
    }[schema]
    result = {}
    for row in read_table(path):
        if schema in {'plink', 'regenie'} and row['TEST'] != 'ADD':
            continue
        if schema == 'plink' and row['ERRCODE'] != '.':
            raise ValueError(f'PLINK failure at {row["ID"]}: {row["ERRCODE"]}')
        identifier, chromosome, position, effect, other, freq, beta, se, pvalue, n = fields
        p = float(row[pvalue])
        if schema == 'regenie':
            logp = p
        else:
            if not 0 < p <= 1:
                raise ValueError('This demo requires finite nonzero P; inspect underflow/failed records separately')
            logp = -math.log10(p)
        record = {'ID': row[identifier], 'CHR': row[chromosome], 'POS': int(row[position]),
                  'EA': row[effect], 'OA': row[other], 'EAF': float(row[freq]),
                  'BETA': float(row[beta]), 'SE': float(row[se]), 'NEG_LOG10_P': logp,
                  'N': int(row[n]) if n and n in row else sample_count}
        if (not all(math.isfinite(record[key]) for key in ('EAF', 'BETA', 'SE', 'NEG_LOG10_P')) or
                record['SE'] <= 0 or not 0 <= record['EAF'] <= 1 or record['NEG_LOG10_P'] < 0):
            raise ValueError(f'Invalid numerical result at {record["ID"]}')
        # This demo has no missing genotypes after QC. Do not infer arbitrary GEMMA N this way.
        missing = row.get('n_miss', row.get('n_mis', '0'))
        if schema == 'gemma' and int(missing) != 0:
            raise ValueError('Demo assumption violated: inspect GEMMA missingness and effective N explicitly')
        if record['ID'] in result:
            raise ValueError(f'Duplicate variant ID: {record["ID"]}')
        result[record['ID']] = record
    return result


def harmonize(reference, records):
    if set(reference) != set(records):
        raise ValueError('Variant sets differ; compare exclusions before harmonizing')
    result = {}
    flipped = 0
    for identifier, row in records.items():
        baseline = reference[identifier]
        if (row['CHR'], row['POS'], row['N']) != (baseline['CHR'], baseline['POS'], baseline['N']):
            raise ValueError(f'Coordinate or sample count differs: {identifier}')
        alleles = (row['EA'], row['OA'])
        wanted = (baseline['EA'], baseline['OA'])
        updated = dict(row)
        if alleles == wanted:
            pass
        elif alleles == wanted[::-1]:
            updated.update(EA=wanted[0], OA=wanted[1], BETA=-row['BETA'], EAF=1-row['EAF'])
            flipped += 1
        else:
            raise ValueError(f'Alleles incompatible: {identifier}; no automatic strand or assembly conversion')
        result[identifier] = updated
    return result, flipped


def load_results(directory):
    metadata = json.loads((directory/'run-metadata.json').read_text())
    completed = set(metadata['completed_tasks'])
    specifications = [
        ('PLINK no PC', 'plink-unadjusted', 'results/plink_unadjusted.PHENO1.glm.linear', 'plink'),
        ('PLINK PC3', 'plink-pc3', 'results/plink_pc3.PHENO1.glm.linear', 'plink'),
        ('GEMMA LM', 'gemma-lm', 'gemma/lm_pc3.assoc.txt', 'gemma'),
        ('GEMMA LMM', 'gemma-lmm', 'gemma/lmm_pc3.assoc.txt', 'gemma'),
        ('GCTA MLMA', 'gcta-mlma', 'gcta/mlma_pc3.mlma', 'gcta'),
        ('GCTA fastGWA', 'gcta-fastgwa', 'gcta/fastgwa_pc3.fastGWA', 'fastgwa'),
        ('REGENIE', 'regenie-step2', 'regenie/step2_CD8.regenie', 'regenie'),
    ]
    parsed = {label: normalize(directory/filename, schema, metadata['qc_samples'])
              for label, task, filename, schema in specifications if task in completed}
    reference = parsed['PLINK PC3']
    harmonized, flipped = {}, {}
    for label, rows in parsed.items():
        harmonized[label], flipped[label] = harmonize(reference, rows)
    return metadata, harmonized, flipped


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=PROJECT/'examples/output/gwas-real')
    parser.add_argument('--figures', type=Path, default=PROJECT/'examples/output/gwas-real/figures')
    args = parser.parse_args()
    import numpy as np
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from scipy.stats import chi2
    plt.rcParams.update({'font.size': 11, 'axes.spines.top': False, 'axes.spines.right': False,
                         'svg.fonttype': 'none', 'savefig.facecolor': 'white'})
    directory, figures = args.input.resolve(), args.figures.resolve()
    figures.mkdir(parents=True, exist_ok=True)
    metadata, results, flipped = load_results(directory)
    reference = results['PLINK PC3']
    ids = sorted(reference, key=lambda key: (int(reference[key]['CHR']), reference[key]['POS'], key))
    threshold = -math.log10(0.05/len(ids))
    summary = {'samples': metadata['qc_samples'], 'variants': len(ids), 'LD_pruned_variants': metadata['pca_variants'],
               'bonferroni_threshold': 0.05/len(ids), 'methods': {}}
    for label, rows in results.items():
        logp = np.array([rows[key]['NEG_LOG10_P'] for key in ids])
        p = np.power(10.0, -logp)
        if np.any(p == 0):
            raise ValueError('P underflow: update diagnostic calculation before using these results')
        summary['methods'][label] = {
            'variants': len(rows), 'lambda_GC_1df': float(np.median(chi2.isf(p, 1))/chi2.ppf(.5, 1)),
            'bonferroni_hits': int(np.sum(logp >= threshold)), 'allele_flips_to_PLINK_PC3': flipped[label],
            'top_variant': max(rows.values(), key=lambda row: row['NEG_LOG10_P'])}
    a, b = results['PLINK PC3'], results['GEMMA LM']
    summary['matched_LM_check'] = {
        'max_abs_beta_difference': max(abs(a[key]['BETA']-b[key]['BETA']) for key in ids),
        'max_abs_neg_log10_p_difference': max(abs(a[key]['NEG_LOG10_P']-b[key]['NEG_LOG10_P']) for key in ids)}
    if (summary['matched_LM_check']['max_abs_beta_difference'] > 1e-5 or
            summary['matched_LM_check']['max_abs_neg_log10_p_difference'] > 1e-4):
        raise ValueError('Matched ordinary-LM results differ more than printed precision predicts; inspect inputs')
    with (directory/'harmonized-results.tsv').open('w') as stream:
        writer = csv.DictWriter(stream, delimiter='\t', fieldnames=['METHOD']+list(reference[ids[0]]))
        writer.writeheader()
        for label, rows in results.items():
            for key in ids:
                writer.writerow({'METHOD': label, **rows[key]})

    def save(fig, name):
        fig.savefig(figures/(name+'.png'), dpi=180, bbox_inches='tight')
        svg_path = figures/(name+'.svg')
        fig.savefig(svg_path, bbox_inches='tight')
        svg_path.write_text('\n'.join(line.rstrip() for line in svg_path.read_text().splitlines())+'\n')
        plt.close(fig)

    fig, axes = plt.subplots(2, 2, figsize=(11.5, 7.5), constrained_layout=True)
    axes[0, 0].bar(['All records', 'CD8 available', 'After QC'],
                   [metadata['raw_samples'], metadata['complete_CD8_samples'], metadata['qc_samples']], color=['#a0a7ad','#4488bb','#206095'])
    axes[0, 0].set(title='Individuals entering the demo', ylabel='Individuals')
    axes[0, 1].bar(['Source', 'Association QC', 'PCA pruned'],
                   [metadata['raw_variants'], metadata['qc_variants'], metadata['pca_variants']], color=['#a0a7ad','#4488bb','#dd8822'])
    axes[0, 1].set(title='Variant sets have different purposes', ylabel='Variants')
    axes[1, 0].hist([min(row['EAF'], 1-row['EAF']) for row in reference.values()], bins=25, color='#4488bb', edgecolor='white')
    axes[1, 0].set(title='After-QC minor allele frequencies', xlabel='MAF', ylabel='Variants')
    eigen = read_table(directory/'prepared/pca.eigenvec')
    fam = [line.split() for line in (directory/'prepared/qc.fam').read_text().splitlines()]
    family = {tuple(row[:2]): row[0] for row in fam}
    from collections import Counter
    counts = Counter(family.values())
    highlighted = [key for key, _ in counts.most_common(4)]
    colors = ['#0072b2', '#d55e00', '#009e73', '#cc79a7']
    ax = axes[1, 1]
    for i, key in enumerate([None]+highlighted):
        subset = [row for row in eigen if (family[(row['#FID'], row['IID'])] not in highlighted if key is None else family[(row['#FID'], row['IID'])] == key)]
        ax.scatter([float(row['PC1']) for row in subset], [float(row['PC2']) for row in subset], s=13,
                   alpha=.45 if key is None else .8, color='#b9bfc4' if key is None else colors[i-1],
                   label='Other families' if key is None else f'Family group {i}')
    ax.set(title='PCA; four largest recorded families highlighted', xlabel='PC1 coordinate', ylabel='PC2 coordinate')
    ax.legend(fontsize=8, frameon=False, loc='best')
    save(fig, 'data-and-pca')

    offsets, ticks, labels = {}, [], []
    running = 0
    for chromosome in range(1, 20):
        positions = [row['POS'] for row in reference.values() if row['CHR'] == str(chromosome)]
        if not positions:
            continue
        offsets[str(chromosome)] = running
        ticks.append(running+max(positions)/2)
        labels.append(str(chromosome))
        running += max(positions)+10_000_000
    selected = ['PLINK PC3', 'GEMMA LMM'] + (['REGENIE'] if 'REGENIE' in results else [])
    fig, axes = plt.subplots(len(selected), 1, figsize=(12, 3.0*len(selected)), sharex=True, sharey=True, constrained_layout=True)
    for ax, label in zip(np.atleast_1d(axes), selected):
        for chromosome in range(1, 20):
            subset = [row for row in results[label].values() if row['CHR'] == str(chromosome)]
            ax.scatter([row['POS']+offsets[str(chromosome)] for row in subset], [row['NEG_LOG10_P'] for row in subset],
                       s=8, color='#1f77b4' if chromosome % 2 else '#79b4d2', rasterized=True)
        ax.axhline(threshold, linestyle='--', color='#bb5533', linewidth=1)
        ax.set(title=label, ylabel='-log10(P)')
    axes[-1].set(xticks=ticks, xticklabels=labels, xlabel='Source chromosome; original coordinates')
    save(fig, 'manhattan-models')

    fig, axes = plt.subplots(1, 2, figsize=(12, 5.4), constrained_layout=True)
    palette = ['#999999','#e69f00','#cc79a7','#0072b2','#009e73','#56b4e9','#d55e00']
    for color, (label, rows) in zip(palette, results.items()):
        values = np.sort([row['NEG_LOG10_P'] for row in rows.values()])[::-1]
        expected = -np.log10((np.arange(len(values))+.5)/len(values))
        axes[0].plot(expected, values, linewidth=1.3, color=color,
                     label=f'{label}: lambda={summary["methods"][label]["lambda_GC_1df"]:.2f}')
    axes[0].plot([0, 4.5], [0, 4.5], '--', color='#333333', linewidth=1)
    axes[0].set(title='QQ diagnostics for seven analysis configurations', xlabel='Expected -log10(P)', ylabel='Observed -log10(P)')
    axes[0].legend(fontsize=8.5, frameon=False)
    axes[1].scatter([a[key]['BETA'] for key in ids], [b[key]['BETA'] for key in ids], s=9, alpha=.4, color='#0072b2')
    bounds = [min(row['BETA'] for row in a.values()), max(row['BETA'] for row in a.values())]
    axes[1].plot(bounds, bounds, '--', color='#444444', linewidth=1)
    axes[1].set(title='Matched ordinary models agree after allele alignment', xlabel='PLINK PC3 beta', ylabel='GEMMA LM beta')
    save(fig, 'qq-and-lm-check')
    if 'loco-chr17' in metadata['completed_tasks']:
        loco = normalize(directory/'loco/chr17_lmm.assoc.txt', 'gemma', metadata['qc_samples'])
        baseline = {key: reference[key] for key in loco}
        loco, swaps = harmonize(baseline, loco)
        fig, ax = plt.subplots(figsize=(10.8, 4.6), constrained_layout=True)
        for label, rows, color in [('Whole-genome GRM', results['GEMMA LMM'], '#0072b2'),
                                   ('GRM excluding chr17', loco, '#d55e00')]:
            subset = sorted((row for row in rows.values() if row['CHR'] == '17'), key=lambda row: row['POS'])
            ax.scatter([row['POS']/1e6 for row in subset], [row['NEG_LOG10_P'] for row in subset], s=17, alpha=.65, label=label, color=color)
        ax.axhline(threshold, linestyle='--', color='#666666', linewidth=1)
        ax.set(title='Chr17-only background comparison', xlabel='Source chr17 position (Mb)', ylabel='-log10(P)')
        ax.legend(frameon=False)
        save(fig, 'chr17-loco')
        summary['chr17_LOCO'] = {'tested_variants': len(loco), 'target': 'rs6249614',
                                'whole_genome_GRM': results['GEMMA LMM']['rs6249614'],
                                'GRM_excluding_chr17': loco['rs6249614'], 'allele_flips': swaps}
    summary['software_for_figures'] = {'numpy': np.__version__, 'matplotlib': matplotlib.__version__}
    (figures/'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
