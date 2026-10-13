# P值效应量与多重检验

> 更新：2026-10-13；验证范围：文档核对；操作需按所用环境验证。

P 值衡量特定零假设下的数据相容性，效应量描述差异大小；大量检验需要额外控制错误。

## 三件事分别回答什么

在零假设与检验假设成立时，P值是获得至少与观测结果同样极端的检验统计量的概率；“极端”由事先定义的检验决定。

P 值不是“零假设为真的概率”，也不是结果可复现的概率。BETA、差值、log2 fold change 等效应量有方向和单位，还应结合标准误或[置信区间与重采样](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%BD%AE%E4%BF%A1%E5%8C%BA%E9%97%B4%E4%B8%8E%E9%87%8D%E9%87%87%E6%A0%B7)解释。

在许多位点或基因上做检验时，仅用单次 P < 0.05 会增加误报。Bonferroni 常用 α/m 控制家族错误率；BH 方法在相应条件下控制错误发现率（FDR）。FDR 关注发现集合中的错误比例期望，不表示每个条目有同样的错误概率。

## 一个练习

检验 1000 个完全无效条目时，单次 0.05 阈值下误报数量的期望约为 50。这个例子说明检验数量重要，不表示实际数据一定出现 50 个误报。

报告应同时保留原始 P、调整方法、调整后值、效应量、样本量和检验集合。`padj=NA` 也应查明过滤或异常值原因，不能自动当成“不显著”。

## 延伸阅读

[FDR 原始论文](https://doi.org/10.1111/j.2517-6161.1995.tb02031.x)和 [R 的 p.adjust 文档](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/p.adjust.html)提供方法定义与适用条件。应用见[GWAS从数据准备到结果解释](https://github.com/SpiralKernel/bioinfo-wiki/wiki/GWAS%E4%BB%8E%E6%95%B0%E6%8D%AE%E5%87%86%E5%A4%87%E5%88%B0%E7%BB%93%E6%9E%9C%E8%A7%A3%E9%87%8A)、[RNA-seq从计数矩阵到差异表达](https://github.com/SpiralKernel/bioinfo-wiki/wiki/RNA-seq%E4%BB%8E%E8%AE%A1%E6%95%B0%E7%9F%A9%E9%98%B5%E5%88%B0%E5%B7%AE%E5%BC%82%E8%A1%A8%E8%BE%BE)。
