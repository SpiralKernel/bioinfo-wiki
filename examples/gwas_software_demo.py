#!/usr/bin/env python3
"""Pinned public mouse data: matched PLINK/GEMMA and optional GCTA/REGENIE demos."""
import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import time
import urllib.request

PROJECT = Path(__file__).resolve().parents[1]
DATA_URL = 'https://raw.githubusercontent.com/genetics-statistics/GEMMA/v0.98.5/example/'
DATA_HASHES = {
    'mouse_hs1940.bed': '82ae9049806a896b12547fe892a85465949005bca8f7e855fdb2b0ea558936d2',
    'mouse_hs1940.bim': '86d28fb5bda51b33972366218f5ad834de937ce55e444fb1a682e77e3adc9cf1',
    'mouse_hs1940.fam': '8b23d60fd5f25a004b3725f6f0c66001b3ddc8a58aca07525b005529b0e1f54c',
    'mouse_hs1940.pheno.txt': '60ced3ddb4ad6e158d858c77d309bfcd4966e27f38878da36b4547f8da28fb64',
}


def download_data(directory):
    directory.mkdir(parents=True, exist_ok=True)
    records = {}
    for name, expected in DATA_HASHES.items():
        path = directory/name
        if not path.exists():
            temporary = path.with_name(name+'.part')
            for attempt in range(3):
                try:
                    request = urllib.request.Request(DATA_URL+name, headers={'User-Agent': 'bioinfo-wiki-demo/1.0'})
                    with urllib.request.urlopen(request, timeout=60) as response:
                        temporary.write_bytes(response.read())
                    if hashlib.sha256(temporary.read_bytes()).hexdigest() != expected:
                        raise ValueError(f'Download checksum mismatch: {name}')
                    temporary.replace(path)
                    break
                except (OSError, ValueError):
                    temporary.unlink(missing_ok=True)
                    if attempt == 2:
                        raise
                    time.sleep(1)
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError(f'Existing input checksum mismatch: {path}; preserve and inspect it before retrying')
        records[name] = {'url': DATA_URL+name, 'sha256': expected, 'bytes': path.stat().st_size}
    return records


def prepare_input(raw, prepared):
    prepared.mkdir(parents=True, exist_ok=True)
    fam = [line.split() for line in (raw/'mouse_hs1940.fam').read_text().splitlines()]
    phenotypes = [line.split() for line in (raw/'mouse_hs1940.pheno.txt').read_text().splitlines()]
    if len(fam) != len(phenotypes) or any(row[5:] != phenotype for row, phenotype in zip(fam, phenotypes)):
        raise ValueError('Extended FAM and phenotype matrix are inconsistent')
    identifiers = [tuple(row[:2]) for row in fam]
    if len(identifiers) != len(set(identifiers)):
        raise ValueError('Duplicate FID/IID in source')
    for extension in ('bed', 'bim'):
        shutil.copy2(raw/f'mouse_hs1940.{extension}', prepared/f'cohort.{extension}')
    with (prepared/'cohort.fam').open('w') as out, (prepared/'complete.keep').open('w') as keep:
        complete = 0
        for row in fam:
            phenotype = row[5] if row[5] not in {'NA', '-9'} else '-9'
            # Pedigree parents are not used here; original file remains intact.
            out.write('\t'.join(row[:2]+['0', '0', row[4], phenotype])+'\n')
            if phenotype != '-9':
                complete += 1
                keep.write('\t'.join(row[:2])+'\n')
    return {'raw_samples': len(fam), 'raw_family_IDs': len({row[0] for row in fam}), 'complete_CD8_samples': complete,
            'raw_variants': len((raw/'mouse_hs1940.bim').read_text().splitlines()),
            'pedigree_note': 'FID retained; parents zeroed in the teaching copy; genotype-based GRM used',
            'phenotype_note': 'Source-preprocessed CD8, first phenotype; not raw cell percentage',
            'coordinate_note': 'Source coordinates retained; assembly not established for contemporary annotation'}


