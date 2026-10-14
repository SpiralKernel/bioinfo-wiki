#!/usr/bin/env python3
"""Run bcftools on artificial VCF/SAM inputs; no real genome performance claim."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess

PROJECT = Path(__file__).resolve().parents[1]


def read_records(path):
    """Inspect our plain-text teaching outputs, not a general VCF parser."""
    rows = []
    for line in Path(path).read_text().splitlines():
        if line and not line.startswith('#'):
            fields = line.split('\t')
            info = dict(item.split('=', 1) if '=' in item else (item, True)
                        for item in fields[7].split(';') if item != '.')
            rows.append(dict(chrom=fields[0], pos=int(fields[1]), id=fields[2],
                             ref=fields[3], alt=fields[4], filter=fields[6],
                             info=info, format=fields[8].split(':'),
                             samples=[dict(zip(fields[8].split(':'), x.split(':')))
                                      for x in fields[9:]]))
    return rows


def validate_paths(input_dir, output):
    """Outputs may be siblings, never overwrite or contain the input directory."""
    source, target = Path(input_dir).resolve(), Path(output).resolve()
    if source == target or source in target.parents or target in source.parents:
        raise ValueError('Input and output must be separate, non-nested directories')
    required = ['toy.fa', 'toy.fa.fai', 'calls.vcf', 'regions.bed', 'samples.txt', 'toy.sam']
    for name in required:
        if not (source/name).is_file():
            raise ValueError(f'Missing teaching input: {name}')
    return source, target, required


def run_demo(bcftools, input_dir, output):
    source, output, required = validate_paths(input_dir, output)
    executable = shutil.which(str(bcftools))
    if executable is None:
        raise ValueError('bcftools not found; install it or pass --bcftools /path/to/bcftools')
    executable = str(Path(executable).resolve())
    output.mkdir(parents=True, exist_ok=True)
    for name in required:
        if (output/name).is_symlink():
            raise ValueError(f'Output must not be a symbolic link: {name}')
        shutil.copy2(source/name, output/name)
    log = []

    def run(*args, save=None):
        # Use relative paths in the recorded command and no shell interpolation.
        result = subprocess.run([executable, *map(str, args)], cwd=output,
                                capture_output=True, text=True, check=True)
        log.append(dict(command=['bcftools', *map(str, args)], stderr=result.stderr))
        if save:
            (output/save).write_text(result.stdout)
        return result.stdout

    def extract(name, *args):
        run('view', '--no-version', *args, '-Ov', '-o', name+'.vcf', 'normalized.vcf.gz')
        return read_records(output/(name+'.vcf'))

    version = run('--version').splitlines()[:2]
    # Fail on REF mismatch instead of silently changing alleles or genotypes.
    run('norm', '--no-version', '-f', 'toy.fa', '-c', 'e', '-m', '-any',
        '-Ov', '-o', 'normalized.unsorted.vcf', 'calls.vcf')
    run('sort', '-Oz', '-o', 'normalized.vcf.gz', 'normalized.unsorted.vcf')
    run('index', '-f', 'normalized.vcf.gz')
    run('view', '--no-version', '-Ov', '-o', 'normalized.vcf', 'normalized.vcf.gz')
    normalized = read_records(output/'normalized.vcf')
    small = extract('sequence_resolved', '-i', 'INFO/SVTYPE="."')
    groups = {}
    for name, kind in [('snps', 'snps'), ('indels', 'indels'), ('mnps', 'mnps')]:
        groups[name] = extract(name, '-i', 'INFO/SVTYPE="."', '-v', kind)
    groups['symbolic_del'] = extract('symbolic_del', '-i', 'INFO/SVTYPE="DEL"')
    groups['inv'] = extract('inv', '-i', 'INFO/SVTYPE="INV"')
    groups['dup'] = extract('dup', '-i', 'INFO/SVTYPE="DUP"')
    groups['bnd'] = extract('bnd', '-i', 'INFO/SVTYPE="BND"')
    groups['cnv'] = extract('cnv', '-i', 'INFO/SVTYPE="CNV"')
    groups['str'] = extract('str', '-i', 'INFO/SVTYPE="STR"')
    groups['te'] = extract('te', '-i', 'INFO/TEFAMILY!="."')
    groups['pass'] = extract('pass', '-f', 'PASS')
    groups['pass_or_unassessed'] = extract('pass_or_unassessed', '-f', 'PASS,.')
    # The deletion anchor is outside BED, but the record overlaps the requested base.
    groups['region_record'] = extract('region_record', '-R', 'regions.bed', '--regions-overlap', 'record')
    groups['region_pos'] = extract('region_pos', '-R', 'regions.bed', '--regions-overlap', 'pos')
    subset = extract('sample_S01', '-S', 'samples.txt')
    # view updates AC/AN; explicitly recompute AF after changing the sample set.
    run('+fill-tags', 'sample_S01.vcf', '-Ov', '-o', 'sample_S01.tags.vcf', '--', '-t', 'AC,AN,AF')
    subset_tags = read_records(output/'sample_S01.tags.vcf')
    # Apply the genotype expression AFTER selecting samples in a separate step.
    run('view', '--no-version', '-i', 'GT="alt"', '-Ov', '-o',
        'S01_nonref.vcf', 'sample_S01.tags.vcf')
    groups['S01_nonref'] = read_records(output/'S01_nonref.vcf')
    groups['same_sample_quality'] = extract('same_sample_quality', '-i', 'FMT/DP>=8 & FMT/GQ>=20')
    groups['cross_sample_quality'] = extract('cross_sample_quality', '-i', 'FMT/DP>=8 && FMT/GQ>=20')
    run('norm', '--no-version', '-a', '--atom-overlaps', '.', '-f', 'toy.fa',
        '-Ov', '-o', 'atomized.vcf', 'sequence_resolved.vcf')
    atomized = read_records(output/'atomized.vcf')
    run('filter', '--no-version', '-S', '.', '-e',
        'FMT/DP<8 | FMT/DP="." | FMT/GQ<20 | FMT/GQ="."',
        '-Ov', '-o', 'masked.vcf', 'normalized.vcf.gz')
    run('+fill-tags', 'masked.vcf', '-Ov', '-o', 'masked.tags.vcf', '--', '-t', 'AC,AN,AF')
    masked = read_records(output/'masked.tags.vcf')
    run('query', '-f', '%CHROM\t%POS\t%ID\t%REF\t%ALT\t%FILTER[\t%GT]\n',
        'normalized.vcf.gz', save='variants.tsv')
    run('query', '-i', 'INFO/SVTYPE="CNV"',
        '-f', '%CHROM\t%POS\t%INFO/END[\t%SAMPLE=%CN]\n',
        'normalized.vcf.gz', save='cnv.tsv')
    run('query', '-i', 'INFO/SVTYPE="STR"',
        '-f', '%CHROM\t%POS\t%INFO/RU[\t%SAMPLE=%REPCN]\n',
        'normalized.vcf.gz', save='str.tsv')
    # A separate calling exercise: no mapper was used, alignments are artificial.
    run('mpileup', '-f', 'toy.fa', '-Ob', '-o', 'pileup.bcf', 'toy.sam')
    run('call', '-m', '-v', '-Ov', '-o', 'toy_called.vcf', 'pileup.bcf')
    called = read_records(output/'toy_called.vcf')

    get = lambda records, identifier: next(r for r in records if r['id'] == identifier)
    assert len(normalized) == 17 and len(small) == 9
    assert {key: len(groups[key]) for key in ['snps','indels','mnps','bnd']} == dict(snps=5,indels=3,mnps=1,bnd=2)
    assert get(normalized, 'left_shift')['pos'] == 179
    assert [r['id'] for r in groups['region_record']] == ['small_del']
    assert not groups['region_pos']
    assert len(groups['pass_or_unassessed']) == len(groups['pass']) + 1
    assert get(subset, 'snv')['info']['AC'] == '1' and get(subset, 'snv')['info']['AN'] == '2'
    assert abs(float(get(subset_tags, 'snv')['info']['AF']) - .5) < 1e-6
    assert get(masked, 'low_site')['samples'][0]['GT'] == './.'
    assert get(masked, 'low_site')['samples'][1]['GT'] == '0/0'
    assert 'unassessed' not in [r['id'] for r in groups['same_sample_quality']]
    assert 'unassessed' in [r['id'] for r in groups['cross_sample_quality']]
    assert 'missing' not in [r['id'] for r in groups['S01_nonref']]
    assert 'cnv' not in [r['id'] for r in groups['S01_nonref']]
    assert len(called) == 1 and called[0]['pos'] == 100 and called[0]['samples'][0]['GT'] == '0/1'
    summary = dict(scope='Artificial VCF extraction and artificial SAM small-variant calling only; no real data, mapper, SV/CNV/STR/TE caller, clinical inference or benchmark',
        versions=version, raw_records=16, normalized_records=len(normalized), atomized_sequence_records=len(atomized),samples=['S01','S02','S03'],
        selected_ids={key: [r['id'] for r in value] for key,value in groups.items()},
        counts={key:len(value) for key,value in groups.items()},
        left_shift=dict(input_pos=200,output_pos=get(normalized,'left_shift')['pos']),
        sample_subset_snv=dict(view_info=get(subset,'snv')['info'],recomputed_info=get(subset_tags,'snv')['info']),
        masked_low_site=dict(genotypes=[s['GT'] for s in get(masked,'low_site')['samples']],info=get(masked,'low_site')['info']),
        bnd_records=len(groups['bnd']),bnd_unique_event_ids=len({r['info']['EVENT'] for r in groups['bnd']}),
        artificial_call=dict(pos=called[0]['pos'],ref=called[0]['ref'],alt=called[0]['alt'],gt=called[0]['samples'][0]['GT'],alignments=40),
        input_sha256={name:hashlib.sha256((source/name).read_bytes()).hexdigest() for name in required})
    (output/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
    (output/'commands.json').write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:summary[k] for k in ['versions','raw_records','normalized_records','counts','artificial_call']},ensure_ascii=False,indent=2))
    return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bcftools', default=os.environ.get('BCFTOOLS_BIN', 'bcftools'))
    parser.add_argument('--input-dir', type=Path, default=PROJECT/'examples/data/variants')
    parser.add_argument('--output', type=Path, default=PROJECT/'examples/output/variants')
    args = parser.parse_args()
    try:
        run_demo(args.bcftools, args.input_dir, args.output)
    except subprocess.CalledProcessError as error:
        parser.exit(1, f'bcftools failed (exit {error.returncode}):\n{error.stderr}\n')
    except ValueError as error:
        parser.exit(1, f'{error}\n')
