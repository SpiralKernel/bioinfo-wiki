#!/usr/bin/env Rscript
# Regenerate diagnostics from saved model and tables without refitting.
plot_rnaseq_diagnostics <- function(out) {
  suppressPackageStartupMessages(library(DESeq2))
  dds <- readRDS(file.path(out,'dds.rds'));vsd <- readRDS(file.path(out,'vsd.rds'))
  res <- results(dds,contrast=c('dex','trt','untrt'),alpha=.05)
  tab <- read.csv(file.path(out,'differential-expression.csv'),check.names=FALSE)
  tab <- tab[match(rownames(dds),tab$gene_id),]
  stopifnot(identical(tab$gene_id,rownames(dds)))
  shrunk <- res;shrunk$log2FoldChange <- tab$apeglm_log2FC;shrunk$lfcSE <- tab$apeglm_posterior_SD
  pca <- plotPCA(vsd,intgroup=c('cell','dex'),returnData=TRUE)
  percent <- attr(pca,'percentVar');alpha <- .05
  sig <- !is.na(res$padj) & res$padj < alpha
png(file.path(out,'diagnostics.png'),width=1600,height=1250,res=160)
par(mfrow=c(2,2),mar=c(4.3,4.5,3.3,1))
colors <- ifelse(pca$dex=='trt','#a63254','#187ca8')
plot(pca$PC1,pca$PC2,ylim=range(pca$PC2)+c(-1,1)*diff(range(pca$PC2))*.12,col=colors,pch=as.integer(pca$cell)+14,cex=1.5,
    xlab=sprintf('PC1 (%.1f%%)',100*percent[1]),ylab=sprintf('PC2 (%.1f%%)',100*percent[2]),main='VST: paired cell lines / condition')
text(pca$PC1,pca$PC2,labels=sub('SRR10395','',rownames(pca)),pos=3,cex=.7)
legend('topright',legend=c('untrt','trt'),col=c('#187ca8','#a63254'),pch=16,bty='n',cex=.8)
legend('bottomright',legend=levels(pca$cell),pch=15:18,bty='n',cex=.65)
plotMA(res,alpha=alpha,main='MA: raw Wald LFC')
plotMA(shrunk,alpha=alpha,main='MA: apeglm LFC (same Wald padj)')
finite <- is.finite(res$pvalue) & is.finite(res$log2FoldChange)
plot(res$log2FoldChange[finite],-log10(pmax(res$pvalue[finite],.Machine$double.xmin)),
    pch=16,cex=.4,col=ifelse(sig[finite],'#a63254','#aab4bb'),
    xlab='Raw log2FC (trt / untrt)',ylab='-log10(raw Wald P)',main='Volcano: color = BH padj < 0.05')
abline(v=0,lty=2,col='gray50');dev.off()
  invisible(out)
}
if (sys.nframe()==0L) {
  args <- commandArgs(trailingOnly=TRUE)
  if (length(args)>1L) stop('Usage: Rscript examples/plot_rnaseq_airway.R [existing-output-directory]')
  script <- sub('^--file=','',grep('^--file=',commandArgs(),value=TRUE)[[1]])
  root <- dirname(dirname(normalizePath(script)))
  out <- if(length(args)) args[[1]] else file.path(root,'examples/output/rnaseq-airway')
  plot_rnaseq_diagnostics(out)
}
