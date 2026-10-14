#!/usr/bin/env python3
"""Check fresh run, no-op rerun and recovery of one missing teaching output."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess

PROJECT=Path(__file__).resolve().parents[1]


def validate(snakemake,workdir):
    executable=shutil.which(str(snakemake))
    if not executable:raise ValueError('Snakemake not found')
    executable=str(Path(executable).resolve());workdir=Path(workdir).resolve()
    if workdir.exists():raise ValueError('Use a fresh work directory; existing output is not deleted')
    command=[executable,'--snakefile','examples/workflows/annotation/Snakefile',
        '--configfile','examples/workflows/annotation/config.yaml','--directory',str(workdir),'--cores','1']
    def run(name):
        result=subprocess.run(command,cwd=PROJECT,capture_output=True,text=True,check=True)
        text=result.stdout+result.stderr
        (workdir/(name+'.log')).write_text(text)
        return text,re.findall(r'^localrule ([A-Za-z_]+):',text,flags=re.M)
    first,first_rules=run('first-run')
    folder=workdir/'results';database=folder/'database/data/toy/snpEffectPredictor.bin'
    intervals=folder/'interval-verification.json';table=folder/'annotation/consequences.tsv';report=folder/'summary.json'
    digest=lambda path:hashlib.sha256(path.read_bytes()).hexdigest()
    tracked=[database,intervals,table,report]
    before={str(p.relative_to(folder)):dict(hash=digest(p),mtime_ns=p.stat().st_mtime_ns) for p in tracked}
    second,second_rules=run('no-change-run')
    assert 'Nothing to be done' in second and not second_rules
    assert all(p.stat().st_mtime_ns==before[str(p.relative_to(folder))]['mtime_ns'] for p in tracked)
    # Only delete a known generated table in this fresh, dedicated test directory.
    table.unlink()
    third,third_rules=run('recover-missing-table')
    assert set(first_rules)=={'build_database','annotate','intervals','report','all'},first_rules
    assert set(third_rules)=={'annotate','report','all'},third_rules
    assert table.exists() and digest(table)==before['annotation/consequences.tsv']['hash']
    assert database.stat().st_mtime_ns==before['database/data/toy/snpEffectPredictor.bin']['mtime_ns']
    assert intervals.stat().st_mtime_ns==before['interval-verification.json']['mtime_ns']
    assert report.stat().st_mtime_ns>before['summary.json']['mtime_ns']
    summary=dict(scope='Actual local Snakemake dependency scheduling on artificial annotation case; no cluster/container/cloud benchmark',
        snakemake_version=subprocess.check_output([executable,'--version'],text=True).strip(),
        first_run_rules=first_rules,no_change_rules=second_rules,recovery_rules=third_rules,
        no_change_preserves_output_mtimes=True,missing_table_restored_identically=True,
        database_reused=True,interval_results_reused=True,report_regenerated=True,
        final_summary_sha256=digest(report))
    (workdir/'validation.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2));return summary


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--snakemake',default=os.environ.get('SNAKEMAKE_BIN','snakemake'))
    parser.add_argument('--workdir',type=Path,default=PROJECT/'examples/output/workflow-validation')
    args=parser.parse_args()
    try:validate(args.snakemake,args.workdir)
    except subprocess.CalledProcessError as error:parser.exit(1,f'Workflow failed:\n{error.stdout}\n{error.stderr}\n')
    except ValueError as error:parser.exit(1,f'{error}\n')