def prepare_covariates(prepared):
    fam = [line.split() for line in (prepared/'qc.fam').read_text().splitlines()]
    with (prepared/'pca.eigenvec').open() as stream:
        rows = list(csv.DictReader(stream, delimiter='\t'))
    pcs = {(row['#FID'], row['IID']): [row[f'PC{i}'] for i in range(1, 4)] for row in rows}
    ids = [tuple(row[:2]) for row in fam]
    if len(pcs) != len(rows) or set(ids) != set(pcs) or len(ids) != len(set(ids)):
        raise ValueError('PCA and genotype IDs do not match one-to-one')
    with (prepared/'gemma.covariates.txt').open('w') as gemma, \
            (prepared/'gcta.qcovar.txt').open('w') as gcta, \
            (prepared/'gcta.pheno.txt').open('w') as pheno, \
            (prepared/'regenie.pheno.txt').open('w') as regenie:
        regenie.write('FID\tIID\tCD8\n')
        for row in fam:
            values = pcs[tuple(row[:2])]
            gemma.write('\t'.join(['1']+values)+'\n')
            gcta.write('\t'.join(row[:2]+values)+'\n')
            pheno.write('\t'.join(row[:2]+[row[5]])+'\n')
            regenie.write('\t'.join(row[:2]+[row[5]])+'\n')
    (prepared/'regenie.covariates.txt').write_text((prepared/'pca.eigenvec').read_text().replace('#FID', 'FID', 1))
    return {'qc_samples': len(fam), 'qc_family_IDs': len({row[0] for row in fam}), 'qc_variants': len((prepared/'qc.bim').read_text().splitlines()),
            'pca_variants': len((prepared/'prune.prune.in').read_text().splitlines()), 'association_PCs': 3}


