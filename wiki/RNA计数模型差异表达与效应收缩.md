# RNA计数模型差异表达与效应收缩

> 更新：2026-10-15；状态：可用；验证范围：DESeq2/apeglm公开计数案例已在原生R执行；edgeR与voom未测。

差异表达同时依赖计数生成、归一化、离散度和设计，效应收缩与显著性检验是不同环节。

## 从计数模型出发

bulk RNA-seq基因计数受文库规模和生物学变异影响。DESeq2和edgeR常用负二项框架，均值由设计和归一化因子联系到组别，离散度描述超出Poisson的变异。limma-voom则对相应变换的计数估计均值—方差权重，再进入线性模型，不是直接对TPM逐基因普通t检验。

## 需要分别学习的步骤

归一化处理可比尺度，离散度借助跨基因信息稳定估计，设计矩阵定义协变量和对比。基因组装、转录本汇总与长度偏差又是上游问题；整数计数接口和tximport等导入方式不能混用。

低计数预过滤和独立过滤影响检验集合，应保留实际规则。批次与组别完全混杂时，换一种差异算法也不能凭空分开效应。

## 收缩改变什么

log fold change收缩可降低低信息基因的极端效应，适合排名和展示。收缩系数不应与任意原始标准误拼成新P值；具体检验和效应阈值应使用软件支持的对应接口。显著性、效应大小和预测价值分别判断。

报告对比方向、计数来源、归一化、设计、过滤、效应/区间和FDR。完整操作见[RNA-seq从计数矩阵到差异表达](https://github.com/SpiralKernel/bioinfo-wiki/wiki/RNA-seq%E4%BB%8E%E8%AE%A1%E6%95%B0%E7%9F%A9%E9%98%B5%E5%88%B0%E5%B7%AE%E5%BC%82%E8%A1%A8%E8%BE%BE)，验证见[转录组差异与qPCR验证设计](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E8%BD%AC%E5%BD%95%E7%BB%84%E5%B7%AE%E5%BC%82%E4%B8%8EqPCR%E9%AA%8C%E8%AF%81%E8%AE%BE%E8%AE%A1)。

DESeq2与apeglm已有[公开airway数据贯通DESeq2](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%85%AC%E5%BC%80airway%E6%95%B0%E6%8D%AE%E8%B4%AF%E9%80%9ADESeq2)实测，edgeR与voom未运行。依据：[DESeq2官方教程](https://bioconductor.org/packages/release/bioc/vignettes/DESeq2/inst/doc/DESeq2.html)、[voom原始论文](https://doi.org/10.1186/gb-2014-15-2-r29)、[edgeR原始论文](https://doi.org/10.1093/bioinformatics/btp616)。

## 一个低信息例子

某基因在对照几乎都是0，处理只有少量计数，原始log2FC可能很大，但估计很不稳定。收缩会结合估计不确定性与先验，通常把信息不足的效应拉向更保守值；不是按固定倍数缩小所有基因。

设计矩阵是把组别和协变量编码成模型列；离散度描述额外变异；收缩用共同信息稳定估计。前置见[广义线性模型与逻辑回归](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%B9%BF%E4%B9%89%E7%BA%BF%E6%80%A7%E6%A8%A1%E5%9E%8B%E4%B8%8E%E9%80%BB%E8%BE%91%E5%9B%9E%E5%BD%92)、[线性模型与混合模型](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%BA%BF%E6%80%A7%E6%A8%A1%E5%9E%8B%E4%B8%8E%E6%B7%B7%E5%90%88%E6%A8%A1%E5%9E%8B)、[概率条件概率与贝叶斯定理](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E6%A6%82%E7%8E%87%E6%9D%A1%E4%BB%B6%E6%A6%82%E7%8E%87%E4%B8%8E%E8%B4%9D%E5%8F%B6%E6%96%AF%E5%AE%9A%E7%90%86)。

## 实测与细分概念

[负二项离散度与均值方差](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E8%B4%9F%E4%BA%8C%E9%A1%B9%E7%A6%BB%E6%95%A3%E5%BA%A6%E4%B8%8E%E5%9D%87%E5%80%BC%E6%96%B9%E5%B7%AE)、[RNA文库大小因子与组成偏差](https://github.com/SpiralKernel/bioinfo-wiki/wiki/RNA%E6%96%87%E5%BA%93%E5%A4%A7%E5%B0%8F%E5%9B%A0%E5%AD%90%E4%B8%8E%E7%BB%84%E6%88%90%E5%81%8F%E5%B7%AE)解释模型；[RNA效应收缩与阈值检验](https://github.com/SpiralKernel/bioinfo-wiki/wiki/RNA%E6%95%88%E5%BA%94%E6%94%B6%E7%BC%A9%E4%B8%8E%E9%98%88%E5%80%BC%E6%A3%80%E9%AA%8C)区分效应估计与不同零假设。airway实测普通零效应检验与阈值1检验发现数不同，具体数值和条件见案例。
