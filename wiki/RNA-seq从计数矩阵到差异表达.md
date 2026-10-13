# RNA-seq从计数矩阵到差异表达

> 更新：2026-10-13；状态：可用；验证范围：文档核对；完整流程未在本机运行。

从基因计数和实验设计出发，估计表达差异，并区分统计证据、效应大小与功能解释。

## 两个起点

已有 FASTQ 时，先完成原始质量评估、比对或定量、基因层面汇总和样本检查；可参考 [nf-core/rnaseq](https://nf-co.re/rnaseq/)。已有计数矩阵时，先确认行是基因、列是样本、计数单位及前序处理，见[计数丰度与标准化](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E8%AE%A1%E6%95%B0%E4%B8%B0%E5%BA%A6%E4%B8%8E%E6%A0%87%E5%87%86%E5%8C%96)。

## 可复现的官方数据练习

需要 R、Bioconductor 的 airway 与 DESeq2；安装版本应与当前 Bioconductor 发布匹配。以下代码基于公开 airway 数据接口，已核对文档，当前环境没有 R，尚未实际执行。

```r
library(airway)
library(DESeq2)
data(airway)
airway$dex <- relevel(airway$dex, ref = "untrt")
dds <- DESeqDataSet(airway, design = ~ cell + dex)
dds <- dds[rowSums(counts(dds)) >= 10, ]
dds <- DESeq(dds)
res <- results(dds, contrast = c("dex", "trt", "untrt"), alpha = 0.05)
write.csv(as.data.frame(res), "airway_differential_expression.csv")
sessionInfo()
```

`cell` 表示该数据中的细胞系配对因素，`dex` 是处理条件；它们的含义不能直接复制到自己的样本。低计数筛选是练习选择。对比方向为 trt 相对 untrt，正 log2FoldChange 表示该方向上的增加。

## 检查与解释

先检查样本对应、设计矩阵可估计性、样本距离和离群；保留原始计数。结果表同时读 baseMean、log2FoldChange、lfcSE、P 和 padj，排查 NA 原因。展示使用的变换值与检验输入分开保存。

通路解释见[富集分析与GSEA](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%AF%8C%E9%9B%86%E5%88%86%E6%9E%90%E4%B8%8EGSEA)。批次和重复问题见[批次效应与混杂](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E6%89%B9%E6%AC%A1%E6%95%88%E5%BA%94%E4%B8%8E%E6%B7%B7%E6%9D%82)、[生物学重复与技术重复](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%94%9F%E7%89%A9%E5%AD%A6%E9%87%8D%E5%A4%8D%E4%B8%8E%E6%8A%80%E6%9C%AF%E9%87%8D%E5%A4%8D)。

深入：[DESeq2 官方教程](https://bioconductor.org/packages/release/bioc/vignettes/DESeq2/inst/doc/DESeq2.html)、[airway 数据包](https://bioconductor.org/packages/airway/)、[DESeq2 原始论文](https://doi.org/10.1186/s13059-014-0550-8)。
