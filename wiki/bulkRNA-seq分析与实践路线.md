# bulkRNA-seq分析与实践路线

> 更新：2026-10-15；状态：可用；验证范围：原生R与公开airway计数案例已执行；范围和结果见正文。

从样本设计和计数来源出发，完成基因层面差异分析，再进入解释与验证。

## 先选起点

已有计数矩阵，先读[RNA计数矩阵与样本表核对](https://github.com/SpiralKernel/bioinfo-wiki/wiki/RNA%E8%AE%A1%E6%95%B0%E7%9F%A9%E9%98%B5%E4%B8%8E%E6%A0%B7%E6%9C%AC%E8%A1%A8%E6%A0%B8%E5%AF%B9)；已有FASTQ，先读[RNA-seq从FASTQ到基因计数](https://github.com/SpiralKernel/bioinfo-wiki/wiki/RNA-seq%E4%BB%8EFASTQ%E5%88%B0%E5%9F%BA%E5%9B%A0%E8%AE%A1%E6%95%B0)。两条路径在“有来源、有单位、样本对应正确的计数”汇合。TPM、标准化计数和原始计数不能因为都是数字表就互换。

## 建议阅读顺序

1. [RNA设计矩阵配对与对比方向](https://github.com/SpiralKernel/bioinfo-wiki/wiki/RNA%E8%AE%BE%E8%AE%A1%E7%9F%A9%E9%98%B5%E9%85%8D%E5%AF%B9%E4%B8%8E%E5%AF%B9%E6%AF%94%E6%96%B9%E5%90%91)：研究单位、配对因素、参考水平和可估计性。
2. [RNA文库大小因子与组成偏差](https://github.com/SpiralKernel/bioinfo-wiki/wiki/RNA%E6%96%87%E5%BA%93%E5%A4%A7%E5%B0%8F%E5%9B%A0%E5%AD%90%E4%B8%8E%E7%BB%84%E6%88%90%E5%81%8F%E5%B7%AE)、[负二项离散度与均值方差](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E8%B4%9F%E4%BA%8C%E9%A1%B9%E7%A6%BB%E6%95%A3%E5%BA%A6%E4%B8%8E%E5%9D%87%E5%80%BC%E6%96%B9%E5%B7%AE)：为什么不能逐基因照搬普通t检验。
3. [DESeq2安装对象与结果提取](https://github.com/SpiralKernel/bioinfo-wiki/wiki/DESeq2%E5%AE%89%E8%A3%85%E5%AF%B9%E8%B1%A1%E4%B8%8E%E7%BB%93%E6%9E%9C%E6%8F%90%E5%8F%96)，然后实际运行[公开airway数据贯通DESeq2](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%85%AC%E5%BC%80airway%E6%95%B0%E6%8D%AE%E8%B4%AF%E9%80%9ADESeq2)。
4. [独立过滤低计数与结果NA](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E7%8B%AC%E7%AB%8B%E8%BF%87%E6%BB%A4%E4%BD%8E%E8%AE%A1%E6%95%B0%E4%B8%8E%E7%BB%93%E6%9E%9CNA)、[VSTrlog与样本距离](https://github.com/SpiralKernel/bioinfo-wiki/wiki/VSTrlog%E4%B8%8E%E6%A0%B7%E6%9C%AC%E8%B7%9D%E7%A6%BB)、[RNA效应收缩与阈值检验](https://github.com/SpiralKernel/bioinfo-wiki/wiki/RNA%E6%95%88%E5%BA%94%E6%94%B6%E7%BC%A9%E4%B8%8E%E9%98%88%E5%80%BC%E6%A3%80%E9%AA%8C)：读懂诊断和结果。
5. [RNA差异结果报告与富集背景](https://github.com/SpiralKernel/bioinfo-wiki/wiki/RNA%E5%B7%AE%E5%BC%82%E7%BB%93%E6%9E%9C%E6%8A%A5%E5%91%8A%E4%B8%8E%E5%AF%8C%E9%9B%86%E8%83%8C%E6%99%AF)与[转录组差异与qPCR验证设计](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E8%BD%AC%E5%BD%95%E7%BB%84%E5%B7%AE%E5%BC%82%E4%B8%8EqPCR%E9%AA%8C%E8%AF%81%E8%AE%BE%E8%AE%A1)：组织证据和后续验证。

## 本轮完成和未完成

原生R实际运行公开airway的8个样本计数，完成配对DESeq2、apeglm收缩、效应阈值检验、VST/PCA及输入错误检查。FASTQ比对、featureCounts、Salmon/tximport、复杂交互与LRT在本轮仍为指南，没有执行。

单细胞数据先看[单细胞差异表达与差异丰度](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%8D%95%E7%BB%86%E8%83%9E%E5%B7%AE%E5%BC%82%E8%A1%A8%E8%BE%BE%E4%B8%8E%E5%B7%AE%E5%BC%82%E4%B8%B0%E5%BA%A6)；细胞数不能自动替代供体重复。bulkRNA-seq也不直接回答剪接、转录本使用或单细胞组成变化等全部问题。
