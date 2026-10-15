# VSTrlog与样本距离

> 更新：2026-10-15；状态：可用；验证范围：原生R与公开airway计数案例已执行；范围和结果见正文。

方差稳定变换用于观察样本结构，计数模型的检验输入仍应保持原来的计数语义。

## 先区分用途

VST和rlog用于让不同表达强度的变异更适合距离、PCA和展示。它们不是TPM，也不是把处理效应或批次自动消掉的步骤。本轮实际执行VST，未执行rlog。

示例用`vst(dds, blind=FALSE)`利用已知设计相关的离散度趋势；blind的选择影响估计方式，但FALSE不表示“把组间差异去掉”。探索样本质量和保留强处理差异时应根据任务解释选择。

## PCA怎么读

PCA展示变换后数据的主要变化方向；分开并不自动证明差异显著，混合也不直接证明没有处理效应。查看是否被细胞系、文库、批次或少量异常样本驱动，再回到样本表和原始计数。

本例使用DESeq2 plotPCA默认选择的高变异基因，不是先按差异P挑基因后展示。PC百分比应针对实际使用的矩阵，图形方向正负本身没有固定生物学意义。

热图若逐基因做z-score，颜色表示该基因内的相对位置，不能跨基因当绝对表达高低。方法与诊断入口见[官方RNA-seq工作流](https://bioconductor.org/packages/release/workflows/vignettes/rnaseqGene/inst/doc/rnaseqGene.html)、[公开airway数据贯通DESeq2](https://github.com/SpiralKernel/bioinfo-wiki/wiki/%E5%85%AC%E5%BC%80airway%E6%95%B0%E6%8D%AE%E8%B4%AF%E9%80%9ADESeq2)。
