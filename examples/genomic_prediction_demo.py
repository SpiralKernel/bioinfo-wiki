#!/usr/bin/env python3
"""Teaching GBLUP/RR-BLUP equivalence and nested prediction validation on artificial families."""
import argparse
import csv
import json
from pathlib import Path
import numpy as np

PROJECT = Path(__file__).resolve().parents[1]


def preprocess(train_genotypes, test_genotypes):
    means = train_genotypes.mean(axis=0)
    keep = train_genotypes.var(axis=0) > 0
    if not keep.any():
        raise ValueError('No polymorphic training markers')
    frequency = means[keep]/2
    scale = float(np.sum(2*frequency*(1-frequency)))
    if scale <= 0:
        raise ValueError('Invalid relationship-matrix scaling')
    return train_genotypes[:, keep]-means[keep], test_genotypes[:, keep]-means[keep], scale, keep


def gblup(train_genotypes, train_y, test_genotypes, penalty):
    if penalty <= 0:
        raise ValueError('Positive penalty required')
    z, ztest, scale, keep = preprocess(train_genotypes, test_genotypes)
    k = z@z.T/scale
    matrix = k+penalty*np.eye(len(train_y))
    solved = np.linalg.solve(matrix, np.column_stack([train_y, np.ones(len(train_y))]))
    intercept = float(solved[:, 0].sum()/solved[:, 1].sum())
    alpha = solved[:, 0]-intercept*solved[:, 1]
    marker_effects = z.T@alpha/scale
    genetic_prediction = ztest@marker_effects
    return intercept+genetic_prediction, genetic_prediction, marker_effects, {'intercept':intercept, 'scale':scale, 'markers':int(keep.sum())}


def equivalence_check():
    rng=np.random.default_rng(20261013)
    train=rng.binomial(2, .4, size=(35, 50)).astype(float)
    test=rng.binomial(2, .4, size=(10, 50)).astype(float)
    y=rng.normal(size=35)
    prediction, _, _, details=gblup(train, y, test, .7)
    z, ztest, scale, _=preprocess(train, test)
    # The matching marker penalty is lambda_G * scale, not lambda_G.
    beta=np.linalg.solve(z.T@z+.7*scale*np.eye(z.shape[1]), z.T@(y-details['intercept']))
    primal=details['intercept']+ztest@beta
    error=float(np.max(np.abs(primal-prediction)))
    if error>1e-10:
        raise ValueError('GBLUP and matching ridge system disagree')
    return error


def simulate(seed=20261013, families=20, per_family=12, markers=400):
    rng=np.random.default_rng(seed)
    frequency=rng.uniform(.1,.5,markers)
    parents=rng.binomial(2,frequency,size=(families,2,markers))
    group=np.repeat(np.arange(families),per_family)
    genotype=np.stack([rng.binomial(1,parents[f,0]/2)+rng.binomial(1,parents[f,1]/2) for f in group]).astype(float)
    beta=np.zeros(markers)
    selected=rng.choice(markers,60,replace=False)
    beta[selected]=rng.normal(size=len(selected))
    true_g=(genotype-2*frequency)@beta
    true_g=(true_g-true_g.mean())/true_g.std()
    environment=rng.normal(0,.6,families)[group]
    phenotype=true_g+environment+rng.normal(0,np.sqrt(1.5),len(group))
    return genotype,phenotype,true_g,group


def folds(indices, groups, mode, count, seed):
    rng=np.random.default_rng(seed)
    if mode=='random':
        for test in np.array_split(rng.permutation(indices),count):
            yield np.setdiff1d(indices,test),test
    elif mode=='family':
        unique=np.unique(groups[indices])
        if len(unique)<count:
            raise ValueError('Not enough families')
        for held in np.array_split(rng.permutation(unique),count):
            test=indices[np.isin(groups[indices],held)]
            yield indices[~np.isin(groups[indices],held)],test
    else:
        raise ValueError('Unknown validation mode')


def tune(genotype,phenotype,groups,training,mode,seed):
    candidates=[.1,.3,1.,3.,10.]
    splits=list(folds(training,groups,mode,3,seed))
    losses=[]
    for penalty in candidates:
        errors=[]
        for train,test in splits:
            prediction,*_=gblup(genotype[train],phenotype[train],genotype[test],penalty)
            errors.extend((phenotype[test]-prediction)**2)
        losses.append(float(np.mean(errors)))
    choice=int(np.argmin(losses))
    return candidates[choice],dict(zip(map(str,candidates),losses))


def correlation(a,b):
    return float(np.corrcoef(a,b)[0,1])


