# RNA效应收缩与阈值检验

> 更新：2026-10-15；状态：可用；验证范围：原生R与公开airway计数案例已执行；范围和结果见正文。

稳定效应估计、检验零效应和检验超过预定阈值，是三个需要分别报告的任务。

## 收缩用于什么

低信息基因的原始log2FC可能极端且不稳定。apeglm用重尾先验稳定效应估计；收缩程度取决于信息，不是固定乘数。[原始研究](https://pmc.ncbi.nlm.nih.gov/articles/PMC6581436/)解释方法。本例另存原始Wald log2FC/SE与apeglm log2FC/后验SD。

apeglm给出的后验SD不能直接当原始Wald标准误，和收缩LFC拼出新的普通P。本轮通过lfcShrink保留原结果P/padj，实际核对一致性；图上收缩LFC和原Wald显著性必须说明来源。

## 大效应检验是另一个零假设

筛选`padj<0.05 & abs(log2FC)>1`并不等于统计检验真实绝对效应大于1。后者可用`results(..., lfcThreshold=1, altHypothesis="greaterAbs")`检验H0：|log2FC|≤1，并产生单独P/padj。

本例同时输出普通零效应结果和阈值1的结果；没有用收缩值替换检验输入，也不把二者发现数差异当软件错误。阈值1只是教学选择，应在研究前结合问题确定。

继续读[DESeq2安装对象与结果提取](https://github.com/SpiralKernel/bioinfo-wiki/wiki/DESeq2%E5%AE%89%E8%A3%85%E5%AF%B9%E8%B1%A1%E4%B8%8E%E7%BB%93%E6%9E%9C%E6%8F%90%E5%8F%96)、[RNA差异结果报告与富集背景](https://github.com/SpiralKernel/bioinfo-wiki/wiki/RNA%E5%B7%AE%E5%BC%82%E7%BB%93%E6%9E%9C%E6%8A%A5%E5%91%8A%E4%B8%8E%E5%AF%8C%E9%9B%86%E8%83%8C%E6%99%AF)。
