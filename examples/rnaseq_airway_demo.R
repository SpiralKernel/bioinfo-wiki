#!/usr/bin/env Rscript
# Real public processed counts; native R/DESeq2, not a FASTQ-to-count benchmark.
args <- commandArgs(trailingOnly=TRUE)
file_arg <- grep('^--file=', commandArgs(), value=TRUE)
project <- dirname(dirname(normalizePath(sub('^--file=', '', file_arg[[1]]))))
source(file.path(project, 'examples/rnaseq_input_checks.R'))
out <- if (length(args)) args[[1]] else file.path(project, 'examples/output/rnaseq-airway')
if (length(args) > 1L) stop('Usage: Rscript examples/rnaseq_airway_demo.R [new-output-directory]')
out <- normalizePath(out, mustWork=FALSE)
if (dir.exists(out) && length(list.files(out, all.files=TRUE, no..=TRUE))) stop('Use an empty/new output directory; existing results are preserved')
dir.create(out, recursive=TRUE, showWarnings=FALSE)
Sys.setenv(OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1')
required <- c('airway','DESeq2','apeglm','jsonlite')
for (package in required) if (!requireNamespace(package, quietly=TRUE)) stop(paste('Install package first:', package))
suppressPackageStartupMessages({library(airway);library(DESeq2)})
set.seed(20261015)
data('airway', package='airway')
raw <- assay(airway)
samples <- data.frame(sample_id=colnames(raw),cell=as.character(airway$cell),dex=as.character(airway$dex),stringsAsFactors=FALSE)
aligned <- align_rnaseq_inputs(raw, samples[rev(seq_len(nrow(samples))), , drop=FALSE])
samples <- aligned$samples
samples$cell <- factor(samples$cell)
samples$dex <- factor(samples$dex, levels=c('untrt','trt'))
stopifnot(nrow(samples)==8L, nlevels(samples$cell)==4L, all(table(samples$cell,samples$dex)==1L))
design_matrix <- check_rnaseq_design(samples, ~ cell + dex)
keep <- rowSums(raw) >= 10L
write.csv(data.frame(gene_id=rownames(raw),raw,check.names=FALSE), file.path(out,'counts.csv'),row.names=FALSE)
write.csv(samples,file.path(out,'samples.csv'),row.names=FALSE)
write.csv(data.frame(sample_id=rownames(design_matrix),design_matrix,check.names=FALSE),file.path(out,'design-matrix.csv'),row.names=FALSE)
dds <- DESeqDataSetFromMatrix(raw[keep,,drop=FALSE],samples,design=~cell+dex)
dds <- DESeq(dds,parallel=FALSE)
alpha <- 0.05
res <- results(dds,contrast=c('dex','trt','untrt'),alpha=alpha)
reverse <- results(dds,contrast=c('dex','untrt','trt'),alpha=alpha)
no_filter <- results(dds,contrast=c('dex','trt','untrt'),alpha=alpha,independentFiltering=FALSE)
coef <- 'dex_trt_vs_untrt'
stopifnot(coef %in% resultsNames(dds))
shrunk <- lfcShrink(dds,coef=coef,type='apeglm',res=res)
threshold <- results(dds,contrast=c('dex','trt','untrt'),alpha=alpha,lfcThreshold=1,altHypothesis='greaterAbs')
near <- function(a,b) isTRUE(all.equal(as.numeric(a),as.numeric(b),tolerance=1e-8))
stopifnot(near(res$log2FoldChange,-reverse$log2FoldChange),near(res$pvalue,reverse$pvalue),near(res$padj,reverse$padj))
stopifnot(near(res$pvalue,shrunk$pvalue),near(res$padj,shrunk$padj))
stopifnot(near(p.adjust(no_filter$pvalue,method='BH'),no_filter$padj))
row_info <- as.data.frame(rowData(airway))
symbols <- if ('symbol' %in% names(row_info)) as.character(row_info$symbol)[match(rownames(dds),rownames(airway))] else rep(NA_character_,nrow(dds))
results_table <- data.frame(gene_id=rownames(dds),symbol=symbols,as.data.frame(res),
    apeglm_log2FC=shrunk$log2FoldChange,apeglm_posterior_SD=shrunk$lfcSE,
    threshold1_pvalue=threshold$pvalue,threshold1_padj=threshold$padj,
    no_independent_filter_padj=no_filter$padj,check.names=FALSE)
results_table <- results_table[order(results_table$padj,results_table$pvalue,na.last=TRUE),]
write.csv(results_table,file.path(out,'differential-expression.csv'),row.names=FALSE,na='NA')
write.csv(head(results_table,50),file.path(out,'top50.csv'),row.names=FALSE,na='NA')
normalized <- counts(dds,normalized=TRUE)
write.csv(data.frame(gene_id=rownames(dds),normalized,check.names=FALSE),file.path(out,'normalized-counts.csv'),row.names=FALSE)
# VST is for diagnostics; raw counts went into the model.
vsd <- vst(dds,blind=FALSE)
pca <- plotPCA(vsd,intgroup=c('cell','dex'),returnData=TRUE)
percent <- attr(pca,'percentVar')
write.csv(data.frame(sample_id=rownames(pca),pca),file.path(out,'pca.csv'),row.names=FALSE)
write.csv(as.matrix(dist(t(assay(vsd)))),file.path(out,'sample-distances.csv'))
write.csv(data.frame(sample_id=colnames(dds),size_factor=sizeFactors(dds),library_count=colSums(raw),samples[,c('cell','dex')]),file.path(out,'sample-qc.csv'),row.names=FALSE)
reason <- ifelse(is.na(res$pvalue),'pvalue_NA_review_Cooks_or_other',ifelse(is.na(res$padj),'independent_filter','tested'))
# All-zero rows were already removed by the documented prefilter.
reason_table <- data.frame(gene_id=rownames(dds),baseMean=res$baseMean,pvalue=res$pvalue,padj=res$padj,status=reason)
write.csv(reason_table,file.path(out,'result-status.csv'),row.names=FALSE,na='NA')
status_counts <- as.list(table(factor(reason,levels=c('tested','independent_filter','pvalue_NA_review_Cooks_or_other'))))
sig <- !is.na(res$padj) & res$padj < alpha
summary <- list(scope='Real public airway processed gene counts; no FASTQ mapping, original-paper replication or functional validation',
    data=list(package='airway',geo='GSE52778',input_genes=nrow(raw),samples=ncol(raw),paired_cell_lines=nlevels(samples$cell),
      upstream_reference='GRCh37 / Ensembl release 75 as described in airway vignette',prefilter='rowSums(raw_counts) >= 10',retained_genes=sum(keep)),
    model=list(design='~ cell + dex',contrast='trt versus untrt',alpha=alpha,design_rank=qr(design_matrix)$rank,residual_df=nrow(design_matrix)-ncol(design_matrix),
      shrinkage='apeglm; original Wald P and padj retained; posterior SD is not original Wald SE',threshold_test='H0: abs(log2FC) <= 1, greaterAbs'),
    results=list(significant=sum(sig),up=sum(sig & res$log2FoldChange > 0),down=sum(sig & res$log2FoldChange < 0),status_counts=status_counts,
      no_independent_filter_significant=sum(no_filter$padj < alpha,na.rm=TRUE),threshold1_significant=sum(threshold$padj < alpha,na.rm=TRUE),
      independent_filter_baseMean_threshold=as.numeric(metadata(res)$filterThreshold),pca_percent_variance=as.numeric(percent)),
    checks=list(shuffled_metadata_aligned_by_ID=TRUE,paired_design_full_rank=TRUE,reverse_contrast_negates_LFC_preserves_P=TRUE,
      unfiltered_padj_matches_BH=TRUE,shrinkage_preserves_Wald_P_and_padj=TRUE),
    versions=c(list(R=as.character(getRversion())),setNames(lapply(required,function(p) as.character(packageVersion(p))),required)))
jsonlite::write_json(summary,file.path(out,'summary.json'),pretty=TRUE,auto_unbox=TRUE,digits=10)
capture.output(sessionInfo(),file=file.path(out,'session-info.txt'))
saveRDS(dds,file.path(out,'dds.rds'));saveRDS(vsd,file.path(out,'vsd.rds'))
source(file.path(project,'examples/plot_rnaseq_airway.R'))
plot_rnaseq_diagnostics(out)
cat(jsonlite::toJSON(summary,pretty=TRUE,auto_unbox=TRUE,digits=10),'\n')