def binary_path(name):
    value = shutil.which(name)
    if not value:
        raise ValueError(f'Executable not found: {name}')
    return str(Path(value).resolve())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=PROJECT/'examples/output/gwas-real')
    parser.add_argument('--plink2', default='plink2')
    parser.add_argument('--gemma', default='gemma')
    parser.add_argument('--gcta', help='Optional GCTA executable')
    parser.add_argument('--regenie', help='Optional REGENIE executable')
    parser.add_argument('--fastgwa', action='store_true', help='Also run sparse-GRM quantitative fastGWA; requires --gcta')
    parser.add_argument('--loco-chr17', action='store_true', help='Additional GEMMA chr17-only LOCO demonstration')
    parser.add_argument('--threads', type=int, default=2)
    args = parser.parse_args()
    if args.threads < 1 or (args.fastgwa and not args.gcta):
        parser.error('Positive threads required; --fastgwa requires --gcta')
    tools = {key: binary_path(value) for key, value in {'plink2': args.plink2, 'gemma': args.gemma,
             'gcta': args.gcta, 'regenie': args.regenie}.items() if value}
    output = args.output.resolve()
    for folder in ('data', 'prepared', 'results', 'gemma', 'logs'):
        (output/folder).mkdir(parents=True, exist_ok=True)
    commands = []
    environment = dict(os.environ, OPENBLAS_NUM_THREADS=str(args.threads), OMP_NUM_THREADS=str(args.threads))

    def run(label, *command):
        started = time.monotonic()
        print('Running', label, flush=True)
        with (output/'logs'/f'{label}.log').open('w') as log:
            process = subprocess.run([str(x) for x in command], cwd=output, env=environment,
                                     stdout=log, stderr=subprocess.STDOUT)
        commands.append({'task': label, 'argv': [str(x) for x in command],
                         'exit_code': process.returncode, 'seconds': round(time.monotonic()-started, 3)})
        (output/'commands.json').write_text(json.dumps(commands, indent=2)+'\n')
        if process.returncode:
            raise RuntimeError(f'{label} failed; inspect {output/"logs"/(label+".log")}')

    files = download_data(output/'data')
    metadata = prepare_input(output/'data', output/'prepared')
    metadata['source'] = {'repository': 'https://github.com/genetics-statistics/GEMMA', 'release': 'v0.98.5', 'files': files}
    plink, gemma = tools['plink2'], tools['gemma']
    species = ['--chr-set', '19', 'no-xy', 'no-mt']
    run('plink-version', plink, '--version')
    run('gemma-version', gemma, '-h')
    run('qc', plink, '--bfile', 'prepared/cohort', *species, '--autosome', '--keep', 'prepared/complete.keep',
        '--geno', '0.05', '--mind', '0.05', '--maf', '0.05', '--make-bed', '--threads', args.threads, '--out', 'prepared/qc')
    run('prune', plink, '--bfile', 'prepared/qc', *species, '--missing', '--freq', '--indep-pairwise', '50', '5', '0.2',
        '--threads', args.threads, '--out', 'prepared/prune')
    run('pca', plink, '--bfile', 'prepared/qc', *species, '--extract', 'prepared/prune.prune.in', '--pca', '5',
        '--threads', args.threads, '--out', 'prepared/pca')
    metadata.update(prepare_covariates(output/'prepared'))
    run('plink-unadjusted', plink, '--bfile', 'prepared/qc', *species, '--glm', 'allow-no-covars', 'hide-covar',
        '--threads', args.threads, '--out', 'results/plink_unadjusted')
    run('plink-pc3', plink, '--bfile', 'prepared/qc', *species, '--covar', 'prepared/pca.eigenvec', '--covar-name', 'PC1-PC3',
        '--glm', 'hide-covar', '--threads', args.threads, '--out', 'results/plink_pc3')
    gemma_common = [gemma, '-bfile', 'prepared/qc', '-c', 'prepared/gemma.covariates.txt', '-maf', '0.05', '-miss', '0.05']
    run('gemma-grm', *gemma_common, '-gk', '2', '-outdir', 'gemma', '-o', 'grm')
    run('gemma-lm', *gemma_common, '-lm', '1', '-outdir', 'gemma', '-o', 'lm_pc3')
    run('gemma-lmm', *gemma_common, '-k', 'gemma/grm.sXX.txt', '-lmm', '1', '-outdir', 'gemma', '-o', 'lmm_pc3')
    if args.gcta:
        (output/'gcta').mkdir(exist_ok=True)
        gcta = tools['gcta']
        run('gcta-grm', gcta, '--bfile', 'prepared/qc', '--autosome-num', '19', '--make-grm',
            '--thread-num', args.threads, '--out', 'gcta/full')
        association = ['--bfile', 'prepared/qc', '--autosome-num', '19', '--pheno', 'prepared/gcta.pheno.txt',
                       '--qcovar', 'prepared/gcta.qcovar.txt', '--thread-num', args.threads]
        run('gcta-mlma', gcta, *association, '--grm', 'gcta/full', '--mlma', '--out', 'gcta/mlma_pc3')
        if args.fastgwa:
            run('gcta-sparse', gcta, '--grm', 'gcta/full', '--make-bK-sparse', '0.05', '--out', 'gcta/sparse')
            run('gcta-fastgwa', gcta, *association, '--grm-sparse', 'gcta/sparse', '--fastGWA-mlm',
                '--seed', '20261013', '--out', 'gcta/fastgwa_pc3')
    if args.regenie:
        (output/'regenie').mkdir(exist_ok=True)
        common = [tools['regenie'], '--bed', 'prepared/qc', '--phenoFile', 'prepared/regenie.pheno.txt', '--phenoCol', 'CD8',
                  '--covarFile', 'prepared/regenie.covariates.txt', '--covarColList', 'PC1,PC2,PC3', '--qt',
                  '--bsize', '200', '--threads', args.threads]
        run('regenie-step1', *common, '--step', '1', '--lowmem', '--out', 'regenie/step1')
        run('regenie-step2', *common, '--step', '2', '--minMAC', '20', '--pred', 'regenie/step1_pred.list', '--out', 'regenie/step2')
    if args.loco_chr17:
        (output/'loco').mkdir(exist_ok=True)
        run('loco-prepare', plink, '--bfile', 'prepared/qc', *species, '--not-chr', '17', '--make-bed',
            '--threads', args.threads, '--out', 'loco/without17')
        bim = [line.split() for line in (output/'prepared/qc.bim').read_text().splitlines()]
        (output/'loco/chr17.snps').write_text(''.join(row[1]+'\n' for row in bim if row[0] == '17'))
        run('loco-grm', gemma, '-bfile', 'loco/without17', '-c', 'prepared/gemma.covariates.txt', '-maf', '0.05', '-miss', '0.05',
            '-gk', '2', '-outdir', 'loco', '-o', 'without17')
        run('loco-chr17', *gemma_common, '-snps', 'loco/chr17.snps', '-k', 'loco/without17.sXX.txt', '-lmm', '1',
            '-outdir', 'loco', '-o', 'chr17_lmm')
    metadata['completed_tasks'] = [row['task'] for row in commands]
    (output/'run-metadata.json').write_text(json.dumps(metadata, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({key: value for key, value in metadata.items() if key not in {'source'}}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