def evaluate(genotype,phenotype,true_g,groups,mode):
    records=[]
    predictions=np.full(len(phenotype),np.nan)
    genetic_predictions=np.full(len(phenotype),np.nan)
    assignments=np.full(len(phenotype),-1,dtype=int)
    all_indices=np.arange(len(phenotype))
    for fold_number,(training,test) in enumerate(folds(all_indices,groups,mode,5,20261013)):
        if mode=='family' and set(groups[training]) & set(groups[test]):
            raise ValueError('Family split is not disjoint')
        penalty,inner_losses=tune(genotype,phenotype,groups,training,mode,20261013+fold_number)
        prediction,genetic,_,fit=gblup(genotype[training],phenotype[training],genotype[test],penalty)
        predictions[test]=prediction
        genetic_predictions[test]=genetic
        assignments[test]=fold_number
        # true_g is accessed only for evaluation, never fitting or tuning.
        slope=float(np.polyfit(prediction,phenotype[test],1)[0])
        records.append({'fold':fold_number,'train_n':len(training),'test_n':len(test),
                        'shared_family_IDs':len(set(groups[training]) & set(groups[test])),
                        'lambda_G':penalty,'inner_MSE_by_lambda':inner_losses,
                        'corr_observed_y':correlation(phenotype[test],prediction),
                        'corr_true_g_simulation_only':correlation(true_g[test],genetic),
                        'MSE_observed_y':float(np.mean((phenotype[test]-prediction)**2)),
                        'regression_observed_on_prediction':slope,'fit':fit})
    if not np.isfinite(predictions).all() or (assignments<0).any():
        raise ValueError('Some observations have no outer prediction')
    return {'mode':mode,'outer_folds':records,
            'mean_fold_corr_y':float(np.mean([r['corr_observed_y'] for r in records])),
            'mean_fold_corr_true_g':float(np.mean([r['corr_true_g_simulation_only'] for r in records])),
            'pooled_MSE_y':float(np.mean((phenotype-predictions)**2))},predictions,assignments,genetic_predictions


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=PROJECT/'examples/output/gs')
    args=parser.parse_args()
    output=args.output.resolve();output.mkdir(parents=True,exist_ok=True)
    error=equivalence_check()
    all_genotypes,all_phenotypes,all_true_g,all_groups=simulate(families=25)
    genotype,phenotype,true_g,groups=(values[:240] for values in (all_genotypes,all_phenotypes,all_true_g,all_groups))
    candidate_genotypes=all_genotypes[240:]
    summary={'seed':20261013,'individuals':len(phenotype),'markers':genotype.shape[1],
             'families':len(np.unique(groups)),'equivalence_max_abs_prediction_error':error,
             'model':'Training-centered VanRaden-style K and positive lambda; intercept fitted by GLS',
             'scope':'Artificial data; no pedigree BLUP, REML, Bayesian sampling, ssGBLUP or commercial software run',
             'numpy_version':np.__version__,'validation':{}}
    predictions={}
    for mode in ['random','family']:
        result,prediction,assignment,genetic=evaluate(genotype,phenotype,true_g,groups,mode)
        summary['validation'][mode]=result
        predictions[mode]=(prediction,assignment,genetic)
    with (output/'predictions.tsv').open('w') as stream:
        writer=csv.writer(stream,delimiter='\t');writer.writerow(['ID','family','observed_y','true_g_simulation_only','prediction_random','GEBV_random','fold_random','prediction_family','GEBV_family','fold_family'])
        for i in range(len(phenotype)):
            writer.writerow([f'TOY{i:03}',int(groups[i]),phenotype[i],true_g[i],predictions['random'][0][i],predictions['random'][2][i],int(predictions['random'][1][i]),predictions['family'][0][i],predictions['family'][2][i],int(predictions['family'][1][i])])
    final_penalty,final_losses=tune(genotype,phenotype,groups,np.arange(len(phenotype)),'family',20261014)
    candidate_yhat,candidate_gebv,effects,fit=gblup(genotype,phenotype,candidate_genotypes,final_penalty)
    _,_,_,keep=preprocess(genotype,candidate_genotypes)
    np.savez_compressed(output/'prediction-model.npz',marker_means=genotype.mean(axis=0),kept_markers=keep,
                        marker_effects=effects,intercept=fit['intercept'],lambda_G=final_penalty,scale=fit['scale'],
                        marker_ids=np.array([f'M{i:03}' for i in range(genotype.shape[1])]),
                        allele_encoding='0/1/2 copies of the simulated counted allele',
                        reference='Training individuals TOY000 to TOY239')
    with (output/'candidate-predictions.tsv').open('w') as stream:
        writer=csv.writer(stream,delimiter='\t');writer.writerow(['ID','family','GEBV_training_reference','predicted_y'])
        for i in range(len(candidate_genotypes)):
            writer.writerow([f'CANDIDATE{i:03}',int(all_groups[240+i]),candidate_gebv[i],candidate_yhat[i]])
    with (output/'genotypes.tsv').open('w') as stream:
        writer=csv.writer(stream,delimiter='\t');writer.writerow(['ID']+[f'M{i:03}' for i in range(genotype.shape[1])])
        for i,row in enumerate(all_genotypes):
            identifier=f'TOY{i:03}' if i<240 else f'CANDIDATE{i-240:03}'
            writer.writerow([identifier]+row.astype(int).tolist())
    with (output/'phenotypes.tsv').open('w') as stream:
        writer=csv.writer(stream,delimiter='\t');writer.writerow(['ID','family','trait'])
        for i in range(len(all_genotypes)):
            identifier=f'TOY{i:03}' if i<240 else f'CANDIDATE{i-240:03}'
            writer.writerow([identifier,int(all_groups[i]),phenotype[i] if i<240 else 'NA'])
    summary['candidate_prediction']={'individuals':len(candidate_genotypes),'new_families':5,
                                     'lambda_G':final_penalty,'inner_MSE_by_lambda':final_losses,'selection_basis':'Family-wise training-only inner CV MSE',
                                     'phenotype_used_for_candidates':False,'fit':fit}
    np.savez_compressed(output/'artificial-data.npz',genotype=genotype,phenotype=phenotype,true_g=true_g,family=groups)
    (output/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in summary.items() if k!='validation'},ensure_ascii=False))
    for mode,result in summary['validation'].items():
        print(mode,'mean fold corr(y,prediction)=',round(result['mean_fold_corr_y'],4),
              'mean fold corr(true_g,prediction)=',round(result['mean_fold_corr_true_g'],4))


if __name__=='__main__':
    main()
