#!/usr/bin/env bash
set -euo pipefail
project_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
plink_bin="${PLINK2_BIN:-plink2}"
output_dir="$project_dir/examples/output/population"
python3 "$project_dir/examples/generate_population_data.py" --output "$output_dir"
"$plink_bin" --version
"$plink_bin" --vcf "$output_dir/toy.vcf" --make-pgen --out "$output_dir/imported"
"$plink_bin" --pfile "$output_dir/imported" --missing --freq --out "$output_dir/before_qc"
"$plink_bin" --pfile "$output_dir/imported" --geno 0.05 --mind 0.05 --maf 0.05 --make-pgen --out "$output_dir/qc"
"$plink_bin" --pfile "$output_dir/qc" --indep-pairwise 50 5 0.2 --out "$output_dir/prune"
"$plink_bin" --pfile "$output_dir/qc" --extract "$output_dir/prune.prune.in" --pca 5 --out "$output_dir/pca"
"$plink_bin" --pfile "$output_dir/qc" --pheno "$output_dir/phenotype.tsv" --pheno-name trait --covar "$output_dir/pca.eigenvec" --covar-name PC1-PC5 --glm hide-covar --out "$output_dir/gwas"
