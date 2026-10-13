#!/usr/bin/env python3
"""Small artificial examples for inference, resampling and omics replication units."""
import argparse
import csv
import json
from pathlib import Path
import numpy as np
import scipy
from scipy import stats

PROJECT = Path(__file__).resolve().parents[1]
SEED = 20261013


def welch_summary(a, b, confidence=.95):
    """Estimate mean(b)-mean(a), with a two-sided Welch interval."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    if min(len(a), len(b)) < 2 or not (np.isfinite(a).all() and np.isfinite(b).all()):
        raise ValueError('Need at least two finite independent observations per group')
    va, vb = a.var(ddof=1)/len(a), b.var(ddof=1)/len(b)
    if va+vb <= 0:
        raise ValueError('No sampling variance')
    se = np.sqrt(va+vb)
    df = (va+vb)**2/(va**2/(len(a)-1)+vb**2/(len(b)-1))
    effect = b.mean()-a.mean()
    statistic = effect/se
    p = 2*stats.t.sf(abs(statistic), df)
    width = stats.t.ppf((1+confidence)/2, df)*se
    return dict(effect_B_minus_A=float(effect), SE=float(se), df=float(df),
                t=float(statistic), p=float(p), CI=[float(effect-width), float(effect+width)])


def adjust_bh(p):
    p = np.asarray(p, float)
    if p.ndim != 1 or not len(p) or not np.isfinite(p).all() or ((p<0)|(p>1)).any():
        raise ValueError('Need a nonempty vector of finite probabilities')
    order = np.argsort(p, kind='stable')
    ranked = p[order]*len(p)/np.arange(1, len(p)+1)
    adjusted = np.minimum.accumulate(ranked[::-1])[::-1].clip(0, 1)
    result = np.empty_like(p)
    result[order] = adjusted
    return result


def mean_difference(b, a, axis=0):
    return np.mean(b, axis=axis)-np.mean(a, axis=axis)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=PROJECT/'examples/output/statistics')
    args = parser.parse_args()
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(SEED)
    a = rng.normal(0, 1, 24)
    b = rng.normal(.7, 2, 36)
    welch = welch_summary(a, b)
    scipy_welch = stats.ttest_ind(b, a, equal_var=False)
    np.testing.assert_allclose([welch['t'], welch['p']],
                               [scipy_welch.statistic, scipy_welch.pvalue], rtol=1e-12)
    baseline = rng.normal(0, 3, 40)
    after = baseline+.4+rng.normal(0, .6, 40)
    paired = stats.ttest_rel(after, baseline)
    unpaired = stats.ttest_ind(after, baseline, equal_var=False)
    # Dedicated equal-variance location-shift example: exchangeability under the null.
    pa, pb = rng.normal(0, 1, 18), rng.normal(.6, 1, 18)
    permutation = stats.permutation_test((pb, pa), mean_difference,
                    n_resamples=9999, alternative='two-sided',
                    permutation_type='independent', rng=np.random.default_rng(SEED+1))
    exact = stats.permutation_test((np.array([4.,5.,6.]), np.array([1.,2.,3.])),
                    mean_difference, n_resamples=np.inf, alternative='two-sided')
    bootstrap = stats.bootstrap((b, a), mean_difference, paired=False,
                    method='BCa', n_resamples=4999, batch=500,
                    rng=np.random.default_rng(SEED+2))
    fisher_table = np.array([[8,2],[1,9]])
    fisher = stats.fisher_exact(fisher_table, alternative='two-sided')
    chi_table = np.array([[20,15,10],[10,20,15]])
    chi = stats.chi2_contingency(chi_table, correction=False)
    # Independent normal artificial features, not a raw RNA-seq count model.
    ga = rng.normal(0, 1, (24, 2000))
    gb = rng.normal(0, 1, (24, 2000))
    gb[:, :100] += 1
    gene_tests = stats.ttest_ind(gb, ga, axis=0, equal_var=False)
    p = gene_tests.pvalue
    bh = adjust_bh(p)
    np.testing.assert_allclose(bh, stats.false_discovery_control(p, method='bh'), atol=1e-14)
    bonferroni = np.minimum(1, len(p)*p)
    null = np.arange(len(p)) >= 100
    discovery = {}
    for name, values in [('raw',p),('BH',bh),('Bonferroni',bonferroni)]:
        rejected = values < .05
        count = int(rejected.sum())
        false = int((rejected & null).sum())
        discovery[name] = dict(discoveries=count, false_discoveries_simulation_only=false,
                                realized_FDP=false/max(count,1))
    # Two hundred cells are nested in twenty independent donors; true group effect is zero.
    donor_group = np.repeat([0,1], 10)
    donor_effect = rng.normal(0, 1.8, 20)
    cells = donor_effect[:,None]+rng.normal(0, .35, (20,10))
    donor_means = cells.mean(axis=1)
    donor_test = stats.ttest_ind(donor_means[donor_group==1], donor_means[donor_group==0], equal_var=False)
    cell_test = stats.ttest_ind(cells[donor_group==1].ravel(), cells[donor_group==0].ravel(), equal_var=False)
    # Repeated confidence intervals for independent normal observations: not bootstrap of one data set.
    samples = rng.normal(0,1,(1000,20))
    means, se = samples.mean(axis=1), samples.std(axis=1, ddof=1)/np.sqrt(20)
    width = stats.t.ppf(.975, 19)*se
    coverage = (means-width<=0)&(means+width>=0)
    summary = dict(seed=SEED, versions=dict(numpy=np.__version__, scipy=scipy.__version__),
        scope='Artificial continuous data only; no real omics, wet-lab, classifier, GLM or mixed model fit',
        independent_welch=welch,
        paired=dict(subjects=40, mean_difference=float((after-baseline).mean()),
                    paired_p=float(paired.pvalue), incorrectly_ignoring_pairs_p=float(unpaired.pvalue)),
        permutation=dict(effect_B_minus_A=float(permutation.statistic), p=float(permutation.pvalue),
                    resamples=9999, exact_six_observations_p=float(exact.pvalue)),
        bootstrap=dict(method='BCa', resamples=4999, statistic='mean(B)-mean(A)',
                    CI=list(map(float,bootstrap.confidence_interval))),
        contingency=dict(fisher_table=fisher_table.tolist(), odds_ratio=float(fisher.statistic),
                    fisher_p=float(fisher.pvalue), chi_square_table=chi_table.tolist(),
                    chi_square_p=float(chi.pvalue), min_expected=float(chi.expected_freq.min())),
        multiple_testing=dict(features=2000, nonnull_features_simulation_only=100, results=discovery),
        pseudoreplication=dict(donors=20, cells=200, true_group_effect=0,
                    correct_donor_level_p=float(donor_test.pvalue),
                    incorrectly_independent_cells_p=float(cell_test.pvalue),
                    observed_difference=float(donor_means[donor_group==1].mean()-donor_means[donor_group==0].mean())),
        repeated_confidence_intervals=dict(repetitions=1000, observations_each=20,
                    nominal_coverage=.95, observed_coverage=float(coverage.mean())))
    with (out/'feature-tests.tsv').open('w') as stream:
        writer=csv.writer(stream, delimiter='\t')
        writer.writerow(['feature','effect_B_minus_A','p','BH','Bonferroni','nonnull_simulation_only'])
        for i in range(len(p)):
            writer.writerow([f'FEATURE{i:04}', float(gb[:,i].mean()-ga[:,i].mean()), p[i], bh[i], bonferroni[i], int(not null[i])])
    with (out/'donor-cells.tsv').open('w') as stream:
        writer=csv.writer(stream, delimiter='\t');writer.writerow(['donor','group','cell','measurement'])
        for i in range(20):
            for j in range(10):writer.writerow([f'DONOR{i:02}',int(donor_group[i]),j,cells[i,j]])
    (out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none'})
    fig,axes=plt.subplots(2,2,figsize=(11,7.5),constrained_layout=True)
    for before,end in zip(baseline,after):axes[0,0].plot([0,1],[before,end],color='#777777',alpha=.35,lw=.8)
    axes[0,0].scatter([0,1],[baseline.mean(),after.mean()],color='#0072b2',s=65,zorder=5)
    axes[0,0].set(xticks=[0,1],xticklabels=['Before','After'],ylabel='Artificial measurement',title='Paired observations: retain subject identity')
    for i in range(100):
        axes[0,1].plot([means[i]-width[i],means[i]+width[i]],[i,i],color='#0072b2' if coverage[i] else '#d55e00',lw=1)
    axes[0,1].axvline(0,color='black',linestyle='--',lw=1)
    axes[0,1].set(xlabel='Mean estimate and 95% t interval',ylabel='Repeated study',title=f'First 100 intervals; coverage of all 1000: {coverage.mean():.3f}')
    jitter=np.random.default_rng(SEED+3).uniform(-.12,.12,20)
    axes[1,0].scatter(donor_group+jitter,donor_means,color='#0072b2',s=45)
    axes[1,0].set(xticks=[0,1],xticklabels=['Group A','Group B'],ylabel='Mean per donor',title=f'20 donors, 200 cells: donor P={donor_test.pvalue:.3g}\nTreating cells as independent: P={cell_test.pvalue:.3g}')
    rank=np.arange(1,len(p)+1)
    axes[1,1].plot(rank,np.sort(p),label='Raw P',color='#0072b2')
    axes[1,1].plot(rank,np.sort(bh),label='BH-adjusted P',color='#d55e00')
    axes[1,1].axhline(.05,color='#777777',linestyle='--')
    axes[1,1].set(xlabel='Rank among 2000 independent artificial features',ylabel='P or adjusted P',title='Multiplicity changes the discovery threshold',ylim=(0,1))
    axes[1,1].legend()
    fig.savefig(out/'inference-and-replication.png',dpi=180,bbox_inches='tight',facecolor='white')
    svg=out/'inference-and-replication.svg';fig.savefig(svg,bbox_inches='tight',facecolor='white')
    svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines())+'\n')
    plt.close(fig)
    print(json.dumps(summary,ensure_ascii=False,indent=2))


if __name__ == '__main__':main()
