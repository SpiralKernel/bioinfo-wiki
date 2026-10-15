# RNA-seq从计数矩阵到差异表达

> 更新：2026-10-15；状态：可用；验证范围：公开airway计数流程已在原生R4.4.3/DESeq2 1.46.0执行；FASTQ上游未测。

从基因计数和实验设计出发，估计表达差异，并区分统计证据、效应大小与功能解释。

## 两个起点

已有 FASTQ 时，先完成原始质量评估、比对或定量、基因层面汇总和样本检查；可参考 [nf-core/rnaseq](https://nf-co.re/rnaseq/)。已有计数矩阵时，先确认行是基因、列是样本、计数单位及前序处理，见[计数丰度与标准化](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E8%AE%A1%E6%95%B0%E4%B8%B0%E5%BA%A6%E4%B8%8E%E6%A0%87%E5%87%86%E5%8C%96)。

## 可复现的官方数据练习

需要原生R及Bioconductor的airway与DESeq2。先按[R包Python包与可复现环境](https://github.com/SpiralKernel/bioinfo-wiki/wiki/R%E5%8C%85Python%E5%8C%85%E4%B8%8E%E5%8F%AF%E5%A4%8D%E7%8E%B0%E7%8E%AF%E5%A2%83)在R控制台安装这两个包，再执行下面代码；安装与载入不同。2026-10-15已在原生R实际运行airway计数模型；完整环境、命令、输出和诊断见[公开airway数据贯通DESeq2](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%85%AC%E5%BC%80airway%E6%95%B0%E6%8D%AE%E8%B4%AF%E9%80%9ADESeq2)。下方片段是模型核心，完整脚本还核对样本、对比、收缩及NA。

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


## 统计基础与验证入口

[转录组差异与qPCR验证设计](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E8%BD%AC%E5%BD%95%E7%BB%84%E5%B7%AE%E5%BC%82%E4%B8%8EqPCR%E9%AA%8C%E8%AF%81%E8%AE%BE%E8%AE%A1)补充本任务所需的统计或验证判断。分析前先确认[统计方法选择与分析计划](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%BB%9F%E8%AE%A1%E6%96%B9%E6%B3%95%E9%80%89%E6%8B%A9%E4%B8%8E%E5%88%86%E6%9E%90%E8%AE%A1%E5%88%92)，结果解释时区分[组学验证的层级与证据](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%BB%84%E5%AD%A6%E9%AA%8C%E8%AF%81%E7%9A%84%E5%B1%82%E7%BA%A7%E4%B8%8E%E8%AF%81%E6%8D%AE)。


## 测序技术与上游输入

先确认[RNA测序建库选择与偏倚](https://github.com/SpiralKernel/bioinfo-wiki/wiki/RNA%E6%B5%8B%E5%BA%8F%E5%BB%BA%E5%BA%93%E9%80%89%E6%8B%A9%E4%B8%8E%E5%81%8F%E5%80%9A)与[链特异性与RNA测序方向](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E9%93%BE%E7%89%B9%E5%BC%82%E6%80%A7%E4%B8%8ERNA%E6%B5%8B%E5%BA%8F%E6%96%B9%E5%90%91)，再生成计数；RNA来源、UMI和read布局影响有效计数。

## 对应方法与深入

[RNA计数模型差异表达与效应收缩](https://github.com/SpiralKernel/bioinfo-wiki/wiki/RNA%E8%AE%A1%E6%95%B0%E6%A8%A1%E5%9E%8B%E5%B7%AE%E5%BC%82%E8%A1%A8%E8%BE%BE%E4%B8%8E%E6%95%88%E5%BA%94%E6%94%B6%E7%BC%A9)、[组学批次校正与信号保留](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%BB%84%E5%AD%A6%E6%89%B9%E6%AC%A1%E6%A0%A1%E6%AD%A3%E4%B8%8E%E4%BF%A1%E5%8F%B7%E4%BF%9D%E7%95%99)解释输入条件和适用边界；软件运行步骤与方法假设一起核对。

## 拆分阅读入口

[bulkRNA-seq分析与实践路线](https://github.com/SpiralKernel/bioinfo-wiki/wiki/bulkRNA-seq%E5%88%86%E6%9E%90%E4%B8%8E%E5%AE%9E%E8%B7%B5%E8%B7%AF%E7%BA%BF)给出顺序。输入先看[RNA计数矩阵与样本表核对](https://github.com/SpiralKernel/bioinfo-wiki/wiki/RNA%E8%AE%A1%E6%95%B0%E7%9F%A9%E9%98%B5%E4%B8%8E%E6%A0%B7%E6%9C%AC%E8%A1%A8%E6%A0%B8%E5%AF%B9)，模型先看[RNA设计矩阵配对与对比方向](https://github.com/SpiralKernel/bioinfo-wiki/wiki/RNA%E8%AE%BE%E8%AE%A1%E7%9F%A9%E9%98%B5%E9%85%8D%E5%AF%B9%E4%B8%8E%E5%AF%B9%E6%AF%94%E6%96%B9%E5%90%91)；结果NA、VST和收缩分别见[独立过滤低计数与结果NA](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%8B%AC%E7%AB%8B%E8%BF%87%E6%BB%A4%E4%BD%8E%E8%AE%A1%E6%95%B0%E4%B8%8E%E7%BB%93%E6%9E%9CNA)、[VSTrlog与样本距离](https://github.com/SpiralKernel/bioinfo-wiki/wiki/VSTrlog%E4%B8%8E%E6%A0%B7%E6%9C%AC%E8%B7%9D%E7%A6%BB)、[RNA效应收缩与阈值检验](https://github.com/SpiralKernel/bioinfo-wiki/wiki/RNA%E6%95%88%E5%BA%94%E6%94%B6%E7%BC%A9%E4%B8%8E%E9%98%88%E5%80%BC%E6%A3%80%E9%AA%8C)。真实FASTQ到计数目前仍为[RNA-seq从FASTQ到基因计数](https://github.com/SpiralKernel/bioinfo-wiki/wiki/RNA-seq%E4%BB%8EFASTQ%E5%88%B0%E5%9F%BA%E5%9B%A0%E8%AE%A1%E6%95%B0)指南。
